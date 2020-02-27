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

def print_devices(device_list, device):
    for i in device_list:
       blynk.virtual_write(i.address, 1 )         
        
def get_devices():
    device = AtlasI2C()
    device_address_list = device.list_i2c_devices()
    device_list = []
    
    for i in device_address_list:
        device.set_i2c_address(i)
        response = device.query("I")
        moduletype = response.split(",")[1] 
        response = device.query("name,?").split(",")[1]
        device_list.append(AtlasI2C(address = i, moduletype = moduletype, name = response))
    return device_list 




# The ID and range of a sample spreadsheet.
BLYNK_AUTH = 'SHraFqInf27JKowTcFZapu0rHH2QGtuO' #atlasReservoir
#BLYNK_AUTH = 'XVbhfI6ZYxkqFp7d4RsCIN6Is9YnKp9q' #atlasButt

# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH)

# Create BlynkTimer Instance
timer = BlynkTimer()

#61 - Dissolved Oxygen 97 (0x61)
#62 - OPR
#63 - PH    99 (0x63)
#64 - EC   100 (0x64)
#66 - Temp 102 (0x66)
#67 - pump
#68 - flow
#69 - co2
#70 - colour
#6A - pressure
device = AtlasI2C()
temp = AtlasI2C(102, "TEMP")
ec = AtlasI2C(100,"EC")
ph = AtlasI2C(99, "PH")
do = AtlasI2C(97, "DO")


print(device.list_i2c_devices())
print("Temp Device Info = " + temp.query("i")
print("pH Device Info = " + ph.query("i")
print("EC Device Info = " + ec.query("i")
#print("DO Device Info = " + ec.query("i")      

print("Temp Cal = " + temp.query("Cal,?")
print("Temp Scale = " + temp.query("S,?")
      
print("pH Cal = " + ph.query("Cal,?")
print("pH Temp Cal = " + ph.query("T,?")

print("EC Cal = " + ec.query("Cal,?")
print("EC Temp Cal = " + ec.query("Cal,?")
print("EC Probe Type = " + ec.query("K,?")

#print("DO Cal = " + do.query("Cal,?")     
#print("EC Temp Cal = " + do.query("Cal,?")
#print("DO Salinity Cal = " + do.query("S,?")
#print("DO Pressure Cal = " + do.query("P,?")
      
cTemp = temp.query("R,")
print("Temp = " + cTemp)
print("EC = " + ec.query("RT,"+cTemp))
print("PH = " + ph.query("RT,"+cTemp))
print("DO = " + d0.query("RT,"+cTemp))




# Will Print Every 10 Seconds
def blynk_data():

    now = datetime.now()
    blynk.virtual_write(3, now.strftime("%d/%m/%Y %H:%M:%S"))
    cTemp = temp.query("R,")
    print("Temp = " + cTemp)
    blynk.virtual_write(4, cTemp)
    blynk.virtual_write(5, ec.query("R,"))
    blynk.virtual_write(6, ph.query("R,"))



# Add Timers
timer.set_interval(10, blynk_data)



while True:
    blynk.run()
    timer.run()


