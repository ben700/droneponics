import json
from devicePayload import  getDeviceStatePayload

stateJson = json.loads(getDeviceStatePayload())
serializedState= json.dumps(stateJson, sort_keys=False, indent=3)
print(serializedState)
print("The length of the json is " + str(len(serializedState)))
