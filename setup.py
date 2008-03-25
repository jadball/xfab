#!/usr/bin/env python
from distutils.core import setup,Extension
import sys


setup(
  name='xfab',
  version='RELEASE',
  description='Crystallographic toolbox and library',
  license='GPL', maintainer='Henning Osholm Soerensen and Jon Wright',
  maintainer_email='henning.sorensen@risoe.dk or wright@esrf.eu',
  url='http://fable.wiki.sourceforge.net',
  packages=['xfab'],
  package_dir={"xfab": "src"}
)
