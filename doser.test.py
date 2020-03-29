##!/usr/bin/env python3 
BLYNK_AUTH = 'e06jzpI2zuRD4KB5eHyHdCQTGFT7einR' #i2cLogger
BLYNK_AUTH_DATA = 'XVbhfI6ZYxkqFp7d4RsCIN6Is9YnKp9q' #i2cLogger

try:
    from python_tsl2591 import tsl2591
    import datetime
    import time
    import shlex, requests
    import board
    import busio
    import smbus 
    from ctypes import c_short
    from ctypes import c_byte
    from ctypes import c_ubyte
    import mh_z19
    import blynklib
    import blynktimer
    import logging
    from datetime import datetime
    import adafruit_tsl2591
    import sys
    import os
    import RPi.GPIO as GPIO

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


    LED = [10,11,12,13,14,15]
    VolumePin = [0,21,22,23,24,25]

    _log.info("build array") 
    nutrientMix = []
    nutrientMix = nutrientSchedule.buildNutrientMix(nutrientMix, _log)
    _log.info("Array built")

    answer = input("Are you sure you want to test (y/n)")
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
                   dosage.pump.query("D,10")	
                   while (True):
                        dosed = dosage.pump.query("R").split(":")[1].strip().rstrip('\x00')
                        _log.info( "Pump id " + str(dosage.pumpId) + " has dosed = " + str(dosed) + "ml of 10ml")
                        if (str(dosed) == "10.00"):
                            break
                  	
	    
        except:
            _log.info("Expected error: Use Atlas Error")
            
  
except:
   _log.info('Unexpected error')
