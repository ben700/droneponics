import time
import sys
import os
sys.path.append('/home/pi/droneponics')
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
    
sensors = []
if(str(device_sensor_type) == "PH"):
    sensors = drone.buildSensors(sensors, _log)
else:
    sensors = drone.buildMonitorSensors(sensors, _log)
_log.info("All Monitor Sensors created")

for sensor in sensors:
    if sensor is not None:
        _log.critical("Going to read the " + sensor.name)    
        sensor.read()
        _log.critical("The " + sensor.name + " is " + str(sensor.value))
        _log.critical("The " + sensor.name + " probe calibration is  " + str(sensor.currenCalibration()))

try:		
    _log.info("Going to call drone.getTempColour")    
    sensors[0].color = drone.getTempColour(_log, int(round(float(sensors[0].value)*10,0)))
except:
    _log.critical("Working out sensor colour crashed")
    
    

_log.info("Going to call drone.getTempColour")   
payload = ''
payload = drone.buildPayload(sensors, _log, payload)
_log.info("payload for google is = " + payload)


_log.info("Going to call drone.pubToGoolgeCloud")   
drone.pubSensorReadingsToGoolgeCloud(sensors, _log)
_log.info("Completed call drone.pubToGoolgeCloud")   
    
