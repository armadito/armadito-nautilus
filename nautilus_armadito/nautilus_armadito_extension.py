# Copyright (C) 2016-2017 Teclib'

# This file is part of Armadito Nautilus extension.

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

import os
import urllib
import dbus
from gi.repository import Nautilus, GObject

class ArmaditoExtension(Nautilus.MenuProvider, GObject.GObject):

    def __init__(self):
        self._dbus = dbus.SessionBus()

    def menu_activate_cb(self, menu, file):
        with open("/var/tmp/testnautilus.txt", "a") as f:
            f.write(file.get_name())
            f.write("\n")
#            f.write(file.get_parent_location())
#            f.write("\n")
            f.write(file.get_uri()[7:] + "\n")
            f.write("\n")
        filename = urllib.unquote(file.get_uri()[7:])
        armadito_service = self._dbus.get_object("org.armadito.AntivirusService", "/")
        iface = dbus.Interface(armadito_service, "org.armadito.AntivirusInterface")
        iface.scan(filename)

    def get_file_items(self, window, files):
        if len(files) != 1:
            return
        file = files[0]
        item = Nautilus.MenuItem(name='NautilusPython::scanwitharmadito',
                                 label='Scan with Armadito...',
                                 tip='Scan %s with Armadito...' % file.get_name(),
                                 icon='armadito')
        item.connect('activate', self.menu_activate_cb, file)
        return item,

    def get_background_items(self, window, file):
        item = Nautilus.MenuItem(name='NautilusPython::scanwitharmadito',
                                 label='Scan with Armadito...',
                                 tip='Scan %s with Armadito...' % file.get_name(),
                                 icon='armadito')
        item.connect('activate', self.menu_activate_cb, file)
        return item,
