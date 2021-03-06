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
        do = AtlasI2C(97)
        _log.info("sensor created")
    except:
        _log.info("Unexpected error: Atlas")
    else:
        if True:	
             oDO = do.query("R").split(":")[1].strip().rstrip('\x00')
             answer = input("Are you sure you want to calibrate DO (y/n)")
             if answer == 'y':
                 answer = input("Going to calibrate DO to atmospheric oxygen levels. Enter y when you are ready(y/n)")
                 if answer == 'y':
                      cDO = do.query("R").split(":")[1].strip().rstrip('\x00')
                      while ( cDO != oDO):
                           oDO = cDO 
                           cDO = do.query("R").split(":")[1].strip().rstrip('\x00')
                           _log.info("Waiting for DO to be stable. It's now :" + str(cDO) + '\n')
                           
                      do.query("Cal,clear")
                      do.query("T,19.5")
                      do.query("P,97.879")
                      do.query("S,0")
                      do.query("Cal")
                      
             if answer == 'y':
                 answer = input("Going to calibrate DO to  0 dissolved oxygen. Enter y when you are ready(y/n)")
                 if answer == 'y':
                      cDO = do.query("R").split(":")[1].strip().rstrip('\x00')
                      while ( cDO != oDO):
                           oDO = cDO 
                           cDO = do.query("R").split(":")[1].strip().rstrip('\x00')
                           _log.info("Waiting for DO to be stable. It's now :" + str(cDO) + '\n')
                      do.query("Cal,0")
                      
      
            
 
