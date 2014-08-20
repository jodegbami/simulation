# ===========================================================================
# Copyright 2013 University of Limerick
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

@author: Ioannis
'''
'''
Models a machine that processes a (Sub)Batch and can scrap a number of units in each one. Also, the processing time
depends on the number of units of the (Sub)Batch
'''

# from SimPy.Simulation import Process, Resource
# from SimPy.Simulation import activate, passivate, waituntil, now, hold
import simpy
from RandomNumberGenerator import RandomNumberGenerator

from Machine import Machine

# ================================================================
#                  the BatchScrapMachine object
# ================================================================
class BatchScrapMachine(Machine):
    
    # =======================================================================
    # constructor run every time a new instance is created
    # calls the Machine constructor, but also reads attributes for 
    # scraping distribution
    # ======================================================================= 
    def __init__(self, id='', name='', capacity=1, \
                 processingTime=None,
                 failureDistribution='No', MTTF=0, MTTR=0, availability=0, repairman='None',\
                 scrapDistribution='Fixed',scrMean=1,scrStdev=0,scrMin=0,scrMax=10,
                 inputsDict={}):
        # if input is given in a dictionary
        if inputsDict:
            Machine.__init__(self,inputsDict=inputsDict)
        # else read the separate ones
        else:
            if not processingTime:
              processingTime = {'distribution': 'Fixed',
                                'mean': 1}
            # initialize using the default method of the object 
            Machine.__init__(self,id=id,name=name,\
                                        capacity=capacity,\
                                        processingTime=processingTime,
                                        failureDistribution=failureDistribution,MTTF=MTTF,MTTR=MTTR,\
                                        availability=availability,
                                        repairman=repairman)
    
            self.scrapDistType=scrapDistribution    #the distribution that the failure follows   
            # set the attributes of the scrap quantity distribution
            self.scrapRng=RandomNumberGenerator(self, self.scrapDistType)
            self.scrapRng.mean=scrMean
            self.scrapRng.stdev=scrStdev
            self.scrapRng.min=scrMin
            self.scrapRng.max=scrMax

    # =======================================================================
    # parses inputs if they are given in a dictionary
    # =======================================================================       
    def parseInputs(self, inputsDict):
        Machine.parseInputs(self, inputsDict)
        # set the attributes of the scrap quantity distribution
        scrapQuantity=inputsDict.get('scrapQuantity', {})
        self.scrapDistType=scrapQuantity.get('distributionType', 'Fixed')
        self.scrapRng=RandomNumberGenerator(self, self.scrapDistType)
        self.scrapRng.mean=float(scrapQuantity.get('mean') or 0)
        self.scrapRng.stdev=float(scrapQuantity.get('stdev') or 0)
        self.scrapRng.min=float(scrapQuantity.get('min') or 0)
        self.scrapRng.max=float(scrapQuantity.get('max') or self.scrapRng.mean+5*self.scrapRng.stdev)
        from Globals import G
        G.BatchScrapMachineList.append(self)

    # =======================================================================
    # removes an Entity from the Object the Entity to be removed is passed
    # as argument by getEntity of the receiver
    # extends the default behaviour so that
    # it can scrap a number of units before disposing the Batch/SubBatch
    # =======================================================================
    def removeEntity(self, entity=None):
        activeEntity = Machine.removeEntity(self, entity)
        scrapQuantity=self.scrapRng.generateNumber()  
        activeEntity.numberOfUnits-=int(scrapQuantity)  # the scrapQuantity should be integer at whatever case
        if activeEntity.numberOfUnits<0:
            activeEntity.numberOfUnits==0
        return activeEntity


    # =======================================================================
    # calculates the processing time
    # extends the default behaviour so that 
    # the per-unit processing time is multiplied with the number of units
    # =======================================================================                                                                                
    def calculateProcessingTime(self):
        activeEntity = self.getActiveObjectQueue()[0]
        # this is only for processing of the initial wip
        if self.isProcessingInitialWIP:
            if activeEntity.unitsToProcess:
                return self.rng.generateNumber()*activeEntity.unitsToProcess 
        return self.rng.generateNumber()*activeEntity.numberOfUnits        

                
