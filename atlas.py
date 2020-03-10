#!/usr/bin/python

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
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import os
import logging


bootup = True 

# tune console logging
_log = logging.getLogger('BlynkLog')
logFormatter = logging.Formatter("%(asctime)s [%(levelname)s]  %(message)s")
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
_log.addHandler(consoleHandler)
_log.setLevel(logging.DEBUG)

class Dose:
    def __init__(self, Pump, Dose, Led, name):
        self.pump = Pump
        self.dose = Dose
        self.LED = Led
        self.name = name


LOG_LEVEL = dosesLogging.INFO
LOG_FILE = "/home/pi/doseslog"
LOG_FORMAT = "%(asctime)s %(levelname)s %(message)s"
logging.basicConfig(filename=LOG_FILE, format=LOG_FORMAT, level=LOG_LEVEL)


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

BLYNK_GREEN     ="#23C48E"
BLYNK_BLUE      ="#04C0F8"
BLYNK_YELLOW    ="#ED9D00"
BLYNK_RED       ="#D3435C"
BLYNK_DARK_BLUE ="#5F7CD8"
colors = {'1': '#23C48E', '0': '#D3435C', 'OFFLINE': '#FF0000'}


buttFullSensor =  17
buttEmptySensor = 4

#pins for solenoid
solenoidIn = 0
solenoidOut = 0


Pump1 = 26
Pump2 = 19
Pump3 = 13
Pump4 = 11
Pump5 = 9
Pump6 = 10
Pump7 = 22
Pump8 = 27
Pump9 = 25
Pump10 = 24


#setup sensor 2
GPIO.setup(buttFullSensor, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(buttEmptySensor, GPIO.IN, GPIO.PUD_DOWN)

Relay1 = 21
Relay2 = 20
Relay3 = 16
Relay4 = 12

nutrientMix = []
nutrientMix.append( Dose(Pump1, 6, 40, "Hydro Grow A")) 
nutrientMix.append( Dose(Pump2, 6, 41, "Hydro Grow B")) 
nutrientMix.append( Dose(Pump3, 10, 42, "Root Stimulant"))
nutrientMix.append( Dose(Pump4, 4, 43, "Enzyme"))
nutrientMix.append( Dose(Pump5, 1, 44, "Hydro Silicon")) 
nutrientMix.append( Dose(Pump6, 1, 45, "Pure Clean"))


noisyThingsWhenButtEmpty = [Relay1, Relay2, Relay3]

Mixer = Relay1

GPIO.setup(Relay1,GPIO.OUT)
GPIO.setup(Relay2,GPIO.OUT)
GPIO.setup(Relay3,GPIO.OUT)
GPIO.setup(Relay4,GPIO.OUT)
#GPIO.output(Relay1,GPIO.LOW)
#GPIO.output(Relay2,GPIO.LOW)
#GPIO.output(Relay3,GPIO.LOW)
#GPIO.output(Relay4,GPIO.LOW)

GPIO.setup(solenoidIn,GPIO.OUT)
GPIO.setup(solenoidOut,GPIO.OUT)
GPIO.output(solenoidIn,GPIO.LOW)
GPIO.output(solenoidOut,GPIO.LOW)


GPIO.setup(Pump1,GPIO.OUT)
GPIO.setup(Pump2,GPIO.OUT)
GPIO.setup(Pump3,GPIO.OUT)
GPIO.setup(Pump4,GPIO.OUT)
GPIO.setup(Pump5,GPIO.OUT)
GPIO.setup(Pump6,GPIO.OUT)
GPIO.setup(Pump7,GPIO.OUT)
GPIO.setup(Pump8,GPIO.OUT)
GPIO.setup(Pump9,GPIO.OUT)
GPIO.setup(Pump10,GPIO.OUT)

GPIO.output(Pump1,GPIO.HIGH)
GPIO.output(Pump2,GPIO.HIGH)
GPIO.output(Pump3,GPIO.HIGH)
GPIO.output(Pump4,GPIO.HIGH)
GPIO.output(Pump5,GPIO.HIGH)
GPIO.output(Pump6,GPIO.HIGH)
GPIO.output(Pump7,GPIO.HIGH)
GPIO.output(Pump8,GPIO.HIGH)
GPIO.output(Pump9,GPIO.HIGH)
GPIO.output(Pump10,GPIO.HIGH)

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1015(i2c)

# Create single-ended input on channel 0
chan = AnalogIn(ads, ADS.P0)

# The ID and range of a sample spreadsheet.
BLYNK_AUTH = 'XVbhfI6ZYxkqFp7d4RsCIN6Is9YnKp9q' #atlasButt

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


#62 - OPR
#69 - co2
#70 - colour 112 (0x70)
#6A - pressure
device = AtlasI2C()
temp = AtlasI2C(102)
ec = AtlasI2C(100)
ph = AtlasI2C(99)
#do = AtlasI2C(97)
#flow = AtlasI2C(104)
#pump = AtlasI2C(103)
#colour = AtlasI2C(70)


_log.info("Temp Device Info = " + temp.query("i"))
_log.info("pH Device Info = " + ph.query("i"))
_log.info("EC Device Info = " + ec.query("i"))
#print("colour Device Info = " + colour.query("i"))    
#print("Temp Device Info = " + temp.query("i"))
#print("pH Device Info = " + ph.query("i"))
#print("EC Device Info = " + ec.query("i"))
#print("DO Device Info = " + do.query("i"))      
#print("Flow Device Info = " + flow.query("i"))      

      
_log.info("Temp Cal = " + temp.query("Cal,?"))
_log.info("Temp Scale = " + temp.query("S,?"))
      
_log.info("pH Cal = " + ph.query("Cal,?"))
_log.info("pH Temp Cal = " + ph.query("T,?"))

_log.info("EC Cal = " + ec.query("Cal,?"))
_log.info("EC Temp Cal = " + ec.query("Cal,?"))
_log.info("EC Probe Type = " + ec.query("K,?"))

#print("DO Cal = " + do.query("Cal,?"))     
#print("DO Temp Cal = " + do.query("Cal,?"))
#print("DO Salinity Cal = " + do.query("S,?"))
#print("DO Pressure Cal = " + do.query("P,?"))

#print("Flow Meter Type = " + flow.query("Set,?"))
#print("Flow number of K Values = " + flow.query("K,?"))  #returns the number of K values stored
#print("Flow K Values = " + flow.query("K,all"))  #query the programmed K-value(s)
#print("Flow Rate = " + flow.query("Frp,?"))
#print("Flow Rate Time Base = " + flow.query("Vp,?"))
#print("Flow Resistors = " + flow.query("P,?")) #pull-up or pull-down resistors
    
#print("Pump Cal = " + pump.query("Cal,?"))
#print("Pump Voltage Check = " + pump.query("PV,?"))
#print("Pump Dispense Status = " + pump.query("D,?"))
#print("Pump maximum possible flow rate = " + pump.query("DC,?")) # maximum flow rate is determined after calibration.
#print("Pump Pause Status = " + pump.query("P,?"))
#print("Pump total volume dispensed = " + pump.query("TV,?")) #shows total volume dispensed  
#print("Pump absolute value of the total volume dispensed  = " + pump.query("ATV,?")) #absolute value of the total volume dispensed 
    
      
      
cTemp = temp.query("R").split(":")[1]
_log.info("Temp = " + cTemp)
_log.info("EC = " + ec.query("RT,16.699"))
_log.info("PH = " + ph.query("RT"+cTemp))
#print("DO = " + d0.query("RT,"+cTemp))


@blynk.handle_event("connect")
def connect_handler():
    _log.info('SCRIPT_START')
    for pin in range(5):
        _log.info('Syncing virtual pin {}'.format(pin))
        blynk.virtual_sync(pin)

        # within connect handler after each server send operation forced socket reading is required cause:
        #  - we are not in script listening state yet
        #  - without forced reading some portion of blynk server messages can be not delivered to HW
        blynk.read_response(timeout=0.5)
    
  
@blynk.handle_event('write V1')
def buttonV1Pressed(pin, value):
    _log.info(WRITE_EVENT_PRINT_MSG.format(pin, value))
    blynk.virtual_write(1, str(value[0]))
    blynk.set_property(5, 'color', colors[value[0]])
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
    blynk.set_property(6, 'color', colors[value[0]])
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
    blynk.set_property(7, 'color', colors[value[0]])
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
    blynk.set_property(8, 'color', colors[value[0]])
    if(value[0] == '1'):
        print("Pump/UV turned off")
        GPIO.output(Relay4,GPIO.HIGH)
    else:
        print("Pump/UV turned on")
        GPIO.output(Relay4,GPIO.LOW)

    
    
@blynk.handle_event('write V255')
def rebooter(pin, value):
    _log.info(WRITE_EVENT_PRINT_MSG.format(pin, value))
    _log.info("User Reboot")
    os.system('sh /home/pi/updateDroneponics.sh')
    os.system('sudo reboot')
    

        
@blynk.handle_event('write 30')
def buttonV30Pressed(value):
    logging.info("Dose started at" + now.strftime("%d/%m/%Y %H:%M:%S"))
    print("Dose started at " + now.strftime("%d/%m/%Y %H:%M:%S"))
    for dose in nutrientMix: 
       blynk.virtual_write(dose.LED,255)
       blynk.set_property(dose.LED, 'color', BLYNK_GREEN)
       GPIO.output(dose.Pump,GPIO.LOW)
       time.sleep(dose.dose)
       GPIO.output(dose.pump,GPIO.HIGH)
       blynk.set_property(dose.LED, 'color', BLYNK_GREEN)
       logger.info("Dosing " + dose.name +" for " + dose.dose + " using pin " + dose.pump + " and led " + dose.LED) 
    
@blynk.handle_event('write 69')
def buttonV69Pressed(value):
    logging.info("Dose Line Fill at " + now.strftime("%d/%m/%Y %H:%M:%S"))
    print("Dose Line Stop Fill at " + now.strftime("%d/%m/%Y %H:%M:%S"))
    GPIO.output(Pump1,GPIO.LOW)
    GPIO.output(Pump2,GPIO.LOW)
    GPIO.output(Pump3,GPIO.LOW)
    GPIO.output(Pump4,GPIO.LOW)
    GPIO.output(Pump5,GPIO.LOW)
    GPIO.output(Pump6,GPIO.LOW)
    GPIO.output(Pump7,GPIO.LOW)
    GPIO.output(Pump8,GPIO.LOW)
    GPIO.output(Pump9,GPIO.LOW)
    GPIO.output(Pump10,GPIO.LOW)
       
@blynk.handle_event('write 70')
def buttonV70Pressed(value):
    logging.info("Dose Line Stop All at " + now.strftime("%d/%m/%Y %H:%M:%S"))
    print("Dose Line Stop All at " + now.strftime("%d/%m/%Y %H:%M:%S"))
    GPIO.output(Pump1,GPIO.HIGH)
    GPIO.output(Pump2,GPIO.HIGH)
    GPIO.output(Pump3,GPIO.HIGH)
    GPIO.output(Pump4,GPIO.HIGH)
    GPIO.output(Pump5,GPIO.HIGH)
    GPIO.output(Pump6,GPIO.HIGH)
    GPIO.output(Pump7,GPIO.HIGH)
    GPIO.output(Pump8,GPIO.HIGH)
    GPIO.output(Pump9,GPIO.HIGH)
    GPIO.output(Pump10,GPIO.HIGH)    


        
def turnOffNoisyThingsWhenButtEmpty(): 
   for Relay in noisyThingsWhenButtEmpty:
       if GPIO.input(Relay) != GPIO.HIGH : 
           GPIO.output(Relay,GPIO.HIGH)
      
def turnOnNoisyThingsWhenButtNotEmpty(): 
   for Relay in noisyThingsWhenButtEmpty:
       if GPIO.input(Relay) != GPIO.LOW : 
           GPIO.output(Relay,GPIO.LOW)
      
def DoseNutrients(): 
    _log.info("DoseNutrients")
    now = datetime.now()
    blynk.virtual_write(98, now.strftime("%d/%m/%Y %H:%M:%S"))
    print ("Going to dose butt time is now " + now.strftime("%d/%m/%Y %H:%M:%S"))
    for dose in nutrientMix:
        blynk.set_property(dose.LED, 'color', BLYNK_RED)
        blynk.log_event(dose.name, dose.dose)
        GPIO.output(dose.pump,GPIO.LOW)
        time.sleep(dose.Dose)
        GPIO.output(dose.pump,GPIO.HIGH)
        blynk.set_property(dose.LED, 'color', BLYNK_RED)
        print ("Dosed " + dose.name + " for " + dose.Dose + " seconds. Using PIN " + dose.Pump + " and showed using LED" + dose.LED)

        
        
# Will Print Every 10 Seconds
@timer.register(interval=10, run_once=False)
def blynk_data():
    _log.info("Start of blynk_data")
    now = datetime.now()
    blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))
    
    _log.info("now the t3")
    cTemp = temp.query("R,").split(":")[1]
    print("Temp = " + cTemp)
    blynk.virtual_write(20, cTemp)
    cEC = ec.query("RT,"+cTemp).split(":")[1]
    blynk.virtual_write(21, cEC)
    print ("EC  = " + cEC)
    cPH = ph.query("RT,"+cTemp).split(":")[1]
    blynk.virtual_write(22, cPH)
    print ("PH = " + cPH)
   
    _log.info("now the adc")
    
    volt = chan.voltage
    if volt is not None:
       blynk.virtual_write(25, str("{0}".format((volt-1.5)*100)))
       blynk.virtual_write(26, str("{0:.2f}".format((volt-1.5)*12)))
      
    _log.info("now the digital single wire")
    blynk.virtual_write(27, GPIO.input(buttEmptySensor))
    blynk.virtual_write(28, GPIO.input(buttFullSensor))
    
    _log.info("make actions for empty butt")
    if (GPIO.input(buttEmptySensor) == GPIO.LOW) :
       blynk.set_property(11, 'color', BLYNK_GREEN)
       turnOnNoisyThingsWhenButtNotEmpty()
       blynk.virtual_write(11,255)
    else:
       blynk.virtual_write(11,255)
       turnOffNoisyThingsWhenButtEmpty()
       blynk.set_property(11, 'color', BLYNK_RED)
  
    _log.info("make actions for full butt")
    if (GPIO.input(buttFullSensor) == GPIO.LOW) :
       blynk.virtual_write(10,255)
       blynk.set_property(10, 'color', BLYNK_RED)
    else:
       blynk.set_property(10, 'color', BLYNK_GREEN)
       blynk.virtual_write(10,255)
        


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
    