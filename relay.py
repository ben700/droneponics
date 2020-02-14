import BlynkLib

BLYNK_AUTH = 'GP_sDPLJqyEN7jky9_zcQVSkgiyx-AeW' #motherLights

# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH)

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(26, GPIO.OUT)

@blynk.on("connected")
def connect_handler():
   blynk.virtual_sync(38)
        
@blynk.on("V38")
def v38_write_handler(pin, value):
    GPIO.output(26,value[0])
    
###########################################################
# infinite loop that waits for event
###########################################################
try:
    while True:
        blynk.run()
except KeyboardInterrupt:
    blynk.disconnect()
    print('SCRIPT WAS INTERRUPTED')