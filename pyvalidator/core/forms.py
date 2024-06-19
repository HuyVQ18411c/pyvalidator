__all__ = ('Form', )

from collections import defaultdict

from pyvalidator.core.validators import Field


class BaseFormMetaClass(type):
    def __new__(cls, name, bases, attrs: dict):
        # Get all class attributes and add to dict
        # This piece of code is inspired from Django:
        # https://github.com/django/django/blob/main/django/forms/forms.py#L24
        attrs["declared_fields"] = {
            key: attrs.get(key)
            for key, value in list(attrs.items())
            if isinstance(value, Field)
        }

        new_class = super().__new__(cls, name, bases, attrs)

        declared_fields: dict[str, Field] = {}
        # Loop through the super class and get all class attributes
        for base_class in reversed(new_class.__mro__):
            if hasattr(base_class, 'declared_fields'):
                declared_fields.update(base_class.declared_fields)

        new_class.declared_fields = declared_fields

        return new_class


class Form(metaclass=BaseFormMetaClass):
    def __init__(self, data: dict = None, raise_exception_on_error=False):
        self._data = data if data else {}
        self._cleaned_data = {}
        self._raise_exception_on_error = raise_exception_on_error
        self._errors = defaultdict(list)

    @property
    def cleaned_data(self):
        return self._cleaned_data

    @property
    def errors(self):
        return self._errors

    def is_valid(self):
        """
        Return if the form is valid

        Returns
        -------
        is_valid (bool): True if the form is valid, else False
        """
        if not self._cleaned_data and not self.errors:
            self.full_clean()

        return False if self._errors else True

    def _clean_field(self, field_name: str, field_value: any):
        """
        Seek for clean method and clean single field
        Parameters
        ----------
        field_name (str): field name to be cleaned
        field_value (any): value to be cleaned

        Returns
        -------
        field_value (any): value after clean

        Notes
        -----
        Custom clean method for field must start with clean_<field-name>
        """
        clean_func_name = 'clean_%s' % field_name
        if hasattr(self, clean_func_name):
            func = getattr(self, clean_func_name)

            return func(field_value)

        return field_value

    def _clean_fields(self):
        """
        Clean form data and set value fields
        """
        for key, value in self.declared_fields.items():
            try:
                setattr(self, key, self._data[key])
                # Call the custom clean methods first
                cleaned_field = self._clean_field(key, getattr(self, key))
                # Set value to field
                setattr(self, key, cleaned_field)
                self._cleaned_data[key] = value
            except Exception as ex:
                if self._raise_exception_on_error:
                    raise ex
                else:
                    self._errors[key].append(ex)

    def full_clean(self):
        """ Run full clean on input data """
        if not self._data:
            raise ValueError('No data was provided for %s' % self.__class__.__name__)

        # Clean fields and set values to fields
        self._clean_fields()

        # Run custom clean, usually use with cleaned_data
        try:
            if hasattr(self, 'clean') and not self._errors:
                getattr(self, 'clean')()
        except Exception as ex:
            if self._raise_exception_on_error:
                raise ex
            else:
                self._errors[self.__class__.__name__].append(ex)
