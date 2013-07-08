# ===========================================================================
# Copyright 2013 Georgios Dagkakis
#
# This file is part of DREAM.
#
# DREAM is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# DREAM is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with DREAM.  If not, see <http://www.gnu.org/licenses/>.
# ===========================================================================
'''
Created on 8 Nov 2012

@author: George
'''

'''
script for making the project into a standalone .exe file
this fails since I used sciPy
'''

from distutils.core import setup
import py2exe

setup(
          options = {
            "py2exe":{
            #"dll_excludes": [ "HID.DLL", "libmmd.dll","w9xpopen.exe"],        
            #"MSVCP90.dll","libifcoremd.dll",
        }
    },
      
      
      console=['Line01.py'])
