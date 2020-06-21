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
      
       
   def testIt(self): 
       try:
          self._log.info("Testing relay " + self.name)
       except:
          self._log.error("Except: Testing relay " + self.name)
         
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
     
   
   def setManual(self):
         self.automatic = False
   
   def setAutomatic(self):
         self.automatic = True
     
   def isAutomatic(self, _log):
        return self.automatic
      
   def cycleResetSet(self, cycleReset):
      self.cycleReset = int(cycleReset) 
         
   def cycleOffResetSet(self, cycleReset):
      self.hasOffCycle = True
      self.offCycleReset = int(cycleReset) 
   
   def cycleOffResetClear(self):
      self.hasOffCycle = False
      self.offCycleReset = 0    
   
   def cycleReset(self, _log):
      self.cycle = 0 
   
   def offCycleReset(self, _log):
      self.offCycle = 0 
      
   def incCycle(self):
      if(self.automatic):
           self.cycle = self.cycle + 1
           if(self.cycle > self.cycleReset):
                self.cycleReset(_log)
      return self.cycle
   
   def incOffCycle(self):
      if(self.automatic):
           self.offCycle = self.offCycle + 1
           if(self.offCycle > self.offCycleReset):
                self.offCycleReset(_log)
      return self.offCycle
