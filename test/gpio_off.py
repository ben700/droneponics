
import RPi.GPIO as GPIO            # import RPi.GPIO module  
from time import sleep             # lets us have a delay  
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)             # choose BCM or BOARD  

GPIO.setup(12, GPIO.OUT)           # set GPIO24 as an output   
GPIO.setup(16, GPIO.OUT)           # set GPIO24 as an output   
GPIO.setup(20, GPIO.OUT)           # set GPIO24 as an output   
GPIO.setup(21, GPIO.OUT)           # set GPIO24 as an output   
  
GPIO.output(12, 0)         # set GPIO24 to 1/GPIO.HIGH/True  
GPIO.output(16, 0)         # set GPIO24 to 1/GPIO.HIGH/True  
GPIO.output(20, 0)         # set GPIO24 to 1/GPIO.HIGH/True  
GPIO.output(21, 0)         # set GPIO24 to 1/GPIO.HIGH/True  

print ("12, 16, 20 and 21 are off")
