##!/usr/bin/env python3 
import time
import sys
import os
sys.path.append('/home/pi/droneponics/droneAirAtlas')
from AtlasI2C import (AtlasI2C)
    
device = AtlasI2C()
device_address_list = device.list_i2c_devices()
print("Found " + str(len(device_address_list)) + " devices" + '\n')
for i in device_address_list:
   print("Device at address " + str(i))  
   idevice = AtlasI2C(i)
   try:
     moduletype = idevice.query("I").split(",")[1]
     print("Device type " + moduletype) 
     time.sleep(1)
   except:
     print("Error query info")

   try:
     reading = idevice.query("R").split(":")[1]
     print("Device Reading " + str(reading)) 
     time.sleep(1)
   except:
     print("Error reading")

   try:
     cal = idevice.query("cal,?").split(",")[1]
     print("Device calibration " + cal) 
   except:
     print("Error query cal")
