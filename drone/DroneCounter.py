class DroneCounter:
   
   def __init__(self):
    self.cycle = 0
    self.onCycle=0 
    self.offCycle=0
    self.overwrite = False
   
   def manual(self, _log, value):
         overwrite = value
         
   def isAutomatic(self, _log):
      _log.debug("in class DroneCounter function isAutomatic and manual mode is set to " + str(self.overwrite))
      if (self.overwrite is False):
           _log.debug("in class DroneCounter function isAutomatic and manual mode is set to " + str(self.overwrite) + " returning true")
           return True
      else:
           _log.debug("in class DroneCounter function isAutomatic and manual mode is set to " + str(self.overwrite) + " returning false")
           return False
          
   def isItAnOnCycle(self, _log) :
        _log.debug("in class counter function isItAnOnCycle self.overwrite = " + str(self.overwrite))
        if (self.overwrite is "On"):
             return True
        elif(self.overwrite is "Off"):
             return False
        else:
            _log.debug("not in manual mode")
            now = self.cycle - self.onCycle
            if (now < 0):
                _log.debug("returning true form isItAnOnCycle")
                return True
            else:
                _log.debug("returning false form isItAnOnCycle")
                return False

   def isItAnOffCycle(self, _log) :
        _log.debug("in class counter function isItAnOffCycle states are")
        _log.debug("in class counter function isItAnOffCycle this.cycle = " + str(self.cycle))
        _log.debug("in class counter function isItAnOffCycle this.onCycle = " + str(self.onCycle))
        _log.debug("in class counter function isItAnOffCycle this.offCycle = " + str(self.offCycle))
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
      _log.debug("current this.cycle = " + str(self.cycle))
      _log.debug("current this.onCycle = " + str(self.onCycle))
      _log.debug("going to set onCycleValue to " + str(onCycleValue))
      self.onCycle = int(onCycleValue) 
        
   def setOffCycle(self, _log, offCycleValue):
      _log.debug("current this.cycle = " + str(self.cycle))
      _log.debug("current this.onCycle = " + str(self.onCycle))
      _log.debug("going to set offCycleValue to " + str(offCycleValue))
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
        self.cycle = self.cycle + 1
        _log.debug("Cycle now " + str(self.cycle))
        return self.cycle
             
   def  reset(self, _log):
        _log.debug("in class counter function reset")
        _log.debug("Cycle was " + str(self.cycle))
        self.cycle = 0
        _log.debug("Cycle now " + str(self.cycle))
        return self.cycle
