import sys
from os import path

from setuptools import setup, find_packages

from notetool.tool import get_version

version_path = path.join(path.abspath(path.dirname(__file__)), 'script/__version__.md')

version = get_version(sys.argv, version_path, step=32)

install_requires = []

setup(name='notestock',
      version=version,
      description='notestock',
      author='euler',
      author_email='1007530194@qq.com',
      url='https://github.com/1007530194',

      packages=find_packages(),
      install_requires=install_requires
      )
