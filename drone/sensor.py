#from colour import Color
import blynklib
import blynktimer
import logging
from configparser import ConfigParser
import RPi.GPIO as GPIO   
from AtlasI2C import (
   AtlasI2C
)

def buildSensors(sensors, _log):
    _log.debug("in built sensors function")
    sensors.append( Sensor(102, "Temperature", 30, _log, Target=20, LowAlarm=10, HighAlarm=25))
    _log.debug("built temperature sensor")
    sensors.append( Sensor(100, "EC", 31 , _log, Target=100, LowAlarm=50, HighAlarm=1500))
    _log.debug("built ec sensor")
    sensors.append( Sensor(99, "pH", 32, _log, Target=5.5, LowAlarm=5.3, HighAlarm=6.5))
    _log.debug("built ph sensor")
    return sensors

def buildMonitorSensors(sensors, _log):
    _log.debug("in built sensors function")
    sensors.append( Sensor(102, "Temperature", 30, _log))
    _log.debug("built temperature sensor")
    sensors.append( Sensor(97, "Dissolved Oxygen", 33 , _log))
    _log.debug("built DO sensor")
    sensors.append( Sensor(98, "Oxidation Reduction Potential", 34, _log))
    _log.debug("built ORP sensor")
    return sensors

def buildOxySensors(sensors, _log):
    sensors.append( Sensor(97, "Dissolved Oxygen", 30, _log, Target=10))
    return sensors

def buildExperimentalSensors(sensors, _log):
    sensors.append( Sensor(97, "Dissolved Oxygen", 30, _log, Target=10))
    return sensors

class Sensor:
   def __init__(self, SensorId, name, DisplayPin, _log, *args, **kwargs):
       _log.info("__init__ for "  + name )
       self._log = _log
       self.sensor = AtlasI2C(SensorId)
       self.sensorId = SensorId
       self.name = name
       self.high =26
       self.low =15
       self.displayPin = DisplayPin
       self.target = kwargs.get('Target', None)
       self.mode = 1  # 1 = off 2 = on 3 = auto       
       self.value = None
       self.oldValue = None
       self.lowAlarm = kwargs.get('LowAlarm', None)
       self.highAlarm = kwargs.get('HighAlarm', None)
       self.color = None
       self.Cal= None
       
   def read(self):
       self.value = self.sensor.query("R").split(":")[1].strip().rstrip('\x00')
       self._log.info("Read for sensor " + self.name +" sensorId = " + str(self.sensorId) + " was " + str(self.value))      
       return self.value
   
   def display(self, blynk):
    self._log.info("base:display(blynk)")
    self._log.info("Going to update " + str(self.name) + " using pin " + str(self.displayPin) + " with value " + str(self.value))                  
   # blynk.virtual_write(98,"Going to update " + str(self.name) + " using pin " + str(self.displayPin) + " with value " + str(self.value) +'\n')
    blynk.set_property(self.displayPin, "label", self.name)
    blynk.set_property(self.displayPin, 'color', self.color)
    blynk.virtual_write(self.displayPin, self.value)
      
   def currenCalibration(self):
       self._log.info ("currenCalibration")
       self.Cal = self.sensor.query("Cal,?").split(":")[1].strip().rstrip('\x00')
       self._log.info("Read Calibration for sensor " + self.name +" sensorId = " + str(self.sensorId) + " was " + str(self.Cal))      
       return self.Cal
      
   def displayCurrenCalibration(self, blynk):
       self._log.info ("displayCurrenCalibration")
       self.Cal = self.sensor.query("Cal,?").split(":")[1].strip().rstrip('\x00')
       blynk.virtual_write(self.displayPin + 9, self.Cal)
       self._log.info ("finished displayCurrenCalibration") 
       self._log.info ("self.displayPin + 9 = " + str(self.displayPin + 9)) 
       self._log.info ("self.Cal=" + str(self.Cal) ) 
      
       
   
class WaterLevel():  
   GPIO.setmode(GPIO.BCM)
   GPIO.setwarnings(False)
 
 
   def __init__(self, _log, Name, gpioPin, blynkDisplayPin, blynkDisplayLEDPin,  lcdDisplayLine,  *args, **kwargs):
      self._log = _log
      _log.info("in WaterLevel constructor")
      self.gpioPin = gpioPin
      _log.info("WaterLevel constructor: going to do GPIO setup for pin " + str(gpioPin))
      self.gpio = GPIO.setup(gpioPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
      _log.info("WaterLevel constructor: done GPIO setup")
      self.name = Name
      self.blynkDisplayPin = blynkDisplayPin
      self.blynkDisplayLEDPin =blynkDisplayLEDPin
      self.lcdDisplayLine = lcdDisplayLine
      _log.info("WaterLevel constructor : About to read input")
      self.value = GPIO.input(self.gpioPin)
      _log.info("Completed WaterLevel constructor")
      
    
   def read(self):
      self.value = GPIO.input(self.gpioPin)
      return self.value
     
   def display(self, blynk, lcdObj):
    
     if self.read():
          
         # lcdObj.printline(self.lcdDisplayLine, self.name + " is true")
          blynk.virtual_write(self.blynkDisplayPin, self.name + " is true")  
          blynk.virtual_write(self.blynkDisplayLEDPin, 255)  
          blynk.set_property(self.blynkDisplayLEDPin, 'color', Color("green"))
        
     else:
      
        #  lcdObj.printline(self.lcdDisplayLine, self.name + " is false")
          blynk.virtual_write(self.blynkDisplayPin,self.name + " is false")
          blynk.virtual_write(self.blynkDisplayLEDPin, 255)  
          blynk.set_property(self.blynkDisplayLEDPin, 'color', Color("red"))
     
   def setBlynkLabel(self, blynk):
     blynk.set_property(self.blynkDisplayPin, "label", self.name)
    
