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

def setFormOnline(*args, **kwargs):
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
   _log.debug("in setFormOnline")
   if blynk is None:
      blynk = blynklib.Blynk(parser.get('droneAir', 'BLYNK_AUTH'))
   blynk.run()
   _log.debug("Going to set Msg from setFormOnline")
   if msg is not None:
       blynk.virtual_write(98, msg + " " + '\n')
       _log.info(msg)
   _log.debug("Going to set from colour Offline from setFormOnline")
   for i in range(255): 
      blynk.set_property(i, 'color', colours['ONLINE'])
   blynk.set_property(98, 'color', "#000000")   
   _log.debug("Completed setFormOnline")
   
   
def setFormOffline(*args, **kwargs):
   blynk = kwargs.get('blynkObj', None)
   _log = kwargs.get('loggerObj', None)
   msg =  kwargs.get('Msg', None)
   _log.debug("in setFormOffline")
   if blynk is None:
      blynk = blynklib.Blynk(parser.get('droneAir', 'BLYNK_AUTH'))
   blynk.run()
   _log.debug("Going to set Msg from setFormOffline")
   if msg is not None:
       blynk.virtual_write(98, msg + " " + '\n')
       _log.info(Msg)
   _log.debug("Going to set from colour Offline from setFormOffline")
   for i in range(255): 
      blynk.set_property(i, 'color', colours['OFFLINE'])
   _log.debug("Completed setFormOffline")



def setBMEFormOnline(*args, **kwargs):
   blynk = kwargs.get('blynkObj', None)
   _log = kwargs.get('loggerObj', None)
   if _log is None:
      _log = logging.getLogger('BlynkLog')
      logFormatter = logging.Formatter("%(asctime)s [%(levelname)s]  %(message)s")
      consoleHandler = logging.StreamHandler()
      consoleHandler.setFormatter(logFormatter)
      _log.addHandler(consoleHandler)
      _log.setLevel(logging.DEBUG)
   _log.debug("in setBMEFormOnline")
   
   if blynk is None:
      blynk = blynklib.Blynk(parser.get('droneAir', 'BLYNK_AUTH'))
   
   blynk.run()
   blynk.set_property(1, 'color', colours['ONLINE'])
   blynk.set_property(2, 'color', colours['ONLINE'])
   blynk.set_property(3, 'color', colours['ONLINE'])
   blynk.set_property(4, 'color', colours['ONLINE'])
   blynk.set_property(5, 'color', colours['ONLINE'])
   blynk.set_property(11, 'color', colours['ONLINE'])


def setBMEFormOffline(*args, **kwargs):
   blynk = kwargs.get('blynkObj', None)
   _log = kwargs.get('loggerObj', None)
   if _log is None:
      _log = logging.getLogger('BlynkLog')
      logFormatter = logging.Formatter("%(asctime)s [%(levelname)s]  %(message)s")
      consoleHandler = logging.StreamHandler()
      consoleHandler.setFormatter(logFormatter)
      _log.addHandler(consoleHandler)
      _log.setLevel(logging.DEBUG)
   _log.debug("in setBMEFormOffline")
   
   if blynk is None:
      blynk = blynklib.Blynk(parser.get('droneAir', 'BLYNK_AUTH'))
   blynk.run()
   blynk.set_property(1, 'color', colours['OFFLINE'])
   blynk.set_property(2, 'color', colours['OFFLINE'])
   blynk.set_property(3, 'color', colours['OFFLINE'])
   blynk.set_property(4, 'color', colours['OFFLINE'])
   blynk.set_property(5, 'color', colours['OFFLINE'])
   blynk.set_property(11, 'color', colours['OFFLINE'])

   

def setTSLFormOnline(*args, **kwargs):
   blynk = kwargs.get('blynkObj', None)
   _log = kwargs.get('loggerObj', None)
   if _log is None:
      _log = logging.getLogger('BlynkLog')
      logFormatter = logging.Formatter("%(asctime)s [%(levelname)s]  %(message)s")
      consoleHandler = logging.StreamHandler()
      consoleHandler.setFormatter(logFormatter)
      _log.addHandler(consoleHandler)
      _log.setLevel(logging.DEBUG)
   _log.debug("in setTSLFormOnline")
   
   if blynk is None:
      blynk = blynklib.Blynk(parser.get('droneAir', 'BLYNK_AUTH'))
   
   blynk.run()
   blynk.set_property(6, 'color', colours['ONLINE'])
   blynk.set_property(7, 'color', colours['ONLINE'])
   blynk.set_property(8, 'color', colours['ONLINE'])
   blynk.set_property(9, 'color', colours['ONLINE'])


def setTSLFormOffline(*args, **kwargs):
   blynk = kwargs.get('blynkObj', None)
   _log = kwargs.get('loggerObj', None)
   if _log is None:
      _log = logging.getLogger('BlynkLog')
      logFormatter = logging.Formatter("%(asctime)s [%(levelname)s]  %(message)s")
      consoleHandler = logging.StreamHandler()
      consoleHandler.setFormatter(logFormatter)
      _log.addHandler(consoleHandler)
      _log.setLevel(logging.DEBUG)
   _log.debug("in setTSLFormOffline")
   
   if blynk is None:
      blynk = blynklib.Blynk(parser.get('droneAir', 'BLYNK_AUTH'))
   blynk.run()
   blynk.set_property(6, 'color', colours['OFFLINE'])
   blynk.set_property(7, 'color', colours['OFFLINE'])
   blynk.set_property(8, 'color', colours['OFFLINE'])
   blynk.set_property(9, 'color', colours['OFFLINE'])
   
   
   
   
def setMHZFormOnline(*args, **kwargs):
   blynk = kwargs.get('blynkObj', None)
   _log = kwargs.get('loggerObj', None)
   if _log is None:
      _log = logging.getLogger('BlynkLog')
      logFormatter = logging.Formatter("%(asctime)s [%(levelname)s]  %(message)s")
      consoleHandler = logging.StreamHandler()
      consoleHandler.setFormatter(logFormatter)
      _log.addHandler(consoleHandler)
      _log.setLevel(logging.DEBUG)
   _log.debug("in setMHZFormOnline")
   
   if blynk is None:
      blynk = blynklib.Blynk(parser.get('droneAir', 'BLYNK_AUTH'))
   
   blynk.run()
   blynk.set_property(10, 'color', colours['ONLINE'])

def setMHZFormOffline(*args, **kwargs):
   blynk = kwargs.get('blynkObj', None)
   _log = kwargs.get('loggerObj', None)
   if _log is None:
      _log = logging.getLogger('BlynkLog')
      logFormatter = logging.Formatter("%(asctime)s [%(levelname)s]  %(message)s")
      consoleHandler = logging.StreamHandler()
      consoleHandler.setFormatter(logFormatter)
      _log.addHandler(consoleHandler)
      _log.setLevel(logging.DEBUG)
   _log.debug("in setMHZFormOffline")
   
   if blynk is None:
      blynk = blynklib.Blynk(parser.get('droneAir', 'BLYNK_AUTH'))
   blynk.run()
   blynk.set_property(10, 'color', colours['OFFLINE'])

