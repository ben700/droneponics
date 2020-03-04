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
#BLYNK_AUTH = 'SHraFqInf27JKowTcFZapu0rHH2QGtuO' #atlasReservoir
BLYNK_AUTH = 'XVbhfI6ZYxkqFp7d4RsCIN6Is9YnKp9q' #atlasButt

# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH)

# Create BlynkTimer Instance
timer = BlynkTimer()

#61 - Dissolved Oxygen 97 (0x61)
#62 - OPR
#63 - PH    99 (0x63)
#64 - EC   100 (0x64)
#66 - Temp 102 (0x66)
#67 - pump 103 (0x67)
#68 - flow 104 (0x68)
#69 - co2
#70 - colour 112 (0x70)
#6A - pressure
device = AtlasI2C()
temp = AtlasI2C(102)
ec = AtlasI2C(100)
ph = AtlasI2C(99)
#do = AtlasI2C(97, "DO")
#flow = AtlasI2C(104, "FLOW")
#pump = AtlasI2C(103, "PUMP")

#print(device.list_i2c_devices())
#print("Temp Device Info = " + temp.query("i"))
#print("pH Device Info = " + ph.query("i"))
#print("EC Device Info = " + ec.query("i"))
#print("DO Device Info = " + do.query("i"))      
#print("Flow Device Info = " + flow.query("i"))      

      
#print("Temp Cal = " + temp.query("Cal,?"))
#print("Temp Scale = " + temp.query("S,?"))
      
#print("pH Cal = " + ph.query("Cal,?"))
#print("pH Temp Cal = " + ph.query("T,?"))

#print("EC Cal = " + ec.query("Cal,?"))
#print("EC Temp Cal = " + ec.query("Cal,?"))
#print("EC Probe Type = " + ec.query("K,?"))

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




# Will Print Every 10 Seconds
def blynk_data():

    now = datetime.now()
    blynk.virtual_write(3, now.strftime("%d/%m/%Y %H:%M:%S"))
    cTemp = temp.query("R,").split(":")[1]
    print("Temp = " + cTemp)
    blynk.virtual_write(4, cTemp)
    blynk.virtual_write(5, ec.query("RT,"+cTemp).split(":")[1])
    blynk.virtual_write(6, ph.query("RT,"+cTemp).split(":")[1])



# Add Timers
timer.set_interval(10, blynk_data)



while True:
    blynk.run()
    timer.run()


