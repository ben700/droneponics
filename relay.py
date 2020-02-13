import BlynkLib
from BlynkTimer import BlynkTimer

BLYNK_AUTH = '00vIt07mIauITIq4q_quTOakFvcvpgGb' #piClearEnv


# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH)

# Create BlynkTimer Instance
timer = BlynkTimer()


import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(26, GPIO.OUT)
GPIO.output26, GPIO.HIGH)
sleep(10)
GPIO.output26, GPIO.HIGH)



@blynk.handle_event("connect")
def connect_handler():
    _log.info('SCRIPT_START')
    for pin in range(3):
        _log.info('Syncing virtual pin {}'.format(pin))
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
        _log.info("Set 'OFFLINE' color for pin {}".format(pin))
        blynk.set_property(pin, 'color', colors['OFFLINE'])


###########################################################
# infinite loop that waits for event
###########################################################
try:
    while True:
        blynk.run()
except KeyboardInterrupt:
    blynk.disconnect()
    _log.info('SCRIPT WAS INTERRUPTED')