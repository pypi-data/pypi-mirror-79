import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
# README = open(os.path.join(here, 'README.rst')).read()

setup(
    name='django-migration-scripts',
    version='0.1.1',
    packages=['django_migration_scripts'],
    description='Add migration scripts seamlessly',
    # long_description=README,
    author='Harsha Tanguturi',
    author_email='harshatba@gmail.com',
    url='https://github.com/harshatba/django-migration-scripts/',
    license='MIT',
    install_requires=[
        'Django>=1.6',
    ]
)