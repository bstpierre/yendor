#!/usr/bin/python

from setuptools import setup

setup(name='yendor',
      version='0.1.0',
      packages=['yendor'],
      entry_points={
        'gui_scripts': [
            'yendor = yendor.__main__:main'
            ]
        },
      )
