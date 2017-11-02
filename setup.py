from setuptools import find_packages, setup


LONG_DESCRIPTION = """.. image:: http://pinaxproject.com/pinax-design/patches/pinax-teams.svg
   :target: https://github.com/pinax/pinax-teams/

Pinax Teams
========================

.. image:: https://img.shields.io/pypi/v/pinax-teams.svg
   :target: https://pypi.python.org/pypi/pinax-teams/

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://pypi.python.org/pypi/pinax-teams/



.. image:: https://img.shields.io/codecov/c/github/pinax/pinax-teams.svg
   :target: https://codecov.io/gh/pinax/pinax-teams

.. image:: https://circleci.com/gh/pinax/pinax-teams.svg?style=svg
   :target: https://circleci.com/gh/pinax/pinax-teams

.. image:: https://img.shields.io/github/contributors/pinax/pinax-teams.svg
   :target: https://github.com/pinax/pinax-teams/

.. image:: https://img.shields.io/github/issues-pr/pinax/pinax-teams.svg
   :target: https://github.com/pinax/pinax-teams/

.. image:: https://img.shields.io/github/issues-pr-closed/pinax/pinax-teams.svg
   :target: https://github.com/pinax/pinax-teams/


.. image:: http://slack.pinaxproject.com/badge.svg
   :target: http://slack.pinaxproject.com/



``pinax-teams`` is an app for Django sites that supports open, by invitation, and by application teams.



Pinax
-----

Pinax is an open-source platform built on the Django Web Framework. It is an ecosystem of reusable Django apps, themes, and starter project templates.
This collection can be found at http://pinaxproject.com.

This app was developed as part of the Pinax ecosystem but is just a Django app and can be used independently of other Pinax apps.

"""


setup(
    author="Pinax Developers",
    author_email="developers@pinaxproject.com",
    description="An app for Django sites that supports open, by invitation, and by application teams",
    name="pinax-teams",
    long_description=LONG_DESCRIPTION,
    version="0.14.0",
    url="http://pinax-teams.rtfd.org/",
    license="MIT",
    packages=find_packages(),
    tests_require=[
        "Django>=1.8",
        "django-reversion>=1.8.1",
        "pinax-invitations>=5.0.0",  # 5.0.0 changes label from invitations to pinax_invitations
        "unicode-slugify>=0.1.1",
        "Pillow>=2.3.0",
        "django-user-accounts>=1.3",
        "six>=1.9.0"
    ],
    install_requires=[
        "Django>=1.8",
        "django-reversion>=1.8.1",
        "pinax-invitations>=5.0.0",
        "unicode-slugify>=0.1.1",
        "Pillow>=2.3.0",
        "django-user-accounts>=1.3",
        "six>=1.9.0"
    ],
    test_suite="runtests.runtests",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Framework :: Django :: 1.10",
        "Framework :: Django :: 1.11",
        "Framework :: Django :: 1.8",
        "Framework :: Django :: 2.0",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    zip_safe=False
)
