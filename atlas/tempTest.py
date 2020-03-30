##!/usr/bin/env python3 
BLYNK_AUTH = 'SHraFqInf27JKowTcFZapu0rHH2QGtuO' #atlasMonitor

try:
    import datetime
    import time
    import shlex, requests
    import blynklib
    import blynktimer
    import logging
    from datetime import datetime
    import sys
    import os
   
    from AtlasI2C import (
	    AtlasI2C
    )
    
    import subprocess
    import re
    import drone

    class Counter:
        cycle = 0

    bootup = True
    colours = {1: '#FF0000', 0: '#00FF00', 'OFFLINE': '#0000FF'}


    # tune console logging
    _log = logging.getLogger('BlynkLog')
    logFormatter = logging.Formatter("%(asctime)s [%(levelname)s]  %(message)s")
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    _log.addHandler(consoleHandler)
    _log.setLevel(logging.DEBUG)

    nutrientMix = []
    nutrientMix = drone.buildNutrientMix(nutrientMix, _log)
	  
    # Initialize the sensor.
    try:
        temp = AtlasI2C(102)
        _log.info("sensor created")
    except:
        _log.info("Unexpected error: Atlas")
    else:
        try:	
             oTemp = -999
             cTemp = temp.query("R,").split(":")[1]
             while ( cTemp != oTemp):
                 oTemp = cTemp
                 sleep(1)
                 cTemp = temp.query("R,").split(":")[1]
                 _log.info("Waiting for temp to be stable. It's now :" + str(cTemp) + '\n')
                           
        except:
            _log.info("Expected error: Use Atlas Error")
            
  
except:
   print('Unexpected error')
