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


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

buttFullSensor =  20
buttEmptySensor =21

Relay1 = 16


#setup sensor 2
GPIO.setup(buttFullSensor, GPIO.IN)
GPIO.setup(buttEmptySensor, GPIO.IN)
GPIO.setup(Relay1,GPIO.OUT)


GPIO.setup(Relay1,GPIO.OUT)
GPIO.output(Relay1,GPIO.LOW)


while True: 
   print ("Full = " + str(GPIO.input(buttFullSensor)))
   print ("Empty = " + str(GPIO.input(buttEmptySensor)))
   GPIO.output(Relay1,not GPIO.input(Relay1))   
   time.sleep(5)
