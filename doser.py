#!/usr/bin/python

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
    def __init__(self, Pump, Dose, Led, name):
        self.pump = Pump
        self.dose = Dose
        self.LED = Led
        self.name = name


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
blynk.virtual_write(98, ("Started as normal"))
blynk.notify("Rebooted at " + now.strftime("%d/%m/%Y %H:%M:%S"))

for i in LED: 
    blynk.virtual_write(LED[i], 0)
        
@blynk.on("V1")
def buttonV1Pressed(value):
    now = datetime.now()
    blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))
    blynk.virtual_write(98, "User pressed button 1")
    print("Dose started at " + now.strftime("%d/%m/%Y %H:%M:%S"))
    for dose in nutrientMix: 
       blynk.virtual_write(dose.LED,255)
       blynk.set_property(dose.LED, 'color', BLYNK_GREEN)
       GPIO.output(dose.Pump,GPIO.LOW)
       time.sleep(dose.dose)
       GPIO.output(dose.pump,GPIO.HIGH)
       blynk.set_property(dose.LED, 'color', BLYNK_GREEN)
       logger.info("Dosing " + dose.name +" for " + dose.dose + " using pin " + dose.pump + " and led " + dose.LED) 
    
    blynk.virtual_write(1, 0)
    
@blynk.on("V2")
def buttonV2Pressed(value):
    now = datetime.now()
    blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))
    blynk.virtual_write(98, "User pressed button 2")
    print("Dose started at " + now.strftime("%d/%m/%Y %H:%M:%S"))
    for dose in nutrientMix: 
       blynk.virtual_write(dose.LED,255)
       blynk.set_property(dose.LED, 'color', BLYNK_GREEN)
       GPIO.output(dose.Pump,GPIO.LOW)
       time.sleep(dose.dose*10)
       GPIO.output(dose.pump,GPIO.HIGH)
       blynk.set_property(dose.LED, 'color', BLYNK_GREEN)
       logger.info("Dosing " + dose.name +" for " + dose.dose + " using pin " + dose.pump + " and led " + dose.LED) 
    blynk.virtual_write(2, 0)
        
@blynk.on("V3")
def buttonV3Pressed(value):
    now = datetime.now()
    if value[0] == 0:
       print("Dose Line Stop All at " + now.strftime("%d/%m/%Y %H:%M:%S"))
       GPIO.output(Pump1,GPIO.HIGH)
       GPIO.output(Pump2,GPIO.HIGH)
       GPIO.output(Pump3,GPIO.HIGH)
       GPIO.output(Pump4,GPIO.HIGH)
       GPIO.output(Pump5,GPIO.HIGH)
    else  :     
       print("Dose Line Stop Fill at " + now.strftime("%d/%m/%Y %H:%M:%S"))
       GPIO.output(Pump1,GPIO.LOW)
       GPIO.output(Pump2,GPIO.LOW)
       GPIO.output(Pump3,GPIO.LOW)
       GPIO.output(Pump4,GPIO.LOW)
       GPIO.output(Pump5,GPIO.LOW)
    for i in LED: 
       if (value[0] == 0):
            blynk.virtual_write(LED[i], 0)
       else:
            blynk.virtual_write(LED[i], 1)
            
    blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))
    blynk.virtual_write(98, "User pressed button 3")
    blynk.virtual_write(3, 0)
    
               
@blynk.on("V255")
def buttonV255Pressed(value):
    
    now = datetime.now()
    blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))
    blynk.virtual_write(98, "Reboot by user")
    blynk.virtual_write(255, 0)
    os.system('sudo reboot')
        
def turnOffNoisyThingsWhenButtEmpty(): 
   for Relay in noisyThingsWhenButtEmpty:
       if GPIO.inout(Relay) != GPIO.HIGH : 
           GPIO.output(Relay,GPIO.HIGH)
      
def turnOnNoisyThingsWhenButtNotEmpty(): 
   for Relay in noisyThingsWhenButtEmpty:
       if GPIO.inout(Relay) != GPIO.LOW : 
           GPIO.output(Relay,GPIO.LOW)
      
def DoseNutrients(): 
    logging.debug("DoseNutrients")
    now = datetime.now()
    blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))
    print ("Going to dose butt time is now " + now.strftime("%d/%m/%Y %H:%M:%S"))
    for dose in nutrientMix:
        blynk.set_property(dose.LED, 'color', BLYNK_RED)
        blynk.log_event(dose.name, dose.dose)
        GPIO.output(dose.pump,GPIO.LOW)
        time.sleep(dose.Dose)
        GPIO.output(dose.pump,GPIO.HIGH)
        blynk.set_property(dose.LED, 'color', BLYNK_RED)
        print ("Dosed " + dose.name + " for " + dose.Dose + " seconds. Using PIN " + dose.Pump + " and showed using LED" + dose.LED)

while True:
    try:
       blynk.run()
    except:
        logging.error("Something bad happened to did end of programme reboot")
        os.system('sudo reboot')

