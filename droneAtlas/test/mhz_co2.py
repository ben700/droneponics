##!/usr/bin/env python3 
import mh_z19
import sys
import os

while True:
    os.write("sudo chmod 777 /dev/serial0")
    os.write("sudo chown pi:pi /dev/serial0")
    print(mh_z19.read()) 
