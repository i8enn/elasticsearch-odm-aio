import builtins

import pytest
import inspect

from esodm_async.options import ESOptions
from .conftest import TestFieldModel


class BadModel(object):

    _meta = None

    def __new__(cls, *args, **kwargs):
        cls._meta = ESOptions(model=cls)
        return super(BadModel, cls).__new__()


@pytest.mark.asyncio
class TestingOptions(object):

    async def test_raises_if_model_not_subclass__base_model(self):
        with pytest.raises(TypeError, message="is not subclass of %s"):
            BadModel()

    async def test_getting_public_field_of_model(self):
        obj = TestFieldModel()

        fields_list = {f[0]: f[1] for f in inspect.getmembers(obj.__class__)
                       if getattr(f[1], 'is_field', False) and not f[0].startswith("_", 0, 2)}
        assert obj._meta.get_fields() == fields_list

    async def test_getting_all_field_of_model(self):
        obj = TestFieldModel()

        fields_list = {f[0]: f[1] for f in inspect.getmembers(obj.__class__)
                       if getattr(f[1], 'is_field', False)}
        assert obj._meta.get_fields(include_hidden=True) == fields_list

    async def test_get_parents_of_model_classes(self):
        obj = TestFieldModel()

        parents = obj._meta.get_parents()
        for parent in inspect.getmro(TestFieldModel):
            if parent.__name__ not in dir(builtins):
                assert parent in parents

    async def test_get_meta_class_attrs(self):
        meta_attrs = {f[0]: f[1] for f in inspect.getmembers(BadModel._meta)
                      if not f[0].startswith("_", 0, 2)}
        for attr in meta_attrs.keys():
            assert attr in BadModel._meta.get_attrs().keys(), BadModel._meta.get_attrs()

    async def test_get_meta_class_attrs_include_hidden(self):
        meta_attrs = dict(inspect.getmembers(BadModel._meta))
        for attr in meta_attrs.keys():
            assert attr in BadModel._meta.get_attrs(include_hidden=True).keys()

    async def test_get_meta_class_attrs_include_parents(self):
        meta_attrs = {}
        for parent in BadModel._meta.get_parents():
            meta_attrs.update({f[0]: f[1] for f in inspect.getmembers(parent._meta) if not f[0].startswith("_", 0, 2)})
        for attr in meta_attrs.keys():
            assert attr in BadModel._meta.get_attrs(include_parents=True).keys()
