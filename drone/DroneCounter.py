class DroneCounter:
   
   def __init__(self):
    self.cycle = 0
    self.onCycle=0 
    self.offCycle=0
    self.overwrite = False
   
   def manual(self, _log, value):
         overwrite = value
         
   def isAutomatic(self, _log):
      if (self.overwrite is False):
           return True
      else:
           return False
          
   def isItAnOnCycle(self, _log) :
        _log.debug("in class counter function isItAnOnCycle self.overwrite = " + str(self.overwrite))
        if (self.overwrite is "On"):
             return True
        elif(self.overwrite is "Off"):
             return False
        else:
            now = self.cycle - self.onCycle
            if (now < 0):
                return True
            else:
                now = self.cycle - self.onCycle - self.offCycle
                if (now < 0):
                    return False
                else:
                    return True

   def isItAnOffCycle(self, _log) :
        if (self.overwrite is "On"):
             return False
        elif(self.overwrite is "Off"):
             return True
        else:
            now = self.cycle - self.onCycle - self.offCycle
            if (now < 0):
                return True
            else:
                return False
        
   def setOnCycle(self, _log, onCycleValue):
      self.onCycle = int(onCycleValue) 
        
   def setOffCycle(self, _log, offCycleValue):
      self.offCycle = int(offCycleValue) 
      
   def info(self):
        return "Feed is on for " + str(self.onCycle) + " mins and then off for " + str(self.offCycle) + " mins."
   
   def infoCounter(self,_log):
         if (self.overwrite is "On"):
             return "Currently in minute " + str(self.cycle) + " pump is set manually ON " 
         elif(self.overwrite is  "Off"):
             return "In minute " + str(self.cycle) + "  pump is set manually OFF"
         else:   
             _log.debug("self.cycle = " + str(self.cycle))
             if(self.cycle <= self.onCycle):
                  return "In minute " + str(self.cycle) + " pump is on till minute " + str(self.onCycle)
             else:
                  return "In minute " + str(self.cycle) + " pump is off till minute " + str(self.onCycle+self.offCycle)
               
        
   def  incCycle(self, _log):
        _log.debug("in class counter function incCycle this.cycle = " + str(self.cycle))
        if (self.cycle >= (self.onCycle + self.offCycle)):
            _log.debug("reset counter from incCycle")
            self.reset(_log)
            return self.cycle    
        self.cycle = self.cycle + 1
        _log.debug("Cycle now " + str(self.cycle))
        return self.cycle
             
   def  reset(self, _log):
        _log.debug("in class counter function reset")
        _log.debug("Cycle was " + str(self.cycle))
        self.cycle = 0
        _log.debug("Cycle now " + str(self.cycle))
        return self.cycle
