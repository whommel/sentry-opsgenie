#!/usr/bin/env python
from setuptools import setup, find_packages

install_requires = [
    'sentry>=5.3.3'
]

f = open('README.rst')
readme = f.read()
f.close()

setup(
    name='sentry-opsgenie',
    version='0.0.1',
    author='William Hommel',
    author_email='whommel@gmail.com',
    url='https://github.com/whommel/sentry-opsgenie',
    description='A Sentry plugin for sending error occurrences to a OpsGenie instance.',
    long_description=readme,
    packages=find_packages(),
    install_requires=install_requires,
    entry_points={
        'sentry.plugins': [
            'sentry_opsgenie = sentry_opsgenie.plugin:OpsGeniePlugin'
        ],
    },
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
        'Topic :: Software Development'
    ],
    keywords='sentry opsgenie',
)
