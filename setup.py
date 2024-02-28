from setuptools import setup
from os import path

version = '0.1.0'

repo_base_dir = path.abspath(path.dirname(__file__))

# Long description
readme = path.join(repo_base_dir, 'README.md')
with open(readme) as f:
  long_description = f.read()

setup(
  name='i3-focus-group',
  version=version,
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
