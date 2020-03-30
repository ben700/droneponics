##!/usr/bin/env python3 
BLYNK_AUTH = 'SHraFqInf27JKowTcFZapu0rHH2QGtuO' #atlasMonitor

try:
    import datetime
    import time
    import shlex, requests
    import blynklib
    import blynktimer
    import logging
    from datetime import datetime
    import sys
    import os
   
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
        _log.info("sensor created")
    except:
        _log.info("Unexpected error: Atlas")
    else:
        try:	
             oTemp = -999
             cTemp = temp.query("R,").split(":")[1]
             while ( cTemp != oTemp):
                 oTemp = cTemp
                 time.sleep(1)
                 cTemp = temp.query("R,").split(":")[1]
                 _log.info("Waiting for temp to be stable. It's now :" + str(cTemp) + '\n')
                           
        except:
            _log.info("Expected error: Use Atlas Error")
            
  
except:
   print('Unexpected error')
