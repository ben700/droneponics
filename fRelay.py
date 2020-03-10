from board import SCL, SDA
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


bootup = True 

# tune console logging
_log = logging.getLogger('BlynkLog')
logFormatter = logging.Formatter("%(asctime)s [%(levelname)s]  %(message)s")
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
_log.addHandler(consoleHandler)
_log.setLevel(logging.DEBUG)

BLYNK_GREEN     ="#23C48E"
BLYNK_BLUE      ="#04C0F8"
BLYNK_YELLOW    ="#ED9D00"
BLYNK_RED       ="#D3435C"
BLYNK_DARK_BLUE ="#5F7CD8"

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#e06jzpI2zuRD4KB5eHyHdCQTGFT7einR #dfRobotControl
BLYNK_AUTH = 'rHuhXZ97FK3_azBlFK1AC4pIPNUxgw7B' #envControl
#BLYNK_AUTH = 'SHraFqInf27JKowTcFZapu0rHH2QGtuO' #atlasReservoir
#BLYNK_AUTH = 'XVbhfI6ZYxkqFp7d4RsCIN6Is9YnKp9q' #atlasButt

Relay1 = 26 #waste
Relay2 = 19 #Feed
Relay3 = 13 #Air
Relay4 = 6  #Mixer - turned off with low water 


GPIO.setup(Relay1,GPIO.OUT)
GPIO.setup(Relay2,GPIO.OUT)
GPIO.setup(Relay3,GPIO.OUT)
GPIO.setup(Relay4,GPIO.OUT)


#i2c_bus = busio.I2C(SCL, SDA)

#ss1 = Seesaw(i2c_bus, addr=0x36)
#ss2 = Seesaw(i2c_bus, addr=0x37)
#ss3 = Seesaw(i2c_bus, addr=0x38)
#ss4 = Seesaw(i2c_bus, addr=0x38)

# Initialize Blynk
blynk = blynklib.Blynk(BLYNK_AUTH)
timer = blynktimer.Timer()


APP_CONNECT_PRINT_MSG = '[APP_CONNECT_EVENT]'
APP_DISCONNECT_PRINT_MSG = '[APP_DISCONNECT_EVENT]'
CONNECT_PRINT_MSG = '[CONNECT_EVENT]'
DISCONNECT_PRINT_MSG = '[DISCONNECT_EVENT]'
WRITE_EVENT_PRINT_MSG = "[WRITE_VIRTUAL_PIN_EVENT] Pin: V{} Value: '{}'"
READ_PRINT_MSG = "[READ_VIRTUAL_PIN_EVENT] Pin: V{}"
ALLOWED_COMMANDS_LIST = ['ls', 'lsusb', 'ip a', 'ip abc']
TWEET_MSG = "New value='{}' on VPIN({})"

  
@blynk.handle_event('write V1')
def buttonV1Pressed(pin, value):
    _log.info(WRITE_EVENT_PRINT_MSG.format(pin, value))
    blynk.virtual_write(1, str(value[0]))
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
    if(value[0] == '1'):
        print("Air and Mixer turned off")
        GPIO.output(Relay3,GPIO.HIGH)
    else:
        print("Air and Mixer turned on")
        GPIO.output(Relay3,GPIO.LOW)


@blynk.handle_event('write V4')
def buttonV4Pressed(pin, value):
    _log.info(WRITE_EVENT_PRINT_MSG.format(pin, value))
    blynk.virtual_write(4, str(value[0]))
    if(value[0] == '1'):
        print("Pump/UV turned off")
        GPIO.output(Relay4,GPIO.HIGH)
    else:
        print("Pump/UV turned on")
        GPIO.output(Relay4,GPIO.LOW)



    
    
@blynk.handle_event('write V255')
def rebooter(pin, value):
    _log.info(WRITE_EVENT_PRINT_MSG.format(pin, value))

    
    
  
@timer.register(interval=30, run_once=False)
def blynk_data():
    _log.info("Update Timer Run")
    now = datetime.now()
    blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))
    _log.info("Time updated : " + now.strftime("%d/%m/%Y %H:%M:%S"))
   
   # if (ss1 is not None):
   #     blynk.virtual_write(11, str(ss1.moisture_read()))
   #     blynk.virtual_write(12, str(ss1.get_temp()))
   #     _log.info ("Channel 1 moisture reading is "+str(ss1.moisture_read())+" and Temp is :" +  str("{0:.2f}".format(ss1.get_temp())))
   # if (ss2 is not None):    
   #    blynk.virtual_write(13, str(ss2.moisture_read()))
   #    blynk.virtual_write(14, str(ss2.get_temp()))
   #    _log.info ("Channel 2 moisture reading is "+str(ss2.moisture_read())+" and Temp is :" +  str("{0:.2f}".format(ss2.get_temp())))
   # if (ss3 is not None):    
   #    blynk.virtual_write(15, str(ss3.moisture_read()))          
   #    blynk.virtual_write(16, str(ss3.get_temp()))
   #    _log.info ("Channel 3 moisture reading is "+str(ss3.moisture_read())+" and Temp is :" +  str("{0:.2f}".format(ss3.get_temp())))
   # if (ss4 is not None):    
   #    blynk.virtual_write(17, str(ss4.moisture_read()))
   #    blynk.virtual_write(18, str(ss4.get_temp()))
   #    _log.info ("Channel 4 moisture reading is "+str(ss4.moisture_read())+" and Temp is :" +  str("{0:.2f}".format(ss4.get_temp())))
 

        
while True:
    try:
       blynk.run()
       if bootup :
          bootup = False
          now = datetime.now()
          blynk.virtual_write(99, now.strftime("%d/%m/%Y %H:%M:%S"))
          _log.info('Just Booted')
          
       timer.run()
    except:
       _log.info('Unexpected error')
       os.system('sh /home/pi/updateDroneponics.sh')
