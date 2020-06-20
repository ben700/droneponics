import drone
import logging
import sys
import os

_log = logging.getLogger('BlynkLog')
logFormatter = logging.Formatter("%(asctime)s [%(levelname)s]  %(message)s")
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
_log.addHandler(consoleHandler)
_log.setLevel(logging.DEBUG)


droneCounter = drone.DroneCounter()
droneCounter.setAutomatic()
droneCounter.reset(_log)
droneCounter.setOnCycle(_log, 3)
droneCounter.setOffCycle(_log, 2)

while True:
   if(droneCounter.isAutomatic(_log)):
            if (droneCounter.isItAnOnCycle(_log)):
                text = "Automatc : On"
                _log.info("Turn Relay ON") 
         #       GPIO.output(relays[1],GPIO.LOW)
                droneCounter.incOnCycle()
            else :
                text = "Automatc : Off"
                _log.info("Turn off RELAY")
          #      GPIO.output(relays[1],GPIO.HIGH)
                droneCounter.incOffCycle()
               
   _log.debug(text)
   droneCounter.incCycle(_log)
