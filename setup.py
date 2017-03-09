#!/usr/bin/env python
# encoding: UTF-8

# Copyright (C) 2016-2017 Teclib'

# This file is part of Armadito indicator.

# Armadito indicator is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Armadito indicator is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Armadito indicator.  If not, see <http://www.gnu.org/licenses/>.

#
# this setup.py taken from https://github.com/flozz/nautilus-terminal
# Thank you!
# 
# to combine autotools and setuptools, see:
# https://blog.kevin-brown.com/programming/2014/09/24/combining-autotools-and-setuptools.html
# Thank you!

import os
import shutil
from setuptools import setup, find_packages
from setuptools.command.install import install as _install

from nautilus_armadito import VERSION

NAUTILUS_PYTHON_EXTENSION_PATH = "/usr/share/nautilus-python/extensions"

class install(_install):
    def run(self):
        _install.run(self)
        print("Installing Nautilus Python extension...")
        if not os.path.isdir(NAUTILUS_PYTHON_EXTENSION_PATH):
            try:
                os.mkdir(NAUTILUS_PYTHON_EXTENSION_PATH)
            except OSError:
                print("WARNING: Nautilus Python extension have not been installed (%s cannot be created)" % NAUTILUS_PYTHON_EXTENSION_PATH)
                return
        try:
            shutil.copy("./nautilus_armadito/nautilus_armadito_extension.py", NAUTILUS_PYTHON_EXTENSION_PATH)
        except IOError:
            print("WARNING: Nautilus Python extension have not been installed (permission denied)")
            return
        print("Done!")


def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()

setup(
    name = "Armadito antivirus Nautilus extension",
    version = VERSION,
    author = "François Déchelle",
    author_email = "fdechelle@teclib.com",
    description = "Nautilus extension for Armadito antivirus",
    license = "GPLv3",
    keywords = "antivirus nautilus",
    url = "https://github.com/armadito/armadito-nautilus",
    long_description = read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: GPLv3 License",
    ],
    packages = ['nautilus_armadito'],
    cmdclass = {"install": install}
#    data_files = [('share/icons/hicolor/scalable/apps', ['icons/scalable/indicator-armadito-dark.svg', 'icons/scalable/indicator-armadito.svg'])]
)

