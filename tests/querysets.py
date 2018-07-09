import pytest
from collections import AsyncIterable


from esodm_async.querysets import ESBaseQuerySet
from esodm_async.utils import aenumerate
from .conftest import TestFieldModel


@pytest.yield_fixture(scope="module")
def model_objects():
    yield [
        TestFieldModel(name="Object #%s" % i, age=i+10)
        for i in range(1, 5)
    ]


# noinspection PyShadowingNames
@pytest.mark.asyncio
class TestingESBaseQueryset(object):

    async def test_raise_if_not_model_with_create_queryset(self):
        with pytest.raises(TypeError, match="is not instance of ESBaseModel"):
            ESBaseQuerySet([1, 2, 3])

    async def test_raise_if_item_data_is_not_instance_of_model(self):
        with pytest.raises(TypeError, match="is not instance of %s" % TestFieldModel.__name__):
            ESBaseQuerySet(model=TestFieldModel, data=[1, 2, 3])

    async def test_iterate_qs(self, model_objects):
        qs = ESBaseQuerySet(model=TestFieldModel, data=model_objects)

        assert isinstance(qs, AsyncIterable)

        async for i, item in aenumerate(qs):
            assert item == qs[i]

    async def test_immutable_data(self, model_objects):
        qs = ESBaseQuerySet(model=TestFieldModel, data=model_objects)
        with pytest.raises(TypeError, match="ESBaseQuerySet is immutable object"):
            qs[3] = 4

    async def test_negative_index(self, model_objects):
        qs = ESBaseQuerySet(model=TestFieldModel, data=model_objects)
        assert qs[-1] == model_objects[-1]
