import logging
import blynklib
from drone.droneObj import colours

def setFormOffline(blynkObj=None, Msg=None):
   logging.debug("in setFormOffline")
   if blynkObj is None:
      blynkObj = blynklib.Blynk(parser.get('droneAir', 'BLYNK_AUTH'))
   blynkObj.run()
   logging.debug("Going to set Msg from setFormOffline")
   if Msg is not None:
       blynkObj.virtual_write(98, Msg + " " + '\n')
       _log.info(Msg)
   logging.debug("Going to set from colour Offline from setFormOffline")
   for i in range(255): 
      blynkObj.set_property(i, 'color', colours['OFFLINE'])
   logging.debug("Completed setFormOffline")



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
   _log.debug("in setFormOnline")
   
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
   _log.debug("in setFormOffline")
   
   if blynk is None:
      blynk = blynklib.Blynk(parser.get('droneAir', 'BLYNK_AUTH'))
   blynk.run()
   blynk.set_property(1, 'color', colours['OFFLINE'])
   blynk.set_property(2, 'color', colours['OFFLINE'])
   blynk.set_property(3, 'color', colours['OFFLINE'])
   blynk.set_property(4, 'color', colours['OFFLINE'])
   blynk.set_property(5, 'color', colours['OFFLINE'])
   blynk.set_property(11, 'color', colours['OFFLINE'])
