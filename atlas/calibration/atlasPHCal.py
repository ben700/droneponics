##!/usr/bin/env python3 
BLYNK_AUTH = 'SHraFqInf27JKowTcFZapu0rHH2QGtuO' #atlasMonitor

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

    answer = input("Are you sure you want to calibrate Temp, EC or pH? (y/n)")
    if answer is None or answer != 'y':
        _log.info("User Exit")
        quit()
  
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
                      cPH = ph.query("R,").split(":")[1]
                      while ( cPH != oPH):
                           oPH = cPH 
                           cPH = ph.query("R,").split(":")[1]
                           _log.info("Waiting for ph to be stable. It's now :" + str(cPH) + '\n')
                           
                      ph.query("Cal,clear")	
                      temp.query("Cal,mid,7.00")
                      
             if answer == 'y':
                 answer = input("Going to calibrate ph to low 4.00. Enter y when you are ready(y/n)")
                 if answer == 'y':
                      cPH = ph.query("R,").split(":")[1]
                      while ( cPH != oPH):
                           oPH = cPH 
                           cPH = ph.query("R,").split(":")[1]
                           _log.info("Waiting for ph to be stable. It's now :" + str(cPH) + '\n')
                      temp.query("Cal,low,4.00")
                      
             if answer == 'y':
                 answer = input("Going to calibrate ph to high 10.00. Enter y when you are ready(y/n)")
                 if answer == 'y':
                      cPH = ph.query("R,").split(":")[1]
                      while ( cPH != oPH):
                           oPH = cPH 
                           cPH = ph.query("R,").split(":")[1]
                           _log.info("Waiting for ph to be stable. It's now :" + str(cPH) + '\n')
                      temp.query("Cal,high,10.00")
                      
                      
        except:
            _log.info("Expected error: Use Atlas Error")
            
 
