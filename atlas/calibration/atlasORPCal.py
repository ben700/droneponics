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

    answer = input("Are you sure you want to calibrate ORP? (y/n)")
    if answer is None or answer != 'y':
        _log.info("User Exit")
        quit()
  
    # Initialize the sensor.
    try:
        orp = AtlasI2C(98)
        _log.info("sensor created")
    except:
        _log.info("Unexpected error: Atlas")
    else:
        if True:	
             oORP = orp.query("R").split(":")[1].strip().rstrip('\x00')
             answer = input("Are you sure you want to calibrate ORP (y/n)")
             if answer == 'y':
                 answer = input("Going to calibrate ORP to 225 oxidation/reduction potential. Enter y when you are ready(y/n)")
                 if answer == 'y':
                      orp.query("Cal,clear")
                      cORP = orp.query("R").split(":")[1].strip().rstrip('\x00')
                      while ( cORP != oORP):
                           oORP = cORP 
                           cORP = orp.query("R").split(":")[1].strip().rstrip('\x00')
                           _log.info("Waiting for ORP to be stable. It's now :" + str(cORP) + '\n')
                      orp.query("Cal,225")
                      
      
            
 
