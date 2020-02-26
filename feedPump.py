from board import SCL, SDA
import busio
from adafruit_seesaw.seesaw import Seesaw
import time
from datetime import datetime
import RPi.GPIO as GPIO
import time, sys
import BlynkLib
from BlynkTimer import BlynkTimer
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
BLYNK_AUTH = 'SHraFqInf27JKowTcFZapu0rHH2QGtuO' #atlasReservoir
#XVbhfI6ZYxkqFp7d4RsCIN6Is9YnKp9q #atlasButt
#00vIt07mIauITIq4q_quTOakFvcvpgGb #dfRobotMonitor
#GP_sDPLJqyEN7jky9_zcQVSkgiyx-AeW #motherLights

sensorFlowmeterPinPump1       = 9
sensorFlowmeterPinPump2       = 11
sensorFlowmeterPinPump3       = 17
sensorFlowmeterPinPump4       = 18
waterLevel = 10 

GPIO.setup(sensorFlowmeterPinPump1,GPIO.IN)
GPIO.setup(sensorFlowmeterPinPump2,GPIO.IN)
GPIO.setup(sensorFlowmeterPinPump3,GPIO.IN)
GPIO.setup(sensorFlowmeterPinPump4,GPIO.IN)
GPIO.setup(waterLevel,GPIO.IN)


Pump1 = 8
Pump2 = 27
Pump3 = 13 
Pump4 = 25
Pump1Backup = 7
Pump2Backup = 21
Pump3Backup = 26
Pump4Backup = 16

GPIO.setup(Pump1,GPIO.OUT)
GPIO.setup(Pump2,GPIO.OUT)
GPIO.setup(Pump3,GPIO.OUT)
GPIO.setup(Pump4,GPIO.OUT)

GPIO.output(Pump1, GPIO.LOW)
GPIO.output(Pump2, GPIO.LOW)
GPIO.output(Pump3, GPIO.LOW)
GPIO.output(Pump4, GPIO.LOW)

GPIO.setup(Pump1Backup,GPIO.OUT)
GPIO.setup(Pump2Backup,GPIO.OUT)
GPIO.setup(Pump3Backup,GPIO.OUT)
GPIO.setup(Pump4Backup,GPIO.OUT)


GPIO.output(Pump1Backup, GPIO.LOW)
GPIO.output(Pump2Backup, GPIO.LOW)
GPIO.output(Pump3Backup, GPIO.LOW)
GPIO.output(Pump4Backup, GPIO.LOW)


i2c_bus = busio.I2C(SCL, SDA)

ss1 = Seesaw(i2c_bus, addr=0x36)
ss2 = Seesaw(i2c_bus, addr=0x37)
ss3 = Seesaw(i2c_bus, addr=0x38)
ss4 = Seesaw(i2c_bus, addr=0x38)

# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH)

# Create BlynkTimer Instance
timer = BlynkTimer()


# Will Print Every 10 Seconds
def blynk_data():
    now = datetime.now()
    blynk.virtual_write(20, now.strftime("%d/%m/%Y %H:%M:%S"))

   
    print("Time updated : " + now.strftime("%d/%m/%Y %H:%M:%S"))
    print("Moisture plat 1 = " + str(ss1.moisture_read()))
    
    blynk.virtual_write(21, GPIO.input(sensorFlowmeterPinPump1))
    blynk.virtual_write(22, GPIO.input(sensorFlowmeterPinPump2))
    blynk.virtual_write(23, GPIO.input(sensorFlowmeterPinPump3))
    blynk.virtual_write(24, GPIO.input(sensorFlowmeterPinPump4))
    blynk.virtual_write(25, GPIO.input(waterLevel))
    
    blynk.virtual_write(11, str(ss1.moisture_read()))
    blynk.virtual_write(12, str(ss1.get_temp()))
    blynk.virtual_write(13, str(ss2.moisture_read()))
    blynk.virtual_write(14, str(ss2.get_temp()))
    blynk.virtual_write(15, str(ss3.moisture_read()))          
    blynk.virtual_write(16, str(ss3.get_temp()))
    blynk.virtual_write(17, str(ss4.moisture_read()))
    blynk.virtual_write(18, str(ss4.get_temp()))
    
    


# Add Timers
timer.set_interval(10, blynk_data)


while True:
    blynk.run()
    timer.run()

