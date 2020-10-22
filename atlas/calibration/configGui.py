from guizero import App
from guizero import App, Text
import sys
import os
sys.path.append('/home/pi/droneponics')
from AtlasI2C import AtlasI2C

picdir = '/home/pi/droneponics/pic/'


def say_my_name():
    welcome_message.value = my_name.value
    
def change_text_size(slider_value):
    welcome_message.size = slider_value

def phStep1():
    ph = AtlasI2C(99)
    info__message.text ="Current pH reading is " + ph.query("R").split(":")[1] + '/n' + "Press button to continue calibration"
    temp__message = Text(app, text="Enter Temperature or i will use 19.5", size=40, font="Times new roman", color="lightblue")
    phProbe.command = phStep2 
    
def tempStep1():
    temp = AtlasI2C(102)
    info__message.text ="Current Temp reading is " + temp.query("R").split(":")[1]
    
def ecStep1():
    ec = AtlasI2C(100)
    info__message.text ="Current EC reading is " + ec.query("R").split(":")[1]
    
def phStep2():
   info__message.text = "This is step 2"
#ph.query("Cal,clear")
#ph.query("T,19.5")
#ph.query("Cal,mid,7.00")
    phProbe.command = phStep1

app = App(title="Droneponics")
welcome_message = Text(app, text="Droneponics Calibration App", size=40, font="Times new roman", color="lightblue")
info__message = Text(app, text="Use button to select probe type", size=40, font="Times new roman", color="lightblue")
my_name = TextBox(app, width=30)


update_text = PushButton(app, command=say_my_name, text="Display my name")
text_size = Slider(app, command=change_text_size, start=10, end=80)

my_logo = Picture(app, image=os.path.join(picdir, 'droneponics_logo.bmp'))



phProbe = PushButton(app, command=phStep1, text="Calibrate pH Meter")
tempProbe = PushButton(app, command=tempStep1, text="Calibrate Temp Meter")
ecProbe = PushButton(app, command=ecStep1, text="Calibrate EC Meter")


app.display()
