#!/usr/bin/python3

import blynklib
import blynktimer
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


BLYNK_AUTH = 'e06jzpI2zuRD4KB5eHyHdCQTGFT7einR'

# initialize Blynk
blynk = blynklib.Blynk(BLYNK_AUTH)

    
@blynk.handle_event('write V1')
def buttonV1Pressed(pin, value):
   _log.info(WRITE_EVENT_PRINT_MSG.format(pin, value))
   if (value[0] == '1'):
      now = datetime.now()
      blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))
      blynk.virtual_write(98, "User requested dose"  + '\n')
      for dose in nutrientMix: 
         blynk.virtual_write(98, "Dosing " + str(dose.name) +" for " + str(dose.dose) + " using pin " + str(dose.pump) + " and led " + str(dose.LED) + '\n')
         blynk.set_property(dose.LED, 'color', BLYNK_RED)
         GPIO.output(dose.pump,GPIO.LOW)

      #@timer.register(vpin_num=110+pin, interval=dose.dose, run_once=True)                                  
      #timer = blynktimer.Timer()
      #timer.run() 
                    
      #sleep_ms(dose.dose)

         GPIO.output(dose.pump,GPIO.HIGH)
         blynk.set_property(dose.LED, 'color', BLYNK_GREEN)
            
            
   blynk.virtual_write(1, 0)
   blynk.virtual_write(98, "Requested dose completed"  + '\n')
    
    
@blynk.handle_event('write V2')
def buttonV2Pressed(pin, value):
    _log.info(WRITE_EVENT_PRINT_MSG.format(pin, value))
        
@blynk.handle_event('write V3')
def buttonV3Pressed(pin, value):
    _log.info(WRITE_EVENT_PRINT_MSG.format(pin, value))

        
# register handler for virtual pin V4 write event
@blynk.handle_event('write V4')
def write_virtual_pin_handler(pin, value):
    _log.info(WRITE_EVENT_PRINT_MSG.format(pin, value))

@blynk.handle_event('read V4')
def read_virtual_pin_handler(pin):
    _log.info(READ_PRINT_MSG.format(pin))

    
    
###########################################################
# infinite loop that waits for event
###########################################################
while True:
    blynk.run()

