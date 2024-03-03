from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='pyvalidator',
    version='1.0.0',
    description='Simple type validator in pure Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='',
    author='Huy Vu',
    author_email='vuquanghuy2k@gmail.com',
    keywords='validators, typing',
    classifiers=[
        'Programming Language :: Python :: 3.10'
    ]
)