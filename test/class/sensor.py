import time
import sys
import os
sys.path.append('/home/pi/droneponics')
import drone
from configparser import ConfigParser
import logging


parser = ConfigParser()
parser.read("/home/pi/droneponics/config/configOxy/"+drone.gethostname()+".ini")



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

_log.info("ConfigParser path = /home/pi/droneponics/config/configOxy/"+drone.gethostname()+".ini")

sensors = []
sensors = drone.buildMonitorSensors(sensors, _log)
_log.info("All Monitor Sensors created")

for sensor in sensors:
    if sensor is not None:
        _log.critical("Going to read the " + sensor.name)    
        sensor.read()
        _log.critical("The " + sensor.name + " is " + str(sensor.value))
        _log.critical("The " + sensor.name + " probe is connected =" + str(sensor.isProbeConnected()))
        _log.critical("The " + sensor.name + " probe calibration is  " + str(sensor.currenCalibration()))

try:		
    _log.info("Going to call drone.getTempColour")    
    sensors[0].color = drone.getTempColour(_log, int(round(float(sensors[0].value)*10,0)))
except:
    _log.critical("Working out sensor colour crashed")
