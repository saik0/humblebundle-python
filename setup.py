#!/usr/bin/env python

__author__ = "Joel Pedraza"
__copyright__ = "Copyright 2014, Joel Pedraza"
__license__ = "MIT"

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='humblebundle',
      version='0.0.4',
      description='Humble Indie Bundle API client',
      author='Joel Pedraza',
      author_email='joel@joelpedraza.com',
      url='https://github.com/saik0/humblebundle-python',
      download_url='https://github.com/saik0/humblebundle-python/tarball/0.0.4',
      install_requires=['requests >= 2.0.0'],
      packages=['humblebundle'],
     )
