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
#device = AtlasI2C()
#temp = AtlasI2C(102)
#ec = AtlasI2C(100)
#ph = AtlasI2C(99)
#do = AtlasI2C(97, "DO")
#flow = AtlasI2C(104, "FLOW")
#pump = AtlasI2C(103, "PUMP")


answer = input("Are you sure you want to calibrate (y/n)")
if answer is None or answer != 'y':
    break

#print(device.list_i2c_devices())
#print("Temp Device Info = " + temp.query("i"))
#print("pH Device Info = " + ph.query("i"))
#print("EC Device Info = " + ec.query("i"))
#print("DO Device Info = " + ec.query("i")) 
#print("Flow Device Info = " + flow.query("i"))      
#print("Pump Device Info = " + pump.query("i"))      

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
 
    
    
#print("Pump Cal = " + pump.query("Cal,?"))
#print("Pump Dispense Status = " + pump.query("D,?"))
#print("Pump maximum possible flow rate = " + pump.query("DC,?")) # maximum flow rate is determined after calibration.
#print("Pump Pause Status = " + pump.query("P,?"))
#print("Pump total volume dispensed = " + pump.query("TV,?")) #shows total volume dispensed  
#print("Pump absolute value of the total volume dispensed  = " + pump.query("ATV,?")) #absolute value of the total volume dispensed 
        
       
#temp.query("Cal,clear")
#temp.query("Cal,36.4") #t = any temperature
#print("Temp = " + str(temp.query("R")))      

#ec.query("Cal,clear")
#ec.query("K,0.1")
#ec.query("T,15.4")
#ec.query("Cal,dry") #dry calibration
#ec.query("Cal,n") #single point calibration, where n = any value
#ec.query("Cal,low,84") #low end calibration, where n = any value
#ec.query("Cal,high,1413") #high end calibration, where n = any value
#print("ec = " + str(ec.query("R")))


#ph.query("Cal,clear")
#ph.query("T,15.4")
#ph.query("Cal,mid,7") #single point calibration at midpoint
#ph.query("Cal,low,4")   #two point calibration at lowpoint
#ph.query("Cal,high,10") #three point calibration at highpoint 
#print("ph = " + str(ph.query("R")))
      
      
#do.query("Cal,clear")
#do.query("Cal") #calibrate to atmospheric oxygen levels
#do.query("Cal,0") #calibrate device to 0 dissolved oxygen

#flow.query("Frp,s") #calculate flow rate per second
#flow.query("Frp,m") #calculate flow rate per min
#flow.query("Frp,h") #calculate flow rate per hour
#flow.query("Clear") #Clearing the total volume
#flow.query("Set,3/8") #set to 3/8” flow meter
#flow.query("Set,1/4") #set to 1/4” flow meter
#flow.query("Set,1/2") #set to 1/2” flow meter
#flow.query("Set,3/4") #set to 3/4” flow meter
#flow.query("K,clear") #clear all programmed K-values
#flow.query("K,0.36666,1") #for flow meters with 1 K value
      
#pump.query("Clear")  #clears the total dispensed volume     
#pump.query("Cal,clear") #delete calibration data
#pump.query("D,10") #Dose 10ml
#pump.query("Cal,v") #v = corrected volume
#pump.query("D,10,10") #Dose 10ml over 10min
#pump.query("Cal,v") #v = corrected volume

