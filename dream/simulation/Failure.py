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
Created on 9 Nov 2012

@author: George
'''

'''
models the failures that servers can have
'''

# from SimPy.Simulation import now, Process, hold, request, release
import simpy
import math
from RandomNumberGenerator import RandomNumberGenerator
from ObjectInterruption import ObjectInterruption

class Failure(ObjectInterruption):
    
    def __init__(self, victim=None, distribution=None, index=0, repairman=None):
        #Process.__init__(self)
        ObjectInterruption.__init__(self,victim)
        if distribution:
            self.distType=distribution.get('distributionType','No')              # the distribution that the failure duration follows
            self.MTTF=distribution.get('MTTF',60)                  # the MTTF
            self.MTTR=distribution.get('MTTR',5)                  # the MTTR  
            self.availability=distribution.get('availability',100)  # the availability      
        else:
            self.distType='No'
            self.MTTF=60
            self.MTTR=5
            self.availability=100
        self.name="F"+str(index)
        self.repairman=repairman        # the resource that may be needed to fix the failure
                                        # if now resource is needed this will be "None" 
        self.type="Failure"
        self.id=0

        if(self.distType=="Availability"):      
            
            # -------------------------------------------------------------- 
            #     the following are used if we have availability defined 
            #      (as in plant) the erlang is a special case of Gamma. 
            #        To model the Mu and sigma (that is given in plant) 
            #    as alpha and beta for gamma you should do the following:
            #                     beta=(sigma^2)/Mu    
            #                     alpha=Mu/beta
            # --------------------------------------------------------------    
            self.AvailabilityMTTF=self.MTTR*(float(availability)/100)/(1-(float(availability)/100))
            self.sigma=0.707106781185547*self.MTTR   
            self.theta=(pow(self.sigma,2))/float(self.MTTR)             
            self.beta=self.theta
            self.alpha=(float(self.MTTR)/self.theta)        
            self.rngTTF=RandomNumberGenerator(self, "Exp")
            self.rngTTF.avg=self.AvailabilityMTTF
            self.rngTTR=RandomNumberGenerator(self, "Erlang")
            self.rngTTR.alpha=self.alpha
            self.rngTTR.beta=self.beta       
        else:   
            # --------------------------------------------------------------
            #               if the distribution is fixed
            # --------------------------------------------------------------
            self.rngTTF=RandomNumberGenerator(self, self.distType)
            self.rngTTF.mean=self.MTTF
            self.rngTTR=RandomNumberGenerator(self, self.distType)
            self.rngTTR.mean=self.MTTR

    # =======================================================================
    #    The run method for the failure which has to served by a repairman
    # =======================================================================
    def run(self):           
        while 1:
            yield self.env.timeout(self.rngTTF.generateNumber())    # wait until a failure happens                  
            self.interruptVictim()                      # interrupt the victim
            self.victim.Up=False
            self.victim.timeLastFailure=self.env.now           
            self.outputTrace("is down")
            # update the failure time
            failTime=self.env.now            
            if(self.repairman and self.repairman!="None"):     #if the failure needs a resource to be fixed, the machine waits until the 
                                            #resource is available
#                 print self.env.now, self.repairman.id, 'will be requested by', self.victim.id
#                 yield self.repairman.getResource().request()
#                 print self.repairman.Res.users
#                 # update the time that the repair started
#                 timeOperationStarted=self.env.now
#                 self.repairman.timeLastOperationStarted=self.env.now
                
                
                with self.repairman.getResource().request() as request:
                    yield request
                    # update the time that the repair started
                    timeOperationStarted=self.env.now
                    self.repairman.timeLastOperationStarted=self.env.now
                    
                    yield self.env.timeout(self.rngTTR.generateNumber())    # wait until the repairing process is over
                    self.victim.totalFailureTime+=self.env.now-failTime    
                    self.reactivateVictim()                     # since repairing is over, the Machine is reactivated
                    self.victim.Up=True              
                    self.outputTrace("is up")
                    
                    self.repairman.totalWorkingTime+=self.env.now-timeOperationStarted   
                continue
                
                
                                
            yield self.env.timeout(self.rngTTR.generateNumber())    # wait until the repairing process is over
            self.victim.totalFailureTime+=self.env.now-failTime    
            self.reactivateVictim()                     # since repairing is over, the Machine is reactivated
            self.victim.Up=True              
            self.outputTrace("is up")
            
#             if(self.repairman and self.repairman!="None"): #if a resource was used, it is now released
#                 print self.repairman.Res.users
#                 print self.env.now, self.repairman.id, 'about to be release from', self.victim.id
#                 self.repairman.Res.release()
#                 self.repairman.totalWorkingTime+=self.env.now-timeOperationStarted                                
    
#     #===========================================================================
#     # interrupts the victim
#     #===========================================================================
#     def interruptVictim(self):
#         ObjectInterruption.interrupt(self)
#         # TODO: check whether it is a good idea to update the failure timers here