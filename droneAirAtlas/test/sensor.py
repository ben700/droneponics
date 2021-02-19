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
   idevice = AtlasI2C(i) 
   print(idevice.get_device_info())
   print(idevice.query("I"))
   print(idevice.query("R"))
