import logging
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
