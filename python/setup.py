from __future__ import absolute_import, division, print_function

from distutils.core import setup

from setuptools import find_packages

version = open(
    'src/fancontrol/version.py').read().split('= ')[1].rstrip('\n').strip('"')

setup(name='fancontrol',
      version=version,
      description='An Application-level Fan Control',
      author='Bengt Lüers',
      author_email='bengt.lueers@gmail.com',
      url='https://github.com/Bengt/AL-FanControl',
      packages=find_packages(where="src"),
      package_dir={"": "src"},
      py_modules=['fancontrol'])
