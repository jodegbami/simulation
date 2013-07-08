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
Created on 6 Feb 2013

@author: George
'''

'''
models a part entity that flows through the system
'''


from SimPy.Simulation import *
from Globals import G


#The entity object
class Part(object):    
    type="Part"
          
    def __init__(self, name):
        self.name=name
        self.currentStop=None      #contains the current object that the material is in 
        self.creationTime=0
        self.startTime=0           #holds the startTime for the lifespan
        #dimension data
        self.width=1.0
        self.height=1.0
        self.length=1.0
        
    def __del__(self):
        pass      
        #print self.name, now()
