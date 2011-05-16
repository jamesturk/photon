#!/usr/bin/env python

from distutils.core import setup
from photon import __version__

setup(name='photon',
      version=__version__,
      description="experimental python graphics library",
      author="James Turk",
      author_email="james.p.turk@gmail.com",
      url="http://github.com/jamesturk/photon/",
      packages=["photon", "photon.tests"],
     )

