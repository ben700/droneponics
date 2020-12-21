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

LARGE_FONT= ("Verdana", 12)
style.use("ggplot")

droneGUI.f = Figure(figsize=(5,3), dpi=100)
a = droneGUI.f.add_subplot(111)
t = np.arange(0.0,3.0,0.01)
s = np.sin(2*np.pi*t)
a.plot(t,s)
print("Done Plot")




def animate(i):
    print("----------------------------------animate")
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
    
        #tk.Tk.iconbitmap(self, default="/home/pi/droneponics/pic/favicon.ico")
        tk.Tk.wm_title(self, "Sea of BTC client")
        
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, CalibrationPage, ConfigurationPage, OperationalDataPage,  DOCalPage,  ORPCalPage,  PMPCalPage):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

        


app = SeaofBTCapp()
ani = animation.FuncAnimation(f, animate, interval=1000)
app.mainloop()
