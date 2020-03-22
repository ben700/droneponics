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
from adafruit_seesaw.seesaw import Seesaw
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import os
import logging

class Counter:
    cycle = 0
    
colours = {1: '#00FF00', 0: '#FF0000', 'OFFLINE': '#0000FF'}

bootup = True
T_CRI_VALUE = 16.5  # 16.5°C
WT_CRI_VALUE = 16.5  # 16.5°C
T_CRI_MSG = 'Low TEMP!!!'
T_CRI_COLOR = '#c0392b'

T_COLOR = '#f5b041'
H_COLOR = '#85c1e9'
P_COLOR = '#a2d9ce'

TL_COLOR = '#cea2d9'
IR_COLOR = '#a2add9'
VL_COLOR = '#d9cea2'
FS_COLOR = '#add9a2'

CO2_COLOR = '#d9b3a2'

ERR_COLOR = '#444444' 
colors = {'1': '#23C48E', '0': '#D3435C', 'OFFLINE': '#FF0000'}

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

class DosePump:
    def __init__(self, Pump, Led, name):
        self.pump = Pump
        self.LED = Led
        self.name = name


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

BLYNK_GREEN     ="#23C48E"
BLYNK_BLUE      ="#04C0F8"
BLYNK_YELLOW    ="#ED9D00"
BLYNK_RED       ="#D3435C"
BLYNK_DARK_BLUE ="#5F7CD8"

colors = {1: '#23C48E', 0: '#D3435C', 'OFFLINE': '#FF0000'}


buttFullSensor =  17
buttEmptySensor = 6

#pins for solenoid
solenoidIn = 18
solenoidOut = 23


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
GPIO.setup(buttFullSensor, GPIO.IN)
GPIO.setup(buttEmptySensor, GPIO.IN)

Relay1 = 21 #UV & Mixer
Relay2 = 20 #Air
Relay3 = 16 #Waste
Relay4 = 12

LED = [40,41,42,43,44, 45, 46, 47, 48, 49]

nutrientMix = []
nutrientMix.append( Dose(Pump1, 6, LED[0], "Hydro Grow A")) 
nutrientMix.append( Dose(Pump2, 6, LED[1], "Hydro Grow B")) 
nutrientMix.append( Dose(Pump3, 10, LED[2], "Root Stimulant"))
nutrientMix.append( Dose(Pump4, 4, LED[3], "Enzyme"))
nutrientMix.append( Dose(Pump5, 1, LED[4], "Hydro Silicon")) 
nutrientMix.append( Dose(Pump8, 1, LED[8], "Pure Clean")) 


dosePumps = []
dosePumps.append( DosePump(Pump1, LED[0], "Hydro Grow A")) 
dosePumps.append( DosePump(Pump2, LED[1], "Hydro Grow B")) 
dosePumps.append( DosePump(Pump3, LED[2], "Root Stimulant"))
dosePumps.append( DosePump(Pump4, LED[3], "Enzyme"))
dosePumps.append( DosePump(Pump5, LED[4], "Hydro Silicon")) 
dosePumps.append( DosePump(Pump6, LED[5], "Pure Clean")) 
dosePumps.append( DosePump(Pump7, LED[6], "Unused"))
dosePumps.append( DosePump(Pump8, LED[7], "Unused"))
dosePumps.append( DosePump(Pump9, LED[8], "Unused")) 
dosePumps.append( DosePump(Pump10, LED[9], "pH")) 


noisyThingsWhenButtEmpty = [Relay1, Relay2]


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
#GPIO.output(solenoidIn,GPIO.LOW)
#GPIO.output(solenoidOut,GPIO.LOW)


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

print(GPIO.input(buttEmptySensor))

print(GPIO.input(buttFullSensor))




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
#colour = AtlasI2C(112)


#_log.info("Temp Device Info = " + temp.query("i"))
#_log.info("pH Device Info = " + ph.query("i"))
#_log.info("EC Device Info = " + ec.query("i"))
#_log.info("colour Device Info = " + colour.query("i"))    
#_log.info("Temp Device Info = " + temp.query("i"))
#_log.info("pH Device Info = " + ph.query("i"))
#_log.info("EC Device Info = " + ec.query("i"))
#_log.info("DO Device Info = " + do.query("i"))      
#_log.info("Flow Device Info = " + flow.query("i"))      

      
#_log.info("Temp Cal = " + temp.query("Cal,?"))
#_log.info("Temp Scale = " + temp.query("S,?"))
      
#_log.info("pH Cal = " + ph.query("Cal,?"))
#_log.info("pH Temp Cal = " + ph.query("T,?"))

#_log.info("EC Cal = " + ec.query("Cal,?"))
#_log.info("EC Temp Cal = " + ec.query("Cal,?"))
#_log.info("EC Probe Type = " + ec.query("K,?"))

#_log.info("DO Cal = " + do.query("Cal,?"))     
#_log.info("DO Temp Cal = " + do.query("Cal,?"))
#_log.info("DO Salinity Cal = " + do.query("S,?"))
#_log.info("DO Pressure Cal = " + do.query("P,?"))

#_log.info("Flow Meter Type = " + flow.query("Set,?"))
#_log.info("Flow number of K Values = " + flow.query("K,?"))  #returns the number of K values stored
#_log.info("Flow K Values = " + flow.query("K,all"))  #query the programmed K-value(s)
#_log.info("Flow Rate = " + flow.query("Frp,?"))
#_log.info("Flow Rate Time Base = " + flow.query("Vp,?"))
#_log.info("Flow Resistors = " + flow.query("P,?")) #pull-up or pull-down resistors
    
#_log.info("Pump Cal = " + pump.query("Cal,?"))
#_log.info("Pump Voltage Check = " + pump.query("PV,?"))
#_log.info("Pump Dispense Status = " + pump.query("D,?"))
#_log.info("Pump maximum possible flow rate = " + pump.query("DC,?")) # maximum flow rate is determined after calibration.
#_log.info("Pump Pause Status = " + pump.query("P,?"))
#_log.info("Pump total volume dispensed = " + pump.query("TV,?")) #shows total volume dispensed  
#_log.info("Pump absolute value of the total volume dispensed  = " + pump.query("ATV,?")) #absolute value of the total volume dispensed 
    
      
      
#cTemp = temp.query("R").split(":")[1]
#_log.info("Temp = " + cTemp)
#_log.info("EC = " + ec.query("RT,16.699"))
#_log.info("PH = " + ph.query("RT"+cTemp))
#_log.info("colour = " + colour.query("R"))


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
    GPIO.output(Relay1,value[0])
    now = datetime.now()
    blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))
    blynk.set_property(5, 'color', colours[value[0]])
    if(value[0] == '1'):
        blynk.virtual_write(98,"UV & Mixer turned off" + '\n')
    else:
        blynk.virtual_write(98,"UV & Mixer turned on" + '\n')
        
  

@blynk.handle_event('write V2')
def buttonV2Pressed(pin, value):
    GPIO.output(Relay2,value[0])
    now = datetime.now()
    blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))
    blynk.set_property(6, 'color', colours[value[0]])
    if(value[0] == '1'):
        blynk.virtual_write(98,"Air turned off" + '\n')
    else:
        blynk.virtual_write(98,"Air turned on" + '\n')
        

@blynk.handle_event('write V3')
def buttonV3Pressed(pin, value):
    GPIO.output(Relay3,value[0])
    now = datetime.now()
    blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))
    blynk.set_property(7, 'color', colours[value[0]])
    if(value[0] == '1'):
        blynk.virtual_write(98,"Waste turned off" + '\n')
    else:
        blynk.virtual_write(98,"Waste turned on" + '\n')
        

@blynk.handle_event('write V4')
def buttonV4Pressed(pin, value):
    GPIO.output(Relay4,value[0])
    now = datetime.now()
    blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))
    blynk.set_property(8, 'color', colours[value[0]])
    if(value[0] == '1'):
        blynk.virtual_write(98, "Heater turned off" + '\n')
    else:
        blynk.virtual_write(98,"Heater turned on" + '\n')

    
    
@blynk.handle_event('write V255')
def rebooter(pin, value):
    blynk.virtual_write(98, "User Reboot " + '\n')
    os.system('sh /home/pi/updateDroneponics.sh')
    blynk.virtual_write(98, "System updated and restarting " + '\n')
    os.system('sudo reboot')
    

        
@blynk.handle_event('write v30')
def buttonV30Pressed(pin, value):
   blynk.virtual_write(98, "User Dose Nutrients" + '\n')
   if (value[0] == '1'):
      now = datetime.now()
      _log.info("Dose Nutrients started at" + now.strftime("%d/%m/%Y %H:%M:%S"))
      for dose in nutrientMix: 
          blynk.virtual_write(dose.LED,255)
          blynk.set_property(dose.LED, 'color',  colours[GPIO.LOW])
          GPIO.output(dose.Pump,GPIO.LOW)
          time.sleep(dose.dose)
          GPIO.output(dose.pump,GPIO.HIGH)
          blynk.set_property(dose.LED, 'color',  colours[GPIO.HIGH])
          _log.info("Dosing " + dose.name +" for " + dose.dose + " using pin " + dose.pump + " and led " + dose.LED) 
      _log.info("Requested dose completed")
      blynk.virtual_write(98, "Requested dose completed"  + '\n')
   blynk.virtual_write(30, 0)
   
@blynk.handle_event('write v50')
def buttonV50Pressed(pin, value):
   y = 1
   i = y + -1
   _log.info("Dose pump " + str(y) + " value changed to " +str(value))
   now = datetime.now()
   blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))
   blynk.set_property(dosePump.LED[i], 'color',  colours[value[0]])
   GPIO.output(dosePump.Pump[i], value[0])
   blynk.virtual_write(98, "Dose pump " + dosePump[i].name + " to = " + value[0])


@blynk.handle_event('write v69')
def buttonV69Pressed(pin, value):
    now = datetime.now()
    _log.info("Dose Line Fill at " + now.strftime("%d/%m/%Y %H:%M:%S"))
    for pump in dosePump:
        blynk.set_property(pump.LED, 'color', colours[GPIO.LOW])
        GPIO.output(pump.Pump,GPIO.LOW)                                                           
    blynk.virtual_write(98, "All pumps stopped" + '\n')
       
@blynk.handle_event('write v70')
def buttonV70Pressed(pin, value):
    now = datetime.now()
    _log.info("Dose Line Stop All at " + now.strftime("%d/%m/%Y %H:%M:%S"))
    blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))
    blynk.virtual_write(98, "All pumps Started" + '\n')
    for pump in dosePump:
        blynk.set_property(pump.LED, 'color', colours[GPIO.HIGH])
        GPIO.output(pump.Pump,GPIO.HIGH)                                                           
    
@blynk.handle_event('write V90')
def openButtbuttonPressed(pin, value):
    now = datetime.now()
    _log.info(value)
    if (value[0] == '0'):
       _log.info("User requested to fill butt")
    else:
        _log.info("User requested to stop fill butt")
        
    blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))
    blynk.virtual_write(98, "User requested to fill butt" + '\n')
    GPIO.output(solenoidIn, value[0])   

@blynk.handle_event('write V91')
def openButtbuttonPressed(pin, value):
    now = datetime.now()
    _log.info("User requested to close butt")
    blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))
    blynk.virtual_write(98, "User requested to change butt bottom tap" + '\n')
    GPIO.output(solenoidOut, value[0])  
        
# Will Print Every 10 Seconds
@timer.register(interval=10, run_once=False)
def blynk_data():
    _log.info("Start of blynk_data")
    now = datetime.now()
    blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))
    
    _log.info("now the t3")
    cTemp = temp.query("R,").split(":")[1]
    _log.info("Temp = " + cTemp)
    blynk.virtual_write(30, cTemp)
    
  
   
        
    _log.info("read ec")
    try:
        cEC = ec.query("RT,"+cTemp).split(":")[1]
    except:
        blynk.virtual_write(98, "Read EC Error" + '\n')
        cEC = 'Error'
        devices = devices.list_i2c_devices()
        for device in devices:
           blynk.virtual_write(98, device.address() + '\n')
   
    else:
        blynk.virtual_write(98, "EC Else" + '\n')
        blynk.virtual_write(31, cEC)
        _log.info ("EC  = " + cEC)
    finally:
        blynk.virtual_write(98, "EC finally" + '\n')
        
    
       
    
    _log.info("read PH")
    try:
       cPH = ph.query("RT,"+cTemp).split(":")[1]
       blynk.virtual_write(32, cPH)
       _log.info ("PH = " + cPH)
    except:
       blynk.virtual_write(98, "Read PH Error" + '\n') 
       _log.info("Read Ph Error")
       cPH = 'Error'

    
    _log.info("now the digital single wire")
    
    
  #  blynk.virtual_write(37, GPIO.input(buttEmptySensor))
  #  blynk.virtual_write(38, GPIO.input(buttFullSensor))
    
    _log.info("Change LEDs for butt sensors")
    
   # if (GPIO.input(buttEmptySensor) == GPIO.LOW) :
   #    for Relay in noisyThingsWhenButtEmpty:
   #       GPIO.output(Relay,GPIO.LOW)
   #    GPIO.output(solenoidIn, GPIO.HIGH)
   #    GPIO.output(solenoidOut, GPIO.HIGH)   
   # else:
   #    for Relay in noisyThingsWhenButtEmpty:
   #      GPIO.output(Relay,GPIO.HIGH)     
   # _log.info("make actions for full butt")
   # if (GPIO.input(buttFullSensor) == GPIO.LOW) : 
   #    GPIO.output(solenoidIn, GPIO.LOW)

    blynk.virtual_write(98, "Completed Timer Function" + '\n') 
      
while True:
    try:
       blynk.run()
       if bootup :
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
    