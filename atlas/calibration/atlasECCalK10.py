##!/usr/bin/env python3 
if True:
    import datetime
    import time
    import shlex, requests
    import logging
    from datetime import datetime
    import sys
    import os
    sys.path.append('/home/pi/droneponics')
    from AtlasI2C import (
	    AtlasI2C
    )
    import blynklib
    import blynktimer
    
    import subprocess
    import re

    # tune console logging
    _log = logging.getLogger('BlynkLog')
    logFormatter = logging.Formatter("%(asctime)s [%(levelname)s]  %(message)s")
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    _log.addHandler(consoleHandler)
    _log.setLevel(logging.DEBUG)


    # Initialize the sensor.
    try:
        temp = AtlasI2C(102)
        ec = AtlasI2C(100)
        ph = AtlasI2C(99)

        _log.info("sensor created")
    except:
        _log.info("Unexpected error: Atlas")
    else:
        try:	
             oEC = ec.query("R").split(":")[1]
             answer = input("Are you sure you want to calibrate EC (y/n)")
             if answer == 'y':
                 answer = input("Going to calibrate ec DRY. Enter y when you are ready(y/n)")
                 if answer == 'y':
                      cEC = ec.query("R").split(":")[1]
                      while ( cEC != oEC):
                           oEC = cEC 
                           cEC = ec.query("R").split(":")[1]
                           _log.info("Waiting for EC to be stable. It's now :" + str(cEC) + '\n')
                           
                      ec.query("Cal,clear")
                      ec.query("K,10")
                      ec.query("T,19.5")
                      ec.query("Cal,dry")
                      
             if answer == 'y':
                 answer = input("Going to calibrate EC to low 12,880. Enter y when you are ready(y/n)")
                 if answer == 'y':
                      cEC = ec.query("R").split(":")[1]
                      while ( cEC != oEC):
                           oEC = cEC 
                           cEC = ec.query("R").split(":")[1]
                           _log.info("Waiting for EC to be stable. It's now :" + str(cEC) + '\n')
                      ec.query("Cal,low,12880")
                      
             if answer == 'y':
                 answer = input("Going to calibrate ph to high 150000. Enter y when you are ready(y/n)")
                 if answer == 'y':
                      cEC = ec.query("R").split(":")[1]
                      while ( cEC != oEC):
                           oEC = cEC 
                           cEC = ec.query("R").split(":")[1]
                           _log.info("Waiting for EC to be stable. It's now :" + str(cEC) + '\n')
                      ec.query("Cal,high,150000")
                      
                      
        except:
            _log.info("Expected error: Use Atlas Error")
            
 
