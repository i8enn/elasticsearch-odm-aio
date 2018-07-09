import inspect

from esodm_async.querysets import ESQuerySet


class ESBaseManager(object):

    _queryset_cls = None
    model = None
    is_manager = True  # Need for find manager in model

    def __init__(self, *args, **kwargs):
        from esodm_async.models import ESBaseModel
        model = kwargs.get('model')
        if isinstance(model, ESBaseModel):
            raise AttributeError("%s is not instance %s" % (model, ESBaseModel.__name__))
        super(ESBaseManager, self).__init__()

    def __get__(self, instance, owner):
        """
        This method need control access to manager (not access from model instance)
        :param instance: inherit
        :param owner: inherit
        :return: manager instance
        """
        if instance is not None:
            raise AttributeError("Сan not call manager from model instance")
        return self

    @classmethod
    def _get_queryset_methods(cls, queryset_cls) -> dict:
        """
        This method returned public methods of queryset
        :param queryset_cls: queryset class
        :return: methods dictionary (dict)
        """

        # noinspection PyShadowingNames
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
            '_queryset_cls': queryset_cls,
            **cls._get_queryset_methods(queryset_cls),
        })

    def get_queryset(self, *args, **kwargs) -> ESQuerySet:
        """
        This method returned queryset object with args
        :return: Queryset (ESQuerySet object)
        """
        return self._queryset_cls(model=self.model, *args, **kwargs)


class ESManager(ESBaseManager.from_queryset(queryset_cls=ESQuerySet)):

    def __init__(self, *args, **kwargs):
        from esodm_async.models import ESBaseModel
        self.model = kwargs.get('model', None)
        if not self.model or not isinstance(self.model, ESBaseModel):
            raise TypeError("%s is not instance from %s" % (self.model, ESBaseModel.__name__))
