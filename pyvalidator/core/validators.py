__all__ = [
    'Field',
    'IntField',
    'FloatField',
    'StringField',
    'EmailField',
    'URLField',
]

import re

# Define a UnionType for Numeric base class
NumericType = int | float
VALIDATION_ERROR_MESSAGE = 'Field `{field_name}` value {field_value} is {error} {boundary_value}'


###################
# Base Validators #
###################
class Field:
    """
    Base class for all validators
    This class defines 3 essential methods for a validator (__set_name__, __get__, __set__),
    which are specific for a descriptor and was described in Python 3 documentation:
    https://docs.python.org/3/howto/descriptor.html
    Read this guideline, especially section: Technical Tutorial to understand what they do
    """
    __field_type__ = None

    def __init__(
        self,
        *,
        default=None,
        nullable: bool = False,
        custom_validators: list[callable] = None,
        force_conversion: bool = False,
        **kwargs,
    ):
        """
        Parameters
        ----------
        default (any): default value for field
        nullable (bool): is field able to set to None
        custom_validators (list[callable]): list of user-defined functions to validate value
        force_conversion (bool): is forced to cast to desired type before perform validation
        """
        if self.__field_type__ is None:
            raise ValueError('Type is not set for field')

        self._value = default
        self._nullable = nullable
        self._force_conversion = force_conversion

        if custom_validators is None:
            self._custom_validators = []
        else:
            self._custom_validators = custom_validators

    def __set_name__(self, owner, name):
        self._field_name = name
        self._owner_klass = owner.__class__

    def __get__(self, instance, owner):
        return self._value

    def __set__(self, instance, value: any) -> None:
        if self._force_conversion:
            # Don't try/catch, let it raise exception
            value = self.__field_type__(value)

        self.validate(value)

        # Value is safe to be set
        self._value = value

    def _built_in_validation(self, value: any):
        raise NotImplementedError('Initial validator for %s is not implemented' % self.__class__.__name__)

    def _get_error_message(self, field_name, field_value, error, boundary_value=None):
        return VALIDATION_ERROR_MESSAGE.format(
            field_name=field_name,
            field_value=field_value,
            error=error,
            boundary_value=boundary_value,
        ).strip()

    def validate(self, value: any):
        if value is None and self._nullable is False:
            raise ValueError('%s field is not nullable' % self._field_name)

        if not isinstance(value, self.__field_type__):
            raise ValueError(
                '%s value is not a valid type for %s' % (self._field_name, self.__field_type__)
            )

        self._built_in_validation(value)

        for validator in self._custom_validators:
            validator(value)


######################
# Numeric Validators #
######################
class NumericField(Field):
    """
    Base class for all numeric field including IntField, FloatField

    Caution:
    This class is not intended to use directly, it is implemented as a base class
    Set __field_type__ properly if you want to use this base class, since `NumericType` is an UnionType and not callable
    """
    __field_type__ = NumericType

    def __init__(
        self,
        *,
        min_value: NumericType = None,
        max_value: NumericType = None,
        **kwargs
    ):
        self._min_value = self.__field_type__(min_value) if min_value is not None else min_value
        self._max_value = self.__field_type__(max_value) if max_value is not None else max_value
        super().__init__(**kwargs)

    def _built_in_validation(self, value):
        if self._min_value is not None and value < self._min_value:
            raise ValueError(
                self._get_error_message(
                    field_name=self._field_name,
                    field_value=value,
                    error='smaller than min value',
                    boundary_value=self._min_value
                )
            )

        if self._max_value is not None and value > self._max_value:
            raise ValueError(
                self._get_error_message(
                    field_name=self._field_name,
                    field_value=value,
                    error='greater than max value',
                    boundary_value=self._max_value,
                )
            )


class IntField(NumericField):
    __field_type__ = int


class FloatField(Field):
    __field_type__ = float


#####################
# String Validators #
#####################
class StringField(Field):
    __field_type__ = str
    REGEX_PATTERN = None

    def __init__(
            self,
            *,
            min_length: int = None,
            max_length: int = None,
            **kwargs
    ):
        # Set min length = 0 to allow blank
        self._min_length = min_length
        self._max_length = max_length
        super().__init__(**kwargs)

    def _regex_validation(self, value):
        if not re.match(self.REGEX_PATTERN, value):
            raise ValueError(
                self._get_error_message(
                    field_name=self._field_name,
                    field_value=value,
                    error='not a valid pattern',
                    boundary_value='',
                )
            )

    def _built_in_validation(self, value: str):
        value_length = len(value)
        if self._min_length is not None and value_length < self._min_length:
            raise ValueError(
                self._get_error_message(
                    field_name=self._field_name,
                    field_value=value,
                    error='shorter than min length',
                    boundary_value=self._min_length,
                )
            )

        if self._max_length is not None and value_length > self._max_length:
            raise ValueError(
                self._get_error_message(
                    field_name=self._field_name,
                    field_value=value,
                    error='longer than max length',
                    boundary_value=self._max_length,
                )
            )

        if self.REGEX_PATTERN:
            # If a regex pattern is defined, use it to validate
            self._regex_validation(value)


class EmailField(StringField):
    REGEX_PATTERN = re.compile(
        r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)"
        r"*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$",
        re.IGNORECASE
    )


class URLField(StringField):
    """
    Validate if a piece string is a URL
    """
    REGEX_PATTERN = re.compile(
        r'^(?:http|ftp)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$',
        re.IGNORECASE
    )
