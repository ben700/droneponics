##!/usr/bin/env python3 
BLYNK_AUTH = 'e06jzpI2zuRD4KB5eHyHdCQTGFT7einR' #i2cLogger
BLYNK_AUTH_DATA = 'XVbhfI6ZYxkqFp7d4RsCIN6Is9YnKp9q' #i2cLogger
LED = [10,11,12,13,14,15]
VolumePin = [0,21,22,23,24,25] 

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
    colours = {0: '#FF0000', 1: '#00FF00', '0': '#FF0000', '1': '#00FF00', 'OFFLINE': '#0000FF'}


    # tune console logging
    _log = logging.getLogger('BlynkLog')
    logFormatter = logging.Formatter("%(asctime)s [%(levelname)s]  %(message)s")
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    _log.addHandler(consoleHandler)
    _log.setLevel(logging.DEBUG)

    nutrientMix = []
    nutrientMix = drone.buildNutrientMix(nutrientMix, _log)
	
    
    # Initialize Blynk
    blynk = blynklib.Blynk(BLYNK_AUTH)        
    timer = blynktimer.Timer()
    blynk.run()
    blynk.virtual_write(98, "clr")
    
    
    # Initialize the sensor.
    try:
       # Create the I2C bus
       for dosage in nutrientMix:
           dosage.pump = AtlasI2C(dosage.pumpId)
           blynk.set_property(dosage.LED, 'color', colours[1])
       blynk.virtual_write(98, "pump created" + '\n') 
       _log.info("pump created")
    except:

        blynk.virtual_write(98, "Unexpected error: atlas" + '\n') 
        _log.info("Unexpected error: Atlas")
    else:
        blynk.set_property(LED[0], 'color', colours[1])    
        try:	
            _log.info("Try Use Pump")
            for dosage in nutrientMix:
                if(dosage.pump is not None):
                   dosage.volume = dosage.pump.query("TV,?").split("TV,")[1]
                   blynk.virtual_write(dosage.volumePin, dosage.volume )
                   _log.info( "Pump id " + str(dosage.pumpId) + " has dosed = " + str(dosage.volume) + '\n')
          
        except:
            _log.info("Expected error: Use Atlas Error")
            blynk.virtual_write(98, "Expected error: Atlas Error" + '\n') 
            
            
    APP_CONNECT_PRINT_MSG = '[APP_CONNECT_EVENT]'
    APP_DISCONNECT_PRINT_MSG = '[APP_DISCONNECT_EVENT]'
    CONNECT_PRINT_MSG = '[CONNECT_EVENT]'
    DISCONNECT_PRINT_MSG = '[DISCONNECT_EVENT]'
    WRITE_EVENT_PRINT_MSG = "[WRITE_VIRTUAL_PIN_EVENT] Pin: V{} Value: '{}'"
    READ_PRINT_MSG = "[READ_VIRTUAL_PIN_EVENT] Pin: V{}"
    ALLOWED_COMMANDS_LIST = ['ls', 'lsusb', 'ip a', 'ip abc']
    TWEET_MSG = "New value='{}' on VPIN({})"
        
    @blynk.handle_event('write V255')
    def rebooter(pin, value):
        blynk.virtual_write(98, "User Reboot " + '\n')
        for l in LED:
            blynk.set_property(l, 'color', colours['OFFLINE'])
        os.system('sh /home/pi/updateDroneponics.sh')
        blynk.virtual_write(98, "System updated and restarting " + '\n')
        os.system('sudo reboot')

    @blynk.handle_event('write V1')
    def buttonV1Pressed(pin, value):
        blynk.set_property(10, 'color', colours[0]) 
        for dosage in nutrientMix:
           if(dosage.pump is not None):
                   blynk.set_property(dosage.LED, 'color', colours[0])
                   dosage.pump.query("D,"+str(dosage.dose))
                   while (True):
                        dosed = dosage.pump.query("R").split(":")[1].strip().rstrip('\x00')
                        _log.info( "Pump id " + str(dosage.pumpId) + " has dosed = " + str(dosed) + "ml of 10ml")
                        _log.info(str(dosed))
                        _log.info('{:.2f}'.format(dosage.dose))
                        if (str(dosed) == '{:.2f}'.format(dosage.dose)):
                            break	
                   blynk.set_property(dosage.LED, 'color', colours[1])
                   dosage.volume = dosage.pump.query("TV,?").split("TV,")[1]
                   blynk.virtual_write(dosage.volumePin, dosage.volume )
           else:
                   blynk.set_property(dosage.LED, 'color', colours['OFFLINE'])	
        blynk.run()
        blynk.set_property(10, 'color', colours[1])
        _log.info("Completed")
        now = datetime.now()
        blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))    
        blynk.virtual_write(98, now.strftime("%d/%m/%Y %H:%M:%S") + " :- Dosed Complete" + '\n') 
        
           
        
    @blynk.handle_event('write V31')
    def fillLinePump1(pin, value):
        x=0
        _log.info( "Fill Line 1 " + str(value[0]) + '\n')
        now = datetime.now()
        blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))    
        
        blynk.set_property(nutrientMix[x].LED, 'color', colours[value[0]])
        if(value[0] == '1'):
            _log.info("Pump for " +nutrientMix[x].name +" = " + nutrientMix[x].pump.query("X") + '\n')
            blynk.virtual_write(98, now.strftime("%d/%m/%Y %H:%M:%S") + " :- Pump for " + nutrientMix[x].name + ":- STOPPED" + '\n') 
        else:
            blynk.virtual_write(98, now.strftime("%d/%m/%Y %H:%M:%S") + " :- Pump for " + nutrientMix[x].name + ":- STARTED" + '\n') 
            _log.info("Pump Device v!=1 = " + nutrientMix[x].pump.query("D,*") + '\n') 
        
        lVolume= nutrientMix[x].volume
        nutrientMix[x].volume = nutrientMix[x].pump.query("TV,?").split("TV,")[1]
        blynk.virtual_write(nutrientMix[x].volumePin, nutrientMix[x].volume )
        dosed = nutrientMix[x].pump.query("R").split(":")[1].strip().rstrip('\x00')
        _log.info( "Pump id " + str(dosage.pumpId) + " has dosed = " + str(dosed) + "Before was :-" + str(lVolume))
	
                        
    @timer.register(interval=10, run_once=False)
    def blynk_data():
        _log.info("Update Timer Run")
        blynk.virtual_write(98, "Starting Timer Function" + '\n') 
        Counter.cycle += 1
        now = datetime.now()
        blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))    
        
        blynk.virtual_write(98, "Completed Timer Function" + '\n') 

    while True:
        try:
           blynk.run()
   
           if bootup :
              p = subprocess.Popen(['i2cdetect', '-y','1'],stdout=subprocess.PIPE,)
              #cmdout = str(p.communicate())
              for i in range(0,9):
                   blynk.virtual_write(98, str(p.stdout.readline()) + '\n')
              bootup = False
              now = datetime.now()
              blynk.virtual_write(99, now.strftime("%d/%m/%Y %H:%M:%S"))
              for l in LED:
                  blynk.virtual_write(l, 255)
              #blynk.virtual_write(98, "clr")
              blynk.virtual_write(98, "System now updated and restarted " + '\n')
              blynk.virtual_write(255, 0)
              _log.info('Just Booted')
           #timer.run()
        except:
           _log.info('Unexpected error')
           blynk.virtual_write(98, "System has main loop error" + '\n')
           for l in LED:
                blynk.set_property(l, 'color', colours['OFFLINE'])
           os.system('sh /home/pi/updateDroneponics.sh')
           os.system('sudo reboot') 
  
  
except:
   _log.info('Unexpected error')
   blynkErr = blynklib.Blynk(BLYNK_AUTH)
   for l in LED:
        blynkErr.set_property(l, 'color', colours['OFFLINE'])
   blynkErr.virtual_write(98, "System has error" + '\n')
   os.system('sh /home/pi/updateDroneponics.sh')
   os.system('sudo reboot')
finally:
   blynk = blynklib.Blynk(BLYNK_AUTH)        
   blynk.run() 
   for l in LED:
        blynk.set_property(l, 'color', colours['OFFLINE'])
   GPIO.cleanup()
