from setuptools import setup

with open('README.md') as file:
    long_description = file.read()

setup(
    name='destructipy',
    version='0.0.5',
    author='Amit Marcus',
    author_email='marxus@gmail.com',
    description='es6 style dict/object destructure for python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/marxus/destructipy',
    packages=['destructipy']
)
