
import RPi.GPIO as GPIO
import time

Pump1Backup = 7
Pump2Backup = 21
Pump3Backup = 26
Pump4Backup = 16

GPIO.setmode(GPIO.BCM)

GPIO.setup(Pump1Backup, GPIO.OUT)
GPIO.setup(Pump2Backup, GPIO.OUT)
GPIO.setup(Pump3Backup, GPIO.OUT)
GPIO.setup(Pump4Backup, GPIO.OUT)

while True:
#   GPIO.output(Pump1Backup,GPIO.LOW)
#   GPIO.output(Pump2Backup,GPIO.LOW)
   GPIO.output(Pump3Backup,GPIO.LOW)
   GPIO.output(Pump4Backup,GPIO.LOW)
   time.sleep(30)
#   GPIO.output(Pump1Backup, GPIO.HIGH)
#   GPIO.output(Pump2Backup, GPIO.HIGH)
   GPIO.output(Pump3Backup, GPIO.HIGH)
   GPIO.output(Pump4Backup, GPIO.HIGH)
 
