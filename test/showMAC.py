import sys
import os
sys.path.append('/home/pi/droneponics')
import drone 


macAddress = drone.get_mac()
print(macAddress)
  
   
