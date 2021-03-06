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
        temp = AtlasI2C(102)
        _log.info("Temp Sensor Info = " + temp.query("i"))
        _log.info("Temp Sensor Calibration = " + temp.query("cal,?"))
        _log.info("Temp Sensor Status = " + temp.query("Status"))
        _log.info("Temp Sensor Scale = " + temp.query("S,?"))
    except:
        _log.info("Unexpected error: Atlas")
    else:
        try:	
             oTemp = -999
             cTemp = temp.query("R").split(":")[1]
             while ( cTemp != oTemp):
                 oTemp = cTemp
                 time.sleep(1)
                 cTemp = temp.query("R").split(":")[1]
                 _log.info("Waiting for temp to be stable. It's now :" + str(cTemp) + '\n')
                           
        except:
            _log.info("Expected error: Use Atlas Error")

