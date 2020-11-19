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
btFrame.place(relx=0.2,rely=0.1,relheight=0.1,relwidth=0.6)

def pumpPage1():
    actionFrame=tk.Frame(root,bg='lightblue')
    actionFrame.place(relx=0.2,rely=0.3,relheight=0.1,relwidth=0.6)
    label=tk.Label(actionFrame,text='Set-up')
    label.grid(row=0,column=0, columnspan=4)
    bt1=tk.Button(actionFrame,text='Sensors',command=pumpPage1)
    bt2=tk.Button(actionFrame,text='Dosers',command=pumpPage1)
    bt3=tk.Button(actionFrame,text='Timers',command=pumpPage1)
    bt4=tk.Button(actionFrame,text='Network',command=pumpPage1)
    bt1.grid(row=1,column=0)
    bt2.grid(row=1,column=1)
    bt3.grid(row=1,column=2)
    bt4.grid(row=1,column=3)

def pumpPage2():
    actionFrame=tk.Frame(root,bg='green')
    actionFrame.place(relx=0.2,rely=0.3,relheight=0.1,relwidth=0.6)
    label=tk.Label(actionFrame,text='Operation')
    label.grid(row=0,column=0, columnspan=4)
    bt1=tk.Button(actionFrame,text='Sensors',command=pumpPage1)
    bt2=tk.Button(actionFrame,text='Dosers',command=pumpPage1)
    bt3=tk.Button(actionFrame,text='Timers',command=pumpPage1)
    bt1.grid(row=1,column=0)
    bt2.grid(row=1,column=1)
    bt3.grid(row=1,column=2)
   
def pumpPage3():
    actionFrame=tk.Frame(root,bg='red')
    actionFrame.place(relx=0.2,rely=0.3,relheight=0.1,relwidth=0.6)
    label=tk.Label(actionFrame,text='Calibration')
    label.grid(row=0,column=0, columnspan=4)
    bt1=tk.Button(actionFrame,text='Sensors',command=SensorsCalibrationPage)
    bt2=tk.Button(actionFrame,text='Dosers',command=pumpPage1)
    bt1.grid(row=1,column=0)
    bt2.grid(row=1,column=1)
    
def SensorsCalibrationPage():	
    functionFrame=tk.Frame(root,bg='red')
    functionFrame.place(relx=0.05,rely=0.7,relheight=0.1,relwidth=0.9)
    label=tk.Label(functionFrame,text='Sensors Calibration')
    label.grid(row=0,column=0, columnspan=5)
    sensors = []
    sensors = drone.buildAllSensors(sensors, _log)
    _log.info("All Monitor Sensors created")
    tempCalButton=tk.Button(functionFrame,text='Cal Temp',command=SensorsCalibrationPage)
    phCalButton=tk.Button(functionFrame,text='Cal Temp',command=SensorsCalibrationPage)
    ecCalButton=tk.Button(functionFrame,text='Cal Temp',command=SensorsCalibrationPage)
    doCalButton=tk.Button(functionFrame,text='Cal Temp',command=SensorsCalibrationPage)
    orpCalButton=tk.Button(functionFrame,text='Cal Temp',command=SensorsCalibrationPage)

    tempCalButton.grid(row=1,column=0)
    phCalButton.grid(row = 1 ,column = 1)
    ecCalButton.grid(row = 1 ,column = 2)
    doCalButton.grid(row = 1 ,column = 3)
    orpCalButton.grid(row = 1 ,column = 4)

    if(sensors[0].isProbeConnected()):
        tempCalButton["text"]= "Cal Temp \nConnected"
    else:
        tempCalButton["text"]= "Cal Temp \nNot Connected"
        tempCalButton["state"] = DISABLED
	
    if(sensors[2].isProbeConnected()):
        phCalButton["text"]= "Cal PH \nConnected"
    else:
        phCalButton["text"]= "Cal PH \nNot Connected"
        phCalButton["state"] = DISABLED
	
    if(sensors[1].isProbeConnected()):
        ecCalButton["text"]= "Cal EC "+'\n'+"Connected"
    else:
        ecCalButton["text"]= "Cal EC "+'\n'+"Not Connected"
        ecCalButton["state"] = DISABLED
	
    if(sensors[3].isProbeConnected()):
        doCalButton["text"]= "Cal DO "+'\n'+"Connected"
    else:
        doCalButton["text"]= "DO "+'\n'+"Not Connected"
        doCalButton["state"] = DISABLED
	
    if(sensors[4].isProbeConnected()):
        orpCalButton["text"]= "Cal ORP "+'\n'+"Connected"
    else:
        orpCalButton["text"]= "ORP "+'\n'+"Not Connected"
        orpCalButton["state"] = DISABLED
    
def btnExit():
  	root.destroy()

# we can exit when we press the escape key
def end_fullscreen(event):
	root.attributes("-fullscreen", False)


bt1=tk.Button(btFrame,text='Set-up',command=pumpPage1)
bt1.grid(row=1,column=0)

bt2=tk.Button(btFrame,text='Operation',command=pumpPage2)
bt2.grid(row=1,column=1)

bt3=tk.Button(btFrame,text='Calibration',command=pumpPage3)
bt3.grid(row=1,column=2)

exitBt=tk.Button(btFrame,text='Exit',command=btnExit)
exitBt.grid(row=1,column=3)

root.bind("<Escape>", end_fullscreen)
root.mainloop()				# starts the GUI loop
