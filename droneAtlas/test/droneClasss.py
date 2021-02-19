import sys
import os
sys.path.append('/home/pi/droneponics/droneAtlas')
import drone
import json

sensorList = drone.SensorList()
payload = {}
sensorList.payload(payload)
serializedPayload= json.dumps(payload, sort_keys=False, indent=2)
print('publishing ' + str(serializedPayload))
