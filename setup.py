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
import glob
import shutil
import stat
from setuptools import setup, find_packages
from setuptools.command.install import install as _install
from babel.messages import frontend as babel

from nautilus_armadito import VERSION

#NAUTILUS_PYTHON_EXTENSION_PATH = "/usr/share/nautilus-python/extensions"
NAUTILUS_PYTHON_EXTENSION_DIR = "/share/nautilus-python/extensions"

def do_install_file(file, install_dir):
    print("Installing %s in %s..." % (file, install_dir))
    try:
        os.makedirs(install_dir, mode = 0o755, exist_ok = True)
    except OSError:
        print("WARNING: cannot create directory %s" % install_dir)
        return
    try:
        shutil.copy(file, install_dir)
    except IOError:
        print("WARNING: cannot copy file %s" % (file,))
    mode = stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH
    try:
        base_file = os.path.basename(file)
        os.chmod(install_dir + '/' + base_file, mode)
    except IOError:
        print("WARNING: cannot chmod %s" % (base_file,))

class install(_install):
    def get_langs(self):
        return [os.path.basename(os.path.dirname(x)) for x in glob.iglob('po/*/LC_MESSAGES')]

    def run(self):
        _install.run(self)
        do_install_file('./nautilus_armadito/nautilus_armadito_extension.py', self.prefix + NAUTILUS_PYTHON_EXTENSION_DIR)
        self.run_command('compile_catalog')
        for lang in self.get_langs():
            do_install_file('po/%s/LC_MESSAGES/nautilus-armadito.mo' % (lang,), self.prefix + '/share/locale/%s/LC_MESSAGES' % (lang,))

#class install(_install):
#    def run(self):
#        _install.run(self)
#        install_dir = self.prefix + NAUTILUS_PYTHON_EXTENSION_DIR
#        print("Installing Nautilus Python extension in %s..." % (install_dir,))
#        if not os.path.isdir(install_dir):
#            try:
#                os.makedirs(install_dir, mode = 0o755, exist_ok = True)
#            except OSError:
#                print("WARNING: Nautilus Python extension have not been installed (%s cannot be created)" % install_dir)
#                return
#        try:
#            shutil.copy("./nautilus_armadito/nautilus_armadito_extension.py", install_dir)
#        except IOError:
#            print("WARNING: Nautilus Python extension have not been installed (permission denied)")
#            return
#        print("Done!")


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
#    packages = ['nautilus_armadito'],
    cmdclass = {"install": install}
#    data_files = [('share/icons/hicolor/scalable/apps', ['icons/scalable/indicator-armadito-dark.svg', 'icons/scalable/indicator-armadito.svg'])]
)

