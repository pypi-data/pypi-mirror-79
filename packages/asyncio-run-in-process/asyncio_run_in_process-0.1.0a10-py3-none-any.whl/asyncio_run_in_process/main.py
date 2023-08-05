import asyncio
import concurrent
import logging
import os
import signal
import sys
from typing import (
    TYPE_CHECKING,
    Any,
    AsyncContextManager,
    AsyncIterator,
    Callable,
    Optional,
)

from async_generator import (
    asynccontextmanager,
)

from . import (
    constants,
)
from ._utils import (
    cleanup_tasks,
    get_subprocess_command,
    read_exactly,
    receive_pickled_value,
)
from .abc import (
    ProcessAPI,
)
from .exceptions import (
    InvalidDataFromChild,
    InvalidState,
    UnpickleableValue,
)
from .process import (
    Process,
)
from .state import (
    State,
)
from .typing import (
    TReturn,
)

if TYPE_CHECKING:
    from typing import Tuple  # noqa: F401
    from .typing import SubprocessKwargs  # noqa: F401


logger = logging.getLogger("asyncio_run_in_process")
_executor: Optional[concurrent.futures.ThreadPoolExecutor] = None


def _get_executor() -> concurrent.futures.ThreadPoolExecutor:
    global _executor
    if _executor is None:
        max_procs = int(os.getenv('ASYNCIO_RUN_IN_PROCESS_MAX_PROCS', constants.MAX_PROCESSES))
        _executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_procs)
    return _executor


async def _monitor_sub_proc(
    proc: ProcessAPI[TReturn], sub_proc: asyncio.subprocess.Process, parent_w: int
) -> None:
    logger.debug("starting subprocess to run %s", proc)

    await proc.wait_pid()
    if proc.pid != sub_proc.pid:
        raise Exception("Process id mismatch.  This should not be possible")
    logger.debug("subprocess for %s started.  pid=%d", proc, sub_proc.pid)

    # we write the execution data immediately without waiting for the
    # `WAIT_EXEC_DATA` state to ensure that the child process doesn't have
    # to wait for that data due to the round trip times between processes.
    logger.debug("writing execution data for %s over fd=%d", proc, parent_w)
    # pass the child process the serialized `async_fn` and `args`

    with os.fdopen(parent_w, "wb") as to_child:
        to_child.write(proc.sub_proc_payload)
        to_child.flush()

    await proc.wait_for_state(State.WAIT_EXEC_DATA)
    logger.debug("child process %s (pid=%d) waiting for exec data", proc, sub_proc.pid)

    await proc.wait_for_state(State.STARTED)
    logger.debug("waiting for process %s (pid=%d) to finish", proc, sub_proc.pid)

    await sub_proc.wait()

    proc.returncode = sub_proc.returncode
    logger.debug("process %s (pid=%d) finished: returncode=%d", proc, sub_proc.pid, proc.returncode)


async def _relay_signals(
    proc: ProcessAPI[Any],
    queue: 'asyncio.Queue[signal.Signals]',
) -> None:
    if proc.state.is_before(State.EXECUTING):
        # If the process has not reached the state where the child process
        # can properly handle the signal, give it a moment to reach the
        # `EXECUTING` stage.
        logger.debug("_relay_signals(): Waiting for %s to reach EXECUTING state", proc)
        await proc.wait_for_state(State.EXECUTING)
    elif proc.state is State.FINISHED:
        logger.debug("_relay_signals(): %s is already finished, exiting %s", proc)
        return

    logger.debug("_relay_signals(): Waiting for signals to relay to %s", proc)
    while True:
        signum = await queue.get()
        logger.debug("relaying signal %s to child process %s", signum, proc)
        proc.send_signal(signum)


async def _monitor_state(
    proc: ProcessAPI[TReturn],
    parent_read_fd: int,
    child_write_fd: int,
    loop: asyncio.AbstractEventLoop,
) -> None:
    with os.fdopen(parent_read_fd, "rb", closefd=True) as from_child:
        for expected_state in State:
            if proc.state is not expected_state:
                raise InvalidState(
                    f"Process in state {proc.state} but expected state {expected_state}"
                )

            next_expected_state = State(proc.state + 1)
            logger.debug(
                "Waiting for next expected state (%s) from child (%s)", next_expected_state, proc)
            try:
                child_state_as_byte = await loop.run_in_executor(
                    _get_executor(), read_exactly, from_child, 1)
            except asyncio.CancelledError:
                # When the sub process is sent a SIGKILL, the write end of the pipe used in
                # read_exactly is never closed and the thread above attempting to read from it
                # will prevent us from leaving this fdopen() context, so we need to close the
                # write end ourselves to ensure the read_exactly() returns.
                logger.debug(
                    "_monitor_state() cancelled while waiting data from child, closing "
                    "child_write_fd to ensure we exit")
                os.close(child_write_fd)
                raise

            try:
                child_state = State(ord(child_state_as_byte))
            except TypeError:
                raise InvalidState(f"Child sent state: {child_state_as_byte.hex()}")

            if not proc.state.is_next(child_state):
                raise InvalidState(
                    f"Invalid state transition: {proc.state} -> {child_state}"
                )

            logger.debug("Got next state (%s) from child (%s)", child_state, proc)

            if child_state is State.FINISHED:
                # For the FINISHED state we delay updating the state until we also
                # have a return value.
                break
            elif child_state is State.INITIALIZED:
                # For the INITIALIZED state we expect an additional payload of the
                # process id.  The process ID is gotten via this mechanism to
                # prevent the need for ugly sleep based code in
                # `_monitor_sub_proc`.
                pid_bytes = await loop.run_in_executor(_get_executor(), read_exactly, from_child, 4)
                proc.pid = int.from_bytes(pid_bytes, 'big')

            await proc.update_state(child_state)
            logger.debug(
                "Updated process %s state %s -> %s",
                proc,
                expected_state.name,
                child_state.name,
            )

        # This is mostly a sanity check but it ensures that we don't try to get a result from a
        # process which hasn't finished.
        if child_state is not State.FINISHED:
            raise InvalidState(f"Invalid final state: {proc.state}")

        logger.debug("Waiting for result from %s", proc)
        try:
            result = await loop.run_in_executor(_get_executor(), receive_pickled_value, from_child)
        except UnpickleableValue as e:
            result = InvalidDataFromChild(
                "Unable to unpickle data from child. This may be a custom exception class; see "
                "https://github.com/ethereum/asyncio-run-in-process/issues/28 for more details. "
                "Original error: %s" % e.args)
            result.__cause__ = e
        except asyncio.CancelledError:
            # See comment above as to why we need to do this.
            logger.debug(
                "_monitor_state() cancelled while waiting data from child, closing "
                "child_write_fd to ensure we exit")
            os.close(child_write_fd)
            raise

    logger.debug("Waiting for returncode from %s", proc)
    await proc.wait_returncode()

    if isinstance(result, InvalidDataFromChild):
        # When we're unable to unpickle the result from the child, we need to force an error
        # so that the InvalidDataFromChild is raised in .wait_result_or_raise().
        proc.error = result
        proc.returncode = -99
    elif proc.returncode == 0:
        proc.return_value = result
    else:
        proc.error = result

    await proc.update_state(child_state)
    logger.debug(
        "Updated process %s state %s -> %s",
        proc,
        expected_state.name,
        child_state.name,
    )


# SIGINT isn't included here because it's handled by catching the
# `KeyboardInterrupt` exception.
RELAY_SIGNALS = (signal.SIGTERM, signal.SIGHUP)


def open_in_process(
    async_fn: Callable[..., TReturn],
    *args: Any,
    loop: asyncio.AbstractEventLoop = None,
    subprocess_kwargs: 'SubprocessKwargs' = None,
) -> AsyncContextManager[ProcessAPI[TReturn]]:
    return _open_in_process(
        async_fn, *args, loop=loop, subprocess_kwargs=subprocess_kwargs, use_trio=False)


def open_in_process_with_trio(
    async_fn: Callable[..., TReturn],
    *args: Any,
    subprocess_kwargs: 'SubprocessKwargs' = None,
) -> AsyncContextManager[ProcessAPI[TReturn]]:
    return _open_in_process(
        async_fn, *args, loop=None, subprocess_kwargs=subprocess_kwargs, use_trio=True)


def _update_subprocess_kwargs(subprocess_kwargs: Optional['SubprocessKwargs'],
                              child_r: int,
                              child_w: int) -> 'SubprocessKwargs':
    if subprocess_kwargs is None:
        subprocess_kwargs = {}

    base_pass_fds = subprocess_kwargs.get('pass_fds', ())
    pass_fds: Tuple[int, ...]

    if base_pass_fds is None:
        pass_fds = (child_r, child_w)
    else:
        pass_fds = tuple(set(base_pass_fds).union((child_r, child_w)))

    updated_kwargs = subprocess_kwargs.copy()
    updated_kwargs['pass_fds'] = pass_fds

    return updated_kwargs


@asynccontextmanager
async def _open_in_process(
    async_fn: Callable[..., TReturn],
    *args: Any,
    loop: asyncio.AbstractEventLoop = None,
    subprocess_kwargs: 'SubprocessKwargs' = None,
    use_trio: bool = False,
) -> AsyncIterator[ProcessAPI[TReturn]]:
    if use_trio and loop is not None:
        raise ValueError("If using trio, cannot specify a loop")

    proc: Process[TReturn] = Process(async_fn, args)

    parent_r, child_w = os.pipe()
    child_r, parent_w = os.pipe()

    command = get_subprocess_command(child_r, child_w, use_trio)

    sub_proc = await asyncio.create_subprocess_exec(
        *command,
        **_update_subprocess_kwargs(subprocess_kwargs, child_r, child_w),
    )
    if loop is None:
        loop = asyncio.get_event_loop()

    signal_queue: asyncio.Queue[signal.Signals] = asyncio.Queue()

    for signum in RELAY_SIGNALS:
        loop.add_signal_handler(
            signum,
            signal_queue.put_nowait,
            signum,
        )

    # Monitoring
    monitor_sub_proc_task = asyncio.ensure_future(_monitor_sub_proc(proc, sub_proc, parent_w))
    relay_signals_task = asyncio.ensure_future(_relay_signals(proc, signal_queue))
    monitor_state_task = asyncio.ensure_future(_monitor_state(proc, parent_r, child_w, loop))

    startup_timeout = int(
        os.getenv('ASYNCIO_RUN_IN_PROCESS_STARTUP_TIMEOUT', constants.STARTUP_TIMEOUT_SECONDS))
    async with cleanup_tasks(monitor_sub_proc_task, relay_signals_task, monitor_state_task):
        try:
            await asyncio.wait_for(proc.wait_pid(), timeout=startup_timeout)
        except asyncio.TimeoutError:
            sub_proc.kill()
            raise asyncio.TimeoutError(
                f"{proc} took more than {startup_timeout} seconds to start up")

        logger.debug(
            "Got pid %d for %s, waiting for it to reach EXECUTING state before yielding",
            proc.pid, proc)
        # Wait until the child process has reached the EXECUTING
        # state before yielding the context.  This ensures that any
        # calls to things like `terminate` or `kill` will be handled
        # properly in the child process.
        #
        # The timeout ensures that if something is fundamentally wrong
        # with the subprocess we don't hang indefinitely.
        try:
            logger.debug("Waiting for proc pid=%d to reach EXECUTING state", proc.pid)
            await asyncio.wait_for(proc.wait_for_state(State.EXECUTING), timeout=startup_timeout)
        except asyncio.TimeoutError:
            sub_proc.kill()
            raise asyncio.TimeoutError(
                f"{proc} took more than {startup_timeout} seconds to start up")

        try:
            try:
                yield proc
            except KeyboardInterrupt as err:
                # If a keyboard interrupt is encountered relay it to the
                # child process and then give it a moment to cleanup before
                # re-raising
                logger.debug("Relaying SIGINT to pid=%d", sub_proc.pid)
                try:
                    proc.send_signal(signal.SIGINT)
                    try:
                        await asyncio.wait_for(
                            proc.wait(), timeout=constants.SIGINT_TIMEOUT_SECONDS)
                    except asyncio.TimeoutError:
                        logger.debug(
                            "Timed out waiting for pid=%d to exit after relaying SIGINT",
                            sub_proc.pid,
                        )
                except BaseException:
                    logger.exception(
                        "Unexpected error when terminating child; pid=%d", sub_proc.pid)
                finally:
                    raise err
            except asyncio.CancelledError as err:
                # Send the child a SIGINT and wait SIGINT_TIMEOUT_SECONDS for it to terminate. If
                # that times out, send a SIGTERM and wait SIGTERM_TIMEOUT_SECONDS before
                # re-raising.
                logger.debug(
                    "Got CancelledError while running subprocess pid=%d.  Sending SIGINT.",
                    sub_proc.pid,
                )
                try:
                    proc.send_signal(signal.SIGINT)
                    try:
                        await asyncio.wait_for(
                            proc.wait(), timeout=constants.SIGINT_TIMEOUT_SECONDS)
                    except asyncio.TimeoutError:
                        logger.debug(
                            "Timed out waiting for pid=%d to exit after SIGINT, sending SIGTERM",
                            sub_proc.pid,
                        )
                        proc.terminate()
                        try:
                            await asyncio.wait_for(
                                proc.wait(), timeout=constants.SIGTERM_TIMEOUT_SECONDS)
                        except asyncio.TimeoutError:
                            logger.debug(
                                "Timed out waiting for pid=%d to exit after SIGTERM", sub_proc.pid)
                except BaseException:
                    logger.exception(
                        "Unexpected error when terminating child; pid=%d", sub_proc.pid)
                finally:
                    raise err
            else:
                # In the case that the yielded context block exits without an
                # error we wait for the process to finish naturally.  This can
                # hang indefinitely.
                logger.debug(
                    "Waiting for %s (pid=%d) to finish naturally, this can hang forever",
                    proc,
                    proc.pid,
                )
                await proc.wait()
        finally:
            if sub_proc.returncode is None:
                # If the process has not returned at this stage we need to hard
                # kill it to prevent it from hanging.
                logger.warning(
                    "Child process pid=%d failed to exit cleanly.  Sending SIGKILL",
                    sub_proc.pid,
                    # The `any` call is to include a stacktrace if this
                    # happened due to an exception but to omit it if this is
                    # somehow happening outside of an exception context.
                    exc_info=any(sys.exc_info()),
                )
                sub_proc.kill()


async def run_in_process(async_fn: Callable[..., TReturn],
                         *args: Any,
                         loop: asyncio.AbstractEventLoop = None,
                         subprocess_kwargs: 'SubprocessKwargs' = None) -> TReturn:
    proc_ctx = open_in_process(
        async_fn,
        *args,
        loop=loop,
        subprocess_kwargs=subprocess_kwargs,
    )
    async with proc_ctx as proc:
        await proc.wait()
    return proc.get_result_or_raise()


async def run_in_process_with_trio(async_fn: Callable[..., TReturn],
                                   *args: Any,
                                   subprocess_kwargs: 'SubprocessKwargs' = None) -> TReturn:
    proc_ctx = open_in_process_with_trio(
        async_fn, *args, subprocess_kwargs=subprocess_kwargs)
    async with proc_ctx as proc:
        await proc.wait()
    return proc.get_result_or_raise()
