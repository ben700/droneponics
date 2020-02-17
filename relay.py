import BlynkLib

BLYNK_AUTH = 'GP_sDPLJqyEN7jky9_zcQVSkgiyx-AeW' #motherLights

# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH)

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(37, GPIO.OUT)

@blynk.on("connected")
def connect_handler():
   blynk.sync_virtual(38,39)
        
@blynk.on("V38")
def V38Pressed(value):
    if(value[0] == '1'):
        print("Lights turned on")
        GPIO.output(37,GPIO.HIGH)
        blynk.virtual_write(39, 255)
        blynk.set_property(39, 'color', '#00ff00')
    else:
        print("Lights turned off")
        GPIO.output(37,GPIO.LOW)
        blynk.virtual_write(39, 0)
        blynk.set_property(39,'color','#D3435C')
    
###########################################################
# infinite loop that waits for event
###########################################################
try:
    while True:
        blynk.run()
except KeyboardInterrupt:
    blynk.disconnect()
    print('SCRIPT WAS INTERRUPTED')