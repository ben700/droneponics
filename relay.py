import BlynkLib

BLYNK_AUTH = 'GP_sDPLJqyEN7jky9_zcQVSkgiyx-AeW' #motherLights

# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH)

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(26, GPIO.OUT)

@blynk.on("connected")
def connect_handler():
   blynk.sync_virtual(38)
        
@blynk.on("V38")
def V28Pressed(value):
    if(value[0] == '1'):
        print("Lights turned on")
        GPIO.output(26,1)
    else:
        print("Lights turned off")
    
###########################################################
# infinite loop that waits for event
###########################################################
try:
    while True:
        blynk.run()
except KeyboardInterrupt:
    blynk.disconnect()
    print('SCRIPT WAS INTERRUPTED')