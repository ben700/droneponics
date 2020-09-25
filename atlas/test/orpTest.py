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
        orp = AtlasI2C(98)
        _log.info("sensor created")
    except:
        _log.info("Unexpected error: Atlas")
    else:
        try:	
             oORP = None
             cORP = orp.query("R").split(":")[1]
             while ( cORP != oORP):
                 oORP = cORP
                 time.sleep(1)
                 cORP = orp.query("R").split(":")[1]
                 _log.info("Waiting for ORP to be stable. It's now :" + str(cORP) + '\n')
                           
        except:
            _log.info("Expected error: Use Atlas ORP Error")