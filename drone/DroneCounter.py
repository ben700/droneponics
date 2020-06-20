class DroneCounter:
   
   def __init__(self):
    self.cycle = 0
    self.onCycleReset=0 
    self.offCycleReset=0
    self.onCycle=1
    self.offCycle=0
    self.wasteCycle=0
    self.wasteCycleReset=6  
    self.wasteAutomatic = False
    self.wasteCycleState = "Off"  
    self.feedState = "Off"
    self.automatic = False  
   
   def setManual(self):
         self.automatic = False
   
   def setAutomatic(self):
         self.automatic = True
     
   def isAutomatic(self, _log):
        return self.automatic
   
   def isItWasteCycle(self, _log) :
        if(self.wasteAutomatic is False):
            if(self.wasteCycleState == "Off"):
               return False
            else:
               return True
        else:
            if(self.wasteCycleReset <= self.wasteCycle):
               return True
        return False
            
   def isItAnOnCycle(self, _log) :
        _log.debug("in class counter function isItAnOnCycle self.feedState = " + str(self.feedState))
        if(self.isAutomatic(_log) is not True):
             if (self.feedState is "On"):
                  return True
             elif(self.feedState is "Off"):
                  return False
        else:
             _log.debug("in class counter function isItAnOnCycle automatic")
             _log.debug("self.onCycle = " + str(self.onCycle))
             _log.debug("self.onCycleReset = " + str(self.onCycleReset))
               
             if(self.onCycle < self.onCycleReset):
                return True
             else:
                return False
            
   def isItAnOffCycle(self, _log) :
        _log.debug("in class counter function isItAnOffCycle self.feedState = " + str(self.feedState))
        if(self.isAutomatic(_log) is not True):
            if (self.feedState is "On"):
                 return False
            elif(self.feedState is "Off"):
                 return True
        else:
             if(self.offCycle < self.offCycleReset):
                return True
             else:
                return False
        
   def setOnCycle(self, _log, onCycleValue):
      self.onCycleReset = int(onCycleValue) 
        
   def setOffCycle(self, _log, offCycleValue):
      self.offCycleReset = int(offCycleValue) 
              
   def setWasteCycle(self, _log, wasteCycleValue):
      self.wasteCycleReset = int(wasteCycleValue) 
      
   def info(self):
        return "Feed is on for " + str(self.onCycleReset) + " mins and then off for " + str(self.offCycleReset) + " mins."
   
   def infoCounter(self,_log):
         if (self.feedState is "On"):
             return "Currently in minute " + str(self.cycle) + " pump is set manually ON " 
         elif(self.feedState is  "Off"):
             return "In minute " + str(self.cycle) + "  pump is set manually OFF"
         else:   
            if(self.cycle <= self.onCycle):
                  return "In minute " + str(self.cycle) + " pump is on till minute " + str(self.onCycle)
            else:
                  return "In minute " + str(self.cycle) + " pump is off till minute " + str(self.onCycle+self.offCycle)
               
        
   def  incWasteCycle(self, _log):
        if (self.wasteCycle >= self.wasteCycleReset):
            self.wasteCycle=0
            return self.wasteCycle    
        self.wasteCycle = self.wasteCycle + 1
        return self.wasteCycle
   
   def incOnCycle(self):
      self.onCycle = self.onCycle + 1
      return self.onCycle
   
   def incOffCycle(self):
      self.offCycle = self.offCycle + 1
      return self.offCycle
      
   def  incCycle(self, _log):
        self.cycle = self.cycle + 1
        if (self.cycle >= (self.onCycleReset+ self.offCycleReset) ):
            self.reset(_log)
            return self.cycle
        else:
            return self.cycle
      
   def  reset(self, _log):
        self.cycle = 0
        self.onCycle = 0 
        self.offCycle = 0 
         
        return self.cycle

   
   def  getFeedState(self, _log, blynk):
      if(self.isAutomatic(_log)):
            _log.info("droneCounter.isItAnOnCycle(_log)" + str(self.isItAnOnCycle(_log)))
            if (self.isItAnOnCycle(_log)):
                _log.info("Turn Relay ON") 
                self.incOnCycle()
                blynk.virtual_write(250, "Automatc : On")
                return "On"  
            else :
                _log.info("droneCounter.offCycle = " + str(self.offCycle)) 
                _log.info("Turn off RELAY")
                self.incOffCycle()
                blynk.virtual_write(250, "Automatc : Off")
                return "Off"
      elif(self.feedState is "On"):
                blynk.virtual_write(250, "Manual : On")
                return "On"
      elif(self.feedState is "Off"):
                blynk.virtual_write(250, "Manual : Off")
                return "Off"
      
