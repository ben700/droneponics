from board import SCL, SDA
import busio
from adafruit_seesaw.seesaw import Seesaw
import time
from datetime import datetime
import RPi.GPIO as GPIO
import time, sys
import BlynkLib
from BlynkTimer import BlynkTimer

BLYNK_GREEN     ="#23C48E"
BLYNK_BLUE      ="#04C0F8"
BLYNK_YELLOW    ="#ED9D00"
BLYNK_RED       ="#D3435C"
BLYNK_DARK_BLUE ="#5F7CD8"

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#e06jzpI2zuRD4KB5eHyHdCQTGFT7einR #dfRobotControl
BLYNK_AUTH = 'rHuhXZ97FK3_azBlFK1AC4pIPNUxgw7B' #envControl
#BLYNK_AUTH = 'SHraFqInf27JKowTcFZapu0rHH2QGtuO' #atlasReservoir
#BLYNK_AUTH = 'XVbhfI6ZYxkqFp7d4RsCIN6Is9YnKp9q' #atlasButt

Relay1 = 26 #waste
Relay2 = 19 #Feed
Relay3 = 13 #Air
Relay4 = 6  #Mixer - turned off with low water 


GPIO.setup(Relay1,GPIO.OUT)
GPIO.setup(Relay2,GPIO.OUT)
GPIO.setup(Relay3,GPIO.OUT)
GPIO.setup(Relay4,GPIO.OUT)


i2c_bus = busio.I2C(SCL, SDA)

ss1 = Seesaw(i2c_bus, addr=0x36)
ss2 = Seesaw(i2c_bus, addr=0x37)
ss3 = Seesaw(i2c_bus, addr=0x38)
ss4 = Seesaw(i2c_bus, addr=0x38)

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
    blynk.sync_virtual(1, 2, 3, 4)
    
    
def setLEDsonApp():    
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
    
    
    
# Will Print Every 10 Seconds
def blynk_data():
    now = datetime.now()
    blynk.virtual_write(0, now.strftime("%d/%m/%Y %H:%M:%S"))
    print("Time updated : " + now.strftime("%d/%m/%Y %H:%M:%S"))
    setLEDsonApp()
    if (ss1 is not None):
        blynk.virtual_write(11, str(ss1.moisture_read()))
        blynk.virtual_write(12, str(ss1.get_temp()))
        print ("Channel 1 moisture reading is "+str(ss1.moisture_read())+" and Temp is :" +  str("{0:.2f}".format(ss1.get_temp())))
    if (ss2 is not None):    
       blynk.virtual_write(13, str(ss2.moisture_read()))
       blynk.virtual_write(14, str(ss2.get_temp()))
       print ("Channel 2 moisture reading is "+str(ss2.moisture_read())+" and Temp is :" +  str("{0:.2f}".format(ss2.get_temp())))
    if (ss3 is not None):    
       blynk.virtual_write(15, str(ss3.moisture_read()))          
       blynk.virtual_write(16, str(ss3.get_temp()))
       print ("Channel 3 moisture reading is "+str(ss3.moisture_read())+" and Temp is :" +  str("{0:.2f}".format(ss3.get_temp())))
    if (ss4 is not None):    
       blynk.virtual_write(17, str(ss4.moisture_read()))
       blynk.virtual_write(18, str(ss4.get_temp()))
       print ("Channel 4 moisture reading is "+str(ss4.moisture_read())+" and Temp is :" +  str("{0:.2f}".format(ss4.get_temp())))
 


# Add Timers
timer.set_interval(10, blynk_data)

        
while True:
    blynk.run()
    timer.run()

