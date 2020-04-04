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
        colour = AtlasI2C(112)
        _log.info("sensor created")
	_log.info("sensor created")
    except:
        _log.info("Unexpected error: Atlas")
    else:
        try:	
             oColour = colour.query("R").split(":")[1]
             answer = input("Are you sure you want to calibrate colour (y/n)")
             if answer == 'y':
                  answer = input("Going to calibrate colour. Is white object in front of target. Enter y when you are ready(y/n)")
                  if answer == 'y':
                      cColour = colour.query("R").split(":")[1]
                      while ( cColour != oColour):
                           oColour = cColour 
                           cColour = colour.query("R").split(":")[1]
                           _log.info("Waiting for colour to be stable. It's now :" + str(cColour) + '\n')
                           
                      colour.query("Cal,clear")	
                      colour.query("G,1")	
                      colour.query("L,100,T")	
                      
                      colour.query("Cal")
                      _log.info("Colour Calibrated")
		   
        except:
            _log.info("Expected error: Use Atlas Error")
            
 
