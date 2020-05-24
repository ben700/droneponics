import logging
import socket
import blynklib
from configparser import ConfigParser
from drone.droneObj import colours

def gethostname():
    return socket.gethostname()

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def setupBasicFormObjects(*args, **kwargs):
   blynk = kwargs.get('blynkObj', None)
   _log = kwargs.get('loggerObj', None)
   msg =  kwargs.get('Msg', None)

   if _log is None:
      _log = logging.getLogger('BlynkLog')
      logFormatter = logging.Formatter("%(asctime)s [%(levelname)s]  %(message)s")
      consoleHandler = logging.StreamHandler()
      consoleHandler.setFormatter(logFormatter)
      _log.addHandler(consoleHandler)
      parser = ConfigParser()
      parser.read('/home/pi/configAir.ini')
      _log.setLevel(parser.get('logging', 'logLevel', fallback=logging.CRITICAL))
   _log.debug("setFromBlynkLogObjects :- Just created log and now checking if we still have blynk")
   if blynk is None:
      _log.info("setFormOnline :- Didn't have blynk")
      parser = ConfigParser()
      parser.read('/home/pi/configAir.ini')
      blynk = blynklib.Blynk(parser.get('blynk', 'BLYNK_AUTH'))
      _log.info("setFormOnline :- We do now")
   return blynk, _log

def setFormOnline(*args, **kwargs):
   blynk, _log = setFromBlynkLogObjects (blynkObj=kwargs.get('blynkObj', None), loggerObj=kwargs.get('loggerObj', None))  
   _log.debug("setFormOnline :- Going to set from colour Online e.g.("+colours['ONLINE']+") for everything")
   blynk.run()
   for i in range(255): 
      blynk.set_property(i, 'color', colours['ONLINE']) 
   _log.debug("setFormOnline :- end of fx setFormOnline")
      
def setFormOffline(*args, **kwargs):
   blynk, _log = setFromBlynkLogObjects (blynkObj=kwargs.get('blynkObj', None), loggerObj=kwargs.get('loggerObj', None))  
   _log.debug("setFormOffline :- Going to set from colour Online e.g.("+colours['ONLINE']+") for everything")
   blynk.run()
   for i in range(255): 
      blynk.set_property(i, 'color', colours['OFFLINE']) 
   _log.debug("setFormOnline :- end of fx setFormOnline")

def setBMEFormOnline(*args, **kwargs):
    blynk, _log = setFromBlynkLogObjects (blynkObj=kwargs.get('blynkObj', None), loggerObj=kwargs.get('loggerObj', None))  
    _log.debug("setBMEFormOnline : start fx")
    blynk.run()
    pins = [1,2,3,4,5,11]
    for pin in pins:
        _log.debug("setBMEFormOnline : update colour online eg(" + colours['ONLINE']+ ") for vPin = " + str(pin))
        blynk.set_property(pin, 'color', colours['ONLINE']) 
  
def setBMEFormOffline(*args, **kwargs):
   blynk, _log = setFromBlynkLogObjects (blynkObj=kwargs.get('blynkObj', None), loggerObj=kwargs.get('loggerObj', None))  
   _log.debug("setBMEFormOffline : start fx")
   blynk.run()
   pins = [1,2,3,4,5,11]
   for pin in pins:
        _log.debug("setBMEFormOnline : update colour online eg(" + colours['ONLINE']+ ") for vPin = " + str(pin))
        blynk.set_property(pin, 'color', colours['OFFLINE']) 
  
def setTSLFormOnline(*args, **kwargs):
   blynk, _log = setFromBlynkLogObjects (blynkObj=kwargs.get('blynkObj', None), loggerObj=kwargs.get('loggerObj', None))  
   _log.debug("setTSLFormOnline : start fx")
   blynk.run()
   pins = [6,7,8,9]
   for pin in pins: 
        _log.debug("setBMEFormOnline : update colour online eg(" + colours['ONLINE']+ ") for vPin = " + str(pin))
        blynk.set_property(pin, 'color', colours['ONLINE']) 
   
def setTSLFormOffline(*args, **kwargs):
   blynk, _log = setFromBlynkLogObjects (blynkObj=kwargs.get('blynkObj', None), loggerObj=kwargs.get('loggerObj', None))  
   _log.debug("setTSLFormOffline : start fx")
   blynk.run()
   pins = [6,7,8,9]
   for pin in pins:
        _log.debug("setBMEFormOnline : update colour online eg(" + colours['ONLINE']+ ") for vPin = " + str(pin))
        blynk.set_property(pin, 'color', colours['OFFLINE']) 
 
   
def setMHZFormOnline(*args, **kwargs):
   blynk, _log = setFromBlynkLogObjects (blynkObj=kwargs.get('blynkObj', None), loggerObj=kwargs.get('loggerObj', None))  
   _log.debug("setMHZFormOnline : start fx")
   blynk.run()
   _log.debug("setBMEFormOnline : update colour online eg(" + colours['ONLINE']+ ") for vPin = 10")
   blynk.set_property(10, 'color', colours['ONLINE'])

def setMHZFormOffline(*args, **kwargs):
   blynk, _log = setFromBlynkLogObjects (blynkObj=kwargs.get('blynkObj', None), loggerObj=kwargs.get('loggerObj', None))  
   _log.debug("setMHZFormOffline : start fx")
   blynk.run()
   blynk.set_property(10, 'color', colours['OFFLINE'])
