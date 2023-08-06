from setuptools import setup, find_packages
import sys
import os

version = '0.5.0'

long_description = open("README.rst").read()

setup(name='pygamess',
      version=version,
      description="GAMESS wrapper for Python",
      long_description=long_description,
      long_description_content_type='text/x-rst',
      classifiers=[
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering :: Chemistry',
        'Development Status :: 2 - Pre-Alpha',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Programming Language :: Python'
        ], 
      keywords='chemistry',
      author='Ohkawa Kazufumi',
      author_email='kerolinq@gmail.com',
      url='https://github.com/kzfm/pygamess',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests', 'docs']),
      include_package_data=True,
      zip_safe=False,
      requires=['rdkit', 'ruamel.YAML']
      )
