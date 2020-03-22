##!/usr/bin/env python3 
BLYNK_AUTH = '4IfX_hzDREonPi_PIDQrETikxc0-XpqI' #i2cLogger

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

    class Counter:
        cycle = 0

    bootup = True
    colours = {1: '#00FF00', 0: '#FF0000', 'OFFLINE': '#0000FF'}


    # tune console logging
    _log = logging.getLogger('BlynkLog')
    logFormatter = logging.Formatter("%(asctime)s [%(levelname)s]  %(message)s")
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    _log.addHandler(consoleHandler)
    _log.setLevel(logging.DEBUG)
    
    buttFullSensor =  14
    buttEmptySensor = 15
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(buttFullSensor, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(buttEmptySensor, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    _log.info(GPIO.input(buttEmptySensor))
    _log.info(GPIO.input(buttFullSensor))


    
    # Initialize Blynk
    blynk = blynklib.Blynk(BLYNK_AUTH)
    blynkTemp = blynklib.Blynk('ZDy8p4aFPCKGwQhafv4jwUT6TpCY9CyP')
        
    timer = blynktimer.Timer()
    #blynk.run()
    APP_CONNECT_PRINT_MSG = '[APP_CONNECT_EVENT]'
    APP_DISCONNECT_PRINT_MSG = '[APP_DISCONNECT_EVENT]'
    CONNECT_PRINT_MSG = '[CONNECT_EVENT]'
    DISCONNECT_PRINT_MSG = '[DISCONNECT_EVENT]'
    WRITE_EVENT_PRINT_MSG = "[WRITE_VIRTUAL_PIN_EVENT] Pin: V{} Value: '{}'"
    READ_PRINT_MSG = "[READ_VIRTUAL_PIN_EVENT] Pin: V{}"
    ALLOWED_COMMANDS_LIST = ['ls', 'lsusb', 'ip a', 'ip abc']
    TWEET_MSG = "New value='{}' on VPIN({})"

    @blynkTemp.handle_event('read V1')
    def readV1(value):
       _log.info("in read v1")
       _log.info(value)
        
    @blynk.handle_event('write V255')
    def rebooter(pin, value):
        blynk.virtual_write(98, "User Reboot " + '\n')
        blynk.set_property(10, 'color', colours['OFFLINE'])
        blynk.set_property(9, 'color', colours['OFFLINE'])   
        os.system('sh /home/pi/updateDroneponics.sh')
        blynk.virtual_write(98, "System updated and restarting " + '\n')
        os.system('sudo reboot')

        
    

    @timer.register(interval=10, run_once=False)
    def blynk_data():
        _log.info("Update Timer Run")
        blynk.virtual_write(98, "Starting Timer Function" + '\n') 
        Counter.cycle += 1
        now = datetime.now()
        blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))    
        
        blynk.virtual_write(37, GPIO.input(buttEmptySensor))
        blynk.virtual_write(38, GPIO.input(buttFullSensor))
        
        blynk.set_property(10, 'color', colours[GPIO.input(buttFullSensor)])
        blynk.set_property(9, 'color', colours[GPIO.input(buttEmptySensor)])
        blynk.virtual_write(98, "Completed Timer Function" + '\n') 
        
        blynkTemp.virtual_sync('V1')

    while True:
        try:
           blynk.run()
           if bootup :
              bootup = False
              now = datetime.now()
              blynk.virtual_write(99, now.strftime("%d/%m/%Y %H:%M:%S"))
              blynk.virtual_write(10,255)
              blynk.virtual_write(9,255)
              #blynk.virtual_write(98, "clr")
              blynk.virtual_write(98, "System now updated and restarted " + '\n')
              blynk.virtual_write(255, 0)
              _log.info('Just Booted')

           timer.run()
        except:
           _log.info('Unexpected error')
           blynk.virtual_write(98, "System has main loop error" + '\n')
           blynk.set_property(10, 'color', colours['OFFLINE'])
           blynk.set_property(9, 'color', colours['OFFLINE']) 
           os.system('sh /home/pi/updateDroneponics.sh')
           os.system('sudo reboot') 
except:
   _log.info('Unexpected error')
   blynkErr = blynklib.Blynk(BLYNK_AUTH)
   blynkErr.set_property(10, 'color', colours['OFFLINE'])
   blynkErr.set_property(9, 'color', colours['OFFLINE'])   
   blynkErr.virtual_write(98, "System has error" + '\n')
   os.system('sh /home/pi/updateDroneponics.sh')
   os.system('sudo reboot')
finally:
   GPIO.cleanup()
