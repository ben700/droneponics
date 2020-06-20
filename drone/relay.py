import blynklib
import blynktimer
import logging
from configparser import ConfigParser
import RPi.GPIO as GPIO   

class Relay:
   GPIO.setmode(GPIO.BCM)
   GPIO.setwarnings(False)

   def __init__(self, gpioPin, Name, *args, **kwargs):
       print("Building object")
       self.gpioPin = gpioPin
       self.name = Name
       self.gpio = GPIO.setup(gpioPin, GPIO.OUT)
       self.automatic = False
       self.cycle=0
       self.cycleReset=0
       
def turnOn(self, _log): 
    try:
         _log.info("Turning on relay " + self.name)
         self.gpio.output(self.gpioPin,GPIO.HIGH) 
    except:
         _log.error("Except: Turning on relay " + self.name)
      
def turnOff(self, _log): 
    
    try:
         _log.info("Turning off relay " + self.name)
         self.gpio.output(self.gpioPin,GPIO.LOW) 
    except:
         _log.error("Except: Turning off relay " + self.name)
     
def setManual(self):
         self.automatic = False
   
def setAutomatic(self):
         self.automatic = True
     
def isAutomatic(self, _log):
        return self.automatic
      
def cycleResetSet(self, _log, cycleReset):
      self.cycleReset = int(cycleReset) 
   
def cycleReset(self, _log):
      self.cycle = 0 
      
def incCycle(self):
      self.cycle = self.cycle + 1
      return self.cycle
