import builtins
import inspect

from .models import ESBaseModel


class ESOptions(object):
    index = None
    doc_type = None
    model = None

    _fields = {}

    def __init__(self, model, *args, **kwargs):
        super(ESOptions, self).__init__()

        if issubclass(ESBaseModel, model):
            raise TypeError("%s is not subclass of %s" % (model.__class__, ESBaseModel.__class__))

        self.model = model

        self.index = kwargs.get('index', self.index)
        self.doc_type = kwargs.get('doc_type', self.model.__class__.__name__)

    def get_fields(self, include_hidden: bool = False) -> dict:
        """
        This method returning properties market as field.
        :param include_hidden: Returning all properties (including those that begin with "_")
        :return: properties dictionary (dict)
        """
        if include_hidden:
            return {f[0]: f[1] for f in inspect.getmembers(self.model) if getattr(f[1], 'is_field', False)}

        return {f[0]: f[1] for f in inspect.getmembers(self.model)
                if getattr(f[1], 'is_field', False) and not f[0].startswith("_", 0, 2)}

    def get_parents(self) -> list:
        """
        This method returning all parent (without builtin classes) from model class.
        :return: Model parents list (list)
        """
        parents = [parent for parent in inspect.getmro(self.model)
                   if parent.__name__ not in dir(builtins)]
        parents.reverse()
        return parents

    def get_attrs(self, include_parents: bool = False, include_hidden: bool = False) -> dict:
        """
        This method returning Meta attributes.
        :param include_parents: Returning attributes from all parents model class
        :param include_hidden: Returning all attributes (including those that begin with "_")
        :return: attributes dictionary (dict)
        """
        attrs = {}
        if not include_parents:
            attrs.update(dict(inspect.getmembers(self)))
        else:
            for parent in self.get_parents():
                if hasattr(parent, '_meta'):
                    attrs.update(dict(inspect.getmembers(parent._meta)))
        if not include_hidden:
            return {f[0]: f[1] for f in attrs.items() if not f[0].startswith("_", 0, 2)}
        return attrs
