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
    lcd.printline(0, "asdfghjklqwertyuiopzxcvbnm1234567890ASDFGHJKLZXCVBNM<QWERTYUIOP")
    lcd.printline(1, "asdfghjklqwertyuiopzxcvbnm1234567890ASDFGHJKLZXCVBNM<QWERTYUIOP")
    lcd.printline(2, "asdfghjklqwertyuiopzxcvbnm1234567890ASDFGHJKLZXCVBNM<QWERTYUIOP")
    lcd.printline(3, "asdfghjklqwertyuiopzxcvbnm1234567890ASDFGHJKLZXCVBNM<QWERTYUIOP")
except:
    print("no lcd on to fill on bus 1")
    
try:
    lcd.autoscroll()
except NotImplementedError:
    print("NotImplementedError")
except:
    print("no lcd to get autoscroll from on bus 1")
    
