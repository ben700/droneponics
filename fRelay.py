#!/usr/bin/python3
# The ID and range of a sample spreadsheet.
BLYNK_AUTH = 'rHuhXZ97FK3_azBlFK1AC4pIPNUxgw7B' #envControl
BLYNK_AUTH_TEMP = 'FnSZls3WUdCbWmDJvfnjz3f83Sm70HqI' #envLogger2
colours = {1: '#FF0000', 0: '#00FF00', 'OFFLINE': '#0000FF'}

try:
    import board
    import busio
    from adafruit_seesaw.seesaw import Seesaw
    import time
    from datetime import datetime
    import RPi.GPIO as GPIO
    import time, sys
    import blynklib
    import blynktimer
    import logging
    import os
    import subprocess
    import re

    bootup = True
   
    # tune console logging
    _log = logging.getLogger('BlynkLog')
    logFormatter = logging.Formatter("%(asctime)s [%(levelname)s]  %(message)s")
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    _log.addHandler(consoleHandler)
    _log.setLevel(logging.DEBUG)

    
    # Initialize Blynk
    blynk = blynklib.Blynk(BLYNK_AUTH)
    blynkTemp = blynklib.Blynk(BLYNK_AUTH_TEMP)
    timer = blynktimer.Timer()
    blynk.run()

    BLYNK_GREEN     ="#23C48E"
    BLYNK_BLUE      ="#04C0F8"
    BLYNK_YELLOW    ="#ED9D00"
    BLYNK_RED       ="#D3435C"
    BLYNK_DARK_BLUE ="#5F7CD8"

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    
    Relay1 = 26 #heater
    Relay2 = 19 #Feed
    Relay3 = 13 #Air
    Relay4 = 6  #Mixer - turned off with low water 


    GPIO.setup(Relay1,GPIO.OUT)
    GPIO.setup(Relay2,GPIO.OUT)
    GPIO.setup(Relay3,GPIO.OUT)
    GPIO.setup(Relay4,GPIO.OUT)



    
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




    APP_CONNECT_PRINT_MSG = '[APP_CONNECT_EVENT]'
    APP_DISCONNECT_PRINT_MSG = '[APP_DISCONNECT_EVENT]'
    CONNECT_PRINT_MSG = '[CONNECT_EVENT]'
    DISCONNECT_PRINT_MSG = '[DISCONNECT_EVENT]'
    WRITE_EVENT_PRINT_MSG = "[WRITE_VIRTUAL_PIN_EVENT] Pin: V{} Value: '{}'"
    READ_PRINT_MSG = "[READ_VIRTUAL_PIN_EVENT] Pin: V{}"
    ALLOWED_COMMANDS_LIST = ['ls', 'lsusb', 'ip a', 'ip abc']
    TWEET_MSG = "New value='{}' on VPIN({})"

    @blynkTemp.handle_event('write V1')
    def writeV1(pin, value):
       blynk.virtual_write(98, "Write "+'\n') 

    @blynkTemp.handle_event('read V1')
    def readV1(value):
       blynk.virtual_write(98, "Read"+'\n') 



    @blynk.handle_event('write V1')
    def buttonV1Pressed(pin, value):
        _log.info(WRITE_EVENT_PRINT_MSG.format(pin, value))
        blynk.virtual_write(1, str(value[0]))
        blynk.set_property(5, 'color', colours[value[0]])
        if(value[0] == '1'):
            print("Waste turned off")
            GPIO.output(Relay1,GPIO.HIGH)
        else:
            print("Waste turned on")
            GPIO.output(Relay1,GPIO.LOW)




    @blynk.handle_event('write V2')
    def buttonV2Pressed(pin, value):
        _log.info(WRITE_EVENT_PRINT_MSG.format(pin, value))
        blynk.virtual_write(2, str(value[0]))
        blynk.set_property(6, 'color', colours[value[0]])
        if(value[0] == '1'):
            print("Feed Pump turned off")
            GPIO.output(Relay2,GPIO.HIGH)
        else:
            print("Feed Pump turned on")
            GPIO.output(Relay2,GPIO.LOW)

    @blynk.handle_event('write V3')
    def buttonV3Pressed(pin, value):
        _log.info(WRITE_EVENT_PRINT_MSG.format(pin, value))
        blynk.virtual_write(3, str(value[0]))
        blynk.set_property(7, 'color', colours[value[0]])
        if(value[0] == '1'):
            print("Air and Mixer turned off")
            GPIO.output(Relay3,GPIO.HIGH)
        else:
            print("Air and Mixer turned on")
            GPIO.output(Relay3,GPIO.LOW)


    @blynk.handle_event('write V4')
    def buttonV4Pressed(pin, value):
        blynk.virtual_write(98, "User button 4 " + '\n')
        blynk.virtual_write(4, str(value[0]))
        blynk.set_property(8, 'color', colours[value[0]])
        if(value[0] == '1'):
            print("Pump/UV turned off")
            GPIO.output(Relay4,GPIO.HIGH)
        else:
            print("Pump/UV turned on")
            GPIO.output(Relay4,GPIO.LOW)



    @blynk.handle_event('write V255')
    def rebooter(pin, value):
        blynk.virtual_write(98, "User Reboot " + '\n')
        blynk.set_property(5, 'color', colours['OFFLINE'])
        blynk.set_property(6, 'color', colours['OFFLINE'])
        blynk.set_property(7, 'color', colours['OFFLINE'])
        blynk.set_property(8, 'color', colours['OFFLINE'])
        os.system('sh /home/pi/updateDroneponics.sh')
        blynk.virtual_write(98, "System updated and restarting " + '\n')
        os.system('sudo reboot')


    @blynk.handle_event('connect')
    def connect_handler():
        _log.info('SCRIPT_START')
        for pin in range(5):
            _log.info('Syncing virtual pin {}'.format(pin))
            blynk.virtual_sync(pin)

            # within connect handler after each server send operation forced socket reading is required cause:
            #  - we are not in script listening state yet
            #  - without forced reading some portion of blynk server messages can be not delivered to HW
            blynk.read_response(timeout=0.5)


    @timer.register(interval=30, run_once=False)
    def blynk_data():
        _log.info("Update Timer Run")
        now = datetime.now()
        blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))
        blynk.virtual_write(98,"Time updated : " + now.strftime("%d/%m/%Y %H:%M:%S") + '\n')

        if (ss1 is not None):
            blynk.virtual_write(11, str(ss1.moisture_read()))
            blynk.virtual_write(12, str(ss1.get_temp()))
            _log.info ("Channel 1 moisture reading is "+str(ss1.moisture_read())+" and Temp is :" +  str("{0:.2f}".format(ss1.get_temp())))
        if (ss2 is not None):    
           blynk.virtual_write(13, str(ss2.moisture_read()))
           blynk.virtual_write(14, str(ss2.get_temp()))
           _log.info ("Channel 2 moisture reading is "+str(ss2.moisture_read())+" and Temp is :" +  str("{0:.2f}".format(ss2.get_temp())))
        if (ss3 is not None):    
           blynk.virtual_write(15, str(ss3.moisture_read()))          
           blynk.virtual_write(16, str(ss3.get_temp()))
           _log.info ("Channel 3 moisture reading is "+str(ss3.moisture_read())+" and Temp is :" +  str("{0:.2f}".format(ss3.get_temp())))
        if (ss4 is not None):    
           blynk.virtual_write(17, str(ss4.moisture_read()))
           blynk.virtual_write(18, str(ss4.get_temp()))
           _log.info ("Channel 4 moisture reading is "+str(ss4.moisture_read())+" and Temp is :" +  str("{0:.2f}".format(ss4.get_temp())))

        blynk.virtual_write(98, "Timer Function:- virtual_sync" + '\n')
        blynkTemp.run()
        #blynkTemp.virtual_sync('V1')
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
             # blynk.virtual_write(98, "clr")
              blynk.virtual_write(98, "System now updated and restarted " + '\n')
              blynk.virtual_write(255, 0)
              _log.info('Just Booted')

           timer.run()
        except:
           _log.info('Unexpected error')
           blynk.virtual_write(98, "System has main loop error" + '\n')
           #blynk.set_property(5, 'color', colours['OFFLINE'])
           #blynk.set_property(6, 'color', colours['OFFLINE'])
           #blynk.set_property(7, 'color', colours['OFFLINE'])
           #blynk.set_property(8, 'color', colours['OFFLINE'])
           os.system('sh /home/pi/updateDroneponics.sh')
           blynk.virtual_write(98, "System updated and restarting " + '\n')
           os.system('sudo reboot') 
  
  
except:
   _log.info('Unexpected error')
   blynkErr = blynklib.Blynk(BLYNK_AUTH)
   blynkErr.set_property(5, 'color', colours['OFFLINE'])
   blynkErr.set_property(6, 'color', colours['OFFLINE'])
   blynkErr.set_property(7, 'color', colours['OFFLINE'])
   blynkErr.set_property(8, 'color', colours['OFFLINE'])
   blynkErr.virtual_write(98, "System has error" + '\n')
   os.system('sh /home/pi/updateDroneponics.sh')
   os.system('sudo reboot')
finally:
   blynk.set_property(5, 'color', colours['OFFLINE'])
   blynk.set_property(6, 'color', colours['OFFLINE'])
   blynk.set_property(7, 'color', colours['OFFLINE'])
   blynk.set_property(8, 'color', colours['OFFLINE'])
   GPIO.cleanup()
