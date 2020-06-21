import blynklib
import blynktimer
import logging
from configparser import ConfigParser
import RPi.GPIO as GPIO   

class Relay:
   GPIO.setmode(GPIO.BCM)
   GPIO.setwarnings(False)

   def __init__(self, _log, gpioPin, Name, *args, **kwargs):
       _log.info("Building Relay object for Relay " + Name)
       self._log = _log
       self.gpioPin = gpioPin
       self.name = Name
       self.gpio = GPIO.setup(gpioPin, GPIO.OUT)
       self.automatic = False
       self.cycle=0
       self.cycleReset=0
       self.hasOffCycle=False
       self.offCycle=0
       self.offCycleReset=0
       self.state = "Off"
       
   def whatCycle(self): 
       if(self.cycle > self.cycleReset):
            return "Off"
       return "On"
         
   def turnOn(self, _log): 
       try:
          _log.info("Turning on relay " + self.name)
          GPIO.output(self.gpioPin,GPIO.HIGH) 
       except:
          _log.error("Except relayClass: Turning on relay " + self.name)
      
   def turnOff(self, _log): 
       try:
           _log.info("Turning off relay " + self.name)
           GPIO.output(self.gpioPin,GPIO.LOW) 
       except:
           _log.error("Except relayClass: Turning off relay " + self.name)
         
   def turnAuto(self, _log): 
       try:
           _log.info("Turning relay " + self.name + " to auto") 
       except:
           _log.error("Except relayClass: Turnin relay " + self.name+ " to auto")
     
   
   def setState(self, state):
         self._log.debug("in setState")
         self.state = state
         
   def setManual(self, state):
         self.automatic = False
         self.setState(state)
   
   def setAutomatic(self):
         self._log.debug("in setAutomatic")
         self.automatic = True
         self.setState("Auto")
     
   def isAutomatic(self):
        return self.automatic
      
   def cycleResetSet(self, cycleReset):
      self.cycleReset = int(cycleReset) 
         
   def cycleOffResetSet(self, cycleReset):
      self.hasOffCycle = True
      self.offCycleReset = int(cycleReset) 
   
   def cycleOffResetClear(self):
      self.hasOffCycle = False
      self.offCycleReset = 0    
   
   def cycleOnReset(self):
      self._log.debug("in cycleReset")
      self.cycle = 0 
   
   def offCycleReset(self):
      self.offCycle = 0 
      
   def incCycle(self):
      if(self.automatic):
           self.cycle = self.cycle + 1
           if(self.cycle > (self.cycleReset+self.offCycleReset)):
                self.cycleOnReset()
      return self.cycle
   
   def info(self):
        return "Feed is on for " + str(self.cycleReset) + " mins and then off for " + str(self.offCycleReset) + " mins."
   
   def infoCounter(self):
         if (self.feedState is "On"):
             return "Currently in minute " + str(self.cycle) + " pump is set manually ON " 
         elif(self.feedState is  "Off"):
             return "In minute " + str(self.cycle) + "  pump is set manually OFF"
         else:   
            if(self.cycle <= self.onCycle):
                  return "In minute " + str(self.cycle) + " pump is on till minute " + str(self.onCycle)
            else:
                  return "In minute " + str(self.cycle) + " pump is off till minute " + str(self.onCycle+self.offCycle)
        
   def setBlynkLabel(self, blynk, button, LED):
           blynk.set_property(button, "label", self.name)
           blynk.set_property(LED, "label", self.name)
           blynk.virtual_write(LED, 255)
