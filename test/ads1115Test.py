import time
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1015(i2c, address=0x40)
# Create single-ended input on channel 0
#chan = AnalogIn(ads, ADS.P0)

# Create differential input between channel 0 and 1
chan = AnalogIn(ads, ADS.P0, ADS.P1)

print("{:>5}\t{:>5}".format('v', 'ppm'))

while True:

    mVolt = (chan.voltage * 1000)-400
    concentration=mVolt*50.0/16.0
    print("{:>5}\t{:>5.3f}".format(chan.voltage, concentration))
    time.sleep(0.5)
