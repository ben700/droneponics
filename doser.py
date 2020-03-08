#!/usr/bin/python3

import BlynkLib
from BlynkTimer import BlynkTimer
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


LOG_LEVEL = logging.INFO
LOG_FILE = "/home/pi/doseslog"
LOG_FORMAT = "%(asctime)s %(levelname)s %(message)s"
#logging.basicConfig(filename=LOG_FILE, format=LOG_FORMAT, level=LOG_LEVEL)


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

BLYNK_GREEN     ="#23C48E"
BLYNK_BLUE      ="#04C0F8"
BLYNK_YELLOW    ="#ED9D00"
BLYNK_RED       ="#D3435C"
BLYNK_DARK_BLUE ="#5F7CD8"

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
blynk = BlynkLib.Blynk('e06jzpI2zuRD4KB5eHyHdCQTGFT7einR')

    
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

@blynk.on("V1")
def buttonV1Pressed(value):
   now = datetime.now()
   blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))
   blynk.virtual_write(98, "User requested dose"  + '\n')
   for dose in nutrientMix: 
      blynk.virtual_write(98, "Dosing " + str(dose.name) +" for " + str(dose.dose) + " using pin " + str(dose.pump) + " and led " + str(dose.LED) + '\n')
      blynk.set_property(dose.LED, 'color', BLYNK_RED)
      GPIO.output(dose.pump,GPIO.LOW)
      time.sleep(dose.dose)
      GPIO.output(dose.pump,GPIO.HIGH)
      blynk.set_property(dose.LED, 'color', BLYNK_GREEN)
   #blynk.virtual_write(1, 0)
   blynk.virtual_write(98, "Requested dose completed"  + '\n')
    
@blynk.on("V2")
def buttonV2Pressed(value):
    if(value[0] != '1'):
         now = datetime.now()
         blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))
         blynk.virtual_write(98, "User requested butt dose"  + '\n')
         for dose in nutrientMix: 
             blynk.virtual_write(98, "Dosing " + str(dose.name) +" for " + str(dose.dose*10) + " using pin " + str(dose.pump) + " and led " + str(dose.LED) + '\n')
             blynk.set_property(dose.LED, 'color', BLYNK_RED)
             GPIO.output(dose.pump,GPIO.LOW)
             #time.sleep(dose.dose*10)
             time.sleep(1)
             GPIO.output(dose.pump,GPIO.HIGH)
             blynk.set_property(dose.LED, 'color', BLYNK_GREEN)
    #blynk.virtual_write(2, 0)
    blynk.virtual_write(98, "Requested dose butt completed"  + '\n')
        
@blynk.on("V3")
def buttonV3Pressed(value):
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

        
@blynk.on("V4")
def buttonV4Pressed(value):
    now = datetime.now()
    blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))
    blynk.virtual_write(98, "User pressed button 4" + '\n')
               
@blynk.on("V255")
def buttonV255Pressed(value):
    now = datetime.now()
    blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))
    blynk.virtual_write(98, "Update code from github and reboot asked by user" + '\n')
    os.system('sh /home/pi/droneponics/reboot.sh')
    
      
while True:
    try:
       blynk.run()
    except:
       os.system('sh /home/pi/droneponics/reboot.sh')

