import sys
import os
sys.path.append('/home/pi/droneponics')
import drone
import liquidcrystal_i2c

cols = 20
rows = 4
try:
    lcd = liquidcrystal_i2c.LiquidCrystal_I2C(0x27, 1, numlines=rows)
    print("Starting state of the backlight was " + lcd.getBacklight())
    lcd.noBacklight()
    print("State of the backlight is now " + lcd.getBacklight())
except:
    print("no lcd on bus 1")
    
