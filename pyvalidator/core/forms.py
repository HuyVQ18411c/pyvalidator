__all__ = ('Form', )

from pyvalidator.core.validators import Field


class BaseFormMetaClass(type):
    def __new__(cls, name, bases, attrs: dict):
        # Loop through the current class
        attrs["declared_fields"] = {
            key: attrs.pop(key)
            for key, value in list(attrs.items())
            if (
                not callable(value) and
                not key.startswith('__') and
                isinstance(value, Field)
            )
        }

        new_class = super().__new__(cls, name, bases, attrs)

        declared_fields ={}
        # Loop through the super class and get all class attributes
        for base_class in reversed(new_class.__mro__):
            if hasattr(base_class, 'declared_fields'):
                declared_fields.update(base_class.declared_fields)

        new_class.declared_fields = declared_fields

        return new_class


class Form(metaclass=BaseFormMetaClass):
    def __init__(self, data: dict = None, raise_exception_on_error=True):
        self._data = data if data else {}
        self._cleaned_data = {}
        self._raise_exception_on_error = raise_exception_on_error
