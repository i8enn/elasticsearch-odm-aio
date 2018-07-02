import pytest
import inspect

from esodm_async.fields.base import ESBaseField
from tests.conftest import TestField, TestFieldModel


# noinspection PyUnresolvedReferences,PyStatementEffect
@pytest.mark.asyncio
class TestingBaseFields(object):

    @pytest.mark.xfail
    async def test_init_field(self):
        obj = TestFieldModel()
        fields_list = {f[0]: f[1] for f in inspect.getmembers(obj.__class__) if getattr(f[1], 'is_field', False)}
        assert fields_list

        for attr, field in fields_list.items():
            assert issubclass(field.__class__, ESBaseField)
            assert field._model_attr == attr

    @pytest.mark.xfail
    async def test_set_default_field_value(self):
        obj = TestFieldModel()
        assert obj.name == TestFieldModel.name.default

    @pytest.mark.xfail
    async def test_set_value_field_to_model_object(self):
        obj = TestFieldModel()
        assert obj.name == TestFieldModel.name.default
        obj.name = "NewTest"
        assert obj.name == "NewTest"

    @pytest.mark.xfail
    async def test_get_value_field_from_model_object(self):
        obj = TestFieldModel()
        assert obj.name == "Test"

    @pytest.mark.xfail
    async def test_get_field_from_model_class(self):
        assert isinstance(TestFieldModel.name, TestField)

    @pytest.mark.xfail
    async def test_raises_if_get_field_attr_from_model_object(self):
        with pytest.raises(AttributeError):
            TestFieldModel().name.default
