import RPi.GPIO as GPIO            # import RPi.GPIO module  
from time import sleep             # lets us have a delay  
GPIO.setmode(GPIO.BCM)             # choose BCM or BOARD  
for x in range(41):
     GPIO.setup(x, GPIO.OUT)           # set GPIO24 as an output   
  
try:  
    while True:  
    
        for x in range(41):
            GPIO.output(x, 1)         # set GPIO24 to 1/GPIO.HIGH/True  
        sleep(5)                 # wait half a second  
        for x in range(41):
            GPIO.output(x, 0)         # set GPIO24 to 0/GPIO.LOW/False  
        sleep(5)                 # wait half a second  
  
except KeyboardInterrupt:          # trap a CTRL+C keyboard interrupt  
    GPIO.cleanup() 
