from chirp import Chirp
import time
from datetime import datetime
import blynklib
import blynktimer
import logging
    
BLYNK_AUTH = 'n0OuchdtamBdO0V1X_3v3EIwBashSr4n' #envornmental
colours = {1: '#FF0000', 0: '#00FF00', 'OFFLINE': '#0000FF'}

addr = 0x20
min_moist = 240
max_moist = 750
highest_measurement = 0
lowest_measurement = 0
scale_sign = '°C'
        
blynk = blynklib.Blynk(BLYNK_AUTH)
timer = blynktimer.Timer()

# Will Print Every 10 Seconds
@timer.register(interval=10, run_once=False)
def blynk_data():
    highest_measurement = 0
    print("Now in Timer")
    now = datetime.now()
    blynk.virtual_write(1, now.strftime("%d/%m/%Y %H:%M:%S"))
    
    
    # Initialize the sensor.
    chirp = Chirp(address=addr,
                  read_moist=True,
                  read_temp=True,
                  read_light=True,
                  min_moist=min_moist,
                  max_moist=max_moist,
                  temp_scale='celsius',
                  temp_offset=0)
    
    chirp.trigger()
    output = '{:d} {:4.1f}% | {:3.1f}{} | {:d}'
    output = output.format(chirp.moist, chirp.moist_percent,
        chirp.temp, scale_sign, chirp.light)
    print(output)
            
    blynk.virtual_write(11, str(chirp.moist))
    blynk.virtual_write(12, str(chirp.moist_percent))
    blynk.virtual_write(13, str(chirp.temp))
    blynk.virtual_write(14, str(chirp.light))

    # Adjust max and min measurement variables, used for calibrating
    # the sensor and allow using moisture percentage.
    if (highest_measurement is not False):
        if chirp.moist > highest_measurement:
            highest_measurement = chirp.moist
        else:
            highest_measurement = chirp.moist
    if lowest_measurement is not False:    
        if chirp.moist < lowest_measurement:
            lowest_measurement = chirp.moist
        else:
            lowest_measurement = chirp.moist
    blynk.virtual_write(21, str(highest_measurement))
    blynk.virtual_write(22, str(lowest_measurement))
    
while True:
    blynk.run()
    timer.run()
