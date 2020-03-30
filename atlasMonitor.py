#!/usr/bin/python
# The ID and range of a sample spreadsheet.
BLYNK_AUTH = 'SHraFqInf27JKowTcFZapu0rHH2QGtuO' #atlasMonitor

try:
    import logging
    import blynklib
    import blynktimer
    from datetime import datetime
    import io
    import sys
    import fcntl
    import time
    import copy
    import string
    from AtlasI2C import (
         AtlasI2C
    )
    import RPi.GPIO as GPIO
    import os
    import logging
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
    APP_CONNECT_PRINT_MSG = '[APP_CONNECT_EVENT]'
    APP_DISCONNECT_PRINT_MSG = '[APP_DISCONNECT_EVENT]'
    CONNECT_PRINT_MSG = '[CONNECT_EVENT]'
    DISCONNECT_PRINT_MSG = '[DISCONNECT_EVENT]'
    WRITE_EVENT_PRINT_MSG = "[WRITE_VIRTUAL_PIN_EVENT] Pin: V{} Value: '{}'"
    READ_PRINT_MSG = "[READ_VIRTUAL_PIN_EVENT] Pin: V{}"
    ALLOWED_COMMANDS_LIST = ['ls', 'lsusb', 'ip a', 'ip abc']
    TWEET_MSG = "New value='{}' on VPIN({})"


    device = AtlasI2C()
    temp = AtlasI2C(102)
    ec = AtlasI2C(100)
    ph = AtlasI2C(99)

    blynk.virtual_write(98,"Temp Device Info = " + temp.query("i") + '\n')
    blynk.virtual_write(98,"pH Device Info = " + ph.query("i") + '\n')
    blynk.virtual_write(98,"EC Device Info = " + ec.query("i") + '\n')
    
    blynk.virtual_write(98,"Temp Cal = " + temp.query("Cal,?") + '\n')
    blynk.virtual_write(98,"Temp Scale = " + temp.query("S,?") + '\n')

    blynk.virtual_write(98,"pH Cal = " + ph.query("Cal,?") + '\n')
    blynk.virtual_write(98,"pH Temp Cal = " + ph.query("T,?") + '\n')

    blynk.virtual_write(98,"EC Cal = " + ec.query("Cal,?") + '\n')
    blynk.virtual_write(98,"EC Temp Cal = " + ec.query("Cal,?") + '\n')
    blynk.virtual_write(98,"EC Probe Type = " + ec.query("K,?") + '\n')

    

    @blynk.handle_event("connect")
    def connect_handler():
        _log.info('SCRIPT_START')
     #   for pin in range(5):
     #       _log.info('Syncing virtual pin {}'.format(pin))
     #       blynk.virtual_sync(pin)

            # within connect handler after each server send operation forced socket reading is required cause:
            #  - we are not in script listening state yet
            #  - without forced reading some portion of blynk server messages can be not delivered to HW
     #       blynk.read_response(timeout=0.5)


    @blynk.handle_event('write V255')
    def rebooter(pin, value):
        blynk.virtual_write(98, "User Reboot " + '\n')
        os.system('sh /home/pi/updateDroneponics.sh')
        blynk.virtual_write(98, "System updated and restarting " + '\n')
        os.system('sudo reboot')



    # Will Print Every 10 Seconds
    @timer.register(interval=10, run_once=False)
    def blynk_data():
        _log.info("Start of blynk_data")
        now = datetime.now()
        blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))

        cTemp = temp.query("R,").split(":")[1]
        _log.info("Temp = " + cTemp)
        blynk.virtual_write(30, cTemp)

        try:
           cPH = ph.query("RT,"+cTemp).split(":")[1]
           blynk.virtual_write(32, cPH)
           _log.info ("PH = " + cPH)
        except:
           blynk.virtual_write(98, "Read PH Error" + '\n') 
           _log.info("Read Ph Error")
        
        try:
            cEC = ec.query("RT,"+cTemp).split(":")[1]
        except:
            blynk.virtual_write(98, "Read EC Error" + '\n')
        else:
            blynk.virtual_write(31, cEC)
            _log.info ("EC  = " + cEC)


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
              blynk.virtual_write(98, "clr")
              blynk.virtual_write(98, "System now updated and restarted " + '\n')
              blynk.virtual_write(255, 0)
              _log.info('Just Booted')

           timer.run()
        except:
           _log.info('Unexpected error')
           os.system('sh /home/pi/updateDroneponics.sh')
except:
   _log.info('Unexpected error')
   blynkErr = blynklib.Blynk(BLYNK_AUTH)
   blynkErr.virtual_write(98, "System has error" + '\n')
   os.system('sh /home/pi/updateDroneponics.sh')
   os.system('sudo reboot')
finally:
   GPIO.cleanup()
