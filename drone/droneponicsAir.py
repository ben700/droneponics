import logging
from drone.droneObj import colours

def setFormOffline(blynkObj=None, Msg=None):
   _log = logging.getLogger('BlynkLog')
   logFormatter = logging.Formatter("%(asctime)s [%(levelname)s]  %(message)s")
   consoleHandler = logging.StreamHandler()
   consoleHandler.setFormatter(logFormatter)
   _log.addHandler(consoleHandler)
   _log.setLevel(logging.DEBUG)
   _log.info("in setFormOffline")
   
   if blynkObj is None:
      blynkObj = blynklib.Blynk(parser.get('droneAir', 'BLYNK_AUTH'))
   blynkObj.run()
   _log.info("Going to set Msg from setFormOffline")
   if Msg is not None:
       blynkObj.virtual_write(98, Msg + " " + '\n')
       _log.info(Msg)
   _log.info("Going to set from colour Offline from setFormOffline")
   for i in range(255): 
      blynkObj.set_property(i, 'color', colours['OFFLINE'])
   _log.info("Completed setFormOffline")
