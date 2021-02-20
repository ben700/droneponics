##!/usr/bin/env python3 
import sys
import os
import mh_z19
sys.path.append('/home/pi/droneponics/droneAtlas')
import drone

while True:
    drone.noSUDO()
    print(mh_z19.read()) 
