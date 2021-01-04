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


print("{0}: {1}".format("wlan0", drone.get_mac("wlan0")))
  
# list all available network interfaces
#def list_all_netifaces():
#	return psutil.net_if_addrs().keys()

# print them all
#for ifaces in list_all_netifaces():
#	print("{0}: {1}".format(ifaces, drone.get_mac(ifaces)))
  
 
