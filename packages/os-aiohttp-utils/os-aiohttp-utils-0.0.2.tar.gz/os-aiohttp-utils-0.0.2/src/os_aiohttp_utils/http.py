import copy
import io

import aiohttp
from aiohttp.helpers import sentinel
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed


async def request(
    method,
    url,
    timeout=sentinel,
    retry_attempt=0,
    retry_wait=0,
    retry_reraise=False,
    retry_exceptions=None,
    downstream=None,
    text_body=False,
    chunk_size=1 * 1024 * 1024,
    **kwargs,
):

    retry_kwargs = {}
    if retry_attempt > 0:
        retry_kwargs["stop"] = stop_after_attempt(retry_attempt + 1)
    if retry_wait > 0:
        retry_kwargs["wait"] = wait_fixed(retry_wait)
    if retry_exceptions:
        retry_kwargs["retry"] = retry_if_exception_type(retry_exceptions)
    if retry_reraise:
        retry_kwargs["reraise"] = True

    def ensure(obj, *attrs):
        for a in attrs:
            if not hasattr(obj, a):
                raise AttributeError(f"must support {a} with retry enabled")

    class StreamWrapper(io.IOBase):
        def __init__(self, o):
            self.o = o
            self.pos = self.o.tell()

        def read(self, size=-1):
            return self.o.read(size)

        def reset(self, truncate=False):
            self.o.seek(self.pos)
            if truncate:
                self.o.truncate()

        def write(self, block):
            return self.o.write(block)

        def close(self):
            pass

    data = kwargs.get("data", None)
    if retry_kwargs and downstream:
        ensure(downstream, "seek", "truncate", "tell")
        downstream = StreamWrapper(downstream)

    if isinstance(data, io.IOBase):
        if retry_kwargs:
            ensure(data, "seek", "tell")
        data = StreamWrapper(data)
        kwargs = copy.copy(kwargs)
        kwargs["data"] = data

    if timeout is None:
        timeout = sentinel
    elif isinstance(timeout, (int, float)) and timeout > 0:
        timeout = aiohttp.ClientTimeout(total=timeout)

    async def _do():
        body = None
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with aiohttp.request(method, url, **kwargs) as response:
                if not downstream:
                    func = "read"
                    if text_body:
                        func = "text"
                    body = await getattr(response, func)()
                else:
                    while True:
                        block = await response.content.read(chunk_size)
                        if not block:
                            break
                        downstream.write(block)
                return response, body

    async def do():
        try:
            return await _do()
        except Exception as e:
            if retry_kwargs:
                if downstream:
                    downstream.reset(truncate=True)
                if isinstance(data, StreamWrapper):
                    data.reset()
            raise e

    f = do
    if retry_kwargs:
        f = retry(**retry_kwargs)(f)
    return await f()
