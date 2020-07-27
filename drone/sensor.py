from colour import Color
import blynklib
import blynktimer
import logging
from configparser import ConfigParser
import RPi.GPIO as GPIO   
import liquidcrystal_i2c

def displaySensor(blynk, VP, VALUE, NAME , LOW, HIGH):
 print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
 red = Color("red")
 print("loaded color class")
 colors = list(red.range_to(Color("green"),10))
 print("done colour list")
 print(colors)
 print("Going to update blynk")
 blynk.virtual_write(VP,VALUE)
 blynk.set_property(VP, "label", NAME)
 print("Going to update blynk colors")
 blynk.set_property(VP, "color", colors[round((HIGH-LOW)/10,0)])
 print("####################################################")
 return

class Sensor:
   def __init__(self, SensorId, name, *args, **kwargs):
       self.sensor = AtlasI2C(SensorId)
       self.sensorId = SensorId
       self.name = Name
       self.high =26
       self.low =15
       self.displayPin = kwargs.get('DisplayPin', None)
       self.target = kwargs.get('Target', None)
       self.value = None
       self.lowAlarm = kwargs.get('LowAlarm', None)
       self.highAlarm = kwargs.get('HighAlarm', None)

   def read():
       return self.sensor.query("R").split(":")[1].strip().rstrip('\x00')
   
   def display(blynk, VALUE):
    red = Color("red")
    colors = list(red.range_to(Color("green"),10))
    self.value =VALUE
    blynk.set_property(displayPin, "label", self.name)
    blynk.set_property(displayPin, 'color', colors[round((self.high-self.low)/10,0)])
    return blynk.virtual_write(displayPin, self.value)
    
class PH(Sensor):  
   def __init__(self, *args, **kwargs):
    Sensor.__init__(self, 99, "pH", 32, *args, **kwargs)
    self.high=6.3
    self.low=5.4
    self.target=5.5
   
   def read(self, cTemp):
      return self.sensor.query("RT,"+cTemp).split(":")[1].strip().rstrip('\x00')
 
class EC(Sensor):
   def __init__(self,  Target=600, *args, **kwargs):
      Sensor.__init__(self, 100, "EC",  31 , Target=600,  *args, **kwargs) 
      self.target=kwargs.get('Target')
      self.high=self.target+200
      self.low=self.target-200  
   def read(self, cTemp):
      return self.sensor.query("RT,"+cTemp).split(":")[1].strip().rstrip('\x00')
  
class DO(Sensor):
   def __init__(self, *args, **kwargs):
      Sensor.__init__(self, 97, "Dissolved Oxygen", 30, Target=10, *args, **kwargs) 
   def read(self, cTemp):
      return self.sensor.query("RT,"+cTemp).split(":")[1].strip().rstrip('\x00')
  
class TEMP(Sensor):  
   def __init__(self, *args, **kwargs):
      Sensor.__init__(self, 102, "Temprature", 30, Target=20, LowAlarm=10, HighAlarm=25, *args, **kwargs) 
    
class WaterLevel():  
   GPIO.setmode(GPIO.BCM)
   GPIO.setwarnings(False)
 
 
   def __init__(self, _log, Name, gpioPin, blynkDisplayPin, blynkDisplayLEDPin,  lcdDisplayLine,  *args, **kwargs):
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
     
   def display(self, blynk, lcd):
     if self.read():
          
          lcd.printline(self.lcdDisplayLine, self.name + " is true")
          blynk.virtual_write(self.blynkDisplayPin, self.name + " is true")  
          blynk.virtual_write(self.blynkDisplayLEDPin, 255)  
          blynk.set_property(self.blynkDisplayLEDPin, 'color', Color("green"))
        
     else:
      
          lcd.printline(self.lcdDisplayLine, self.name + " is false")
          blynk.virtual_write(self.blynkDisplayPin,self.name + " is false")
          blynk.virtual_write(self.blynkDisplayLEDPin, 255)  
          blynk.set_property(self.blynkDisplayLEDPin, 'color', Color("red"))
     
   def setBlynkLabel(self, blynk):
     blynk.set_property(self.blynkDisplayPin, "label", self.name)
     
