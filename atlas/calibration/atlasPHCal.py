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
             oPH = ph.query("R").split(":")[1]
             answer = input("Are you sure you want to calibrate PH (y/n)")
             if answer == 'y':
                 answer = input("Going to calibrate ph to mid 7.00. Enter y when you are ready(y/n)")
                 if answer == 'y':
                      cPH = ph.query("R").split(":")[1]
                      if ( cPH == oPH):
                           _log.info("Ph to be stable. It's now :" + str(cPH) + '\n')
                      while ( cPH != oPH):
                           oPH = cPH 
                           cPH = ph.query("R").split(":")[1]
                           _log.info("Waiting for ph to be stable. It's now :" + str(cPH) + '\n')
                           
                      ph.query("Cal,clear")
                      ph.query("T,19.5")
                      ph.query("Cal,mid,7.00")
                      
             if answer == 'y':
                 answer = input("Going to calibrate ph to low 4.00. Enter y when you are ready(y/n)")
                 if answer == 'y':
                      cPH = ph.query("R").split(":")[1]
                      while ( cPH != oPH):
                           oPH = cPH 
                           cPH = ph.query("R").split(":")[1]
                           _log.info("Waiting for ph to be stable. It's now :" + str(cPH) + '\n')
                      ph.query("Cal,low,4.00")
                      
             if answer == 'y':
                 answer = input("Going to calibrate ph to high 10.00. Enter y when you are ready(y/n)")
                 if answer == 'y':
                      cPH = ph.query("R").split(":")[1]
                      if ( cPH == oPH):
                           _log.info("Ph to be stable. It's now :" + str(cPH) + '\n')
                      while ( cPH != oPH):
                           oPH = cPH 
                           cPH = ph.query("R").split(":")[1]
                           _log.info("Waiting for ph to be stable. It's now :" + str(cPH) + '\n')
                      ph.query("Cal,high,10.00")
                      
                      
        except:
            _log.info("Expected error: Use Atlas Error")
            
 
