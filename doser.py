#!/usr/bin/python3

import blynklib
from blynktimer import Timer, TimerError
import logging
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

class Dose:
    def __init__(self, Pump, Dose, Led, Name):
        self.pump = Pump
        self.dose = Dose
        self.doseButt = Dose * 10
        self.LED = Led
        self.name = Name
        


# tune console logging
_log = logging.getLogger('BlynkLog')
logFormatter = logging.Formatter("%(asctime)s [%(levelname)s]  %(message)s")
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
_log.addHandler(consoleHandler)
_log.setLevel(logging.DEBUG)


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

BLYNK_GREEN     ="#23C48E"
BLYNK_BLUE      ="#04C0F8"
BLYNK_YELLOW    ="#ED9D00"
BLYNK_RED       ="#D3435C"
BLYNK_DARK_BLUE ="#5F7CD8"


colors = {'1': '#FFC300', '0': '#CCCCCC', 'OFFLINE': '#FF0000'}

APP_CONNECT_PRINT_MSG = '[APP_CONNECT_EVENT]'
APP_DISCONNECT_PRINT_MSG = '[APP_DISCONNECT_EVENT]'
CONNECT_PRINT_MSG = '[CONNECT_EVENT]'
DISCONNECT_PRINT_MSG = '[DISCONNECT_EVENT]'
WRITE_EVENT_PRINT_MSG = "[WRITE_VIRTUAL_PIN_EVENT] Pin: V{} Value: '{}'"
READ_PRINT_MSG = "[READ_VIRTUAL_PIN_EVENT] Pin: V{}"
ALLOWED_COMMANDS_LIST = ['ls', 'lsusb', 'ip a', 'ip abc']
TWEET_MSG = "New value='{}' on VPIN({})"



Pump1 = 4
Pump2 = 27
Pump3 = 21
Pump4 = 13
Pump5 = 26

LED = [10,11,12,13,14]

nutrientMix = []
nutrientMix.append( Dose(Pump1, 6, LED[0], "Hydro Grow A")) 
nutrientMix.append( Dose(Pump2, 6, LED[1], "Hydro Grow B")) 
nutrientMix.append( Dose(Pump3, 10, LED[2], "Root Stimulant"))
nutrientMix.append( Dose(Pump4, 4, LED[3], "Enzyme"))
nutrientMix.append( Dose(Pump5, 1, LED[4], "Hydro Silicon")) 

GPIO.setup(Pump1,GPIO.OUT)
GPIO.setup(Pump2,GPIO.OUT)
GPIO.setup(Pump3,GPIO.OUT)
GPIO.setup(Pump4,GPIO.OUT)
GPIO.setup(Pump5,GPIO.OUT)

GPIO.output(Pump1,GPIO.HIGH)
GPIO.output(Pump2,GPIO.HIGH)
GPIO.output(Pump3,GPIO.HIGH)
GPIO.output(Pump4,GPIO.HIGH)
GPIO.output(Pump5,GPIO.HIGH)

bootup = True
BLYNK_AUTH = 'e06jzpI2zuRD4KB5eHyHdCQTGFT7einR'

# initialize Blynk
blynk = blynklib.Blynk(BLYNK_AUTH)
timer = blynktimer.Timer()
blynk.run()

_log.info("Booted")
blynk.virtual_write(98, "Rebooted"  + '\n')
blynk.virtual_write(99, now.strftime("%d/%m/%Y %H:%M:%S"))
    

@timer.register(interval=60, run_once=True)
def started():
    _log.info("hearbeat")
    now = datetime.now()
    blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))
    blynk.virtual_write(98, "Heartbeat"  + '\n')
       
    
@blynk.handle_event('write V1')
def buttonV1Pressed(pin, value):
   _log.info(WRITE_EVENT_PRINT_MSG.format(pin, value))
   if (value[0] == '1'):
      now = datetime.now()
      blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))
      blynk.virtual_write(98, "User requested dose"  + '\n')
      for dose in nutrientMix: 
         blynk.virtual_write(98, "Dosing " + str(dose.name) +" for " + str(dose.dose) + " using pin " + str(dose.pump) + " and led " + str(dose.LED) + '\n')

         _log.info("Start Dose of " + str(dose.name))
         blynk.set_property(dose.LED, 'color', BLYNK_RED)
         GPIO.output(dose.pump,GPIO.LOW)
        
         _log.info("Going to sleep for " + str(dose.dose))
         time.sleep(dose.dose)

         _log.info("Stop Dose of " + str(dose.name))
         GPIO.output(dose.pump,GPIO.HIGH)
         blynk.set_property(dose.LED, 'color', BLYNK_GREEN)
            
            
   _log.info("Requested dose completed")
   blynk.virtual_write(1, 0)
   blynk.virtual_write(98, "Requested dose completed"  + '\n')
    
    
@blynk.handle_event('write V2')
def buttonV2Pressed(pin, value):
   _log.info(WRITE_EVENT_PRINT_MSG.format(pin, value))
   if (value[0] == '1'):
      now = datetime.now()
      blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))
      blynk.virtual_write(98, "User requested dose"  + '\n')
      for dose in nutrientMix: 
         blynk.virtual_write(98, "Dosing " + str(dose.name) +" for " + str(dose.doseButt) + " using pin " + str(dose.pump) + " and led " + str(dose.LED) + '\n')

         _log.info("Start Dose of " + str(dose.name))
         blynk.set_property(dose.LED, 'color', BLYNK_RED)
         GPIO.output(dose.pump,GPIO.LOW)
        
         _log.info("Going to sleep for " + str(dose.dose))
         time.sleep(dose.doseButt)

         _log.info("Stop Dose of " + str(dose.name))
         GPIO.output(dose.pump,GPIO.HIGH)
         blynk.set_property(dose.LED, 'color', BLYNK_GREEN)
      
    
      _log.info("Finished For Loop")
      blynk.virtual_write(2, 0)
            
            
   _log.info("Requested dose completed")
   blynk.virtual_write(98, "Requested dose completed"  + '\n')
        
@blynk.handle_event('write V3')
def buttonV3Pressed(pin, value):
    _log.info(WRITE_EVENT_PRINT_MSG.format(pin, value))
    now = datetime.now()
    blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))
    blynk.virtual_write(98, "User pressed button 3" + '\n')
    if(value[0] == '1'):
       blynk.virtual_write(98, "Dose Line Stop All at " + now.strftime("%d/%m/%Y %H:%M:%S") + '\n')
       GPIO.output(Pump1,GPIO.HIGH)
       GPIO.output(Pump2,GPIO.HIGH)
       GPIO.output(Pump3,GPIO.HIGH)
       GPIO.output(Pump4,GPIO.HIGH)
       GPIO.output(Pump5,GPIO.HIGH)
       for i in LED: 
          blynk.set_property(i, 'color', BLYNK_GREEN)
       blynk.virtual_write(98, "All pumps stopped" + '\n') 
    else  :     
       blynk.virtual_write(98, "Dose Line Stop Fill at " + now.strftime("%d/%m/%Y %H:%M:%S") + '\n')
       GPIO.output(Pump1,GPIO.LOW)
       GPIO.output(Pump2,GPIO.LOW)
       GPIO.output(Pump3,GPIO.LOW)
       GPIO.output(Pump4,GPIO.LOW)
       GPIO.output(Pump5,GPIO.LOW)
       blynk.virtual_write(98, "All pumps started" + '\n')
       for i in LED: 
           blynk.set_property(i, 'color', BLYNK_RED)

        
# register handler for virtual pin V4 write event
@blynk.handle_event('write V4')
def write_virtual_pin_handler(pin, value):
    _log.info(WRITE_EVENT_PRINT_MSG.format(pin, value))

@blynk.handle_event('read V4')
def read_virtual_pin_handler(pin):
    _log.info(READ_PRINT_MSG.format(pin))

@blynk.handle_event('write V255')  
def buttonV255Pressed(pin, value):
    _log.info(WRITE_EVENT_PRINT_MSG.format(pin, value))
    now = datetime.now()
    try:
        blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))
        blynk.virtual_write(98, "Update code from github and reboot asked by user" + '\n')
    except:
        os.system('sh /home/pi/droneponics/reboot.sh')
    
###########################################################
# infinite loop that waits for event
###########################################################
try:
    while True:
        blynk.run()
        timer.run()
except:
    blynk.disconnect()
    _log.info('SCRIPT WAS INTERRUPTED')
finally: 
     _log.info('Could do finally reboot')
    #os.system('sh /home/pi/droneponics/reboot.sh')

