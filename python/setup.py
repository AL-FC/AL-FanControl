from distutils.core import setup

from setuptools import find_packages

setup(name='fancontrol',
      version='0.1.0',
      modules=['fancontrol'],
      packages=find_packages(where="src"),
      package_dir={"": "src"},
      )
