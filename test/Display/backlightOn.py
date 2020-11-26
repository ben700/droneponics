import sys
import os
sys.path.append('/home/pi/droneponics')
import drone
import liquidcrystal_i2c

cols = 20
rows = 4
try:
    lcd = liquidcrystal_i2c.LiquidCrystal_I2C(0x27, 1, numlines=rows)
    lcd.Backlight()
    print("Device found at address 27 on bus 1")
except:
    print("no lcd on bus 1")
    
try:
    lcd = liquidcrystal_i2c.LiquidCrystal_I2C(0x27, 0, numlines=rows)
    lcd.Backlight()
    print("Device found at address 27 on bus 0")
except:
    print("no lcd on bus 0")
