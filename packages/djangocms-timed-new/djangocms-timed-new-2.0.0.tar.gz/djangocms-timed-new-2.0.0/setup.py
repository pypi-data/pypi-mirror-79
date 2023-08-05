#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from djangocms_timed import __version__

REQUIREMENTS = [
    'django>=2.2,<3.1',
    'django-cms>=3.7',
]

CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
]

setup(
    name='djangocms-timed-new',
    version=__version__,
    description='Timed addon for django CMS',
    long_description=open('README.rst').read(),
    author='arjan5',
    author_email='arjan@anymore.nl',
    url='https://github.com/arjan-s/djangocms-timed',
    packages=find_packages(),
    license='BSD License',
    platforms=['OS Independent'],
    install_requires=REQUIREMENTS,
    classifiers=CLASSIFIERS,
    include_package_data=True,
    zip_safe=False,
    test_suite='tests.settings.run',
)
