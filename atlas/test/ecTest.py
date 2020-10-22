##!/usr/bin/env python3 
BLYNK_AUTH = 'SHraFqInf27JKowTcFZapu0rHH2QGtuO' #atlasMonitor

if True:
    import datetime
    import time
    import logging
    from datetime import datetime
    import sys
    import os
    sys.path.append('/home/pi/droneponics')
    from AtlasI2C import (
	    AtlasI2C
    )
    

    # tune console logging
    _log = logging.getLogger('BlynkLog')
    logFormatter = logging.Formatter("%(asctime)s [%(levelname)s]  %(message)s")
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    _log.addHandler(consoleHandler)
    _log.setLevel(logging.DEBUG)
	  
    # Initialize the sensor.
    try:
        ec = AtlasI2C(100)
        _log.info("sensor created")
    except:
        _log.info("Unexpected error: Atlas")
    else:
        try:	
             while True:
		reading =ec.sensor.query("R") 
		doseLogic = reading.split(":")[1].strip().rstrip('\x00')
                print("reading")
		print(reading)
		print("doseLogic")
		print(doseLogic)
		
		time.sleep(1)
                           
        except:
            _log.info("Expected error: Use Atlas EC Error")
