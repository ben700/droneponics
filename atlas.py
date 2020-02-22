##!/usr/bin/env python3 

import BlynkLib
from BlynkTimer import BlynkTimer
from datetime import datetime
import ArlasI2C


# The ID and range of a sample spreadsheet.
BLYNK_AUTH = 'SHraFqInf27JKowTcFZapu0rHH2QGtuO' #atlasReservoir
#BLYNK_AUTH = 'XVbhfI6ZYxkqFp7d4RsCIN6Is9YnKp9q' #atlasButt

# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH)

# Create BlynkTimer Instance
timer = BlynkTimer()


# Will Print Every 10 Seconds
def blynk_data():

    now = datetime.now()
    blynk.virtual_write(3, now.strftime("%d/%m/%Y %H:%M:%S"))
    


# Add Timers
timer.set_interval(10, blynk_data)


device = AtlasI2C()
temp = AtlasI2C(102, "EC")
ec = AtlasI2C(100,"PH")
ph = AtlasI2C(99, "TEMP")
print(device.list_i2c_devices())
print(temp.query("R,"))

while True:
    blynk.run()
    timer.run()


