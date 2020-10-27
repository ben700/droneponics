#!/usr/bin/python
# -*- coding:utf-8 -*-
import time
import sys
import os
import logging
import time

import liquidcrystal_i2c


picdir = '/home/pi/droneponics/pic/'
libdir = '/home/pi/droneponics/lib/'
if os.path.exists(libdir):
     sys.path.append(libdir)
if os.path.exists(picdir):
     sys.path.append(picdir)
     
from waveshare_2inch_LCD import ST7789
from PIL import Image,ImageDraw,ImageFont

class Display:
   
    def __init__(self, _log):
        self._log = _log 
        self._log.info(picdir)
        self._log.debug(" 2inch LCD Module")
        self.disp = ST7789.ST7789()
        # Initialize library.
        self.disp.Init()
        self.font30 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 30)
        self.font15 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 15)
        self._log.debug("Fonts loaded")
        self.image = Image.new('RGB', (self.disp.height,self.disp.width), (255,255,255)) 

        # read bmp file 
        bmp = Image.open(os.path.join(picdir, 'droneponics_logo.bmp'))	
        self.image.paste(bmp, (10,10))  
        self.image=self.image.rotate(180)
        self.disp.ShowImage(self.image)
        self._log.debug("Display default image")
          
    def updateLCDPumps (self, p1Mode, p2Mode, p3Mode, p4Mode, p1Status, p2Status, p3Status, p4Status):
 
        # Clear display.
        self.disp.clear()
 
        #read bmp file 
        bmp = Image.open(os.path.join(picdir, 'background.bmp'))	
        self.image.paste(bmp, (0,0))  
        draw = ImageDraw.Draw(self.image)
        draw.text((10, 50), 'Pump 1: "+p1Mode+" : "+p1Status+"', font = self.font30, fill = "BLACK")
        draw.text((10, 95), 'Pump 2: "+p2Mode+" : "+p2Status+"', font = self.font30, fill = "BLACK")
        draw.text((10, 140), 'Pump 3: "+p3Mode+" : "+p3Status+"', font = self.font30, fill = "BLACK")
        draw.text((10, 185), 'Pump 4: "+p4Mode+" : "+p4Status+"', font = self.font30, fill = "BLACK")
        self.disp.ShowImage(self.image)
          
    def displayOn (self):
        self.disp.backlight()
        self._log.debug  ("Turned ON display backlight")
          
    def displayOff (self):
        self.disp.noBacklight()
        self._log.debug  ("Turned OFF display backlight")
