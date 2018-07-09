import inspect

from esodm_async.fields.base import ESBaseField
from esodm_async.models import ESModel


class TestField(ESBaseField):
    pass


class TestFieldModel(ESModel):
    class Meta:
        index = "Test"

    name = TestField(default="Test")
    _private_field = TestField(default="Im private :P")

    # # FIXME: Remove after implement model
    # def __init__(self):
    #     fields_list = {f[0]: f[1] for f in inspect.getmembers(self.__class__) if getattr(f[1], 'is_field', False)}
    #     for f_name, field in fields_list.items():
    #         field.model_instance = self
    #         field._model_attr = f_name
