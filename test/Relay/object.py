import sys
import os
sys.path.append('/home/pi/droneponics')
import drone
import blynklib
import blynktimer
import logging  
import sys
import os
from configparser import ConfigParser

parser = ConfigParser()
parser.read("/home/pi/droneponics/config/configRelay/"+drone.gethostname()+".ini")

# tune console logging
_log = logging.getLogger('BlynkLog')
logFormatter = logging.Formatter("%(asctime)s [%(levelname)s]  %(message)s")
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
_log.addHandler(consoleHandler)
_log.setLevel(parser.get('logging', 'logLevel', fallback=logging.DEBUG))
_log.info("/home/pi/droneponics/config/configRelay/"+drone.gethostname()+".ini")



try:
    # Initialize Blynk
    blynk = blynklib.Blynk(parser.get('blynk', 'BLYNK_AUTH'), log=_log.info) 
    timer = blynktimer.Timer()
    _log.debug("start blynk")
    blynk.run()
    _log.info("Blynk Created")  
except:
    _log.info("except : Creating Blynk") 
    
    
relays=drone.RelaysI2C(_log, blynk)
relays.addRelay(1, "Relay1", 21, 85)
   
