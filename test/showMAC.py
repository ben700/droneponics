import socket, psutil
from binascii import hexlify
from configparser import ConfigParser
from datetime import datetime
import time
import logging
import sys
import os
sys.path.append('/home/pi/droneponics')
from AtlasI2C import (
   AtlasI2C
)
import drone 


from getmac import get_mac_address
eth_mac = get_mac_address(interface="wlan0")

#macAddress = drone.get_mac()
print(eth_mac)
  
   

#ipmacAddress = drone.get_ipmac()
#print(ipmacAddress)
  
