#!/usr/bin/python3

import blynklib
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
import logging

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



# Initialize Blynk
blynk = blynklib.Blynk(BLYNK_AUTH, heartbeat=15, max_msg_buffer=512, log=_log.info)
timer = blynktimer.Timer()

APP_CONNECT_PRINT_MSG = '[APP_CONNECT_EVENT]'
APP_DISCONNECT_PRINT_MSG = '[APP_DISCONNECT_EVENT]'
CONNECT_PRINT_MSG = '[CONNECT_EVENT]'
DISCONNECT_PRINT_MSG = '[DISCONNECT_EVENT]'
WRITE_EVENT_PRINT_MSG = "[WRITE_VIRTUAL_PIN_EVENT] Pin: V{} Value: '{}'"
READ_PRINT_MSG = "[READ_VIRTUAL_PIN_EVENT] Pin: V{}"
ALLOWED_COMMANDS_LIST = ['ls', 'lsusb', 'ip a', 'ip abc']
TWEET_MSG = "New value='{}' on VPIN({})"

now = datetime.now()
blynk.virtual_write(99, now.strftime("%d/%m/%Y %H:%M:%S"))
blynk.virtual_write(98, ("Started as normal" + '\n'))
#blynk.notify("Rebooted at " + now.strftime("%d/%m/%Y %H:%M:%S"))
blynk.virtual_write(1, 0)
blynk.virtual_write(2, 0)
blynk.virtual_write(3, 0)
blynk.virtual_write(255, 0)
    
def setLEDColours():
    for i in LED: 
        blynk.virtual_write(i, 255)
        blynk.set_property(i, 'color', BLYNK_GREEN)
        
        
setLEDColours()


@blynk.handle_event('internal_acon')
def app_connect_handler(*args):
    print(APP_CONNECT_PRINT_MSG)

@blynk.handle_event('internal_adis')
def app_disconnect_handler(*args):
    print(APP_DISCONNECT_PRINT_MSG)
    
@blynk.handle_event("connect")
def connect_handler():
    print(CONNECT_PRINT_MSG)
    blynk.internal("rtc", "sync")
    print("RTC sync request was sent")
    _log.info(CONNECT_PRINT_MSG)
    for pin in range(3):
        _log.info('Syncing virtual pin {}'.format(pin))
        blynk.virtual_sync(pin)

        # within connect handler after each server send operation forced socket reading is required cause:
        #  - we are not in script listening state yet
        #  - without forced reading some portion of blynk server messages can be not delivered to HW
        blynk.read_response(timeout=0.5)
        

@blynk.handle_event('internal_rtc')
def rtc_handler(rtc_data_list):
    hr_rtc_value = datetime.utcfromtimestamp(int(rtc_data_list[0])).strftime('%Y-%m-%d %H:%M:%S')
    print('Raw RTC value from server: {}'.format(rtc_data_list[0]))
    print('Human readable RTC value: {}'.format(hr_rtc_value))
    
    
@blynk.handle_event("disconnect")
def disconnect_handler():
    print(DISCONNECT_PRINT_MSG)
    for pin in range(3):
        _log.info("Set 'OFFLINE' color for pin {}".format(pin))
        blynk.set_property(pin, 'color', colors['OFFLINE'])
    

    
@blynk.handle_event('write V1')
def buttonV1Pressed(pin, value):
    
   _log.info(WRITE_EVENT_PRINT_MSG.format(pin, value))
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
                    
      sleep_ms(dose.dose)

      GPIO.output(dose.pump,GPIO.HIGH)
      blynk.set_property(dose.LED, 'color', BLYNK_GREEN)
   blynk.virtual_write(1, 0)
   blynk.virtual_write(98, "Requested dose completed"  + '\n')
    
@blynk.handle_event('write V2')
def buttonV2Pressed(pin, value):
    _log.info(WRITE_EVENT_PRINT_MSG.format(pin, value))
    if(value[0] != '1'):
         now = datetime.now()
         blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))
         blynk.virtual_write(98, "User requested butt dose"  + '\n')
         for dose in nutrientMix: 
             blynk.virtual_write(98, "Dosing " + str(dose.name) +" for " + str(dose.dose*10) + " using pin " + str(dose.pump) + " and led " + str(dose.LED) + '\n')
             blynk.set_property(dose.LED, 'color', BLYNK_RED)
             GPIO.output(dose.pump,GPIO.LOW)
             time.sleep(dose.dose*10)
             GPIO.output(dose.pump,GPIO.HIGH)
             blynk.set_property(dose.LED, 'color', BLYNK_GREEN)
    blynk.virtual_write(2, 0)
    blynk.virtual_write(98, "Requested dose butt completed"  + '\n')
        
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
       setLEDColours()
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
    print(WRITE_EVENT_PRINT_MSG.format(pin, value))
    now = datetime.now()
    blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))
    blynk.virtual_write(98, "User pressed write 4" + '\n')

@blynk.handle_event('read V4')
def read_virtual_pin_handler(pin):
    _log.info(READ_PRINT_MSG.format(pin))
    print(READ_PRINT_MSG.format(pin))
    now = datetime.now()
    blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))
    blynk.virtual_write(98, "User pressed read 4" + '\n')


@blynk.handle_event('write V6')
def write_handler(pin, values):
    header = ''
    result = ''
    delimiter = '{}\n'.format('=' * 30)
    if values and values[0] in ALLOWED_COMMANDS_LIST:
        cmd_params = values[0].split(' ')
        try:
            result = subprocess.check_output(cmd_params).decode('utf-8')
            header = '[output]\n'
        except subprocess.CalledProcessError as exe_err:
            header = '[error]\n'
            result = 'Return Code: {}\n'.format(exe_err.returncode)
        except Exception as g_err:
            print("Command caused '{}'".format(g_err))
    elif values and values[0] == 'help':
        header = '[help -> allowed commands]\n'
        result = '{}\n'.format('\n'.join(ALLOWED_COMMANDS_LIST))

    # communicate with terminal if help or some allowed command
    if result:
        output = '{}{}{}{}'.format(header, delimiter, result, delimiter)
        print(output)
        blynk.virtual_write(pin, output)
        blynk.virtual_write(pin, '\n')

@blynk.handle_event('write V255')
def buttonV255Pressed(value):
    now = datetime.now()
    blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))
    blynk.virtual_write(98, "Update code from github and reboot asked by user" + '\n')
    os.system('sh /home/pi/droneponics/reboot.sh')

    
#@blynk.handle_event('write V*')
#def write_handler(pin, value):
#    _log.info(WRITE_EVENT_PRINT_MSG.format(pin, value))
#    print(WRITE_EVENT_PRINT_MSG.format(pin, value))
#    button_state = value[0]
#    blynk.set_property(pin, 'color', colors[button_state])        
        

    
try:
    while True:
        blynk.run()
except KeyboardInterrupt:
    blynk.disconnect()
    _log.info('SCRIPT WAS INTERRUPTED')
finally:                
    os.system('sh /home/pi/droneponics/reboot.sh')

