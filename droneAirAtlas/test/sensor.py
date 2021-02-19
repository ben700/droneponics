##!/usr/bin/env python3 
import sys
import os
sys.path.append('/home/pi/droneponics/droneAirAtlas')
from AtlasI2C import (AtlasI2C)
    
device = AtlasI2C()
device_address_list = device.list_i2c_devices()
print("Found " + str(len(device_address_list)) + " devices")
for i in device_address_list:
   print("Success :- Found " + str(i))
    
    
try:
  hum = AtlasI2C(111)
except:
  print("Unexpected error: Atlas")
   
   
try:	
  reading = hum.query("R").split(":")[1]
  delay(1000)
  print("Reading :" + str(hum) + '\n')
except:
  print("Expected error: Use Atlas CO2 Error")
