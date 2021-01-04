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

macAddress = drone.get_mac()
print(macAddress)
  
   
