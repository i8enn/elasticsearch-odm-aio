import pytest
from collections import AsyncIterable


from esodm_async.querysets import ESBaseQuerySet
from esodm_async.utils import aenumerate


@pytest.mark.asyncio
class TestingESBaseQueryset(object):

    async def test_iterate_qs(self):
        qs = ESBaseQuerySet([1, 2, 3])

        assert isinstance(qs, AsyncIterable)

        async for i, item in aenumerate(qs):
            assert item == qs[i]

    async def test_immutable_data(self):
        qs = ESBaseQuerySet([1, 2, 3])
        with pytest.raises(TypeError, match="ESBaseQuerySet is immutable object"):
            qs.append(4)

        with pytest.raises(TypeError, match="ESBaseQuerySet is immutable object"):
            qs[3] = 4
