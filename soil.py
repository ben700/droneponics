from chirp import Chirp
import time
from datetime import datetime
import blynklib
import blynktimer
import logging
    
BLYNK_AUTH = 'n0OuchdtamBdO0V1X_3v3EIwBashSr4n' #envornmental
colours = {1: '#FF0000', 0: '#00FF00', 'OFFLINE': '#0000FF'}

# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH)

# Create BlynkTimer Instance
timer = BlynkTimer()

# Will Print Every 10 Seconds
def blynk_data():
    now = datetime.now()
    blynk.virtual_write(1, now.strftime("%d/%m/%Y %H:%M:%S"))
    
    chirp = Chirp(1, 0x20)
    print ("%d\t%d\t%d" % (chirp.moist(), chirp.temp(), chirp.light()))
    
    blynk.virtual_write(11, str(chirp.moist()))
    blynk.virtual_write(12, str(chirp.temp()))
    blynk.virtual_write(12, str(chirp.light()))


# Add Timers
timer.set_interval(10, blynk_data)


while True:
    blynk.run()
    timer.run()
