import queue
import concurrent.futures
import os
from typing import Iterable, Optional


def ensure_single_thread_numeric():
    """
    When you parallelize your input pipeline you often want each worker to work
    on a single thread.

    These are all candidates to set to 1, but the ones checked in this
    function are mandatory as far as we know.

    GOMP_NUM_THREADS
    OMP_NUM_THREADS
    OPENBLAS_NUM_THREADS
    MKL_NUM_THREADS
    VECLIB_MAXIMUM_THREADS
    NUMEXPR_NUM_THREADS

    Returns:

    """
    candidates = 'OMP_NUM_THREADS MKL_NUM_THREADS'.split()

    for key in candidates:
        if not os.environ.get(key) == '1':
            raise EnvironmentError(
                'Make sure to set the following environment variables to '
                'ensure that each worker works on a single thread:\n'
                'export OMP_NUM_THREADS=1\n'
                'export MKL_NUM_THREADS=1\n\n'
                f'But you use: {key}={os.environ.get(key)}'
            )


def _dill_mp_helper(payload):
    import dill

    fun, args, kwargs = dill.loads(payload)
    return fun(*args, **kwargs)


def lazy_parallel_map(
        function: callable,
        generator: Iterable,
        *,
        args: Optional[list] = None,
        kwargs: Optional[dict] = None,
        backend: str = "t",
        buffer_size: int = 5,
        max_workers: int = 2
):
    """
    This is a parallel map where the function is parallel executed and the
    output is buffered. Note the generator is executed serially.

    A serial version of this function is::

        for ele in generator:
            yield function(ele, *args, **kwargs)

    The function is executed in parallel (not the generator) and the output of
    the function is buffered.

    Available backends are:
        - 'mp': Multiprocessing backend. Uses a
            `pathos.multiprocessing.ProcessPool` to parallelize
        - 'dill_mp': Uses `concurrent.futures.ProcessPoolExecutor` to
            parallelize and `dill` for serialization of arguments and
            results of `function`
        - 't' / 'threaded': Uses a `concurrent.futures.ThreadPoolExecutor`
        - 'concurrent_mp': Uses a `concurrent.futures.ProcessPoolExecutor`.
            Note that this uses `pickle` for serialization, so it can not
            handle arbitrary callable objects as `function`.

    Args:
        function: Function to map. Must accept an element of `generator` as
            first positional argument. The provided `args` and `kwargs` are
            forwarded to `function` as `function(element, *args, **kwargs)`.
        generator: Generator to iterate over
        args: Additional arguments for `function`
        kwargs: Additional keyword arguments for `function`
        backend: The backend to use
        buffer_size: Number of examples to buffer
        max_workers: Maximum number of threads/processes used for parallel
            execution

    Yields:
        The results of function applied to each element of `generator`. The
        order of the elements produces by `generator` is preserved.

    Note:
     - The overhead to copy the data from and to the workers can destroy the
       gain from mutiprocessing ('mp', 'dill_mp').
       Only the threaded backend ('t') has no copy overhead.
     - When the function spends a high amount of time in numpy and/or I/O the
       threaded backend ('t') is recommended. The reason for numpy is, that it
       usually releases the GIL.
     - Do not forget to disable low level parallel execution
       (see `ensure_single_thread_numeric`) when you have CPU bound code.
       For bad combinations, the parallel execution can be slower than the
       serial execution.

    """
    if kwargs is None:
        kwargs = {}
    if args is None:
        args = []

    if max_workers > 1 or backend is False:
        ensure_single_thread_numeric()

    q = queue.Queue()

    if backend is not False:
        assert buffer_size >= max_workers
    assert buffer_size > 0

    if backend == "mp":
        # http://stackoverflow.com/a/21345423
        from pathos.multiprocessing import ProcessPool as PathosPool
        PoolExecutor = PathosPool

        def submit(ex, func, *args, **kwargs):
            return ex.apipe(func, *args, **kwargs)

        def result(job):
            return job.get()

    elif backend == "dill_mp":
        import dill

        # https://stackoverflow.com/a/24673524
        PoolExecutor = concurrent.futures.ProcessPoolExecutor

        def submit(ex, func, *args, **kwargs):
            payload = dill.dumps((func, args, kwargs))
            return ex.submit(_dill_mp_helper, payload)

        def result(job):
            return job.result()

    elif backend in [
            "t",
            "thread",
            "concurrent_mp"
    ]:
        if backend in ['t', 'thread']:
            PoolExecutor = concurrent.futures.ThreadPoolExecutor
        elif backend == "concurrent_mp":
            # does not allow to pickle arbitrary functions
            PoolExecutor = concurrent.futures.ProcessPoolExecutor
        else:
            raise ValueError(backend)

        def submit(ex, func, *args, **kwargs):
            return ex.submit(func, *args, **kwargs)

        def result(job):
            return job.result()
    # elif backend is False:
    #
    #     @contextmanager
    #     def PoolExecutor(max_workers):
    #         yield None
    #
    #     def submit(ex, func, *args, **kwargs):
    #         return func(*args, **kwargs)
    #
    #     def result(job):
    #         return job
    else:
        raise ValueError(backend)

    with PoolExecutor(max_workers) as executor:
        # First fill the buffer
        # If buffer full, take one element and push one new inside
        for ele in generator:
            if q.qsize() >= buffer_size:
                yield result(q.get())
            q.put(submit(executor, function, ele, *args, **kwargs))
        while not q.empty():
            yield result(q.get())


if __name__ == '__main__':
    import time

    def identity(x):
        return x


    print(f'Expect: ' + ' '.join(map(str, range(10))))
    print('Got:    ', end='')
    for i in lazy_parallel_map(identity, range(10)):
        print(i, end=' ')
    print()

    print(f'Expect: ' + ' '.join(map(str, range(10))))
    print('Got:    ', end='')
    for backend in [
        't',
        'mp',
        'concurrent_mp',
        # False,
    ]:

        for i in lazy_parallel_map(identity, range(10), backend=backend):
            print(i, end=' ')
        print()


    def task(i):
        time.sleep(0.1)
        return i


    print(f'Expect: ' + ' '.join(map(str, range(10))))
    print('Got:    ', end='')
    for i in lazy_parallel_map(lambda x: x, range(10), backend='dill_mp'):
        print(i, end=' ')
    print()

    from paderbox.utils.timer import Timer
    t = Timer(verbose=True)

    print(f'Serial time: ')
    print('Got:    ', end='')
    with t:
        for i in lazy_parallel_map(task, range(10), backend='dill_mp',
                                   buffer_size=5, max_workers=2):
            print(i)
            # print(i, end=' ')

    # Does not work
    # for i in lazy_parallel_map(lambda x: x, range(10), backend='concurrent_mp'):
    #     print(i, end=' ')
    # print()
