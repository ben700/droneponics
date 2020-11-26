import sys
import os
sys.path.append('/home/pi/droneponics')
import drone
import liquidcrystal_i2c

cols = 20
rows = 4
try:
    lcd = liquidcrystal_i2c.LiquidCrystal_I2C(0x27, 1, numlines=rows)
    lcd.noBacklight()
except:
    print("no lcd on bus 1")
    
