#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import, print_function

import io
import re
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import find_packages
from setuptools import setup


def read(*names, **kwargs):
    return io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()


def remove_rst_roles(text):
    return re.sub(r':[a-z]+:`~?(.*?)`', r'``\1``', text)


def expand_includes(text, path='.'):
    """Recursively expands includes in given text."""
    def read_and_expand(match):
        filename = match.group('filename')
        filename = join(path, filename)
        text = read(filename)
        return expand_includes(
            text, path=join(path, dirname(filename)))

    return re.sub(ur'^\.\. include:: (?P<filename>.*)$',
                  read_and_expand,
                  text,
                  flags=re.MULTILINE)


setup(
    name='pip2amch',
    version='0.1.0',
    license='BSD',
    description="Command to transform pip's requirements.txt into a csv for batch upload to https://allmychanges.com",
    long_description=remove_rst_roles(expand_includes(read('README.rst'))),
    author='Alexander Artemenko',
    author_email='svetlyak.40wt@gmail.com',
    url='https://github.com/allmychanges/pip2amch',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Environment :: Console',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Utilities',
    ],
    keywords=[
        'allmychanges',
        'release notes',
        'amch',
        'changelog',
        'pip',
        'requirements',
    ],
    install_requires=[
        'click>=6.6,<6.7',
        'requirements-parser>=0.1,<0.2',
        'tablib>=0.11,<0.12',
    ],
    entry_points={
        'console_scripts': [
            'pip2amch = pip2amch.__main__:main'
        ]
    },
)
