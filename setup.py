# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='Witches garden',
    version='0.0.1',
    description='game about planting plants',
    long_description=readme,
    author='Rūdolfs Ceimers',
    author_email='me@kennethreitz.com',
    url='https://github.com/ceimerrudis/witches_garden.git',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

