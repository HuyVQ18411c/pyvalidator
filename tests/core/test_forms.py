from unittest import TestCase

from pyvalidator.core.exceptions import ValidationError
from pyvalidator.core.forms import Form
from pyvalidator.core.validators import StringField, IntField


class AudienceForm(Form):
    name = StringField(max_length=20)

    def clean_name(self, value: str):
        if not value.startswith('A'):
            raise ValidationError('Invalid name for audience')
        return value


class MatureAudienceForm(AudienceForm):
    age = IntField(min_value=18)


class TestForm(TestCase):
    def setUp(self):
        self.form = MatureAudienceForm({'name': 'Fake Name', 'age': 12})

    def test_all_class_fields_exists(self):
        self.assertIn('name', self.form.declared_fields)
        self.assertIn('age', self.form.declared_fields)

    def test_form_clean_failed_on_set_min_value(self):
        self.assertFalse(self.form.is_valid())
        self.assertIn('age', self.form.errors)
        self.assertEqual(
            str(self.form.errors['age'][0]),
            'Field `age` value 12 is smaller than min value 18'
        )

    def test_form_clean_raise_error_with_no_data_set(self):
        self.form._data = {}

        with self.assertRaises(ValueError) as ex:
            self.form.is_valid()

        self.assertEqual('No data was provided for MatureAudienceForm', str(ex.exception))

    def test_form_custom_clean_name_called_and_not_validation_error(self):
        self.assertFalse(self.form.is_valid())
        self.assertEqual(str(self.form.errors['name'][0]), 'Invalid name for audience')

    def test_form_custom_clean_name_called_and_raise_validation_error(self):
        self.form._raise_exception_on_error = True
        with self.assertRaises(ValidationError) as ex:
            self.form.is_valid()

        self.assertEqual(str(ex.exception), 'Invalid name for audience')
