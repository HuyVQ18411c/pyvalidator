from datetime import date, datetime
from unittest import TestCase

from pyvalidator.core.exceptions import ConversionError
from pyvalidator.core.validators import (
    IntField,
    StringField,
    EmailField,
    URLField,
    DateField, DateTimeField,
)


class Audience:
    """
    This class is implemented for testing purpose only
    """
    age = IntField(min_value=18, max_value=60, nullable=False, force_conversion=True)
    name = StringField(min_length=1, max_length=5, nullable=True, force_conversion=True)
    email = EmailField()
    social_media_link = URLField()
    date_of_birth = DateField(force_conversion=True)
    created_at = DateTimeField(force_conversion=True)


class BaseFieldTestCase(TestCase):
    def setUp(self):
        self.test_audience = Audience()


class TestIntField(BaseFieldTestCase):
    def test_age_field_failed_with_invalid_min_value_on_set(self):
        with self.assertRaises(ValueError) as ex:
            self.test_audience.age = 17

        self.assertEqual('Field `age` value 17 is smaller than min value 18', str(ex.exception))

    def test_age_field_failed_with_invalid_max_value_on_set(self):
        with self.assertRaises(ValueError) as ex:
            self.test_audience.age = 61

        self.assertEqual(
            'Field `age` value 61 is greater than max value 60',
            str(ex.exception)
        )

    def test_age_field_failed_on_conversion_with_non_numeric_string(self):
        with self.assertRaises(ConversionError) as ex:
            self.test_audience.age = 'abc'

        self.assertEqual(
            "invalid literal for int() with base 10: 'abc'",
            str(ex.exception)
        )

    def test_age_field_is_converted_successfully_with_no_value_error_raised(self):
        self.test_audience.age = '18'
        self.assertTrue(isinstance(self.test_audience.age, int))
        self.assertEqual(18, self.test_audience.age)


class TestStringField(BaseFieldTestCase):
    def test_name_field_failed_with_invalid_min_length_string_on_set(self):
        with self.assertRaises(ValueError) as ex:
            self.test_audience.name = ''
        self.assertEqual(
            'Field `name` value  is shorter than min length 1',
            str(ex.exception)
        )

    def test_name_field_failed_with_invalid_max_length_string_on_set(self):
        with self.assertRaises(ValueError) as ex:
            self.test_audience.name = 'test string'

        self.assertEqual(
            'Field `name` value test string is longer than max length 5',
            str(ex.exception)
        )


class TestEmailField(BaseFieldTestCase):
    def test_email_failed_with_invalid_email_on_set(self):
        invalid_emails = {
            '.invalid1@test.com',
            'invalid2@test.com.',
            '@invalid3@test.com',
            'invalid4test.com',
            'invalid5@test',
        }

        for email in invalid_emails:
            with self.assertRaises(ValueError) as ex:
                self.test_audience.email = email

            self.assertEqual(
                'Field `email` value {} is not a valid pattern'.format(email),
                str(ex.exception)
            )

    def test_email_with_valid_email_on_set(self):
        valid_emails = {
            'test.valid1@test.com',
            'valid2@test.domain.com',
        }

        for email in valid_emails:
            # Ensure no ValueError is raised
            self.test_audience.email = email


class TestURLField(BaseFieldTestCase):

    def test_media_link_with_invalid_url_on_set(self):
        invalid_urls = {
            'http:/test.com:8080',
            'test.com:8000',
            'http://test',
        }

        for url in invalid_urls:
            with self.assertRaises(ValueError) as ex:
                self.test_audience.social_media_link = url

            self.assertEqual(
                'Field `social_media_link` value {} is not a valid pattern'.format(url),
                str(ex.exception)
            )

    def test_media_link_with_valid_url_on_set(self):
        valid_urls = {
            'https://test.com',
            'http://test.com'
        }

        for url in valid_urls:
            # Ensure no ValueError is raised
            self.test_audience.social_media_link = url


class TestDateField(BaseFieldTestCase):
    def test_invalid_date_str(self):
        invalid_date_strings = {
            'a',
            '200-10-2000',
        }
        for date_string in invalid_date_strings:
            with self.assertRaises(ConversionError) as ex:
                self.test_audience.date_of_birth = date_string

            self.assertEqual(str(ex.exception), 'Unknown string format: %s' % date_string)

    def test_valid_date_str_get_converted_to_date_object(self):
        self.test_audience.date_of_birth = '2000-11-07'
        self.assertTrue(isinstance(self.test_audience.date_of_birth, date))


class TestDateTimeField(BaseFieldTestCase):
    def test_invalid_date_str(self):
        invalid_date_strings = {
            'a',
            '200-10-2000',
        }
        for date_string in invalid_date_strings:
            with self.assertRaises(ConversionError) as ex:
                self.test_audience.created_at = date_string

            self.assertEqual(str(ex.exception), 'Unknown string format: %s' % date_string)

    def test_valid_date_str_get_converted_to_datetime_object(self):
        self.test_audience.created_at = '2000-11-07'
        self.assertTrue(isinstance(self.test_audience.created_at, datetime))
