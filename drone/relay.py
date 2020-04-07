from drone import * 
class Relay:
   def __init__(self, PinId, Led, Name):
       print("Building object")
       self.pinId = PinId
       self.LED = Led
       self.name = Name
       
def buildRelay(relays, _log): 
    relays.append( Relay(26, LED[1], "Air"))
    relays.append( Relay(13, LED[2], "Mixer"))
    relays.append( Relay(21, LED[3], "Heater"))
    relays.append( Relay(27, LED[4], "Other"))
    return relays
