##!/usr/bin/env python3 

if True:
    import datetime
    import time
    import shlex, requests
    import logging
    from datetime import datetime
    import sys
    import os
    import RPi.GPIO as GPIO
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
    pumps = [11,12,13,14,15]
	     
    # Initialize the sensor.
    try:
       for pumpId in pumps: 		
           # Create the I2C bus
           pump = AtlasI2C(pumpId)
           _log.info(pump.query("I"))
    except:
        _log.info("Unexpected error: Atlas")
    
