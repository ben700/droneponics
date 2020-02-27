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
      
#temp.query("Cal,clear")
#temp.query("Cal,t") #t = any temperature
      

#ec.query("Cal,clear")
#ec.query("Cal,dry") #dry calibration
#ec.query("Cal,n") #single point calibration, where n = any value
#ec.query("Cal,low,n") #low end calibration, where n = any value
#ec.query("Cal,high,n") #high end calibration, where n = any value



#ph.query("Cal,clear")
#ph.query("Cal,mid,7") #single point calibration at midpoint
#ph.query("Cal,low,4")   #two point calibration at lowpoint
#ph.query("Cal,high,10") #three point calibration at highpoint 
      
      
      
      
#do.query("Cal,clear")
#do.query("Cal") #calibrate to atmospheric oxygen levels
#do.query("Cal,0") #calibrate device to 0 dissolved oxygen

