import inspect

from esodm_async.fields.base import ESBaseField
from esodm_async.models import ESBaseModel
from esodm_async.options import ESOptions


class TestField(ESBaseField):
    pass


class TestFieldModel(ESBaseModel):
    name = TestField(default="Test")
    _private_field = TestField(default="Im private :P")

    # FIXME: Remove after implement model
    def __init__(self):
        self._meta = ESOptions(model=self.__class__)

        fields_list = {f[0]: f[1] for f in inspect.getmembers(self.__class__) if getattr(f[1], 'is_field', False)}
        for f_name, field in fields_list.items():
            field.model_instance = self
            field._model_attr = f_name
