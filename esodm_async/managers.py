import inspect

from esodm_async.querysets import ESQuerySet


class ESBaseManager(object):

    _queryset_cls = None

    def __init__(self, *args, **kwargs):
        self._queryset_cls = kwargs.get('queryset_cls')

    # TODO: Need implement
    def __get__(self, instance, owner):
        raise NotImplementedError

    @classmethod
    def _get_queryset_methods(cls, queryset_cls) -> dict:
        """
        This method returned public methods of queryset
        :param queryset_cls: queryset class
        :return: methods dictionary (dict)
        """
        def create_method(name, method):
            def manager_method(self, *args, **kwargs):
                return getattr(self.get_queryset(), name)(*args, **kwargs)
            manager_method.__name__ = method.__name__
            manager_method.__doc__ = method.__doc__
            return manager_method

        methods = {}
        for name, method in inspect.getmembers(queryset_cls, predicate=inspect.isfunction):
            if hasattr(cls, name):
                continue

            queryset_only = getattr(method, 'queryset_only', None)
            if queryset_only or (queryset_only is None or name.startswith('_')):
                continue

            methods[name] = create_method(name, method)
        return methods

    @classmethod
    def from_queryset(cls, queryset_cls, class_name: str = None):
        """
        This method returned manager class from queryset
        :param queryset_cls: queryset class
        :param class_name: class name (default - {cls.__name__}From{queryset_cls.__name__})
        :return: manager class (cls)
        """
        if class_name is None:
            class_name = "%sFrom%s" % (cls.__name__, queryset_cls.__name__)
        return type(class_name, (cls,), {
            '_queryset_class': queryset_cls,
            **cls._get_queryset_methods(queryset_cls),
        })

    def get_queryset(self, *args, **kwargs) -> ESQuerySet:
        """
        This method returned queryset object with args
        :return: Queryset (ESQuerySet object)
        """
        return self._queryset_cls(*args, **kwargs)


class ESManager(ESBaseManager.from_queryset(queryset_cls=ESQuerySet)):
    pass
