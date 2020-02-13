import blynklib

BLYNK_AUTH = 'GP_sDPLJqyEN7jky9_zcQVSkgiyx-AeW' #motherLights

# Initialize Blynk
blynk = blynklib.Blynk(BLYNK_AUTH)

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(26, GPIO.OUT)

@blynk.handle_event("connect")
def connect_handler():
   blynk.virtual_sync(V38, 38)
   blynk.read_response(timeout=0.5)
        
        
        
@blynk.handle_event('write V38')
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