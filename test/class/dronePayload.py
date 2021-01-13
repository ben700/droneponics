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



_log.critical('{{ "ts": "{}", "deviceMAC": "{}", "deviceName": "{}", "deviceIP": "{}"}}'.format(int(time.time()), drone.get_mac(), drone.gethostname(), drone.get_ip()))

payload = drone.dronePayload(_log)
payload.add("deviceName",  drone.gethostname())
payload.add("deviceIP", drone.get_ip())
payload.add("TestNone", None)
_log.critical(payload.get())

