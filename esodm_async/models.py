import inspect

from esodm_async.options import ESOptions


class ESBaseModel(type):
    """Default metaclass for all models"""

    class Meta:
        pass

    def __init__(cls, *args, **kwargs):

        meta_class = ESOptions(cls)
        meta_attrs = meta_class.get_attrs(include_parents=True, include_hidden=True)
        # Override attrs from customer Meta class
        if hasattr(cls, 'Meta'):
            meta_attrs.update(dict(inspect.getmembers(cls.Meta)))
        # Update meta class attrs
        # FIXME: May be very bad code...
        meta_class.__dict__.update({k: v for k, v in meta_attrs.items() if k not in meta_class.protected_attrs})

        # Check index in Meta
        if not getattr(meta_class, 'index', None) and cls.__name__ != 'ESModel':
            raise ValueError("Required attribute 'index' not defined in the meta class of the model %s" % cls)

        # Check doc_type in Meta
        doc_type = getattr(meta_class, 'doc_type', None)
        # Set default doc_type if not defined user in Meta class
        if (
                not doc_type
                or (doc_type != cls.__name__ and not getattr(cls.Meta, 'doc_type', None))
        ) and cls.__name__ != 'ESModel':
            setattr(meta_class, 'doc_type', cls.__name__)

        # Set new Meta class (Options) to _meta attr in model
        cls._meta = meta_class
        cls.Meta = None

        # Set _model_attr to fields
        for attr, field in cls._meta.get_fields(include_hidden=True).items():
            field._model_attr = attr

        super(ESBaseModel, cls).__init__(*args, **kwargs)


class ESModel(metaclass=ESBaseModel):
    _meta = None

    class Meta:
        pass

    def __init__(self, *args, **kwargs):
        # Load initial values for object from kwargs
        for attr, field in self._meta.get_fields(include_hidden=True).items():
            field.value = kwargs.get(attr, None)
