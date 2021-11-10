#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os
import shutil
import subprocess
import re
import atexit

from setuptools import find_packages
from setuptools import setup

## https://stackoverflow.com/a/48015772
## override the build command class to pre-install diamond/minimap2
from distutils.command.build import build as _build
from setuptools.command.install import install as _install

class install(_install):
    def run(self):
        super().run()

class build(_build):

    def run(self):
        self._pre_install()
        super().run()

    def _pre_install(self):
        _path = os.path.dirname(os.path.realpath(__file__))
        _bin = os.path.join(_path, 'pysarg', 'bin')
        _database = os.path.join(_path, 'pysarg', 'database')
        if not os.path.exists(_bin):
            os.makedirs(_bin) 

        ## install diamond
        _diamond = os.path.join(_path, 'diamond')
        _diamond_bin = os.path.join(_diamond, 'bin')
        _diamond_bin_diamond = os.path.join(_diamond_bin, 'diamond')

        if not os.path.exists(_diamond):
            subprocess.call(['git', 'clone', 'https://github.com/bbuchfink/diamond', '-b', 'v0.8.16', _diamond], cwd=_path)
        
        if not os.path.exists(_diamond_bin):
            subprocess.call(['mkdir', 'bin'], cwd=_diamond)
            subprocess.call(['cmake', '..'], cwd=_diamond_bin)
            subprocess.call(['make', '-j4'], cwd=_diamond_bin)
            subprocess.call(['make','install'], cwd=_diamond_bin)

        _bin_diamond = os.path.join(_bin, 'diamond')
        shutil.copy(_diamond_bin_diamond, _bin_diamond)
        shutil.rmtree(_diamond, ignore_errors=True)

        ## install diamond 2 (remove later)
        _diamond = os.path.join(_path, 'diamond')
        _diamond_bin = os.path.join(_diamond, 'bin')
        _diamond_bin_diamond = os.path.join(_diamond_bin, 'diamond')

        if not os.path.exists(_diamond):
            subprocess.call(['git', 'clone', 'https://github.com/bbuchfink/diamond', '-b', 'v0.9.24', _diamond], cwd=_path)
        
        if not os.path.exists(_diamond_bin):
            subprocess.call(['mkdir', 'bin'], cwd=_diamond)
            subprocess.call(['cmake', '..'], cwd=_diamond_bin)
            subprocess.call(['make', '-j4'], cwd=_diamond_bin)
            subprocess.call(['make','install'], cwd=_diamond_bin)

        _bin_diamond2 = os.path.join(_bin, 'diamond2')
        shutil.copy(_diamond_bin_diamond, _bin_diamond2)
        shutil.rmtree(_diamond, ignore_errors=True)

        ## build database
        _sarg = 'SARG.2.2.fasta'
        subprocess.call([_bin_diamond2, 'makedb', '--in', _sarg, '-d', 'SARG'], cwd=_database)

        # install minimap2
        _minimap2 = os.path.join(_path, 'minimap2')
        _minimap2_minimap2 = os.path.join(_minimap2, 'minimap2')

        if not os.path.exists(_minimap2):
            subprocess.call(['git', 'clone', 'https://github.com/lh3/minimap2', '-b', 'v2.17', _minimap2], cwd=_path)

        subprocess.call(['make'], cwd=_minimap2)

        _bin_minimap2 = os.path.join(_bin, 'minimap2')
        shutil.copy(_minimap2_minimap2, _bin_minimap2)
        shutil.rmtree(_minimap2, ignore_errors=True)

        ## build database
        _gg85 = 'gg85.fasta'
        subprocess.call([_bin_minimap2, '-d', 'gg85.mmi', _gg85], cwd=_database)
        

with open('requirements.txt') as f:
    requirements = list(f.readlines())

setup(
    name='pysarg',
    version='0.0.5',
    license='MIT',
    description='test version',
    author='',
    author_email='',
    url='',
    packages=find_packages(),
    zip_safe=False,
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3'],
    keywords=[
        # eg: 'keyword1', 'keyword2', 'keyword3',
    ],
    package_data={
      'pysarg': ['bin/*','database/*'],
    },
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'pysarg = pysarg.pysarg:main',
        ]
    },
    cmdclass={
    'build': build,
    'install':install
    }
)
