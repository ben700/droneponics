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

    class Dose:
        def __init__(self, PumpId, Dose, Led, name, volumePin):
            self.pump = None
            self.pumpId = PumpId
            self.dose = Dose
            self.LED = Led
            self.name = name
            self.volumePin = volumePin	
            self.volume = 0	
    

    LED = [10,11,12,13,14,15]
    VolumePin = [0,21,22,23,24,25]

    nutrientMix = []
    nutrientMix.append( Dose(111, 6, LED[1], "Hydro Grow A", VolumePin[1])) 
    nutrientMix.append( Dose(112, 6, LED[2], "Hydro Grow B", VolumePin[2])) 
    #nutrientMix.append( Dose(113, 10, LED[3], "Root Stimulant", VolumePin[3]))
    #nutrientMix.append( Dose(114, 4, LED[4], "Enzyme", VolumePin[4]))
    #nutrientMix.append( Dose(115, 1, LED[5], "Hydro Silicon", VolumePin[5])) 

	

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
                   answer = input("Are you sure you want to calibrate pump " + dosage.name + "(y/n)")
                   if answer is None or answer != 'y':
                        _log.info("User Exit")
                        continue
                   answer = input("Going to dose 10ml of " + dosage.name + ". Enter y when you are ready(y/n)")
                   if answer is None or answer != 'y':
                        _log.info("User Exit")
                        continue
                   dosage.pump.query("D,10")	
                   aDose = input("How much in ml did pump dose?")
                   answer = input("Going to calibrate pump. It dosed [" + str(aDose) + "]. Enter y when you are ready(y/n)")
                   if answer is None or answer != 'y':
                        _log.info("User Exit")
                        continue
                   dosage.pump.query("Cal,clear")	
  		   dosage.pump.query("Cal,"+str(aDose))
		   
		   answer = input("Going to dose 10ml of " + dosage.name + " over 1 min. Enter y when you are ready(y/n)")
                   if answer is None or answer != 'y':
                        _log.info("User Exit")
                        continue
                   dosage.pump.query("D,10,1")	
                   aDose = input("How much in ml did pump dose?")
                   answer = input("Going to calibrate pump. It dosed [" + str(aDose) + "]. Enter y when you are ready(y/n)")
                   if answer is None or answer != 'y':
                        _log.info("User Exit")
                        continue
                   dosage.pump.query("Cal,"+str(aDose))
		   	
	    
        except:
            _log.info("Expected error: Use Atlas Error")
            
  
except:
   _log.info('Unexpected error')
