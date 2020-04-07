from drone import * 
class Relay:
   def __init__(self, PinId, Led, Name, Button, *args, **kwargs)):
       print("Building object")
       self.pinId = PinId
       self.LED = Led
       self.name = Name
       self.button = Button
       self.noisy = kwargs.get('Noisy', False)
       
def buildRelay(relays, _log): 
    relays.append( Relay(26, LED[1], "Air", 1, Noisy=True))
    relays.append( Relay(13, LED[2], "Mixer", 2, Noisy=True))
    relays.append( Relay(21, LED[3], "Heater", 3, Noisy=True))
    relays.append( Relay(27, LED[4], "Other", 4))
    return relays
