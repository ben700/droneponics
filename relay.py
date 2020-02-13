import BlynkLib

BLYNK_AUTH = '00vIt07mIauITIq4q_quTOakFvcvpgGb' #piClearEnv


# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH)


import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(26, GPIO.OUT)
GPIO.output(26, GPIO.HIGH)
sleep(10)
GPIO.output(26, GPIO.HIGH)



@blynk.handle_event("connect")
def connect_handler():
    print('SCRIPT_START')
    for pin in range(3):
        print('Syncing virtual pin {}'.format(pin))
        blynk.virtual_sync(pin)

        # within connect handler after each server send operation forced socket reading is required cause:
        #  - we are not in script listening state yet
        #  - without forced reading some portion of blynk server messages can be not delivered to HW
        blynk.read_response(timeout=0.5)
        
        
        
@blynk.handle_event('write V38')
def write_handler(pin, value):
    button_state = value[0]
    print("read" + button_state)
    
    
@blynk.handle_event('read V38')
def write_handler(pin, value):
    button_state = value[0]
    print("read" + button_state)

@blynk.handle_event("disconnect")
def connect_handler():
    for pin in range(3):
        print("Set 'OFFLINE' color for pin {}".format(pin))
        blynk.set_property(pin, 'color', colors['OFFLINE'])


###########################################################
# infinite loop that waits for event
###########################################################
try:
    while True:
        blynk.run()
except KeyboardInterrupt:
    blynk.disconnect()
    print('SCRIPT WAS INTERRUPTED')