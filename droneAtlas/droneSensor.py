#from colour import Color
from AtlasI2C import (
   AtlasI2C
)
import datetime
import time
    
 
   
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
       
      
