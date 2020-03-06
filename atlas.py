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
        selt.name = name


logger = logging.getLogger('doses')
hdlr = logging.FileHandler('/home/pi/dose.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.WARNING)


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

BLYNK_GREEN     ="#23C48E"
BLYNK_BLUE      ="#04C0F8"
BLYNK_YELLOW    ="#ED9D00"
BLYNK_RED       ="#D3435C"
BLYNK_DARK_BLUE ="#5F7CD8"

buttFullSensor =  17
buttEmptySensor = 4

#pins for solenoid
solenoidIn = 0
solenoidOut = 0

nutrientMix = []
nutrientMix.append( Dose(Pump1, 6, 40, "Hydro Grow A")) 
nutrientMix.append( Dose(Pump2, 6, 41, "Hydro Grow B")) 
nutrientMix.append( Dose(Pump3, 10, 42, "Root Stimulant"))
nutrientMix.append( Dose(Pump4, 4, 43, "Enzyme"))
nutrientMix.append( Dose(Pump5, 1, 44, "Hydro Silicon")) 
nutrientMix.append( Dose(Pump6, 1, 45, "Pure Clean"))

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

Pump1Dose = 30 #part A
Pump2Dose = 30 #part B
Pump3Dose = 30
Pump4Dose = 1
Pump5Dose = 1
Pump6Dose = 1
Pump7Dose = 1
Pump8Dose = 1
Pump9Dose = 1
Pump10Dose = 1

#setup sensor 2
GPIO.setup(buttFullSensor, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(buttEmptySensor, GPIO.IN, GPIO.PUD_DOWN)

Relay1 = 21
Relay2 = 20
Relay3 = 16
Relay4 = 12

noisyThingsWhenButtEmpty = [Relay1, Relay2, Relay3]

Mixer = Relay1

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

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1015(i2c)

# Create single-ended input on channel 0
chan = AnalogIn(ads, ADS.P0)



# The ID and range of a sample spreadsheet.
#BLYNK_AUTH = 'SHraFqInf27JKowTcFZapu0rHH2QGtuO' #atlasReservoir
BLYNK_AUTH = 'XVbhfI6ZYxkqFp7d4RsCIN6Is9YnKp9q' #atlasButt



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

# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH)

# Create BlynkTimer Instance
timer = BlynkTimer()

@blynk.on("V1")
def buttonV1Pressed(value):
    blynk.virtual_write(1, str(value[0]))
    if(value[0] == '1'):
        print("Waste turned off")
        GPIO.output(Relay1,GPIO.HIGH)
    else:
        print("Waste turned on")
        GPIO.output(Relay1,GPIO.LOW)
  

@blynk.on("V2")
def buttonV2Pressed(value):
    if(value[0] == '1'):
        print("Feed Pump turned off")
        GPIO.output(Relay2,GPIO.HIGH)
    else:
        print("Feed Pump turned on")
        GPIO.output(Relay2,GPIO.LOW)
  


@blynk.on("V3")
def buttonV3Pressed(value):
    if(value[0] == '1'):
        print("Air and Mixer turned off")
        GPIO.output(Relay3,GPIO.HIGH)
    else:
        print("Air and Mixer turned on")
        GPIO.output(Relay3,GPIO.LOW)
   

@blynk.on("V4")
def buttonV4Pressed(value):
    if(value[0] == '1'):
        print("Pump/UV turned off")
        GPIO.output(Relay4,GPIO.HIGH)
    else:
        print("Pump/UV turned on")
        GPIO.output(Relay4,GPIO.LOW)


        
@blynk.on("V30")
def buttonV30Pressed(value):
    print("Dose Pump 1 Button")
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
    print("Dose Line Fill")
    GPIO.output(Pump1,GPIO.LOW)
    GPIO.output(Pump2,GPIO.LOW)
    GPIO.output(Pump3,GPIO.LOW)
    GPIO.output(Pump4,GPIO.LOW)
    GPIO.output(Pump5,GPIO.LOW)
    GPIO.output(Pump6,GPIO.LOW)
    GPIO.output(Pump7,GPIO.LOW)
    GPIO.output(Pump8,GPIO.LOW)
    GPIO.output(Pump9,GPIO.LOW)
    GPIO.output(Pump10,GPIO.LOW)
       
@blynk.on("V70")
def buttonV70Pressed(value):
    print("Dose Line Stop All")
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

    
@blynk.on("connected")
def blynk_connected():
    # You can also use blynk.sync_virtual(pin)
    # to sync a specific virtual pin
    print("Updating values from the server...")
    for i in range(40): 
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
        
def turnOffNoisyThingsWhenButtEmpty(): 
    for Relay in noisyThingsWhenButtEmpty:
        GPIO.output(Relay,GPIO.HIGH)
      

# Will Print Every 10 Seconds
def blynk_data():

    now = datetime.now()
    blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))
    cTemp = temp.query("R,").split(":")[1]
    print("Temp = " + cTemp)
    blynk.virtual_write(20, cTemp)
    blynk.virtual_write(21, ec.query("RT,"+cTemp).split(":")[1])
    blynk.virtual_write(22, ph.query("RT,"+cTemp).split(":")[1])
    
   
    volt = chan.voltage
    if volt is not None:
       blynk.virtual_write(25, str("{0}".format((volt-1.5)*100)))
       blynk.virtual_write(26, str("{0:.2f}".format((volt-1.5)*12)))
    
    blynk.virtual_write(27, GPIO.input(buttEmptySensor))
    blynk.virtual_write(28, GPIO.input(buttFullSensor))
    
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


# Add Timers
timer.set_interval(10, blynk_data)



while True:
    try:
       blynk.run()
       timer.run()
    except:
        logger.error('We have a problem')
        os.system('sudo reboot')

