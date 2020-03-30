##!/usr/bin/env python3 

if True:
    import datetime
    import time
    import logging
    from datetime import datetime
    import sys
    import os
    import RPi.GPIO as GPIO
    sys.path.append('/home/pi/droneponics')
    from AtlasI2C import (
	    AtlasI2C
    )
    import blynklib
    import blynktimer
    
    import subprocess
    import re
    import drone

    # tune console logging
    _log = logging.getLogger('BlynkLog')
    logFormatter = logging.Formatter("%(asctime)s [%(levelname)s]  %(message)s")
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    _log.addHandler(consoleHandler)
    _log.setLevel(logging.DEBUG)

    nutrientMix = []
    nutrientMix = drone.buildNutrientMix(nutrientMix, _log)

    answer = input("Are you sure you want to reset (y/n)")
    if answer is None or answer != 'y':
        _log.info("User Exit")
        quit()
  
    # Initialize the sensor.
    try:
       # Create the I2C bus
       for dosage in nutrientMix:
           dosage.pump = AtlasI2C(dosage.pumpId)
       _log.info("pump created")
    except:
        _log.info("Unexpected error: Atlas")
    else:
        try:	
            _log.info("Try Use Pump")
            for dosage in nutrientMix:
                if(dosage.pump is not None):
                   answer = input("Are you sure you want to reset pump " + dosage.name + "(y/n)")
                   if answer is None or answer != 'y':
                        _log.info("User Skiped resetting this pump")
                        continue
                   else:
                        dosage.pump.query("Facory")	
		
	    
        except:
            _log.info("Expected error: Use Atlas Error")
            

