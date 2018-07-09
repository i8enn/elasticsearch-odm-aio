from collections import abc


class ESBaseQuerySet(abc.AsyncIterator):

    _data: []
    _aiter: abc.Iterator

    def __init__(self, data: list = None):
        self._data = data or []

        super(ESBaseQuerySet, self).__init__()

    async def __aiter__(self) -> abc.AsyncIterator:
        self._aiter = self._data.__iter__()
        return self

    async def __anext__(self):
        try:
            return self._aiter.__next__()
        except (StopIteration, StopAsyncIteration):
            raise StopAsyncIteration

    def __getitem__(self, item):
        if not isinstance(item, (int, slice)):
            raise TypeError("%s is not %s or %s" % (item, int.__name__, slice.__name__))
        return self._data[item]

    def __setitem__(self, key, value):
        raise TypeError("%s is immutable object" % self.__class__.__name__)

    def append(self, item):
        raise TypeError("%s is immutable object" % self.__class__.__name__)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        raise TypeError("%s is immutable object" % self.__class__.__name__)
