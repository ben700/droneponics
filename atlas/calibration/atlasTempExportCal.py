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
    import drone

    class Counter:
        cycle = 0

    f = open("tempCal.txt", "w")
    
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

        _log.info("sensor created")
    except:
        _log.info("Unexpected error: Atlas")
    else:
        try:	
             x = int(temp.query("Export,?").split(",")[1])
             print(temp.query("Export,?"))
             x =x+1
             for i in range(x):
                y = temp.query("Export").split(":")[1].strip().rstrip('^@')	
                y = y.split('^')[0]
                f.write(y + '\n')
                print(y)
             f.close()
	   
        except:
            _log.info("Expected error: Use Atlas Error")
            
 
