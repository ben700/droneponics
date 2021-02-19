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
        RTD = Sensor(102, "Temperature")
        EC = Sensor(100, "EC")
        PH = Sensor(99, "pH")
        DO = Sensor(97, "Dissolved Oxygen")
        ORP = Sensor(98, "Oxidation Reduction Potential")
        CO2 = Sensor(105, "CO2")
        HUM = Sensor(112, "Humitity")
    except:   
        print("Except creating list")
    i=0    
    try:
      if (RTD.connected()):
        self.sensorlist[i] = RTD
        i = i +1
    except:   
        print("Except creating temp")
    try:
      if (HUM.connected()):
        self.sensorlist[i] = HUM
        i = i +1
    except:   
        print("Except creating hum")
        
    for y in self.sensorlist
        print("Found " + i.name)    
        
  def devicesConnected(self):
        device_address_list = AtlasI2C().list_i2c_devices()
        print("Found " + str(len(device_address_list)) + " devices" + '\n')
        for i in device_address_list:
          print("Device at address " + str(i)) 
  
class Sensor:
   def __init__(self, SensorId, name="", *args, **kwargs):
       self.sensor = AtlasI2C(SensorId)
       self.sensorId = SensorId
       self.name = name
       self.value = None
       self.value2 = None
       self.value3 = None
       self.value4 = None
       self.Cal= None
       self.CalPoint= None
       self.HighCalPoint= None
       self.MidCalPoint= None
       self.LowCalPoint= None
       print("Build sensor " + self.name )
        
        
   def connected(self):
       try:
          print("testing connected")
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
   
         

 

   def currenCalibration(self):
       self.print ("currenCalibration")
       self.Cal = self.sensor.query("Cal,?").split(":")[1].strip().rstrip('\x00')
       self.print("Read Calibration for sensor " + self.name +" sensorId = " + str(self.sensorId) + " was " + str(self.Cal))      
       
      
