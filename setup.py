# Copyright (c) 2021, Anders Lervik.
# Distributed under the LGPLv2.1+ License. See LICENSE for more info.
"""
gpxplotter - A library for reading gpx files and making some simple plots.
Copyright (C) 2021, Anders Lervik.

This file is part of gpxplotter.

gpxplotter is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 2.1 of the License, or
(at your option) any later version.

gpxplotter is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with gpxplotter. If not, see <http://www.gnu.org/licenses/>
"""
import ast
import pathlib
from setuptools import setup, find_packages


GITHUB = 'https://github.com/andersle/gpxplotter'
DOCS = 'https://gpxplotter.readthedocs.io/en/latest'

FULL_VERSION = '0.2.10'  # Automatically set by setup_version.py


def get_long_description():
    """Return the contents of the README.md file."""
    # Get the long description from the README file
    long_description = ''
    here = pathlib.Path(__file__).absolute().parent
    readme = here.joinpath('pypireadme.md')
    with open(readme, 'r') as fileh:
        long_description = fileh.read()
    return long_description


def get_version():
    """Return the version from version.py as a string."""
    here = pathlib.Path(__file__).absolute().parent
    filename = here.joinpath('gpxplotter', 'version.py')
    with open(filename, 'r') as fileh:
        for lines in fileh:
            if lines.startswith('FULL_VERSION ='):
                version = ast.literal_eval(lines.split('=')[1].strip())
                return version
    return FULL_VERSION


def get_requirements():
    """Read requirements.txt and return a list of requirements."""
    here = pathlib.Path(__file__).absolute().parent
    requirements = []
    filename = here.joinpath('requirements.txt')
    with open(filename, 'r') as fileh:
        for lines in fileh:
            requirements.append(lines.strip())
    return requirements


setup(
    name='gpxplotter',
    version=get_version(),
    description='A package for reading gpx files and creating simple plots',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    url=GITHUB,
    author='Anders Lervik',
    author_email='andersle@gmail.com',
    license='LGPLv2.1+',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        ('License :: OSI Approved :: '
         'GNU Lesser General Public License v2 or later (LGPLv2+)'),
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Other/Nonlisted Topic',
    ],
    keywords='gpx gps',
    packages=find_packages(),
    install_requires=get_requirements(),
)
