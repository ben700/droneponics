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
    print("Except: no lcd to create on bus 1")
    
try:
    lcd.Backlight()
except:
    print("Except: Turning on backlight on bus 1")
    
try:
    print("State of the backlight is now " + str(lcd.getBacklight()))
except NotImplementedError:
    print("Except: NotImplementedError getBacklight()")
except:
    print("Except: Getting state from on bus 1")
    
