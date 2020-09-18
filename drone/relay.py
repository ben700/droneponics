from datetime import datetime, date
import time
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
       self.startTime = None
       self.stopTime = None
       self.days = None
       self.infoPin = None
       
   def setInfoPin(self, infoPin): 
        self.infoPin = infoPin
         
   def getInfoPin(self): 
        return self.infoPin      
   
   def hasInfoPin(self):
      if(self.infoPin is None):
         return False
      else:
         return True
         
   def whatCycle(self): 
       self._log.debug("whatCycle for "+self.name+" self.cycle = " + str(self.cycle) + " reset at " +str(self.cycleReset))
       if(self.isAutomatic()):
         if(self.getState() == "Auto"):
             if(self.cycle > self.cycleReset):
                 return "Off"
             return "On"
         elif(self.getState() == "Timer"):
            today = date.today()
            seconds_since_midnight = int(time.time() - time.mktime(today.timetuple()))
            if( self.startTime < seconds_since_midnight and self.stopTime > seconds_since_midnight):
               self._log.debug(self.name + " On")
               return "On"
            else:
               self._log.debug(self.name + " Off")
               return "Off"
         else:
            return self.state
         
   def turnOn(self, _log): 
       try:
          _log.info("Turning on relay " + self.name)
          GPIO.output(self.gpioPin,GPIO.LOW) 
          _log.info("Turned on relay " + self.name + " on pin " + str(self.gpioPin))
       except:
          _log.error("Except relayClass: Turning on relay " + self.name)
      
   def turnOff(self, _log): 
       try:
           _log.info("Turning off relay " + self.name)
           GPIO.output(self.gpioPin,GPIO.HIGH) 
           _log.info("Turned off relay " + self.name + " on pin " + str(self.gpioPin))
       except:
           _log.error("Except relayClass: Turning off relay " + self.name)
         
   def turnAuto(self, _log): 
       try:
           _log.info("Turning relay " + self.name + " to auto") 
       except:
           _log.error("Except relayClass: Turnin relay " + self.name+ " to auto")
     
   
   def setState(self, state):
         self._log.debug("in setState State = " + state)
         self.state = state

   def getState(self):
         return self.state
         
   def setManual(self, state):
         self._log.debug("in setManual state = " + state)
         self.automatic = False
         self.setState(state)
         self.startTime = None
         self.stopTime = None   
         
   def setTimer(self, startTime, stopTime, days):
         self._log.debug("in setTimer")
         self.automatic = True
         self.startTime = startTime
         self.stopTime = stopTime
         self.days = days         
         self.setState("Timer")
   
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
      if(self.hasOffCycle):
          self.cycle = 0 
   
   def setOffCycleReset(self):
      self._log.debug("in setOffCycleReset")
      self.offCycle = 0 
      
   def incCycle(self):
      if(self.automatic):
           self.cycle = self.cycle + 1
           if(self.cycle > (self.cycleReset+self.offCycleReset)):
                self.cycleOnReset()
      return self.cycle
   
   def info(self):   
         if (self.getState() is "Auto"):
            if(self.hasOffCycle):
                  return self.name + " is "+str(self.whatCycle())+" In minute " + str(self.cycle) + " for " + str(self.cycleReset) + " mins."
            else:
                  return self.name + " is "+str(self.whatCycle())+" In minute " + str(self.cycle) + " On " + str(self.cycleReset) + " off for "+ str(self.offCycleReset) + " mins."
         elif(self.getState() is  "Timer"):
            return self.name + " is on Timer mode and is " + str(self.whatCycle()) + "."
         elif(self.getState() is  "On"):
            return self.name + " set manually ON " 
         elif(self.getState() is  "Off"):   
            return self.name + " set manually OFF"
         
   def setBlynkLabel(self, blynk, button, LED):
           blynk.set_property(button, "label", self.name)
           blynk.set_property(LED, "label", self.name)
           blynk.virtual_write(LED, 255)
