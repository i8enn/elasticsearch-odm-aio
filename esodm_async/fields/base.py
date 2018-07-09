class ESBaseField(object):

    _value = None
    _model_attr = None

    def __init__(self, *args, **kwargs):
        super(ESBaseField, self).__init__()
        self.default = kwargs.get('default')

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self.value

    def __set__(self, instance, value):
        self._value = value

    def __str__(self):
        return "<ModelField %s: %s>" % (self.__class__.__name__, self._model_attr)

    @property
    def value(self):
        return self._value if self._value else self.default

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def is_field(self):
        return True
