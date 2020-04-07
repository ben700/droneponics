##!/usr/bin/env python3 
BLYNK_AUTH = '4IfX_hzDREonPi_PIDQrETikxc0-XpqI' #i2cLogger
BLYNK_AUTH_RELAY = 'iipK7r0pSz68i8ZDo4sVdtkhbCzXM_ns' #i2cLogger


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
    
    import subprocess
    import re

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

    
    
    
    # Initialize Blynk
    blynk = blynklib.Blynk(BLYNK_AUTH)
    blynkRelay = blynklib.Blynk(BLYNK_AUTH_RELAY)
    timer = blynktimer.Timer()
    blynk.run()
    blynkRelay.run()
    blynk.virtual_write(98, "clr")
    
    
    # Initialize the sensor.
    try:
       # Create the I2C bus
       blynk.virtual_write(98, "Try to I2C" + '\n') 
       i2c = busio.I2C(board.SCL, board.SDA)
       blynk.virtual_write(98, "I2C created" + '\n') 
    except:
        i2c = None
        ss1 = None
        ss2 = None
        ss3 = None
        ss4 = None
        blynk.virtual_write(98, "Unexpected error: I2C" + '\n') 
        _log.info("Unexpected error: I2C")
    else:
        try:
            blynk.virtual_write(98, "Try to create soil sonsors" + '\n') 
            ss1 = Seesaw(i2c, addr=0x36)
            ss2 = Seesaw(i2c, addr=0x37)
            ss3 = Seesaw(i2c, addr=0x38)
            ss4 = Seesaw(i2c, addr=0x38)
            blynk.virtual_write(98, "Created soil sonsors" + '\n') 
            
        except:
            ss1 = None
            ss2 = None
            ss3 = None
            ss4 = None
            blynk.virtual_write(98, "Expected error: No soil sonsors" + '\n') 
        try:
            blynk.virtual_write(98, "Try to create ADC" + '\n') 
            ads = ADS.ADS1015(i2c) 
            chan = AnalogIn(ads, ADS.P0)
            blynk.virtual_write(98, "Created ADC" + '\n')     
        except:
            blynk.virtual_write(98, "Expected error: No Water Level Sensor" + '\n') 
            
    
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
        blynk.set_property(10, 'color', colours['OFFLINE'])
        blynk.set_property(9, 'color', colours['OFFLINE'])   
        os.system('sh /home/pi/updateDroneponics.sh')
        blynk.virtual_write(98, "System updated and restarting " + '\n')
        os.system('sudo reboot')


    @timer.register(interval=10, run_once=False)
    def blynk_data():
        _log.info("Update Timer Run")
        #blynk.virtual_write(98, "Starting Timer Function" + '\n') 
        Counter.cycle += 1
        now = datetime.now()
        blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))    
        
        bES = GPIO.input(buttEmptySensor)
        bFS = GPIO.input(buttFullSensor)
        blynk.virtual_write(38, bES)
        blynkRelay.virtual_write(38, bES)
        blynkRelay.virtual_write(98, "I2C logger updated 38 to be " + str(bES) + '\n')
        blynk.virtual_write(37, bFS)
        blynk.virtual_write(39, bES+bFS)
      #  if(bES == 0):
      #       blynk.notify("Water Butt is Empty")
        blynk.set_property(10, 'color', colours[bES])
        blynk.set_property(9, 'color', colours[bFS])
        
        
        #blynk.virtual_write(98, "Completed Timer Function" + '\n') 

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
   blynk.set_property(10, 'color', colours['OFFLINE'])
   blynk.set_property(9, 'color', colours['OFFLINE'])    
   GPIO.cleanup()
