import sys
import os
sys.path.append('/home/pi/droneponics')
import drone
import liquidcrystal_i2c

cols = 20
rows = 4
lcd=None
try:
    lcd = liquidcrystal_i2c.LiquidCrystal_I2C(0x27, 1, numlines=rows)
except:
    print("no lcd to create on bus 1")
    
try:
    lcd.Backlight()
except:
    print("no lcd on turn on backloight on bus 1")
    
try:
    print("State of the backlight is now ")
    print(lcd.getBacklight())
except:
    print("no lcd to get state from on bus 1")
    
