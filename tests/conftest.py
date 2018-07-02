import inspect

from esodm_async.fields.base import ESBaseField


class TestField(ESBaseField):
    pass


class TestFieldModel(object):
    name = TestField(default="Test")

    # FIXME: Remove after implement model
    def __init__(self):
        fields_list = {f[0]: f[1] for f in inspect.getmembers(self.__class__) if getattr(f[1], 'is_field', False)}
        for fname, field in fields_list.items():
            field.model_instance = self
            field._model_attr = fname