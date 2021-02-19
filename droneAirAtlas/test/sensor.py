##!/usr/bin/env python3 
import time
import sys
import os
sys.path.append('/home/pi/droneponics/droneAirAtlas')
from AtlasI2C import (AtlasI2C)
    
device = AtlasI2C()
device_address_list = device.list_i2c_devices()
print("Found " + str(len(device_address_list)) + " devices" + '/n')
for i in device_address_list:
   idevice = AtlasI2C(i)
   print("Device Name " + '/n') 
   print(idevice.name())

   print("Device Information " + '/n') 
   print(idevice.get_device_info())
   print("Device Information " + '/n') 
   print(idevice.query("i"))
   time.sleep(1)
   print("Device Reading " + '/n') 
   print(idevice.query("R"))
