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
        _log.debug("in class counter function isItAnOnCycle states are")
        _log.debug("in class counter function isItAnOnCycle this.cycle = " + str(self.cycle))
        _log.debug("in class counter function isItAnOnCycle this.onCycle = " + str(self.onCycle))
        _log.debug("in class counter function isItAnOnCycle this.offCycle = " + str(self.offCycle))
        if (self.overwrite is "On"):
             return True
        elif(self.overwrite is "Off"):
             return False
        else:
            now = self.cycle - self.onCycle
            if (now < 0):
                return True
            else:
                return False
        
   def isItAnOffCycle(self, _log) :
        _log.debug("in class counter function isItAnOffCycle")
        if (self.overwrite is "On"):
             return False
        elif(self.overwrite is  "Off"):
             return True
        else:
            if(self.offCycle == 0):
                return False
               
            now = self.cycle - self.onCycle
            now = now - self.offCycle
            _log.debug("now = " + str(now))
            
            if (now < 0):
                _log.debug("in class counter function isItAnOffCycle and it is true")
                return True
            else:
                _log.debug("in class counter function isItAnOffCycle and if is false")
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
   
   def infoCounter(self):
         if (self.overwrite is "On"):
             return "Currently in minute " + str(self.cycle) + " pump is set manually ON " 
         elif(self.overwrite is  "Off"):
             return "Currenlt in minute " + str(self.cycle) + "  pump is set manually OFF"
         else:
             if 
         return "Currenlt in minute " + str(self.cycle) + " so the pump is on untill mminute " + str(self.onCycle) + " when it will stop for " + str(self.offCycle)
     
        
   def  incCycle(self, _log):
        _log.debug("in class counter function incCycle")
        _log.debug("Cycle was " + str(self.cycle))
        self.cycle = self.cycle + 1
        if (self.cycle > (self.onCycle + self.offCycle)):
            self.cycle = 0
        _log.debug("Cycle now " + str(self.cycle))
        return self.cycle
             
   def  reset(self, _log):
        _log.debug("in class counter function reset")
        _log.debug("Cycle was " + str(self.cycle))
        self.cycle = 0
        _log.debug("Cycle now " + str(self.cycle))
        return self.cycle
