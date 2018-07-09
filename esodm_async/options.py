import builtins
import inspect


class ESOptions(object):
    """This class using for template Meta class in model"""
    index = None
    doc_type = None
    model_cls = None

    # Not overrides attributes in ESBaseModel.__init__ metaclass
    protected_attrs = ('model_cls',)

    def __init__(self, model_cls, *args, **kwargs):
        from esodm_async.models import ESBaseModel
        if not isinstance(model_cls, ESBaseModel):
            raise TypeError("%s not instance of %s metaclass" % (model_cls, ESBaseModel))

        self.model_cls = model_cls

    def get_fields(self, include_hidden: bool = False) -> dict:
        """
        This method returning properties market as field.
        :param include_hidden: Returning all properties (including those that begin with "_")
        :return: properties dictionary (dict)
        """
        if include_hidden:
            return {f[0]: f[1] for f in inspect.getmembers(self.model_cls)
                    if getattr(f[1], 'is_field', False)}

        return {f[0]: f[1] for f in inspect.getmembers(self.model_cls)
                if getattr(f[1], 'is_field', False) and not f[0].startswith("_", 0, 2)}

    def get_parents(self) -> list:
        """
        This method returning all parent (without builtin classes) from model class.
        :return: Model parents list (list)
        """
        # [::-1] - reverse list
        return [parent for parent in inspect.getmro(self.model_cls)
                if parent.__name__ not in dir(builtins)][::-1]

    def get_attrs(self, include_parents: bool = False, include_hidden: bool = False) -> dict:
        """
        This method returning Meta attributes.
        :param include_parents: Returning Meta attributes from all parents model class
        :param include_hidden: Returning all attributes (including those that begin with "_")
        :return: attributes dictionary (dict)
        """
        attrs = {}
        if include_parents:
            for parent in self.get_parents():
                if hasattr(parent, '_meta'):
                    attrs.update(dict(inspect.getmembers(parent._meta)))
        attrs.update(dict(inspect.getmembers(self)))
        if not include_hidden:
            return {f[0]: f[1] for f in attrs.items() if not f[0].startswith("_", 0, 2)}
        return attrs
