#!/usr/bin/env python

# This will try to import setuptools. If not here, it fails with a message
import os
import codecs
import os.path

try:
    from setuptools import setup, find_packages
except ImportError:
    raise ImportError(
        "This module could not be installed, probably because"
        " setuptools is not installed on this computer."
        "\nInstall ez_setup ([sudo] pip install ez_setup) and try again."
    )


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


pre_version = get_version("syspassclient/__init__.py")

if os.environ.get('CI_COMMIT_TAG'):
    version = os.environ['CI_COMMIT_TAG']
else:
    if os.environ.get('CI_JOB_ID'):
        version = os.environ['CI_JOB_ID']
    else:
        version = pre_version

with open('README.md') as f:
    long_description = f.read()

setup(
    name='digdeo-syspass-client',
    version=version,
    description='DigDeo Syspass Client',
    author='DigDeo',
    author_email='jerome.ornech@digdeo.fr',
    include_package_data=True,
    url='https://git.digdeo.fr/digdeo-system/FLOSS/digdeo-syspass-client/',
    license='GNU GENERAL PUBLIC LICENSE Version 3',
    zip_safe=False,
    long_description=long_description,
    long_description_content_type='text/markdown; charset=UTF-8',
    keywords="DigDeo Syspass Client",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Security",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5"
    ],
    setup_requires=[
        'green',
        'wheel'
    ],
    packages=['syspassclient'],
    tests_require=[
        'wheel',
        'colorama',
        'six',
        'PyYAML',
        'requests',
        'urllib3'
    ],
    install_requires=[
        'colorama',
        'six',
        'PyYAML',
        'requests',
        'urllib3'
    ]
)
