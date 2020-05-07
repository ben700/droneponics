def setFormOffline(blynkObj=None, Msg=None):
   print("in setFormOffline")
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
