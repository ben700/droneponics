sys.path.append('/home/pi/droneponics')
import chirp
import time

# These values needs to be calibrated for the percentage to work!
# The highest and lowest value the individual sensor outputs.
min_moist = 240
max_moist = 790

# Initialize the sensor.
chirp = chirp.Chirp(address=0x20,
                    read_moist=True,
                    read_temp=True,
                    read_light=True,
                    min_moist=min_moist,
                    max_moist=max_moist,
                    temp_scale='celsius',
                    temp_offset=0)

try:
    print('Old I2C address:        {}\n'.format(chirp.sensor_address))
    chirp.sensor_address = new_address 
    time.sleep(1)
    print('New I2C address:        {}\n'.format(chirp.sensor_address))
    
except KeyboardInterrupt:
    print('\nCtrl-C Pressed! Exiting.\n')
finally:
    print('Bye!')
