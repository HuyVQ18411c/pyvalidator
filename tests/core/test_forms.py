from unittest import TestCase

from pyvalidator.core.forms import Form
from pyvalidator.core.validators import StringField


class AudienceForm(Form):
    name = StringField()


class TestForm(TestCase):
    def setUp(self):
        self.form = AudienceForm()

    def test_all_class_fields_exists(self):
        self.assertIn('name', self.form.declared_fields)
