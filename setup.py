"""
i3-focus-group
Copyright (C) 2024  DCsusnet

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from setuptools import setup
from pathlib import Path

version = '0.1.0'

repo_dir = Path(__file__).parent.absolute()

# get version
main_ns = {}
with open(repo_dir.joinpath("i3_focus_group", "_version.py")) as f:
  exec(f.read(), main_ns)

# Long description
with open(repo_dir.joinpath('README.md')) as f:
  long_description = f.read()

setup(
  name='i3-focus-group',
  version=main_ns["__version__"],
  description='Create a group for i3/sway containers to easily switch focus between',
  long_description_content_type='text/markdown',
  long_description=long_description,
  author='DCsunset',
  author_email='DCsunset@protonmail.com',
  license='AGPL-3.0',
  url='https://github.com/DCsunset/i3-focus-group',
  install_requires=['i3ipc>=2.2.1'],
  # Add to lib so that it can be included
  packages=["i3_focus_group"],
  entry_points={
    'console_scripts': [
      'i3-focus-group = i3_focus_group.main:main'
    ]
  },
  classifiers=[
    'Environment :: Console',
    'Intended Audience :: End Users/Desktop',
    'Programming Language :: Python',
    'License :: OSI Approved :: GNU Affero General Public License v3',
    'Topic :: Desktop Environment :: Window Managers',
    'Topic :: Utilities'
  ]
)
