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
        if(i == device):
            print("--> " + i.get_device_info())
        else:
            print(" - " + i.get_device_info())
            
for n in range (10):
    i = 0
    x = 0
    while (i ==0):
        device = AtlasI2C()
        device_address_list = device.list_i2c_devices()
        i = len(device_address_list)
        if(i==0):
            x=x+1
            continue
        output = "On test cycle " + str(n) +" Found " + str(i) + " and that took " + str(x) + " trys. Ids of atlas devices found ar$
        for y in device_address_list:
            output += str(y) + ","
        print(output[0:-1])
