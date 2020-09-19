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
    import drone


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
             oTemp = temp.query("R,").split(":")[1]
             answer = input("Are you sure you want to calibrate Temprature (y/n)")
             if answer == 'y':
                 aTemp = input("What Temprate is it?")
                 answer = input("Going to calibrate temprature. Sensor is now at [" + str(aTemp) + "]. Enter y when you are ready(y/n)")
                 if answer == 'y':
                      cTemp = temp.query("R,").split(":")[1]
                      while ( cTemp != oTemp):
                           oTemp = cTemp 
                           cTemp = temp.query("R,").split(":")[1]
                           _log.info("Waiting for temp to be stable. It's now :" + str(cTemp) + '\n')
                           
                      temp.query("Cal,clear")	
                      temp.query("S,c")
                      temp.query("Cal,"+str(aTemp))
                      _log.info("Temprature Calibrated")
		   
        except:
            _log.info("Expected error: Use Atlas Error")
            
 
