from board import SCL, SDA
import busio
from adafruit_seesaw.seesaw import Seesaw
import time
from datetime import datetime
import RPi.GPIO as GPIO
import time, sys
import BlynkLib
from BlynkTimer import BlynkTimer
import Adafruit_ADS1x15


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#pHjiH8dnAW3NrkAPSNTcVKsfa7BAdnBP #soilogger3
#pHjiH8dnAW3NrkAPSNTcVKsfa7BAdnBP #soilogger2
#5P-DiNBQH6_YLNM1aqPEQjorV84i9rfG #soilogger1
#FnSZls3WUdCbWmDJvfnjz3f83Sm70HqI #envLogger2
#ZDy8p4aFPCKGwQhafv4jwUT6TpCY9CyP #envLogger1
#e06jzpI2zuRD4KB5eHyHdCQTGFT7einR #dfRobotControl
##XQuDhOorEscbMFLzbP1SOebbe39uXbA7 #envMonitor
#rHuhXZ97FK3_azBlFK1AC4pIPNUxgw7B #envControl
#BLYNK_AUTH = 'SHraFqInf27JKowTcFZapu0rHH2QGtuO' #atlasReservoir
BLYNK_AUTH = 'XVbhfI6ZYxkqFp7d4RsCIN6Is9YnKp9q' #atlasButt
#00vIt07mIauITIq4q_quTOakFvcvpgGb #dfRobotMonitor
#GP_sDPLJqyEN7jky9_zcQVSkgiyx-AeW #motherLights

waterLevel = 10 
waterFullLevel = 11


GPIO.setup(waterLevel,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(waterFullLevel,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


Relay1 = 8
Relay2 = 27
Relay3 = 13 
Relay4 = 25

GPIO.setup(Relay1,GPIO.OUT)
GPIO.setup(Relay2,GPIO.OUT)
GPIO.setup(Relay3,GPIO.OUT)
GPIO.setup(Relay4,GPIO.OUT)

GPIO.output(Relay1, GPIO.LOW)
GPIO.output(Relay2, GPIO.LOW)
GPIO.output(Relay3, GPIO.LOW)
GPIO.output(Relay4, GPIO.LOW)



adc = Adafruit_ADS1x15.ADS1115()
reading = adc.read_adc(0, gain=GAIN)
reading = (1023 / reading)  - 1
reading = 500 / reading;
print("Level = " + str(reading))

# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH)

# Create BlynkTimer Instance
timer = BlynkTimer()


@blynk.on("V1")
def buttonV1Pressed(value):
    if(value[0] == '1'):
        print("Relay1 turned on")
        GPIO.output(Relay1,GPIO.HIGH)
    else:
        print("Relay1 turned off")
        GPIO.output(Relay1,GPIO.LOW)


@blynk.on("V2")
def buttonV2Pressed(value):
    if(value[0] == '1'):
        print("Relay2 turned on")
        GPIO.output(Relay2,GPIO.HIGH)
    else:
        print("Relay2 turned off")
        GPIO.output(Relay2,GPIO.LOW)


@blynk.on("V3")
def buttonV3Pressed(value):
    if(value[0] == '1'):
        print("Relay3 turned on")
        GPIO.output(Relay3,GPIO.HIGH)
    else:
        print("Relay3 turned off")
        GPIO.output(Relay3,GPIO.LOW)


@blynk.on("V4")
def buttonV4Pressed(value):
    if(value[0] == '1'):
        print("Relay4 turned on")
        GPIO.output(Relay4,GPIO.HIGH)
    else:
        print("Relay4 turned off")
        GPIO.output(Relay4,GPIO.LOW)


@blynk.on("connected")
def blynk_connected():
    # You can also use blynk.sync_virtual(pin)
    # to sync a specific virtual pin
    print("Updating values from the server...")
    blynk.sync_virtual(1, 2, 3, 4, 20, 25, 26, 27)
    

    
# Will Print Every 10 Seconds
def blynk_data():
    now = datetime.now()
    blynk.virtual_write(20, now.strftime("%d/%m/%Y %H:%M:%S"))

    print("Time updated : " + now.strftime("%d/%m/%Y %H:%M:%S"))

    reading = adc.read_adc(0, gain=GAIN)
    reading = (1023 / reading)  - 1
    reading = 500 / reading;
    print("Level = " + str(reading))
    
    blynk.virtual_write(25, GPIO.input(waterLevel))
    blynk.virtual_write(26, GPIO.input(waterFullLevel))
    blynk.virtual_write(27, str(reading))
    


# Add Timers
timer.set_interval(10, blynk_data)


while True:
    blynk.run()
    timer.run()

