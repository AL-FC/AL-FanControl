from __future__ import absolute_import, division, print_function

from distutils.core import setup

from setuptools import find_packages

setup(name='fancontrol',
      version='0.1.0',
      description='An Application-level Fan Control',
      author='Bengt Lüers',
      author_email='bengt.lueers@gmail.com',
      url='https://github.com/Bengt/AL-FanControl',
      packages=find_packages(where="src"),
      package_dir={"": "src"},
      py_modules=['foo'],
      modules=['fancontrol'])
