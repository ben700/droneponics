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

nutrientMix = []
nutrientMix = drone.buildNutrientMix(nutrientMix, _log)
_log.info("All Monitor Sensors created")
	
sensors = []
sensors = drone.buildAllSensors(sensors, _log)
_log.info("All Monitor Sensors created")
	
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
entry1 = tk.Entry (root) 
entry1.place(x=200, y=0)


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
    actionFrame.place(relx=0.2,rely=0.2,relheight=0.1,relwidth=0.6)
    label=tk.Label(actionFrame,text='Calibration')
    label.grid(row=0,column=0, columnspan=4)
    bt1=tk.Button(actionFrame,text='Sensors',command=SensorsCalibrationPage)
    bt2=tk.Button(actionFrame,text='Dosers',command=PumpCalibrationPage)
    bt1.grid(row=1,column=0)
    bt2.grid(row=1,column=1)
    
def PumpCalibrationPage():	
    functionFrame=tk.Frame(root,bg='red')
    functionFrame.place(relx=0.2,rely=0.3,relheight=0.2,relwidth=0.6)
    label=tk.Label(functionFrame,text='Pump Calibration')
    label.grid(row=0,column=0, columnspan=7)

    pump1CalButton=tk.Button(functionFrame,text='Pump 1',command=Pump1CalibrationPage)
    pump2CalButton=tk.Button(functionFrame,text='Pump 2',command=Pump2CalibrationPage)
    pump3CalButton=tk.Button(functionFrame,text='Pump 3',command=Pump3CalibrationPage)
    pump4CalButton=tk.Button(functionFrame,text='Pump 4',command=Pump4CalibrationPage)
    pump5CalButton=tk.Button(functionFrame,text='Pump 5',command=Pump5CalibrationPage)
    pump6CalButton=tk.Button(functionFrame,text='Pump 6',command=Pump6CalibrationPage)
    pump7CalButton=tk.Button(functionFrame,text='Pump 7',command=Pump7CalibrationPage)

    pump1CalButton.grid(row = 1 ,column=0)
    pump2CalButton.grid(row = 1 ,column = 1)
    pump3CalButton.grid(row = 1 ,column = 2)
    pump4CalButton.grid(row = 1 ,column = 3)
    pump5CalButton.grid(row = 2 ,column = 0)
    pump6CalButton.grid(row = 2 ,column = 1)
    pump7CalButton.grid(row = 2 ,column = 2)

	
def pump1StartButtonfx():
    resultFrame=tk.Frame(root,bg='green')
    resultFrame.place(relx=0.2,rely=0.8,relheight=0.05,relwidth=0.6)
    pump1=AtlasI2C(nutrientMix[0].pumpId)
    resultText = pump1.query("D,*")
    label=tk.Label(resultFrame,text=resultText)
    label.grid(row=0,column=0, columnspan=7)
	
def pump1StopCalButtonfx():	
    resultFrame=tk.Frame(root,bg='green')
    resultFrame.place(relx=0.2,rely=0.8,relheight=0.05,relwidth=0.6)
    pump1=AtlasI2C(nutrientMix[0].pumpId)
    resultText = pump1.query("X")
    label=tk.Label(resultFrame,text=resultText)
    label.grid(row=0,column=0, columnspan=7)

def pump1DoseCalButtonfx():	
    resultFrame=tk.Frame(root,bg='green')
    resultFrame.place(relx=0.2,rely=0.8,relheight=0.05,relwidth=0.6)
    pump1=AtlasI2C(nutrientMix[0].pumpId)
    resultText = pump1.query("D,8")
    label=tk.Label(resultFrame,text=resultText)
    label.grid(row=0,column=0, columnspan=7)
	
def pump1DoseCalButtonfx():	
    resultFrame=tk.Frame(root,bg='green')
    resultFrame.place(relx=0.2,rely=0.8,relheight=0.05,relwidth=0.6)
    pump1=AtlasI2C(nutrientMix[0].pumpId)
    resultText = pump1.query("D,8,1")
    label=tk.Label(resultFrame,text=resultText)
    label.grid(row=0,column=0, columnspan=7)
	
def pump1ClearCalButtonfx():	
    resultFrame=tk.Frame(root,bg='green')
    resultFrame.place(relx=0.2,rely=0.8,relheight=0.05,relwidth=0.6)
    pump1=AtlasI2C(nutrientMix[0].pumpId)
    resultText = pump1.query("CAL,clear")
    label=tk.Label(resultFrame,text=resultText)
    label.grid(row=0,column=0, columnspan=7)
	
def pump1SetCalButtonfx():	
	
    resultFrame=tk.Frame(root,bg='green')
    resultFrame.place(relx=0.2,rely=0.8,relheight=0.05,relwidth=0.6)
    pump1=AtlasI2C(nutrientMix[0].pumpId)
    #resultText = pump1.query("CAL,*")
    resultText = entry1.get()
    label=tk.Label(resultFrame,text=resultText)
    label.grid(row=0,column=0, columnspan=7)


	
def Pump1CalibrationPage():	
    functionFrame=tk.Frame(root,bg='red')
    functionFrame.place(relx=0.2,rely=0.6,relheight=0.1,relwidth=0.6)
    label=tk.Label(functionFrame,text='Pump 1 Calibration')
    label.grid(row=0,column=0, columnspan=7)
    pump1=AtlasI2C(nutrientMix[0].pumpId)
    label2Text = pump1.query("Cal,?").strip().rstrip('\x00')
    label2=tk.Label(functionFrame,text=label2Text)
    label2.grid(row=1,column=5, columnspan=4)
    pump1StartButton=tk.Button(functionFrame,text='Start',command=pump1StartButtonfx)
    pump1StopCalButton=tk.Button(functionFrame,text='Stop',command=pump1StopCalButtonfx)
    pump1ClearCalButton=tk.Button(functionFrame,text='Clear',command=pump1ClearCalButtonfx)
    pump1DoseCalButton=tk.Button(functionFrame,text='Dose',command=pump1DoseCalButtonfx)
    pump1DoseOverTimeCalButton=tk.Button(functionFrame,text='Dose/Time',command=pump1DoseOverTimeCalButtonfx)	
    pump1SetCalButton=tk.Button(functionFrame,text='Set',command=pump1SetCalButtonfx)
   
    pump1StartButton.grid(row = 1 ,column=0)
    pump1StopCalButton.grid(row = 1 ,column = 1)
    pump1DoseCalButton.grid(row = 1 ,column = 2)
    pump1SetCalButton.grid(row = 1 ,column = 3)	

	
def pump2StartButtonfx():
    resultFrame=tk.Frame(root,bg='green')
    resultFrame.place(relx=0.2,rely=0.8,relheight=0.05,relwidth=0.6)
    pump1=AtlasI2C(nutrientMix[1].pumpId)
    resultText = pump1.query("D,*")
    label=tk.Label(resultFrame,text=resultText)
    label.grid(row=0,column=0, columnspan=7)
	
def pump2StopCalButtonfx():	
    resultFrame=tk.Frame(root,bg='green')
    resultFrame.place(relx=0.2,rely=0.8,relheight=0.05,relwidth=0.6)
    pump1=AtlasI2C(nutrientMix[1].pumpId)
    resultText = pump1.query("X")
    label=tk.Label(resultFrame,text=resultText)
    label.grid(row=0,column=0, columnspan=7)

def pump2DoseCalButtonfx():	
    resultFrame=tk.Frame(root,bg='green')
    resultFrame.place(relx=0.2,rely=0.8,relheight=0.05,relwidth=0.6)
    pump1=AtlasI2C(nutrientMix[1].pumpId)
    resultText = pump1.query("D,8")
    label=tk.Label(resultFrame,text=resultText)
    label.grid(row=0,column=0, columnspan=7)
	
def pump2DoseCalButtonfx():	
    resultFrame=tk.Frame(root,bg='green')
    resultFrame.place(relx=0.2,rely=0.8,relheight=0.05,relwidth=0.6)
    pump1=AtlasI2C(nutrientMix[1].pumpId)
    resultText = pump1.query("D,8,1")
    label=tk.Label(resultFrame,text=resultText)
    label.grid(row=0,column=0, columnspan=7)
	
def pump2ClearCalButtonfx():	
    resultFrame=tk.Frame(root,bg='green')
    resultFrame.place(relx=0.2,rely=0.8,relheight=0.05,relwidth=0.6)
    pump1=AtlasI2C(nutrientMix[1].pumpId)
    resultText = pump1.query("CAL,clear")
    label=tk.Label(resultFrame,text=resultText)
    label.grid(row=0,column=0, columnspan=7)
	
def pump2SetCalButtonfx():	
	
    resultFrame=tk.Frame(root,bg='green')
    resultFrame.place(relx=0.2,rely=0.8,relheight=0.05,relwidth=0.6)
    pump1=AtlasI2C(nutrientMix[1].pumpId)
    #resultText = pump1.query("CAL,*")
    resultText = entry1.get()
    label=tk.Label(resultFrame,text=resultText)
    label.grid(row=0,column=0, columnspan=7)


	
def Pump2CalibrationPage():	
    functionFrame=tk.Frame(root,bg='red')
    functionFrame.place(relx=0.2,rely=0.6,relheight=0.1,relwidth=0.6)
    label=tk.Label(functionFrame,text='Pump 2 Calibration')
    label.grid(row=0,column=0, columnspan=7)
    pump1=AtlasI2C(nutrientMix[1].pumpId)
    label2Text = pump1.query("Cal,?").strip().rstrip('\x00')
    label2=tk.Label(functionFrame,text=label2Text)
    label2.grid(row=1,column=5, columnspan=4)
    pump1StartButton=tk.Button(functionFrame,text='Start',command=pump2StartButtonfx)
    pump1StopCalButton=tk.Button(functionFrame,text='Stop',command=pump2StopCalButtonfx)
    pump1ClearCalButton=tk.Button(functionFrame,text='Clear',command=pump2ClearCalButtonfx)
    pump1DoseCalButton=tk.Button(functionFrame,text='Dose',command=pump2DoseCalButtonfx)
    pump1DoseOverTimeCalButton=tk.Button(functionFrame,text='Dose/Time',command=pump2DoseOverTimeCalButtonfx)	
    pump1SetCalButton=tk.Button(functionFrame,text='Set',command=pump2SetCalButtonfx)
   
    pump1StartButton.grid(row = 1 ,column=0)
    pump1StopCalButton.grid(row = 1 ,column = 1)
    pump1DoseCalButton.grid(row = 1 ,column = 2)
    pump1SetCalButton.grid(row = 1 ,column = 3)	



def pump3StartButtonfx():
    resultFrame=tk.Frame(root,bg='green')
    resultFrame.place(relx=0.2,rely=0.8,relheight=0.05,relwidth=0.6)
    pump1=AtlasI2C(nutrientMix[2].pumpId)
    resultText = pump1.query("D,*")
    label=tk.Label(resultFrame,text=resultText)
    label.grid(row=0,column=0, columnspan=7)
	
def pump3StopCalButtonfx():	
    resultFrame=tk.Frame(root,bg='green')
    resultFrame.place(relx=0.2,rely=0.8,relheight=0.05,relwidth=0.6)
    pump1=AtlasI2C(nutrientMix[2].pumpId)
    resultText = pump1.query("X")
    label=tk.Label(resultFrame,text=resultText)
    label.grid(row=0,column=0, columnspan=7)

def pump3DoseCalButtonfx():	
    resultFrame=tk.Frame(root,bg='green')
    resultFrame.place(relx=0.2,rely=0.8,relheight=0.05,relwidth=0.6)
    pump1=AtlasI2C(nutrientMix[2].pumpId)
    resultText = pump1.query("D,8")
    label=tk.Label(resultFrame,text=resultText)
    label.grid(row=0,column=0, columnspan=7)
	
def pump3DoseCalButtonfx():	
    resultFrame=tk.Frame(root,bg='green')
    resultFrame.place(relx=0.2,rely=0.8,relheight=0.05,relwidth=0.6)
    pump1=AtlasI2C(nutrientMix[2].pumpId)
    resultText = pump1.query("D,8,1")
    label=tk.Label(resultFrame,text=resultText)
    label.grid(row=0,column=0, columnspan=7)
	
def pump3ClearCalButtonfx():	
    resultFrame=tk.Frame(root,bg='green')
    resultFrame.place(relx=0.2,rely=0.8,relheight=0.05,relwidth=0.6)
    pump1=AtlasI2C(nutrientMix[2].pumpId)
    resultText = pump1.query("CAL,clear")
    label=tk.Label(resultFrame,text=resultText)
    label.grid(row=0,column=0, columnspan=7)
	
def pump3SetCalButtonfx():	
	
    resultFrame=tk.Frame(root,bg='green')
    resultFrame.place(relx=0.2,rely=0.8,relheight=0.05,relwidth=0.6)
    pump1=AtlasI2C(nutrientMix[2].pumpId)
    #resultText = pump1.query("CAL,*")
    resultText = entry1.get()
    label=tk.Label(resultFrame,text=resultText)
    label.grid(row=0,column=0, columnspan=7)


	
def Pump3CalibrationPage():	
    functionFrame=tk.Frame(root,bg='red')
    functionFrame.place(relx=0.2,rely=0.6,relheight=0.1,relwidth=0.6)
    label=tk.Label(functionFrame,text='Pump 3 Calibration')
    label.grid(row=0,column=0, columnspan=7)
    pump1=AtlasI2C(nutrientMix[2].pumpId)
    label2Text = pump1.query("Cal,?").strip().rstrip('\x00')
    label2=tk.Label(functionFrame,text=label2Text)
    label2.grid(row=1,column=5, columnspan=4)
    pump1StartButton=tk.Button(functionFrame,text='Start',command=pump3StartButtonfx)
    pump1StopCalButton=tk.Button(functionFrame,text='Stop',command=pump3StopCalButtonfx)
    pump1ClearCalButton=tk.Button(functionFrame,text='Clear',command=pump3ClearCalButtonfx)
    pump1DoseCalButton=tk.Button(functionFrame,text='Dose',command=pump3DoseCalButtonfx)
    pump1DoseOverTimeCalButton=tk.Button(functionFrame,text='Dose/Time',command=pump3DoseOverTimeCalButtonfx)	
    pump1SetCalButton=tk.Button(functionFrame,text='Set',command=pump3SetCalButtonfx)
   
    pump1StartButton.grid(row = 1 ,column=0)
    pump1StopCalButton.grid(row = 1 ,column = 1)
    pump1DoseCalButton.grid(row = 1 ,column = 2)
    pump1SetCalButton.grid(row = 1 ,column = 3)	


def pump4StartButtonfx():
    resultFrame=tk.Frame(root,bg='green')
    resultFrame.place(relx=0.2,rely=0.8,relheight=0.05,relwidth=0.6)
    pump1=AtlasI2C(nutrientMix[3].pumpId)
    resultText = pump1.query("D,*")
    label=tk.Label(resultFrame,text=resultText)
    label.grid(row=0,column=0, columnspan=7)
	
def pump4StopCalButtonfx():	
    resultFrame=tk.Frame(root,bg='green')
    resultFrame.place(relx=0.2,rely=0.8,relheight=0.05,relwidth=0.6)
    pump1=AtlasI2C(nutrientMix[3].pumpId)
    resultText = pump1.query("X")
    label=tk.Label(resultFrame,text=resultText)
    label.grid(row=0,column=0, columnspan=7)

def pump4DoseCalButtonfx():	
    resultFrame=tk.Frame(root,bg='green')
    resultFrame.place(relx=0.2,rely=0.8,relheight=0.05,relwidth=0.6)
    pump1=AtlasI2C(nutrientMix[3].pumpId)
    resultText = pump1.query("D,8")
    label=tk.Label(resultFrame,text=resultText)
    label.grid(row=0,column=0, columnspan=7)
	
def pump4DoseCalButtonfx():	
    resultFrame=tk.Frame(root,bg='green')
    resultFrame.place(relx=0.2,rely=0.8,relheight=0.05,relwidth=0.6)
    pump1=AtlasI2C(nutrientMix[3].pumpId)
    resultText = pump1.query("D,8,1")
    label=tk.Label(resultFrame,text=resultText)
    label.grid(row=0,column=0, columnspan=7)
	
def pump4ClearCalButtonfx():	
    resultFrame=tk.Frame(root,bg='green')
    resultFrame.place(relx=0.2,rely=0.8,relheight=0.05,relwidth=0.6)
    pump1=AtlasI2C(nutrientMix[3].pumpId)
    resultText = pump1.query("CAL,clear")
    label=tk.Label(resultFrame,text=resultText)
    label.grid(row=0,column=0, columnspan=7)
	
def pump4SetCalButtonfx():	
	
    resultFrame=tk.Frame(root,bg='green')
    resultFrame.place(relx=0.2,rely=0.8,relheight=0.05,relwidth=0.6)
    pump1=AtlasI2C(nutrientMix[3].pumpId)
    #resultText = pump1.query("CAL,*")
    resultText = entry1.get()
    label=tk.Label(resultFrame,text=resultText)
    label.grid(row=0,column=0, columnspan=7)


	
def Pump4CalibrationPage():	
    functionFrame=tk.Frame(root,bg='red')
    functionFrame.place(relx=0.2,rely=0.6,relheight=0.1,relwidth=0.6)
    label=tk.Label(functionFrame,text='Pump 4 Calibration')
    label.grid(row=0,column=0, columnspan=7)
    pump1=AtlasI2C(nutrientMix[3].pumpId)
    label2Text = pump1.query("Cal,?").strip().rstrip('\x00')
    label2=tk.Label(functionFrame,text=label2Text)
    label2.grid(row=1,column=5, columnspan=4)
    pump1StartButton=tk.Button(functionFrame,text='Start',command=pump4StartButtonfx)
    pump1StopCalButton=tk.Button(functionFrame,text='Stop',command=pump4StopCalButtonfx)
    pump1ClearCalButton=tk.Button(functionFrame,text='Clear',command=pump4ClearCalButtonfx)
    pump1DoseCalButton=tk.Button(functionFrame,text='Dose',command=pump4DoseCalButtonfx)
    pump1DoseOverTimeCalButton=tk.Button(functionFrame,text='Dose/Time',command=pump4DoseOverTimeCalButtonfx)	
    pump1SetCalButton=tk.Button(functionFrame,text='Set',command=pump4SetCalButtonfx)
   
    pump1StartButton.grid(row = 1 ,column=0)
    pump1StopCalButton.grid(row = 1 ,column = 1)
    pump1DoseCalButton.grid(row = 1 ,column = 2)
    pump1SetCalButton.grid(row = 1 ,column = 3)	


def pump5StartButtonfx():
    resultFrame=tk.Frame(root,bg='green')
    resultFrame.place(relx=0.2,rely=0.8,relheight=0.05,relwidth=0.6)
    pump1=AtlasI2C(nutrientMix[4].pumpId)
    resultText = pump1.query("D,*")
    label=tk.Label(resultFrame,text=resultText)
    label.grid(row=0,column=0, columnspan=7)
	
def pump5StopCalButtonfx():	
    resultFrame=tk.Frame(root,bg='green')
    resultFrame.place(relx=0.2,rely=0.8,relheight=0.05,relwidth=0.6)
    pump1=AtlasI2C(nutrientMix[4].pumpId)
    resultText = pump1.query("X")
    label=tk.Label(resultFrame,text=resultText)
    label.grid(row=0,column=0, columnspan=7)

def pump5DoseCalButtonfx():	
    resultFrame=tk.Frame(root,bg='green')
    resultFrame.place(relx=0.2,rely=0.8,relheight=0.05,relwidth=0.6)
    pump1=AtlasI2C(nutrientMix[4].pumpId)
    resultText = pump1.query("D,8")
    label=tk.Label(resultFrame,text=resultText)
    label.grid(row=0,column=0, columnspan=7)
	
def pump5DoseCalButtonfx():	
    resultFrame=tk.Frame(root,bg='green')
    resultFrame.place(relx=0.2,rely=0.8,relheight=0.05,relwidth=0.6)
    pump1=AtlasI2C(nutrientMix[4].pumpId)
    resultText = pump1.query("D,8,1")
    label=tk.Label(resultFrame,text=resultText)
    label.grid(row=0,column=0, columnspan=7)
	
def pump5ClearCalButtonfx():	
    resultFrame=tk.Frame(root,bg='green')
    resultFrame.place(relx=0.2,rely=0.8,relheight=0.05,relwidth=0.6)
    pump1=AtlasI2C(nutrientMix[4].pumpId)
    resultText = pump1.query("CAL,clear")
    label=tk.Label(resultFrame,text=resultText)
    label.grid(row=0,column=0, columnspan=7)
	
def pump5SetCalButtonfx():	
	
    resultFrame=tk.Frame(root,bg='green')
    resultFrame.place(relx=0.2,rely=0.8,relheight=0.05,relwidth=0.6)
    pump1=AtlasI2C(nutrientMix[4].pumpId)
    #resultText = pump1.query("CAL,*")
    resultText = entry1.get()
    label=tk.Label(resultFrame,text=resultText)
    label.grid(row=0,column=0, columnspan=7)


	
def Pump5CalibrationPage():	
    functionFrame=tk.Frame(root,bg='red')
    functionFrame.place(relx=0.2,rely=0.6,relheight=0.1,relwidth=0.6)
    label=tk.Label(functionFrame,text='Pump 5 Calibration')
    label.grid(row=0,column=0, columnspan=7)
    pump1=AtlasI2C(nutrientMix[4].pumpId)
    label2Text = pump1.query("Cal,?").strip().rstrip('\x00')
    label2=tk.Label(functionFrame,text=label2Text)
    label2.grid(row=1,column=5, columnspan=4)
    pump1StartButton=tk.Button(functionFrame,text='Start',command=pump5StartButtonfx)
    pump1StopCalButton=tk.Button(functionFrame,text='Stop',command=pump5StopCalButtonfx)
    pump1ClearCalButton=tk.Button(functionFrame,text='Clear',command=pump5ClearCalButtonfx)
    pump1DoseCalButton=tk.Button(functionFrame,text='Dose',command=pump5DoseCalButtonfx)
    pump1DoseOverTimeCalButton=tk.Button(functionFrame,text='Dose/Time',command=pump5DoseOverTimeCalButtonfx)	
    pump1SetCalButton=tk.Button(functionFrame,text='Set',command=pump5SetCalButtonfx)
   
    pump1StartButton.grid(row = 1 ,column=0)
    pump1StopCalButton.grid(row = 1 ,column = 1)
    pump1DoseCalButton.grid(row = 1 ,column = 2)
    pump1SetCalButton.grid(row = 1 ,column = 3)	


def pump6StartButtonfx():
    resultFrame=tk.Frame(root,bg='green')
    resultFrame.place(relx=0.2,rely=0.8,relheight=0.05,relwidth=0.6)
    pump1=AtlasI2C(nutrientMix[5].pumpId)
    resultText = pump1.query("D,*")
    label=tk.Label(resultFrame,text=resultText)
    label.grid(row=0,column=0, columnspan=7)
	
def pump6StopCalButtonfx():	
    resultFrame=tk.Frame(root,bg='green')
    resultFrame.place(relx=0.2,rely=0.8,relheight=0.05,relwidth=0.6)
    pump1=AtlasI2C(nutrientMix[5].pumpId)
    resultText = pump1.query("X")
    label=tk.Label(resultFrame,text=resultText)
    label.grid(row=0,column=0, columnspan=7)

def pump6DoseCalButtonfx():	
    resultFrame=tk.Frame(root,bg='green')
    resultFrame.place(relx=0.2,rely=0.8,relheight=0.05,relwidth=0.6)
    pump1=AtlasI2C(nutrientMix[5].pumpId)
    resultText = pump1.query("D,8")
    label=tk.Label(resultFrame,text=resultText)
    label.grid(row=0,column=0, columnspan=7)
	
def pump6DoseCalButtonfx():	
    resultFrame=tk.Frame(root,bg='green')
    resultFrame.place(relx=0.2,rely=0.8,relheight=0.05,relwidth=0.6)
    pump1=AtlasI2C(nutrientMix[5].pumpId)
    resultText = pump1.query("D,8,1")
    label=tk.Label(resultFrame,text=resultText)
    label.grid(row=0,column=0, columnspan=7)
	
def pump6ClearCalButtonfx():	
    resultFrame=tk.Frame(root,bg='green')
    resultFrame.place(relx=0.2,rely=0.8,relheight=0.05,relwidth=0.6)
    pump1=AtlasI2C(nutrientMix[5].pumpId)
    resultText = pump1.query("CAL,clear")
    label=tk.Label(resultFrame,text=resultText)
    label.grid(row=0,column=0, columnspan=7)
	
def pump6SetCalButtonfx():	
	
    resultFrame=tk.Frame(root,bg='green')
    resultFrame.place(relx=0.2,rely=0.8,relheight=0.05,relwidth=0.6)
    pump1=AtlasI2C(nutrientMix[5].pumpId)
    #resultText = pump1.query("CAL,*")
    resultText = entry1.get()
    label=tk.Label(resultFrame,text=resultText)
    label.grid(row=0,column=0, columnspan=7)


	
def Pump6CalibrationPage():	
    functionFrame=tk.Frame(root,bg='red')
    functionFrame.place(relx=0.2,rely=0.6,relheight=0.1,relwidth=0.6)
    label=tk.Label(functionFrame,text='Pump 6 Calibration')
    label.grid(row=0,column=0, columnspan=7)
    pump1=AtlasI2C(nutrientMix[5].pumpId)
    label2Text = pump1.query("Cal,?").strip().rstrip('\x00')
    label2=tk.Label(functionFrame,text=label2Text)
    label2.grid(row=1,column=5, columnspan=4)
    pump1StartButton=tk.Button(functionFrame,text='Start',command=pump6StartButtonfx)
    pump1StopCalButton=tk.Button(functionFrame,text='Stop',command=pump6StopCalButtonfx)
    pump1ClearCalButton=tk.Button(functionFrame,text='Clear',command=pump6ClearCalButtonfx)
    pump1DoseCalButton=tk.Button(functionFrame,text='Dose',command=pump6DoseCalButtonfx)
    pump1DoseOverTimeCalButton=tk.Button(functionFrame,text='Dose/Time',command=pump6DoseOverTimeCalButtonfx)	
    pump1SetCalButton=tk.Button(functionFrame,text='Set',command=pump6SetCalButtonfx)
   
    pump1StartButton.grid(row = 1 ,column=0)
    pump1StopCalButton.grid(row = 1 ,column = 1)
    pump1DoseCalButton.grid(row = 1 ,column = 2)
    pump1SetCalButton.grid(row = 1 ,column = 3)	


def pump7StartButtonfx():
    resultFrame=tk.Frame(root,bg='green')
    resultFrame.place(relx=0.2,rely=0.8,relheight=0.05,relwidth=0.6)
    pump1=AtlasI2C(nutrientMix[6].pumpId)
    resultText = pump1.query("D,*")
    label=tk.Label(resultFrame,text=resultText)
    label.grid(row=0,column=0, columnspan=7)
	
def pump7StopCalButtonfx():	
    resultFrame=tk.Frame(root,bg='green')
    resultFrame.place(relx=0.2,rely=0.8,relheight=0.05,relwidth=0.6)
    pump1=AtlasI2C(nutrientMix[6].pumpId)
    resultText = pump1.query("X")
    label=tk.Label(resultFrame,text=resultText)
    label.grid(row=0,column=0, columnspan=7)

def pump2DoseCalButtonfx():	
    resultFrame=tk.Frame(root,bg='green')
    resultFrame.place(relx=0.2,rely=0.8,relheight=0.05,relwidth=0.6)
    pump1=AtlasI2C(nutrientMix[1].pumpId)
    resultText = pump1.query("D,8")
    label=tk.Label(resultFrame,text=resultText)
    label.grid(row=0,column=0, columnspan=7)
	
def pump7DoseCalButtonfx():	
    resultFrame=tk.Frame(root,bg='green')
    resultFrame.place(relx=0.2,rely=0.8,relheight=0.05,relwidth=0.6)
    pump1=AtlasI2C(nutrientMix[6].pumpId)
    resultText = pump1.query("D,8,1")
    label=tk.Label(resultFrame,text=resultText)
    label.grid(row=0,column=0, columnspan=7)
	
def pump7ClearCalButtonfx():	
    resultFrame=tk.Frame(root,bg='green')
    resultFrame.place(relx=0.2,rely=0.8,relheight=0.05,relwidth=0.6)
    pump1=AtlasI2C(nutrientMix[6].pumpId)
    resultText = pump1.query("CAL,clear")
    label=tk.Label(resultFrame,text=resultText)
    label.grid(row=0,column=0, columnspan=7)
	
def pump7SetCalButtonfx():	
	
    resultFrame=tk.Frame(root,bg='green')
    resultFrame.place(relx=0.2,rely=0.8,relheight=0.05,relwidth=0.6)
    pump1=AtlasI2C(nutrientMix[6].pumpId)
    #resultText = pump1.query("CAL,*")
    resultText = entry1.get()
    label=tk.Label(resultFrame,text=resultText)
    label.grid(row=0,column=0, columnspan=7)


	
def Pump7CalibrationPage():	
    functionFrame=tk.Frame(root,bg='red')
    functionFrame.place(relx=0.2,rely=0.6,relheight=0.1,relwidth=0.6)
    label=tk.Label(functionFrame,text='Pump 7 Calibration')
    label.grid(row=0,column=0, columnspan=7)
    pump1=AtlasI2C(nutrientMix[6].pumpId)
    label2Text = pump1.query("Cal,?").strip().rstrip('\x00')
    label2=tk.Label(functionFrame,text=label2Text)
    label2.grid(row=1,column=5, columnspan=4)
    pump1StartButton=tk.Button(functionFrame,text='Start',command=pump7StartButtonfx)
    pump1StopCalButton=tk.Button(functionFrame,text='Stop',command=pump7StopCalButtonfx)
    pump1ClearCalButton=tk.Button(functionFrame,text='Clear',command=pump7ClearCalButtonfx)
    pump1DoseCalButton=tk.Button(functionFrame,text='Dose',command=pump7DoseCalButtonfx)
    pump1DoseOverTimeCalButton=tk.Button(functionFrame,text='Dose/Time',command=pump7DoseOverTimeCalButtonfx)	
    pump1SetCalButton=tk.Button(functionFrame,text='Set',command=pump7SetCalButtonfx)
   
    pump1StartButton.grid(row = 1 ,column=0)
    pump1StopCalButton.grid(row = 1 ,column = 1)
    pump1DoseCalButton.grid(row = 1 ,column = 2)
    pump1SetCalButton.grid(row = 1 ,column = 3)	
	
def SensorsCalibrationPage():	
    functionFrame=tk.Frame(root,bg='red')
    functionFrame.place(relx=0.05,rely=0.7,relheight=0.1,relwidth=0.9)
    label=tk.Label(functionFrame,text='Sensors Calibration')
    label.grid(row=0,column=0, columnspan=5)

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
