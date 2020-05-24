import logging
import socket
import blynklib
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

def setFromBlynkLogObjects(*args, **kwargs):
   blynk = kwargs.get('blynkObj', None)
   _log = kwargs.get('loggerObj', None)
   msg =  kwargs.get('Msg', None)
   if _log is None:
      _log = logging.getLogger('BlynkLog')
      logFormatter = logging.Formatter("%(asctime)s [%(levelname)s]  %(message)s")
      consoleHandler = logging.StreamHandler()
      consoleHandler.setFormatter(logFormatter)
      _log.addHandler(consoleHandler)
      _log.setLevel(logging.DEBUG)
   _log.debug("setFromBlynkLogObjects :- Just created log and now checking if we still have blynk")
   if blynk is None:
      _log.info("setFormOnline :- Didn't have blynk")
      blynk = blynklib.Blynk(parser.get('droneAir', 'BLYNK_AUTH'))
      _log.info("setFormOnline :- We do now")
   _log.debug("setFromBlynkLogObjects :- See if anything to send to terminal to set update blynk")
   if msg is not None:
      _log.debug("setFromBlynkLogObjects :- sending msg to terminal")
      blynk.run()
      blynk.virtual_write(98, msg + " " + '\n')
      _log.info("setFromBlynkLogObjects msg : " +msg)
   _log.debug("setFromBlynkLogObjects :- returning")
   return blynk, _log

def setFormOnline(*args, **kwargs):
   blynk, _log = drone.setFromBlynkLogObjects (kwargs.get('blynkObj', None),kwargs.get('loggerObj', None))  
   _log.debug("setFormOnline :- Going to set from colour Online e.g.("+colours['ONLINE']+") for everything")
   blynk.run()
   for i in range(255): 
      drone.set_property(i, 'color', colours['ONLINE']) 
   _log.debug("setFormOnline :- end of fx setFormOnline")
      
def setFormOffline(*args, **kwargs):
   blynk, _log = drone.setFromBlynkLogObjects (kwargs.get('blynkObj', None),kwargs.get('loggerObj', None))  
   _log.debug("setFormOffline :- Going to set from colour Online e.g.("+colours['ONLINE']+") for everything")
   blynk.run()
   for i in range(255): 
      blynk.set_property(i, 'color', colours['OFFLINE']) 
   _log.debug("setFormOnline :- end of fx setFormOnline")

def setBMEFormOnline(*args, **kwargs):
   blynk, _log = drone.setFromBlynkLogObjects (kwargs.get('blynkObj', None),kwargs.get('loggerObj', None))    
   blynk.run()
   pins = [1,2,3,4,5,11]
   for pin in pins:
        blynk.set_property(pin, 'color', colours['ONLINE']) 
  
def setBMEFormOffline(*args, **kwargs):
   blynk, _log = drone.setFromBlynkLogObjects (kwargs.get('blynkObj', None),kwargs.get('loggerObj', None))    
   blynk.run()
   pins = [1,2,3,4,5,11]
   for pin in pins:
      blynk.set_property(pin, 'color', colours['OFFLINE']) 
  
def setTSLFormOnline(*args, **kwargs):
   blynk, _log = drone.setFromBlynkLogObjects (kwargs.get('blynkObj', None),kwargs.get('loggerObj', None))    
   blynk.run()
   pins = [6,7,8,9]
   for pin in pins: 
      blynk.set_property(pin, 'color', colours['ONLINE']) 
  
def setTSLFormOffline(*args, **kwargs):
   blynk, _log = drone.setFromBlynkLogObjects (kwargs.get('blynkObj', None),kwargs.get('loggerObj', None))    
   blynk.run()
   pins = [6,7,8,9]
   for pin in pins:
      blynk.set_property(pin, 'color', colours['OFFLINE']) 
 
   
def setMHZFormOnline(*args, **kwargs):
   blynk, _log = drone.setFromBlynkLogObjects (kwargs.get('blynkObj', None),kwargs.get('loggerObj', None))    
   blynk.run()
   blynk.set_property(10, 'color', colours['ONLINE'])

def setMHZFormOffline(*args, **kwargs):
   blynk, _log = drone.setFromBlynkLogObjects (kwargs.get('blynkObj', None),kwargs.get('loggerObj', None))    
   blynk.run()
   blynk.set_property(10, 'color', colours['OFFLINE'])
