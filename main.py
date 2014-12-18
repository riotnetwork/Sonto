#!/usr/bin/env python

__author__ = "Jarryd Bekker"
__copyright__ = "Copyright 2014, Bushveld Labs"
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Jarryd Bekker"
__email__ = "jarryd@bushveldlabs.com"
__status__ = "development"


# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
    
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
   
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from C1098 import Camera

if __name__ == "__main__":

    myCamera = Camera(port='/dev/ttyS4',baudrate=115200)
    myCamera.Capture(filename="image")