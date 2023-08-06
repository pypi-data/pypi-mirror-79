import sys
from setuptools import setup
from bootstrap3_datetime import __version__

setup(
    name='django2-bootstrap3-datetimepicker',
    packages=['bootstrap3_datetime'],
    package_data={
        'bootstrap3_datetime': ['static/bootstrap3_datetime/css/*.css',
                                'static/bootstrap3_datetime/js/*.js',
                                'static/bootstrap3_datetime/js/locales/*.js', ]},
    version=__version__,
    description='Bootstrap3 compatible datetimepicker for Django 2.x projects.',
    long_description=open('README.rst').read(),
    author='Nakahara Kunihiko/Samuel Colvin/Eric Lapouyade',
    author_email='elapouya@gmail.com',
    url='https://github.com/elapouya/django-bootstrap3-datetimepicker',
    license='Apache License 2.0',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
        'Environment :: Web Environment',
        'Framework :: Django',
    ],
)
