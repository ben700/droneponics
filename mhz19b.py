import mh_z19
import BlynkLib
from BlynkTimer import BlynkTimer

BLYNK_AUTH = 'ZDy8p4aFPCKGwQhafv4jwUT6TpCY9CyP'

# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH)

# Create BlynkTimer Instance
timer = BlynkTimer() 
    
    
# Will Print Every 5 Seconds
def blynk_data():
    mhz19b = mh_z19.read()
    blynk.virtual_write(11, mhz19b['co2'])
    
   
# Add Timers
timer.set_interval(10, blynk_data)


while True:
    blynk.run()
    timer.run()

