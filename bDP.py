#!/usr/bin/python
# -*- coding: utf-8 -*-
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import datetime
import time
import BlynkLib
from BlynkTimer import BlynkTimer
from ctypes import *
import RPi.GPIO as GPIO
from gpiozero import Servo
import pigpio

#define BLYNK_GREEN     "#23C48E"
#define BLYNK_BLUE      "#04C0F8"
#define BLYNK_YELLOW    "#ED9D00"
#define BLYNK_RED       "#D3435C"
#define BLYNK_DARK_BLUE "#5F7CD8"


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(4,GPIO.OUT)
GPIO.setup(27,GPIO.OUT)
GPIO.setup(21,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(26,GPIO.OUT)

#setup senson 1
GPIO.setup(12, GPIO.IN, GPIO.PUD_DOWN)

GPIO.add_event_detect(16, GPIO.BOTH, callback=buttFull_callback) 
    
# connect to the 
pi = pigpio.pi()


BLYNK_AUTH = 'KHjr44ud-6CEUBFNtse_kHPnFxzMXawy'  #piGTDose
#BLYNK_AUTH = 'i_mmEsu6KBSljmeaqaZ60djp3Vgc_A12' # control centre
#BLYNK_AUTH = 'g9MjyM6-6erTomtN9OFUXqS5dafRHz0D' # black
#BLYNK_AUTH = '5ixcYmoewpFZC5UT-GH5bSMKCSA0eDoF' #black Gloss
SCOPES = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/gmail.send']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1iXetyC5Tqg4kvSs-bFt5BiAsYL5_0O3R-XNEmSUJsLs'
RANGE_NAME = 'cBME280!A:E'


# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH)


dose1 = 0
dose2 = 0
dose3 = 0
dose4 = 0
dose5 = 0



def buttFull_callback(channel): 
   if GPIO.input(12):
      blynk.setProperty(12, "color", BLYNK_GREEN);
      blynk.virtual_write(45,255)
      print ("Water butt OK to dose") 
   else: 
      blynk.setProperty(12, "color", BLYNK_RED);
      blynk.virtual_write(45,127)
      print ("Water butt not full enough to dose")  


@blynk.on("V4")
def buttonV4Pressed(value):
    if(value[0] == '1'):
        print("Button 4 turned on")
        blynk.virtual_write(40,255)
        blynk.virtual_write(41,255)
        pi.set_servo_pulsewidth(4, 2500)
    else:
        print("Button 4 turned off")
        pi.set_servo_pulsewidth(4,0)
        blynk.virtual_write(41,0)
        blynk.virtual_write(40,0)

        
@blynk.on("V27")
def buttonV27Pressed(value):
    if(value[0] == '1'):
        print("Button 27 turned on")
        blynk.virtual_write(40,255)
        blynk.virtual_write(42,255)
        pi.set_servo_pulsewidth(27, 2500)
    else:
        print("Button 27 turned off")
        pi.set_servo_pulsewidth(27, 0)
        blynk.virtual_write(42,0)
        blynk.virtual_write(40,0)

        
        
@blynk.on("V21")
def buttonV21Pressed(value):
    if(value[0] == '1'):
        print("Button 21 turned on")
        blynk.virtual_write(40,255)
        blynk.virtual_write(43,255)
        pi.set_servo_pulsewidth(21, 2500)
    else:
        print("Button 21 turned off")
        pi.set_servo_pulsewidth(21, 0)
        blynk.virtual_write(43,0)
        blynk.virtual_write(40,0)
        
@blynk.on("V13")
def buttonV13Pressed(value):
    if(value[0] == '1'):
        print("Button 13 turned on") 
        blynk.virtual_write(40,255)
        blynk.virtual_write(44,255)
        pi.set_servo_pulsewidth(13, 2500)
    else:
        print("Button 13 turned off")
        pi.set_servo_pulsewidth(13, 0)
        blynk.virtual_write(44,0)
        blynk.virtual_write(40,0)

        
        
@blynk.on("V26")
def buttonV26Pressed(value):
    if(value[0] == '1'):
        print("Button 26 turned on")
        blynk.virtual_write(40,255)
        blynk.virtual_write(45,255)
        pi.set_servo_pulsewidth(26, 2500)
    else:
        print("Button 26 turned off")
        pi.set_servo_pulsewidth(26, 0)
        blynk.virtual_write(45,0)
        blynk.virtual_write(40,0)

        
@blynk.on("V60")
def read_virtual_pin60_handler(pin):
    print(pin)
    global dose1 
    dose1 = int(pin[0])

@blynk.on("V61")
def read_virtual_pin61_handler(pin):
    print(pin)
    global dose2
    dose2 = int(pin[0])
    
@blynk.on("V62")
def read_virtual_pin62_handler(pin):
    print(pin)
    global dose3
    dose3 = int(pin[0])

@blynk.on("V63")
def read_virtual_pin63_handler(pin):
    print(pin)
    global dose4
    dose4 = int(pin[0])

@blynk.on("V64")
def read_virtual_pin64_handler(pin):
    print(pin)
    global dose5
    dose5 = int(pin[0])

        

def doDose(iTime, iPin, iLED):
   print("Turning on pump {} for {} seconds".format(iPin, iTime))
   blynk.virtual_write(40,255)
   blynk.virtual_write(iLED,255)
   pi.set_servo_pulsewidth(iPin, 2500)
   time.sleep(iTime)
   pi.set_servo_pulsewidth(iPin, 0)
   blynk.virtual_write(iLED,0)
   blynk.virtual_write(40,0)
    
        
@blynk.on("V50")
def buttonV50Pressed(value):
   print("Button 50 turned on")
   doDose(dose1,4, 41)
   doDose(dose2,27, 42)
   doDose(dose3,21, 43)
#   doDose(dose4,13, 44)
   doDose(dose5,26, 45)
    

@blynk.on("V51")
def buttonV51Pressed(value):
   print("Button 51 turned on")
   doDose(dose1 * 20,4, 41)
   doDose(dose2 * 20,27, 42)
   doDose(dose3 * 20,21, 43)
#   doDose(dose4 * 20,13, 44)
   doDose(dose5 * 20,26, 45)


@blynk.on("V52")
def buttonV52Pressed(value):
   print("Button 52 turned on")
   doDose(dose4,13, 44)

@blynk.on("V53")
def buttonV53Pressed(value):
   print("Button 53 turned on")
   doDose(dose4 * 20,13, 44)


@blynk.on("connected")
def blynk_connected():
    # You can also use blynk.sync_virtual(pin)
    # to sync a specific virtual pin
    print("Updating values from the server...")
    blynk.sync_virtual("V*")
    blynk.sync_virtual(4,27,21,13,26,40, 41, 42, 43, 44,45, 50, 51, 52, 53, 60, 61, 62, 63, 64)
    


while True:
    blynk.run()
