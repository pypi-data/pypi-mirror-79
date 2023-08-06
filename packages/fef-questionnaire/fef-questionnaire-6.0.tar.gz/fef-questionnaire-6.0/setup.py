import os
import sys
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="fef-questionnaire",
    version="6.0",
    description="A Django application for creating online questionnaires/surveys.",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="Eldest Daughter, LLC., Free Ebook Foundation",
    author_email="gcaprio@eldestdaughter.com, eric@hellman.net",
    license="BSD",
    url="https://github.com/EbookFoundation/fef-questionnaire",
    packages=find_packages(exclude=["example"]),
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        "Framework :: Django",
    ],
    zip_safe=False,
    install_requires=[
        'django>=2',
        'django-transmeta-eh',
        'django-compat',
        'pyyaml',
        'pyparsing',
        'six'
    ],
    setup_requires=[
        'versiontools >= 1.6',
    ],
)

