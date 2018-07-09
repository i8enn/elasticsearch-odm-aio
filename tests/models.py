import pytest

from esodm_async.models import ESModel, ESBaseModel
from esodm_async.managers import ESManager
from .conftest import TestFieldModel


class BaseTestModel(ESModel):
    class Meta:
        index = "Test"


@pytest.mark.asyncio
class TestingESModel(object):

    async def test_init_options_class_in_model_class(self):
        class TestModel(BaseTestModel):
            class Meta:
                index = 'Test'

        assert TestModel._meta.model_cls == TestModel

    async def test_init_options_class_with_meta_class_in_model_class(self):
        class TestModel(BaseTestModel):
            class Meta:
                index = 'Test'
                important_property = ":P"

        assert TestModel._meta.important_property == ":P"

    async def test_override_options_property_in_meta_class_of_model_class(self):
        class TestModel(BaseTestModel):
            class Meta:
                index = 'Test'
                important_property = ":("

        class TestModelChildren(TestModel):
            class Meta:
                index = 'Test'
                important_property = ":P"

        assert TestModel._meta.important_property == ":("
        assert TestModelChildren._meta.important_property == ":P"

    # noinspection PyUnusedLocal
    async def test_raise_if_not_index_attr_in_model_class(self):
        with pytest.raises(ValueError, match="'index' not defined"):
            class TestModel(ESModel):
                class Meta:
                    index = None

    async def test_auto_seated_doc_type_if_not_defined_in_meta(self):
        class TestModel(BaseTestModel):
            class Meta:
                index = "Test"
                doc_type = "TestDocType"

        assert TestModel._meta.doc_type == "TestDocType"
        assert BaseTestModel._meta.doc_type == BaseTestModel.__name__

    async def test_move_meta_class_from_model_class(self):
        assert not getattr(BaseTestModel, 'Meta')
        assert getattr(BaseTestModel, '_meta')

    async def test_create_obj_with_field_values(self):
        kwargs = {"name": "Testing", "_private_field": "im invisible"}
        obj = TestFieldModel(**kwargs)
        for attr, value in kwargs.items():
            assert getattr(obj, attr, None) == value

    async def test_init_manager(self):
        class TestModel(metaclass=ESBaseModel):
            class Meta:
                index = "Test"
            objects = ESManager

        assert isinstance(TestModel.objects, ESManager)

    # noinspection PyUnusedLocal
    async def test_raise_if_no_defined_manager(self):
        with pytest.raises(AttributeError, match="no manager defined"):
            class TestModel(metaclass=ESBaseModel):
                class Meta:
                    index = "Test"

    async def test_get_manager_map_from_meta(self):
        class TestModel(ESModel):
            class Meta:
                index = "Test"

            objects = ESManager
            first_manager = ESManager
            second_manager = ESManager
            last_manager = ESManager

        for attr, manager in TestModel._meta.managers.items():
            assert hasattr(TestModel, attr)
            assert isinstance(manager, getattr(TestModel, attr).__class__)
