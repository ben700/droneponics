from configparser import ConfigParser
from datetime import datetime, date
import logging
import blynklib
import drone


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

blynk.notify("Testing blynk notify from " +  drone.gethostname() + " at " + now.strftime("%d/%m/%Y %H:%M:%S"))
