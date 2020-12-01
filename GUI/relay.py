#!/usr/bin/python3
import sys
import os
sys.path.append('/home/pi/droneponics')
from AtlasI2C import (AtlasI2C)
import drone
import logging

from tkinter import * 			# imports the Tkinter lib
# pip install pillow
from PIL import Image, ImageTk

    # tune console logging
_log = logging.getLogger('BlynkLog')
logFormatter = logging.Formatter("%(asctime)s [%(levelname)s]  %(message)s")
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
_log.addHandler(consoleHandler)
_log.setLevel(logging.DEBUG)

# Initialize Blynk
blynk = blynklib.Blynk(parser.get('blynk', 'BLYNK_AUTH'), log=_log.info) 
timer = blynktimer.Timer()
_log.debug("start blynk")
blynk.run()
_log.info("Blynk Created")  
    

relays=drone.RelaysI2C(_log, blynk)
relays.addRelay(1, parser.get('droneFeed', 'Relay1'), 21, 85)
relays.addRelay(2, parser.get('droneFeed', 'Relay2'), 22, 86)
relays.addRelay(3, parser.get('droneFeed', 'Relay3'), 23, 87)
relays.addRelay(4, parser.get('droneFeed', 'Relay4'), 24, 88)
relays.addRelay(5, parser.get('droneFeed', 'Relay5'), 25, 89)
relays.addRelay(6, parser.get('droneFeed', 'Relay6'), 26, 90)
relays.addRelay(7, parser.get('droneFeed', 'Relay7'), 27, 91)
relays.addRelay(8, parser.get('droneFeed', 'Relay8'), 28, 92)


restartCode = {'P': "Powered Off", 'S':"Software Reset",'B':"Brown Out",'W':"Watchdog",'U':"Unknown"}

import tkinter as tk
root=tk.Tk()
root.wm_title("GUI")			# sets title of the window

load = Image.open("/home/pi/droneponics/pic/store_logo.png")
render = ImageTk.PhotoImage(load)
img = Label(root, image=render)
img.image = render
img.place(x=0, y=0)
root.configure(bg="#99B898")		# change the background color 
root.attributes("-fullscreen", True) 	# set to fullscreen



btFrame=tk.Frame(root,bg='darkblue')
btFrame.place(relx=0.2,rely=0.1,relheight=0.2,relwidth=0.6)

def pumpPage1():
    actionFrame=tk.Frame(root,bg='lightblue')
    actionFrame.place(relx=0.2,rely=0.3,relheight=0.1,relwidth=0.6)
    label=tk.Label(actionFrame,text='Relay 1')
    label.grid(row=0,column=0, columnspan=4)
    bbt1=tk.Button(actionFrame,text='Stop',command=pump1Stop)
    bbt2=tk.Button(actionFrame,text='Start',command=pump1Start)
    bbt1.grid(row=1,column=0)
    bbt2.grid(row=1,column=1)

def pumpPage2():
    actionFrame=tk.Frame(root,bg='lightblue')
    actionFrame.place(relx=0.2,rely=0.3,relheight=0.1,relwidth=0.6)
    label=tk.Label(actionFrame,text='Relay 2')
    label.grid(row=0,column=0, columnspan=4)
    bbt1=tk.Button(actionFrame,text='Stop',command=pump2Stop)
    bbt2=tk.Button(actionFrame,text='Start',command=pump2Start)
    bbt1.grid(row=1,column=0)
    bbt2.grid(row=1,column=1)

def pumpPage3():
    actionFrame=tk.Frame(root,bg='lightblue')
    actionFrame.place(relx=0.2,rely=0.3,relheight=0.1,relwidth=0.6)
    label=tk.Label(actionFrame,text='Relay 3')
    label.grid(row=0,column=0, columnspan=4)
    bbt1=tk.Button(actionFrame,text='Stop',command=pump3Stop)
    bbt2=tk.Button(actionFrame,text='Start',command=pump3Start)
    bbt1.grid(row=1,column=0)
    bbt2.grid(row=1,column=1)

def pumpPage4():
    actionFrame=tk.Frame(root,bg='lightblue')
    actionFrame.place(relx=0.2,rely=0.3,relheight=0.1,relwidth=0.6)
    label=tk.Label(actionFrame,text='Relay 4')
    label.grid(row=0,column=0, columnspan=4)
    bbt1=tk.Button(actionFrame,text='Stop',command=pump4Stop)
    bbt2=tk.Button(actionFrame,text='Start',command=pump4Start)
    bbt1.grid(row=1,column=0)
    bbt2.grid(row=1,column=1)

def pumpPage5():
    actionFrame=tk.Frame(root,bg='lightblue')
    actionFrame.place(relx=0.2,rely=0.3,relheight=0.1,relwidth=0.6)
    label=tk.Label(actionFrame,text='Relay 5')
    label.grid(row=0,column=0, columnspan=4)
    bbt1=tk.Button(actionFrame,text='Stop',command=pump5Stop)
    bbt2=tk.Button(actionFrame,text='Start',command=pump5Start)
    bbt1.grid(row=1,column=0)
    bbt2.grid(row=1,column=1)

def pumpPage6():
    actionFrame=tk.Frame(root,bg='lightblue')
    actionFrame.place(relx=0.2,rely=0.3,relheight=0.1,relwidth=0.6)
    label=tk.Label(actionFrame,text='Relay 6')
    label.grid(row=0,column=0, columnspan=4)
    bbt1=tk.Button(actionFrame,text='Stop',command=pump6Stop)
    bbt2=tk.Button(actionFrame,text='Start',command=pump6Start)
    bbt1.grid(row=1,column=0)
    bbt2.grid(row=1,column=1)

def pumpPage7():
    actionFrame=tk.Frame(root,bg='lightblue')
    actionFrame.place(relx=0.2,rely=0.3,relheight=0.1,relwidth=0.6)
    label=tk.Label(actionFrame,text='Relay 7')
    label.grid(row=0,column=0, columnspan=4)
    bbt1=tk.Button(actionFrame,text='Stop',command=pump7Stop)
    bbt2=tk.Button(actionFrame,text='Start',command=pump7Start)
    bbt1.grid(row=1,column=0)
    bbt2.grid(row=1,column=1)


def pumpPage8():
    actionFrame=tk.Frame(root,bg='lightblue')
    actionFrame.place(relx=0.2,rely=0.3,relheight=0.1,relwidth=0.6)
    label=tk.Label(actionFrame,text='Relay 8')
    label.grid(row=0,column=0, columnspan=4)
    bbt1=tk.Button(actionFrame,text='Stop',command=pump8Stop)
    bbt2=tk.Button(actionFrame,text='Start',command=pump8Start)
    bbt1.grid(row=1,column=0)
    bbt2.grid(row=1,column=1)

def pumpStop(index):
    global relays
    index =  0 
    relays.relays[index].turnOff(_log)	

def pumpStart(index):
    global relays
    relays.relays[index].turnOn(_log)	


def pump1Stop():
    pumpStop(0)

def pump1Start():
    pumpStart(0)

def pump2Stop():
    pumpStop(1)

def pump2Start():
    pumpStart(1)

def pump3Stop():
    pumpStop(2)

def pump3Start():
    pumpStart(2)

def pump4Stop():
    pumpStop(3)

def pump4Start():
    pumpStart(3)

def pump5Stop():
    pumpStop(4)

def pump5Start():
    pumpStart(4)

def pump6Stop():
    pumpStop(5)

def pump6Start():
    pumpStart(5)

def pump7Stop():
    pumpStop(6)

def pump7Start():
    pumpStart(6)

def pump8Stop():
    pumpStop(7)

def pump8Start():
    pumpStart(7)
		
def btnExit():
  	root.destroy()

# we can exit when we press the escape key
def end_fullscreen(event):
	root.attributes("-fullscreen", False)


exitBt=tk.Button(btFrame,text='Exit',command=btnExit)
exitBt.grid(row=1,column=4)

bt1=tk.Button(btFrame,text='Relay 1',command=pumpPage1)
bt1.grid(row=1,column=0)

bt2=tk.Button(btFrame,text='Relay 2',command=pumpPage2)
bt2.grid(row=1,column=1)

bt3=tk.Button(btFrame,text='Relay 3',command=pumpPage3)
bt3.grid(row=1,column=2)

bt4=tk.Button(btFrame,text='Relay 4',command=pumpPage4)
bt4.grid(row=1,column=3)

bt5=tk.Button(btFrame,text='Relay 5',command=pumpPage5)
bt5.grid(row=2,column=0)

bt6=tk.Button(btFrame,text='Relay 6',command=pumpPage6)
bt6.grid(row=2,column=1)

bt7=tk.Button(btFrame,text='Relay 7',command=pumpPage7)
bt7.grid(row=2,column=2)

bt8=tk.Button(btFrame,text='Relay 8',command=pumpPage8)
bt8.grid(row=2,column=3)

root.bind("<Escape>", end_fullscreen)
root.mainloop()				# starts the GUI loop
