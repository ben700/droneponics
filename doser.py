#!/usr/bin/python

import logging
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

#pins for solenoid
solenoidIn = 0
solenoidOut = 0

Pump1 = 4
Pump2 = 27
Pump3 = 21
Pump4 = 13
Pump5 = 26

nutrientMix = []
nutrientMix.append( Dose(Pump1, 6, 40, "Hydro Grow A")) 
nutrientMix.append( Dose(Pump2, 6, 41, "Hydro Grow B")) 
nutrientMix.append( Dose(Pump3, 10, 42, "Root Stimulant"))
nutrientMix.append( Dose(Pump4, 4, 43, "Enzyme"))
nutrientMix.append( Dose(Pump5, 1, 44, "Hydro Silicon")) 
nutrientMix.append( Dose(Pump6, 1, 45, "Pure Clean"))

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

# The ID and range of a sample spreadsheet.


# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH)

now = datetime.now()
blynk.virtual_write(99, now.strftime("%d/%m/%Y %H:%M:%S"))
logging.info("Rebooted at " + now.strftime("%d/%m/%Y %H:%M:%S"))
blynk.notify("Rebooted at " + now.strftime("%d/%m/%Y %H:%M:%S"))

        
@blynk.on("V30")
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
    
@blynk.on("V69")
def buttonV69Pressed(value):
    logging.info("Dose Line Fill at " + now.strftime("%d/%m/%Y %H:%M:%S"))
    print("Dose Line Stop Fill at " + now.strftime("%d/%m/%Y %H:%M:%S"))
    GPIO.output(Pump1,GPIO.LOW)
    GPIO.output(Pump2,GPIO.LOW)
    GPIO.output(Pump3,GPIO.LOW)
    GPIO.output(Pump4,GPIO.LOW)
    GPIO.output(Pump5,GPIO.LOW)
       
@blynk.on("V70")
def buttonV70Pressed(value):
    logging.info("Dose Line Stop All at " + now.strftime("%d/%m/%Y %H:%M:%S"))
    print("Dose Line Stop All at " + now.strftime("%d/%m/%Y %H:%M:%S"))
    GPIO.output(Pump1,GPIO.HIGH)
    GPIO.output(Pump2,GPIO.HIGH)
    GPIO.output(Pump3,GPIO.HIGH)
    GPIO.output(Pump4,GPIO.HIGH)
    GPIO.output(Pump5,GPIO.HIGH)

        
@blynk.on("V255")
def buttonV255Pressed(value):
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

while True:
    try:
       blynk.run()
    except:
        logging.error("Something bad happened to did end of programme reboot")
        os.system('sudo reboot')

