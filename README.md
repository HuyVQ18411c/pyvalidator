# PyValidator - Simple Field Validators Using Python
This project is developed solely for learning purpose using only pure Python (CPython - tested on version 3.12)

## Installation
```
pip install git+ssh://git@github.com:HuyVQ18411c/pyvalidator.git
```
## The idea
Using [Descriptor](https://docs.python.org/3/howto/descriptor.html) we can understand not only one of the most essential concept of Python but also many validation libraries.
Within this repo, I try to avoid external libraries as much as I can. 

Using 3 methods (`__set_name__`, `__get__`, `__set__`) of a `Descriptor` we can perform many actions on value of a field/object including validation, please read the article I mentioned above for more details.
## Usage
```
from pyvalidator.core.validators import IntField

class Person:
    age = IntField(min_value=18)
    
    def __init__(self, age):
        self.age = age

p = Person(2) # raise ValueError since min_value was set to 18 for `age` field
p = Person(19) # No complaint!
```