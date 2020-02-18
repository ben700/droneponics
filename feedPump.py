import time
from datetime import datetime
import RPi.GPIO as GPIO
import time, sys
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

#pHjiH8dnAW3NrkAPSNTcVKsfa7BAdnBP #soilogger3
#pHjiH8dnAW3NrkAPSNTcVKsfa7BAdnBP #soilogger2
#5P-DiNBQH6_YLNM1aqPEQjorV84i9rfG #soilogger1
#FnSZls3WUdCbWmDJvfnjz3f83Sm70HqI #envLogger2
#ZDy8p4aFPCKGwQhafv4jwUT6TpCY9CyP #envLogger1
#e06jzpI2zuRD4KB5eHyHdCQTGFT7einR #dfRobotControl
##XQuDhOorEscbMFLzbP1SOebbe39uXbA7 #envMonitor
#rHuhXZ97FK3_azBlFK1AC4pIPNUxgw7B #envControl
SHraFqInf27JKowTcFZapu0rHH2QGtuO #atlasReservoir
#XVbhfI6ZYxkqFp7d4RsCIN6Is9YnKp9q #atlasButt
#00vIt07mIauITIq4q_quTOakFvcvpgGb #dfRobotMonitor
#GP_sDPLJqyEN7jky9_zcQVSkgiyx-AeW #motherLights

sensorFlowmeterPinPump1       = 23
sensorFlowmeterPinPump2       = 22
sensorFlowmeterPinPump3       = 27
sensorFlowmeterPinPump4       = 28

GPIO.setup(sensorFlowmeterPinPump1,GPIO.IN)
GPIO.setup(sensorFlowmeterPinPump2,GPIO.IN)
GPIO.setup(sensorFlowmeterPinPump3,GPIO.IN)
GPIO.setup(sensorFlowmeterPinPump4,GPIO.IN)



Pump1Flow = 0
Pump2Flow = 0
Pump3Flow = 0
Pump4Flow = 0
Pump1BackupFlow = 0
Pump2BackupFlow = 0
Pump3BackupFlow = 0
Pump4BackupFlow = 0


Pump1 = 27
Pump2 = 21
Pump3 = 13 
Pump4 = 26
Pump1Backup = 25
Pump2Backup = 16
Pump3Backup = 20
Pump4Backup = 19

GPIO.setup(Pump1,GPIO.OUT)
GPIO.setup(Pump2,GPIO.OUT)
GPIO.setup(Pump3,GPIO.OUT)
GPIO.setup(Pump4,GPIO.OUT)

GPIO.setup(Pump1Backup,GPIO.OUT)
GPIO.setup(Pump2Backup,GPIO.OUT)
GPIO.setup(Pump3Backup,GPIO.OUT)
GPIO.setup(Pump4Backup,GPIO.OUT)



# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH)

# Create BlynkTimer Instance
timer = BlynkTimer()


# Will Print Every 10 Seconds
def blynk_data():
    now = datetime.now()
    blynk.virtual_write(20, now.strftime("%d/%m/%Y %H:%M:%S"))
    print(GPIO.input(sensorFlowmeterPinPump1))
    print(GPIO.input(sensorFlowmeterPinPump2))
    print(GPIO.input(sensorFlowmeterPinPump3))
    print(GPIO.input(sensorFlowmeterPinPump4))
    
    Pump1Flow = GPIO.ouput(Pump1)
    
    print(Pump1Flow)
    print(GPIO.ouput(Pump2))
    print(GPIO.ouput(Pump3))
    print(GPIO.ouput(Pump4))

    print(GPIO.ouput(Pump1Backup))
    print(GPIO.ouput(Pump2Backup))
    print(GPIO.ouput(Pump3Backup))
    print(GPIO.ouput(Pump4Backup))

    
    blynk.virtual_write(21, GPIO.input(sensorFlowmeterPinPump1))
    blynk.virtual_write(22, GPIO.input(sensorFlowmeterPinPump2))
    blynk.virtual_write(23, GPIO.input(sensorFlowmeterPinPump3))
    blynk.virtual_write(24, GPIO.input(sensorFlowmeterPinPump4))


# Add Timers
timer.set_interval(10, blynk_data)


while True:
    blynk.run()
    timer.run()

