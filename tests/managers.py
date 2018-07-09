import pytest
import inspect

from esodm_async.managers import ESBaseManager, ESManager
from esodm_async.querysets import ESQuerySet


@pytest.mark.asyncio
class TestingESManager(object):

    async def test_create_manager_from_qs(self):
        objects = ESBaseManager.from_queryset(ESQuerySet)
        assert objects.__name__ == "%sFrom%s" % (ESBaseManager.__name__, ESQuerySet.__name__)

    async def test_create_manager_from_qs_with_custom_cls_name(self):
        cls_name = "NewTestManager"
        objects = ESBaseManager.from_queryset(ESQuerySet, class_name=cls_name)
        assert objects.__name__ == cls_name

    async def test_copy_methods_from_queryset(self):
        # noinspection PyShadowingNames
        def create_method(name, method):
            # noinspection PyShadowingNames
            def manager_method(self, *args, **kwargs):
                return getattr(self.get_queryset(), name)(*args, **kwargs)
            manager_method.__name__ = method.__name__
            manager_method.__doc__ = method.__doc__
            return manager_method

        methods = {}
        for name, method in inspect.getmembers(ESQuerySet, predicate=inspect.isfunction):
            if hasattr(ESBaseManager, name):
                continue

            queryset_only = getattr(method, 'queryset_only', None)
            if queryset_only or (queryset_only is None or name.startswith('_')):
                continue

            methods[name] = create_method(name, method)

        manager = ESBaseManager.from_queryset(ESQuerySet)

        for name, method in methods.items():
            manager_method = getattr(manager, name, None)
            assert manager_method
            assert method.__name__ == manager_method.__name__
            assert method.__doc__ == manager_method.__doc__


@pytest.mark.asyncio
class TestingESQueryset(object):

    async def test_create_standard_manager_from_qs(self):
        assert ESManager._queryset_class == ESQuerySet
