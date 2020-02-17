import time

from board import SCL, SDA
import busio

from adafruit_seesaw.seesaw import Seesaw
from datetime import datetime

#pHjiH8dnAW3NrkAPSNTcVKsfa7BAdnBP #soilogger3
#pHjiH8dnAW3NrkAPSNTcVKsfa7BAdnBP #soilogger2
5P-DiNBQH6_YLNM1aqPEQjorV84i9rfG #soilogger1
#FnSZls3WUdCbWmDJvfnjz3f83Sm70HqI #envLogger2
#ZDy8p4aFPCKGwQhafv4jwUT6TpCY9CyP #envLogger1
#e06jzpI2zuRD4KB5eHyHdCQTGFT7einR #dfRobotControl
##XQuDhOorEscbMFLzbP1SOebbe39uXbA7 #envMonitor
#rHuhXZ97FK3_azBlFK1AC4pIPNUxgw7B #envControl
#SHraFqInf27JKowTcFZapu0rHH2QGtuO #atlasReservoir
#XVbhfI6ZYxkqFp7d4RsCIN6Is9YnKp9q #atlasButt
#00vIt07mIauITIq4q_quTOakFvcvpgGb #dfRobotMonitor
#GP_sDPLJqyEN7jky9_zcQVSkgiyx-AeW #motherLights


# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH)

# Create BlynkTimer Instance
timer = BlynkTimer()

i2c_bus = busio.I2C(SCL, SDA)

ss1 = Seesaw(i2c_bus, addr=0x36)
ss2 = Seesaw(i2c_bus, addr=0x37)
ss3 = Seesaw(i2c_bus, addr=0x38)
ss4 = Seesaw(i2c_bus, addr=0x38)

# Will Print Every 10 Seconds
def blynk_data():
    now = datetime.now()
    blynk.virtual_write(10, now.strftime("%d/%m/%Y %H:%M:%S"))
    blynk.virtual_write(11, str(s1.moisture_read()))
    blynk.virtual_write(12, str(s2.get_temp()))
    blynk.virtual_write(13, str(s2.moisture_read()))
    blynk.virtual_write(14, str(s2.get_temp()))
    blynk.virtual_write(15, str(s3.moisture_read()))          
    blynk.virtual_write(16, str(s3.get_temp()))
    blynk.virtual_write(17, str(s4.moisture_read()))
    blynk.virtual_write(18, str(s4.get_temp()))
    


# Add Timers
timer.set_interval(10, blynk_data)


while True:
    blynk.run()
    timer.run()

