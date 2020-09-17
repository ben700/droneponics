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

def setFormBlynkLogObjects(*args, **kwargs):
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
   _log.debug("setFormBlynkLogObjects :- Just created log and now checking if we still have blynk")
   if blynk is None:
      _log.info("setFormOnline :- Didn't have blynk")
      parser = ConfigParser()
      parser.read('/home/pi/configAir.ini')
      blynk = blynklib.Blynk(parser.get('blynk', 'BLYNK_AUTH'))
      _log.info("setFormOnline :- We do now")
   return blynk, _log

def setFormOnlineColours(*args, **kwargs):
   blynk, _log = setFormBlynkLogObjects (blynkObj=kwargs.get('blynkObj', None), loggerObj=kwargs.get('loggerObj', None))  
   _log.debug("setFormOnlineColours :- Going to set from colour Online e.g.("+colours['ONLINE']+") for everything")
   blynk.run()
   for i in range(255): 
      _log.debug("setFormOnlineColours :- Going to set from colour Online e.g.("+colours['ONLINE']+") for vPin " + str(i))  
      blynk.set_property(i, 'color', colours['ONLINE']) 
   _log.debug("setFormOnlineColours :- end of fx setFormOnline")
      
def setFormOfflineColours(*args, **kwargs):
   blynk, _log = setFormBlynkLogObjects (blynkObj=kwargs.get('blynkObj', None), loggerObj=kwargs.get('loggerObj', None))  
   _log.debug("setFormOfflineColours :- Going to set from colour Online e.g.("+colours['ONLINE']+") for everything")
   blynk.run()
   for i in range(255): 
      _log.debug("setFormOfflineColours :- Going to set from colour Offline e.g.("+colours['OFFLINE']+") for vPin " + str(i))  
      blynk.set_property(i, 'color', colours['OFFLINE']) 
   _log.debug("setFormOfflineColours :- end of fx setFormOnline")

def setBME680FormColours(bme680, *args, **kwargs):
    blynk, _log = setFormBlynkLogObjects (blynkObj=kwargs.get('blynkObj', None), loggerObj=kwargs.get('loggerObj', None))  
    _log.debug("setBME680FormColours : start fx")
    #blynk.run()
    _log.debug("setBME680FormColours : int(bme680.temperature*10) = " + str(int(bme680.temperature*10)))
    _log.debug("setBME680FormColours : drone.getTempColour(_log,int(bme680.temperature*10)) = " + str(drone.getTempColour(_log,int(bme680.temperature*10))))
    
    
    blynk.set_property(1, 'color', drone.getTempColour(_log,int(bme680.temperature*10))) 
    blynk.set_property(2, 'color', colours['ONLINE']) 
    blynk.set_property(3, 'color', drone.getTempColour(_log,int(bme680.humidity))) 
    blynk.set_property(4, 'color', colours['ONLINE']) 
    blynk.set_property(5, 'color', colours['ONLINE']) 
    blynk.set_property(11, 'color', colours['ONLINE']) 

        
def setBME280FormColours(bme280, *args, **kwargs):
    blynk, _log = setFormBlynkLogObjects (blynkObj=kwargs.get('blynkObj', None), loggerObj=kwargs.get('loggerObj', None))  
    _log.debug("setBME280FormColours : start fx")
    blynk.run()
    blynk.set_property(1, 'color', drone.getTempColour(_log,int(bme280.temperature*10))) 
    blynk.set_property(2, 'color', colours['OFFLINE']) 
    blynk.set_property(3, 'color', drone.getTempColour(_log,int(bme280.humidity))) 
    blynk.set_property(4, 'color', colours['ONLINE']) 
    blynk.set_property(5, 'color', colours['ONLINE']) 
    blynk.set_property(11, 'color', colours['ONLINE']) 
  
def setBMEFormOfflineColours(*args, **kwargs):
   blynk, _log = setFormBlynkLogObjects (blynkObj=kwargs.get('blynkObj', None), loggerObj=kwargs.get('loggerObj', None))  
   _log.debug("setBMEFormOfflineColours : start fx")
   blynk.run()
   pins = [1,2,3,4,5,11]
   for pin in pins:
        _log.debug("setBMEFormOfflineColours : update colour online eg(" + colours['ONLINE']+ ") for vPin = " + str(pin))
        blynk.set_property(pin, 'color', colours['OFFLINE']) 
  
def setTSLFormOnlineColours(*args, **kwargs):
   blynk, _log = setFormBlynkLogObjects (blynkObj=kwargs.get('blynkObj', None), loggerObj=kwargs.get('loggerObj', None))  
   _log.debug("setTSLFormOnlineColours : start fx")
   blynk.run()
   pins = [6,7,8,9]
   for pin in pins: 
        _log.debug("setTSLFormOnlineColours : update colour online eg(" + colours['ONLINE']+ ") for vPin = " + str(pin))
        blynk.set_property(pin, 'color', colours['ONLINE']) 
   
def setTSLFormOfflineColours(*args, **kwargs):
   blynk, _log = setFormBlynkLogObjects (blynkObj=kwargs.get('blynkObj', None), loggerObj=kwargs.get('loggerObj', None))  
   _log.debug("setTSLFormOfflineColours : start fx")
   blynk.run()
   pins = [6,7,8,9]
   for pin in pins:
        _log.debug("setTSLFormOfflineColours : update colour online eg(" + colours['ONLINE']+ ") for vPin = " + str(pin))
        blynk.set_property(pin, 'color', colours['OFFLINE']) 
 
   
def setMHZFormOnlineColours(*args, **kwargs):
   blynk, _log = setFormBlynkLogObjects (blynkObj=kwargs.get('blynkObj', None), loggerObj=kwargs.get('loggerObj', None))  
   _log.debug("setMHZFormOnlineColours : start fx")
   blynk.run()
   _log.debug("setMHZFormOnlineColours : update colour online eg(" + colours['ONLINE']+ ") for vPin = 10")
   blynk.set_property(10, 'color', colours['ONLINE'])

def setMHZFormOfflineColours(*args, **kwargs):
   blynk, _log = setFormBlynkLogObjects (blynkObj=kwargs.get('blynkObj', None), loggerObj=kwargs.get('loggerObj', None))  
   _log.debug("setMHZFormOfflineColours : start fx")
   blynk.run()
   blynk.set_property(10, 'color', colours['OFFLINE'])
