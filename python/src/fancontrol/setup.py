from distutils.core import setup

setup(name='fancontrol',
      version='1.0',
      description='An Application-level Fan Control',
      author='Bengt Lüers',
      author_email='bengt.lueers@gmail.com',
      url='https://github.com/Bengt/AL-FanControl',
      packages=find_packages(where="src"),
      package_dir={"": "src"},
      py_modules=['foo'],
      )
