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
    sensors.append( Sensor(100, "EC", 31 , _log, value2DisplayPin=33, DisplayPin2Label="TDS", value3DisplayPin=34, DisplayPin3Label="Salinity", value4DisplayPin=37, DisplayPin4Label="Specific Gravity", Target=100, LowAlarm=50, HighAlarm=1500))
    _log.debug("built ec sensor")
    sensors.append( Sensor(99, "pH", 32, _log, Target=5.5, LowAlarm=5.3, HighAlarm=6.5))
    _log.debug("built ph sensor")
    return sensors

def buildMonitorSensors(sensors, _log):
    _log.debug("in built sensors function")
    sensors.append( Sensor(102, "Temperature", 30, _log))
    _log.debug("built temperature sensor")
    sensors.append( Sensor(97, "Dissolved Oxygen", 33 , _log, value2DisplayPin=35, DisplayPin2Label="Saturation"))
   # sensors.append( Sensor(97, "Dissolved Oxygen", 33 , _log))
    _log.debug("built DO sensor")
    sensors.append( Sensor(98, "Oxidation Reduction Potential", 34, _log))
    _log.debug("built ORP sensor")
    return sensors

def buildCO2Sensors(sensors, _log):
    sensors.append( Sensor(105, "CO2", 10, _log))
    return sensors

def buildOxySensors(sensors, _log):
    sensors.append( Sensor(97, "Dissolved Oxygen", 30, _log, Target=10))
    return sensors

def buildExperimentalSensors(sensors, _log):
    sensors.append( Sensor(97, "Dissolved Oxygen", 30, _log, Target=10))
    return sensors

def buildAllSensors(sensors, _log):
    _log.debug("in built sensors function")
    sensors.append( Sensor(102, "Temperature", 30, _log, Target=20, LowAlarm=10, HighAlarm=25))
    _log.debug("built temperature sensor")
    sensors.append( Sensor(100, "EC", 31 , _log, value2DisplayPin=33, DisplayPin2Label="TDS", value3DisplayPin=34, DisplayPin3Label="Salinity", value4DisplayPin=37, DisplayPin4Label="Specific Gravity", Target=100, LowAlarm=50, HighAlarm=1500))
    _log.debug("built ec sensor")
    sensors.append( Sensor(99, "pH", 32, _log, Target=5.5, LowAlarm=5.3, HighAlarm=6.5))
    _log.debug("built PH sensor")
    sensors.append( Sensor(97, "Dissolved Oxygen", 33 , _log, value2DisplayPin=35, DisplayPin2Label="Saturation"))
   # sensors.append( Sensor(97, "Dissolved Oxygen", 33 , _log))
    _log.debug("built DO sensor")
    sensors.append( Sensor(98, "Oxidation Reduction Potential", 34, _log))
    _log.debug("built ORP sensor")
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
       self.displayPin2 = kwargs.get('value2DisplayPin', None)
       self.DisplayPin2Label = kwargs.get('DisplayPin2Label', None)
       self.displayPin3 = kwargs.get('value3DisplayPin', None)
       self.DisplayPin3Label = kwargs.get('DisplayPin3Label', None)  
       self.displayPin4 = kwargs.get('value4DisplayPin', None)
       self.DisplayPin4Label = kwargs.get('DisplayPin4Label', None)  
       self.target = kwargs.get('Target', None)
       self.mode = 1  # 1 = off 2 = on 3 = auto       
       self.value = None
       self.value2 = None
       self.value3 = None
       self.value4 = None
       self.oldValue = None
       self.lowAlarm = kwargs.get('LowAlarm', None)
       self.highAlarm = kwargs.get('HighAlarm', None)
       self.color = None
       self.Cal= None
       self.CalPoint= None
       self.HighCalPoint= None
       self.MidCalPoint= None
       self.LowCalPoint= None
      
       
   def read(self):
       try:
           reading = self.sensor.query("R")
       except:
           self._log.critial("Error reading raw data from sensor " + self.name)
  
       try:
           self.value = reading.split(":")[1].split(",")[0].strip().rstrip('\x00')
       except:
           self._log.critial("Error Processing value of Sensor " + self.name)
                 
       try:	
           self.value2 = reading.split(":")[1].split(",")[1].strip().rstrip('\x00')
           self._log.debug("Second value from " + self.name + " is " + str(self.value2))
       except:
           self.value2 = None
       
       try:	
           self.value3 = reading.split(":")[1].split(",")[2].strip().rstrip('\x00')
           self._log.debug("3rd value from " + self.name + " is " + str(self.value3))
       except:
           self.value3 = None
        
       try:	
           self.value4 = reading.split(":")[1].split(",")[3].strip().rstrip('\x00')
           self._log.debug("4th value from " + self.name + " is " + str(self.value4))
       except:
           self.value3 = None
            
       self._log.info("Read for sensor " + self.name +" sensorId = " + str(self.sensorId) + " was " + str(self.value))      
       return self.value
   
   def display(self, blynk):
    self._log.info("base:display(blynk)")
    self._log.info("Going to update " + str(self.name) + " using pin " + str(self.displayPin) + " with value " + str(self.value))
    try:      
        blynk.set_property(self.displayPin, "label", self.name)
        self._log.info("Going to update " + str(self.name) + " using pin " + str(self.displayPin) + " with color " + str(self.color)) 
        self.color = red
        blynk.set_property(self.displayPin, 'color', self.color)
        blynk.virtual_write(self.displayPin, self.value)
    except:
        self._log.info("Error updating value 1 on " + self.name)                  
    try:
        self._log.info("going to process displayPin2 for " + self.name)      
        if(self.displayPin2 is not None):
            self._log.info("displayPin2 is " + str(self.displayPin2))
            if(self.DisplayPin2Label is not None):
                self._log.info("Going to update " + str(self.DisplayPin2Label) + " using pin " + str(self.displayPin2) + " with value " + str(self.value2))                  
                blynk.set_property(self.displayPin2, "label", self.DisplayPin2Label)
            else:
                blynk.set_property(self.displayPin2, "label", self.name)
            blynk.set_property(self.displayPin2, 'color', self.color)
            if (self.value2 is not None):
                blynk.virtual_write(self.displayPin2, self.value2)
    except:
        self._log.info("Error updating value 2 on " + self.name)                  
  
    try:
        self._log.info("going to process displayPin3 for " + self.name)      
        if(self.displayPin3 is not None):
            self._log.info("displayPin3 is " + str(self.displayPin3))
            if(self.DisplayPin3Label is not None):
                self._log.info("Going to update " + str(self.DisplayPin3Label) + " using pin " + str(self.displayPin3) + " with value " + str(self.value3))                  
                blynk.set_property(self.displayPin3, "label", self.DisplayPin3Label)
            else:
                blynk.set_property(self.displayPin3, "label", self.name)
            blynk.set_property(self.displayPin3, 'color', self.color)
            if (self.value3 is not None):
                blynk.virtual_write(self.displayPin3, self.value3)
    except:
        self._log.info("Error updating value 3 on " + self.name)  
         
         
    try:
        self._log.info("going to process displayPin4 for " + self.name)      
        if(self.displayPin4 is not None):
            self._log.info("displayPin4 is " + str(self.displayPin4))
            if(self.DisplayPin4Label is not None):
                self._log.info("Going to update " + str(self.DisplayPin4Label) + " using pin " + str(self.displayPin4) + " with value " + str(self.value4))                  
                blynk.set_property(self.displayPin4, "label", self.DisplayPin4Label)
            else:
                blynk.set_property(self.displayPin4, "label", self.name)
            blynk.set_property(self.displayPin4, 'color', self.color)
            if (self.value4 is not None):
                blynk.virtual_write(self.displayPin4, self.value4)
    except:
        self._log.info("Error updating value 4 on " + self.name)           
         



   def currenCalibration(self):
       self._log.info ("currenCalibration")
       self.Cal = self.sensor.query("Cal,?").split(":")[1].strip().rstrip('\x00')
       self._log.info("Read Calibration for sensor " + self.name +" sensorId = " + str(self.sensorId) + " was " + str(self.Cal))      
       
      
   def displayCurrenCalibration(self, blynk):
       self._log.info ("displayCurrenCalibration")
       self.Cal = self.sensor.query("Cal,?").split(":")[1].strip().rstrip('\x00')
       self._log.info ("update app")      
       blynk.virtual_write(self.displayPin + 10, str(self.Cal))
       self._log.info ("finished displayCurrenCalibration") 
       self._log.info ("self.displayPin + 10 = " + str(self.displayPin + 9)) 
       self._log.info ("self.Cal=" + str(self.Cal) ) 
      
   def isProbeConnected(self):
       try:
           info = self.sensor.query("I")
           return True
       except:
           return False
      
   
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
    
