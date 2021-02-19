import sys
import os
sys.path.append('/home/pi/droneponics/droneAtlas/drone')
from AtlasI2C import (AtlasI2C)
import datetime
import time
class SensorList:
  def __init__(self):
    self.sensorlist = []
    try:
        RTD = Sensor(102, "Temperature", "temperature")
        EC = Sensor(100, "EC", "conductivity", "totalDissolvedSolids", "salinity", "specificGravity")
        PH = Sensor(99, "pH", "PH")
        DO = Sensor(97, "Dissolved Oxygen", "DO", "saturation")
        ORP = Sensor(98, "Oxidation Reduction Potential", "oxidationReductionPotential")
        CO2 = Sensor(105, "CO2", "CO2", "temperature")
        HUM = Sensor(111, "Humitity", "humidity", "temperature", "dewPoint")
    except:   
        print("Except creating list")
    devList = [RTD,  EC, PH, DO, ORP, CO2, HUM]
    i=0
    for device in devList:
      try:
        print("Testing to see if "+device.name+" sensor is connected")
        if (device.connected()):
          self.sensorlist.append(device)
          print("Success " + device.name + " is connected")          
      except:
          print("Didn't find " + device.name)
        
    print("Found total of " + str(len(self.sensorlist)) + " devices connected.")
    
  def payload(self, _payload):
    for sensor in self.sensorlist:
      sensor.payload(_payload);
    return _payload
  
class Sensor:
   def __init__(self, SensorId, name="", 
                _valuePayloadName = None,
                _value2PayloadName = None,
                _value3PayloadName = None,
                _value4PayloadName = None                
               ):
       self.sensor = AtlasI2C(SensorId)
       self.sensorId = SensorId
       self.name = name
       self.value = None
       self.value2 = None
       self.value3 = None
       self.value4 = None
       self.valuePayloadName = _valuePayloadName
       self.value2PayloadName = _value2PayloadName
       self.value3PayloadName = _value3PayloadName
       self.value4PayloadName = _value4PayloadName
       self.Cal= None
       self.CalPoint= None
        
        
   def connected(self):
       try:
          self.sensor.query("R")
          return True
       except:
           return False
        
   def read(self):
       try:
           reading = self.sensor.query("R")
           debug(self.name + " Sensor read " + str(reading)) 
           if(reading.find("Error") == -1):
               print("Reading Sensor  OK") 
           else:
               print("Reading Sensor got an Error")  
       except:
           print("Error reading raw data from sensor " + self.name)
  
       try:
           print("Sensor raw read is [" + reading + "]") 
           self.value = reading.split(":")[1].split(",")[0].strip().rstrip('\x00')
           print("Sensor processed read is [" + str(self.value) + "]")
       except:
           print("Error Processing value of Sensor " + self.name)
                 
       try:	
           self.value2 = reading.split(":")[1].split(",")[1].strip().rstrip('\x00')
           print("Second value from " + self.name + " is " + str(self.value2))
       except:
           self.value2 = None
       
       try:	
           self.value3 = reading.split(":")[1].split(",")[2].strip().rstrip('\x00')
           print("3rd value from " + self.name + " is " + str(self.value3))
       except:
           self.value3 = None
        
       try:	
           self.value4 = reading.split(":")[1].split(",")[3].strip().rstrip('\x00')
           print("4th value from " + self.name + " is " + str(self.value4))
       except:
           self.value3 = None
            
       print("Read for sensor " + self.name +" sensorId = " + str(self.sensorId) + " was " + str(self.value))      
       return self.value
   
   def payload(self, _payload):
      self.read()
      if(self.value != None):
        _payload[self.valuePayloadName] = self.value 
      if(self.value2 != None):
        _payload[self.value2PayloadName] = self.value 
      if(self.value3 != None):
        _payload[self.value3PayloadName] = self.value 
      if(self.value3 != None):
        _payload[self.value4PayloadName] = self.value 
         

 

   def currenCalibration(self):
       print ("currenCalibration")
       self.Cal = self.sensor.query("Cal,?").split(":")[1].strip().rstrip('\x00')
       print("Read Calibration for sensor " + self.name +" sensorId = " + str(self.sensorId) + " was " + str(self.Cal))      
       
      
