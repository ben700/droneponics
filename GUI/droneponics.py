import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style

import tkinter as tk
from tkinter import ttk

import urllib
import urllib.request
import shlex, requests
import json

import pandas as pd
import numpy as np
from droneGUI import *
import droneGUI
import sys
import os
sys.path.append('/home/pi/droneponics')
from AtlasI2C import (AtlasI2C)
import drone
from configparser import ConfigParser
import logging

parser = ConfigParser()
parser.read("/home/pi/droneponics/config/configOxy/"+drone.gethostname()+".ini")



# tune console logging
_log = logging.getLogger('BlynkLog')
logFormatter = logging.Formatter("%(asctime)s [%(levelname)s]  %(message)s")
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
_log.addHandler(consoleHandler)
_log.setLevel(parser.get('logging', 'logLevel', fallback=logging.DEBUG))
_log.critical("critical")
_log.error("error")
_log.warning("warning")
_log.info("info")
_log.debug("debug")

_log.info("/home/pi/droneponics/config/configOxy/"+drone.gethostname()+".ini")


droneGUI.nutrientMix = drone.buildOxyMix(nutrientMix, _log)
droneGUI.pumpId = nutrientMix[0].pumpId
droneGUI.sensors = drone.buildMonitorSensors(sensors, _log)

_log.info("All Monitor Sensors created")

LARGE_FONT= ("Verdana", 12)
style.use("ggplot")

droneGUI.f = Figure(figsize=(5,3), dpi=100)
a = droneGUI.f.add_subplot(111)

def animate(i):
    btcData = requests.get("https://api.coindesk.com/v1/bpi/historical/close.json")    
    btcArr = btcData.json()
    btcList = btcArr["bpi"]    
    key_list = list(btcList.keys())
    val_list = list(btcList.values())

    a.clear()

    a.plot_date(key_list, val_list,"#00A3E0", label="BTC Value")
        
    a.legend(bbox_to_anchor=(0, 1.02, 1, .102), loc=3,
             ncol=2, borderaxespad=0)

    title = "BTC Close Prices to: "+str(btcArr["time"]["updated"])
    a.set_title(title)        

class SeaofBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)

        logo = tk.PhotoImage(file='/home/pi/droneponics/pic/favicon.ico')
        self.call('wm', 'iconphoto', self._w, logo)
    
        tk.Tk.wm_title(self, "Sea of BTC client")
        
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, CalibrationPage, ConfigurationPage, OperationalDataPage,  DOCalPage,  ORPCalPage, TempCalPage, PMPCalPage):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

        


app = SeaofBTCapp()
ani = animation.FuncAnimation(droneGUI.f, animate, interval=1000)
app.mainloop()
