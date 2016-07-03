import codecs

from os import path
from setuptools import find_packages, setup


def read(*parts):
    filename = path.join(path.dirname(__file__), *parts)
    with codecs.open(filename, encoding="utf-8") as fp:
        return fp.read()


setup(
    author="",
    author_email="",
    description="An app for Django sites that supports open, by invitation, and by application teams",
    name="pinax-teams",
    long_description=read("README.rst"),
    version="0.12",
    url="http://pinax-teams.rtfd.org/",
    license="MIT",
    packages=find_packages(),
    tests_require=[
        "Django>=1.7",
        "django-reversion>=1.8.1",
        "pinax-invitations>=4.0.4",
        "unicode-slugify>=0.1.1",
        "Pillow>=2.3.0",
        "django-user-accounts>=1.3",
        "six>=1.9.0"
    ],
    install_requires=[
        "Django>=1.7",
        "django-reversion>=1.8.1",
        "pinax-invitations>=4.0.4",
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
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    zip_safe=False
)
