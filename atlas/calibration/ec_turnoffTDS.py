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
        ec = AtlasI2C(100)

        _log.info("sensor created")
    except:
        _log.info("Unexpected error: Atlas")
    else:
        try:	
             print (ec.query("O,TDS,1"))
             
                      
                      
        except:
            _log.info("Expected error: Use Atlas Error")
            
 
