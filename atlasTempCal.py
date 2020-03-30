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
	

    answer = input("Are you sure you want to calibrate (y/n)")
    if answer is None or answer != 'y':
        _log.info("User Exit")
        quit()
  
    # Initialize the sensor.
    try:
        temp = AtlasI2C(102)
        ec = AtlasI2C(100)
        ph = AtlasI2C(99)

        _log.info("sensor created")
    except:
        _log.info("Unexpected error: Atlas")
    else:
        try:	
             oTemp = temp.query("R,").split(":")[1]
             answer = input("Are you sure you want to calibrate Temprature (y/n)")
             if answer == 'y':
                 aTemp = input("What Temprate is it?")
                 answer = input("Going to calibrate temprature. Sensor is now at [" + str(aTemp) + "]. Enter y when you are ready(y/n)")
                 if answer == 'y':
                      cTemp = temp.query("R,").split(":")[1]
                      while ( cTemp != oTemp):
                           oTemp = cTemp 
                           cTemp = temp.query("R,").split(":")[1]
                           _log.info("Waiting for temp to be stable. It's now :" + str(cTemp) + '\n')
                           
                      temp.query("Cal,clear")	
                      temp.query("S,c")
                      temp.query("Cal,"+str(aTemp))
                      _log.info("Temprature Calibrated")
		   
        except:
            _log.info("Expected error: Use Atlas Error")
            
  
except:
   print('Unexpected error')