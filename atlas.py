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
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


buttFullSensor =  4
buttEmptySensor = 17

#pins for solenoid
solenoidIn = 0
solenoidOut = 0


Pump1 = 0
Pump2 = 0
Pump3 = 0
Pump4 = 0
Pump5 = 0
Pump6 = 0
Pump7 = 0
Pump8 = 0
Pump9 = 0
Pump10 = 0

#setup sensor 2
GPIO.setup(buttFullSensor, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(buttEmptySensor, GPIO.IN, GPIO.PUD_DOWN)

Relay1 = 26
Relay2 = 19
Relay3 = 13
Relay4 = 6

GPIO.setup(Relay1,GPIO.OUT)
GPIO.setup(Relay2,GPIO.OUT)
GPIO.setup(Relay3,GPIO.OUT)
GPIO.setup(Relay4,GPIO.OUT)


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


def buttEmpty_callback(channel):
   if GPIO.input(buttEmptySensor): 
      print ("Water butt no longer empty") 
   else: 
      turnOffMixer()
      print ("Water butt empty")
        

      
def buttFull_callback(channel): 
   if GPIO.input(buttFullSensor):
      print ("Water butt now full") 
   else:
      print ("Water butt no longer full") 


GPIO.add_event_detect(buttFullSensor, GPIO.BOTH, callback=buttFull_callback) 
GPIO.add_event_detect(buttEmptySensor, GPIO.BOTH, callback=buttEmpty_callback) 

# The ID and range of a sample spreadsheet.
#BLYNK_AUTH = 'SHraFqInf27JKowTcFZapu0rHH2QGtuO' #atlasReservoir
BLYNK_AUTH = 'XVbhfI6ZYxkqFp7d4RsCIN6Is9YnKp9q' #atlasButt

# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH)

# Create BlynkTimer Instance
timer = BlynkTimer()

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

print("Temp Device Info = " + temp.query("i"))
print("pH Device Info = " + ph.query("i"))
print("EC Device Info = " + ec.query("i"))
#print("DO Device Info = " + do.query("i"))      
#print("Flow Device Info = " + flow.query("i"))      

      
print("Temp Cal = " + temp.query("Cal,?"))
print("Temp Scale = " + temp.query("S,?"))
      
print("pH Cal = " + ph.query("Cal,?"))
print("pH Temp Cal = " + ph.query("T,?"))

print("EC Cal = " + ec.query("Cal,?"))
print("EC Temp Cal = " + ec.query("Cal,?"))
print("EC Probe Type = " + ec.query("K,?"))

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
print("Temp = " + cTemp)
print("EC = " + ec.query("RT,16.699"))
print("PH = " + ph.query("RT"+cTemp))
#print("DO = " + d0.query("RT,"+cTemp))

@blynk.on("V1")
def buttonV1Pressed(value):
    blynk.virtual_write(1, str(value[0]))
    if(value[0] == '1'):
        print("Waste turned off")
        GPIO.output(Relay1,GPIO.HIGH)
    else:
        print("Waste turned on")
        GPIO.output(Relay1,GPIO.LOW)
    setLEDsonApp()


@blynk.on("V2")
def buttonV2Pressed(value):
    blynk.virtual_write(2, str(value[0]))
    if(value[0] == '1'):
        print("Feed Pump turned off")
        GPIO.output(Relay2,GPIO.HIGH)
    else:
        print("Feed Pump turned on")
        GPIO.output(Relay2,GPIO.LOW)
    setLEDsonApp()


@blynk.on("V3")
def buttonV3Pressed(value):
    blynk.virtual_write(3, str(value[0]))
    if(value[0] == '1'):
        print("Air and Mixer turned off")
        GPIO.output(Relay3,GPIO.HIGH)
    else:
        print("Air and Mixer turned on")
        GPIO.output(Relay3,GPIO.LOW)
    setLEDsonApp()


@blynk.on("V4")
def buttonV4Pressed(value):
    blynk.virtual_write(4, str(value[0]))
    if(value[0] == '1'):
        print("Pump/UV turned off")
        GPIO.output(Relay4,GPIO.HIGH)
    else:
        print("Pump/UV turned on")
        GPIO.output(Relay4,GPIO.LOW)
    setLEDsonApp()

@blynk.on("connected")
def blynk_connected():
    # You can also use blynk.sync_virtual(pin)
    # to sync a specific virtual pin
    print("Updating values from the server...")
    blynk.sync_virtual(*)
  
    for i in range(40) 
        result = blynk.sync_virtual(i)
        print("For i = " + str(i) + " the result was "+ str(result))
    
    
def setLEDsonApp():
    #leds for 4 plugs
    if (GPIO.input(Relay1) == GPIO.LOW) :
       blynk.virtual_write(5,255)
       blynk.set_property(5, 'color', BLYNK_RED)
    else:
       blynk.virtual_write(5,255)
       blynk.set_property(5, 'color', BLYNK_GREEN)
        
    if (GPIO.input(Relay2) == GPIO.LOW) :
       blynk.virtual_write(6,255)
       blynk.set_property(6, 'color', BLYNK_RED)
    else:
       blynk.virtual_write(6,255)
       blynk.set_property(6, 'color', BLYNK_GREEN)
        
    if (GPIO.input(Relay3) == GPIO.LOW) :
       blynk.virtual_write(7,255)
       blynk.set_property(7, 'color', BLYNK_RED)
    else:
       blynk.virtual_write(7,255)
       blynk.set_property(7, 'color', BLYNK_GREEN)
        
    if (GPIO.input(Relay4) == GPIO.LOW) :
       blynk.virtual_write(8,255)
       blynk.set_property(8, 'color', BLYNK_RED)
    else:
       blynk.virtual_write(8,255)
       blynk.set_property(8, 'color', BLYNK_GREEN)  
    #now do water level LEDs    
    if (GPIO.input(buttFullSensor) == GPIO.LOW) :
       blynk.virtual_write(10,255)
       blynk.set_property(10, 'color', BLYNK_RED)
    else:
       blynk.virtual_write(10,255)
       blynk.set_property(10, 'color', BLYNK_GREEN)
        
    if (GPIO.input(buttEmptySensor) == GPIO.LOW) :
       blynk.virtual_write(11,255)
       blynk.set_property(11, 'color', BLYNK_RED)
    else:
       blynk.virtual_write(11,255)
       blynk.set_property(11, 'color', BLYNK_GREEN)
        
def turnOffMixer(): 
   GPIO.output(Relay1,GPIO.HIGH)
   GPIO.output(Relay2,GPIO.HIGH)
   GPIO.output(Relay3,GPIO.HIGH)
   GPIO.output(Relay4,GPIO.HIGH)
   setLEDsonApp()     

# Will Print Every 10 Seconds
def blynk_data():

    now = datetime.now()
    blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))
    cTemp = temp.query("R,").split(":")[1]
    print("Temp = " + cTemp)
    blynk.virtual_write(20, cTemp)
    blynk.virtual_write(21, ec.query("RT,"+cTemp).split(":")[1])
    blynk.virtual_write(22, ph.query("RT,"+cTemp).split(":")[1])
    
    
    setLEDsonApp()
    



# Add Timers
timer.set_interval(10, blynk_data)



while True:
    blynk.run()
    timer.run()


