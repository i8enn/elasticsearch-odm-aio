from collections import abc


# noinspection PyPep8Naming
class aenumerate(abc.AsyncIterator):
    def __init__(self, aiterable, start=0):
        self._aiterable = aiterable
        self._i = start - 1

    async def __aiter__(self):
        self._ait = await self._aiterable.__aiter__()
        return self

    async def __anext__(self):
        val = await self._ait.__anext__()
        self._i += 1
        return self._i, val
