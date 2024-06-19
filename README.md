# PyValidator - Simple Field Validator Using Python
This is an unfinished package, further updates may change its functionalities.
## The idea
Using [Descriptor](https://docs.python.org/3/howto/descriptor.html) we can understand not only one of the most essential concept of Python but also many validation libraries.
Within this repo, I try to avoid external libraries as much as I can. Currently, the only library I'm using is [dateutil](https://github.com/dateutil/dateutil), for datetime conversion. 

Using 3 methods (`__set_name__`, `__get__`, `__set__`) of a `Descriptor` we can perform many actions on value of a field/object including validation, please read the article I mentioned above for more details.
## Installation
```
pip install git+ssh://git@github.com:HuyVQ18411c/pyvalidator.git
```

## Usage
The targets of this package are pure Python model and with `Form`, which is also provided within this package. 
### Field
Example with `Field` class:
```
from pyvalidator.core.validators import IntField

class Person:
    age = IntField(min_value=18)
    
    def __init__(self, age):
        self.age = age

p = Person(2) # raise ValueError since min_value was set to 18 for `age` field
p = Person(19) # No complaint!
```
#### Type conversion
Since we are using descriptor, hence an exception is raised on assignment. As soon as you assign a value to the field, it will raise error any.

If you are uncertain about the data type you can either set `force_conversion=True` or set your own conversion function using `custom_conversion` on initialization or through `set_custom_conversion`.

As the result, the value will be converted to target type. For example, if you pass a numeric `str` to `IntField` it will be transformed to an `int` the next time you retrieve it.  
#### Custom field
User defined Field is possible, simply by inheriting `Field`, `NumericField`, `StringField` class from `pyvalidator.core.validators`.

If you decided to use `Field` class, you must implement the following methods in order to make a field work properly:

- `_built_in_validation`: any validations for that field such as: min value, max value, min_length, etc. 

### Form
Example with `Form` class:
```
from pyvalidator.core.forms import Form
from pyvalidator.core.exceptions import ValidationError

class AudienceForm(Form):
    name = StringField(max_length=20)
    age = IntField(min_value=18)
    last_login = DateTimeField(nullable=True, force_conversion=True)

    def clean_name(self, value: str):
        if not value.startswith('A'):
            raise ValidationError('Invalid name for audience')
        return value

    def clean(self):
        print(self.last_login, self.age)
        if (datetime.now().year - self.last_login.year) > self.age:
            raise ValidationError('Invalid last login year')

```
If you have used Django or Django REST Framework before, this piece of code will be fairly familiar.
#### Form clean cycle:
Form is designed to work in the following order, when `is_valid` is called:
- Data is set to matched field
- Trigger field validation
- Run user-defined clean_<field>
- Set value (again) to field
- Trigger field validation
- Run user-defined clean for form

#### User-defined clean
- Field level: if you want to have an additional clean for specific field, you can define a method called `clean_<field_name>`. For example if you have a field name `age` then the custom clean function for it should be named `clean_age`.
- Form level: if you want to have an additional clean for the whole form, using multiple fields by retrieving from `form.cleaned_data`, you can declare a method call `clean`. 

See more in the example above.
## Author & contributor:
Vũ Quang Huy (Huy Vũ)
- **Email**: vuquanghuy2k@gmail.com
- [Github](https://github.com/HuyVQ18411c)
- [LinkedIn](https://www.linkedin.com/in/huy-vu-dev/)

