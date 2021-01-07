import time
import sys
import os
sys.path.append('/home/pi/droneponics')
from AtlasI2C import (AtlasI2C)
import drone
from configparser import ConfigParser
import logging


parser = ConfigParser()
parser.read("/home/pi/droneponics/config/Google/"+drone.gethostname()+".ini")



# tune console logging
_log = logging.getLogger('GoogleLog')
logFormatter = logging.Formatter("%(asctime)s [%(levelname)s]  %(message)s")
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
_log.addHandler(consoleHandler)
_log.setLevel(parser.get('logging', 'logLevel', fallback=logging.DEBUG))
_log.critical("critical")
_log.error("error")
_log.warning("warning")
_log.info("info")
_log.debug("debug")

_log.info("ConfigParser path = /home/pi/droneponics/config/Google/"+drone.gethostname()+".ini")

device_sensor_type = parser.get('Google', 'device_sensor_type')
_log.info('-------------------- device_sensor_type = ' + str(device_sensor_type))
    
    
nutrientMix = []
nutrientMix = drone.buildNutrientMix(nutrientMix, _log, scheduleWeek='Grow')    
for dosage in nutrientMix:
     dosage.pump = AtlasI2C(dosage.pumpId)
     payload = ''
     payload = dosage.buildPayload(payload)
     _log.info(payload)
     drone.pubDoseVolumeToGoolgeCloud(dosage, _log)  
