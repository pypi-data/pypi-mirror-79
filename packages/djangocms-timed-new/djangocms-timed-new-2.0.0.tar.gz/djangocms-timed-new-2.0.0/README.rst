================
django CMS Timed
================


|pypi|

**django CMS Timed** is plugins for `django CMS <http://django-cms.org>`_
that allow you to display plugins content within a defined period of time.

This addon is compatible with `Aldryn <http://aldryn.com>`_ and is also available on the
`django CMS Marketplace <https://marketplace.django-cms.org/en/addons/browse/djangocms-timed/>`_
for easy installation.


Note
====

This is a re-release of the original plugin by Aldryn, of which the development has ceased years ago.



Contributing
============

This is a an open-source project. We'll be delighted to receive your
feedback in the form of issues and pull requests. Before submitting your
pull request, please review our `contribution guidelines
<http://docs.django-cms.org/en/latest/contributing/index.html>`_.


Documentation
=============


See ``REQUIREMENTS`` in the `setup.py <https://github.com/arjan-s/djangocms-timed/blob/master/setup.py>`_
file for additional dependencies:

* Python 3.5 or higher
* Django 2.2 or 3.0


Installation
------------

For a manual install:

* run ``pip install djangocms-timed-new``
* add ``djangocms_timed`` to your ``INSTALLED_APPS``
* run ``python manage.py migrate djangocms_timed``


Configuration
-------------

Note that the provided templates are very minimal by design. You are encouraged
to adapt and override them to your project's requirements.


Running Tests
-------------

You can run tests by executing::

    tox


.. |pypi| image:: https://badge.fury.io/py/djangocms-timed-new.svg
    :target: http://badge.fury.io/py/djangocms-timed-new
