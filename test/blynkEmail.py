from configparser import ConfigParser
from datetime import datetime, date
import logging
import blynklib
import sys
sys.path.append('/home/pi/droneponics')
import drone

TARGET_EMAIL = 'benslittlebitsandbobs@gmail.com'


parser = ConfigParser()
parser.read('/home/pi/configRelay.ini')

now = datetime.now()

# tune console logging
_log = logging.getLogger('BlynkLog')
logFormatter = logging.Formatter("%(asctime)s [%(levelname)s]  %(message)s")
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
_log.addHandler(consoleHandler)
_log.setLevel(parser.get('logging', 'logLevel', fallback=logging.DEBUG))

blynk = blynklib.Blynk(parser.get('blynk', 'BLYNK_AUTH'), log=_log.info) 
blynk.run()  

blynk.email(TARGET_EMAIL, 'BLYNK-HW-TEST-EMAIL', 'Connected!')


    
