##!/usr/bin/env python3 

if True:
    import datetime
    import time
    import shlex, requests
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
    nutrientMix = drone.buildOxyMix(nutrientMix, _log)
	

    answer = input("Are you sure you want to calibrate (y/n)")
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
                   answer = input("Are you sure you want to calibrate pump " + dosage.name + "(y/n to skip)")
                   if answer is None or answer != 'y':
                        _log.info("User Exit")
                        continue
                   answer = input("Going to dose 10ml of " + dosage.name + ". Enter y when you are ready(y/n  to skip)")
                   if answer is None or answer != 'y':
                        _log.info("User Exit")
                        continue
                   dosage.pump.query("D,10")	
		
		
                   while (True):
                        dosed = dosage.pump.query("R").split(":")[1].strip().rstrip('\x00')
                        _log.info( "Pump id " + str(dosage.pumpId) + " has dosed = " + str(dosed) + "ml of 10ml")
                        if (str(dosed) == "10.00"):
                            break
                  		
		
		
                   aDose = input("How much in ml did pump dose?")
                   answer = input("Going to calibrate pump. It dosed [" + str(aDose) + "]. Enter y when you are ready(y/n to skip)")
                   if answer is None or answer != 'y':
                        _log.info("User Exit")
                        continue
                   dosage.pump.query("Cal,clear")	
                   dosage.pump.query("Cal,"+str(aDose))
		   
                   answer = input("Going to dose 10ml of " + dosage.name + " over 1 min. Enter y when you are ready(y/n to skip only done 1 part cal)")
                   if answer is None or answer != 'y':
                        _log.info("User Exit")
                        continue
                   dosage.pump.query("D,10,1")	
		
                   while (True):
                        dosed = dosage.pump.query("R").split(":")[1].strip().rstrip('\x00')
                        _log.info( "Pump id " + str(dosage.pumpId) + " has dosed = " + str(dosed) + "ml of 10ml in 1 min")
                        if (str(dosed) == "10.00"):
                            break		
		
                   aDose = input("How much in ml did pump dose?")
                   answer = input("Going to calibrate pump. It dosed [" + str(aDose) + "]. Enter y when you are ready(y/n to skip only done 1 part cal)")
                   if answer is None or answer != 'y':
                        _log.info("User Exit")
                        continue
                   dosage.pump.query("Cal,"+str(aDose))
		   	
	    
        except:
            _log.info("Expected error: Use Atlas Error")
            
  
