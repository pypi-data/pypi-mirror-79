"""
Copyright (C) 2016, 2017, 2020 biqqles.

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""
from setuptools import setup, find_namespace_packages
import subprocess

# freshly compile resources
subprocess.call(['pyrcc5', 'src/resources.qrc', '-o', 'src/wingman/resources.py'])


setup(
    name='wingman',  # distribution name
    version='0.1.0',

    author='biqqles',
    author_email='biqqles@protonmail.com',
    url='https://github.com/biqqles/wingman',

    description='A companion for Discovery Freelancer',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',

    packages=find_namespace_packages('src'),
    package_dir={'': 'src'},

    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Topic :: Games/Entertainment',
        'Intended Audience :: End Users/Desktop',
        'Development Status :: 3 - Alpha'
    ],

    python_requires='>=3.7',
    install_requires=[
        'dataclassy',
        'fl-flint>=0.3',
        'fl-flair; platform_system=="Windows"',
        'ago',
        'Pillow',
        'PyQt5',
    ],

    entry_points={
          'gui_scripts': [
              'wingman = wingman.main:main'
          ]
    },
    data_files=[
        ('share/applications', ['packaging/linux/eu.biqqles.wingman.desktop']),
        ('share/icons/hicolor/256x256/apps', ['icons/general/wingman.png']),
    ],
)
