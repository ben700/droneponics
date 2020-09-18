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
    
    # Initialize the sensor.
    try:
       # Create the I2C bus
       pump = AtlasI2C(0x10)
       _log.info(pump.query("I2C,11"))
       
       pump = AtlasI2C(0x11)
       _log.info(pump.query("I2C,12"))
       
        pump = AtlasI2C(0x12)
       _log.info(pump.query("I2C,13"))
       
       pump = AtlasI2C(0x13)
       _log.info(pump.query("I2C,14"))
       
       pump = AtlasI2C(0x14)
       _log.info(pump.query("I2C,15"))
       
       pump = AtlasI2C(0x15)
       _log.info(pump.query("I2C,16"))
	
       pump = AtlasI2C(0x16)
       _log.info(pump.query("I2C,17"))
    except:
        _log.info("Unexpected error: Atlas")
    
