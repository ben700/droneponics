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
    
         read bmp file 
        bmp = Image.open(os.path.join(picdir, 'background.bmp'))	
        image.paste(bmp, (0,0))  
  
        draw = ImageDraw.Draw(image)
        draw.text((10, 50), 'Pump 1: "+p1Mode+" : "+p1Status+"', font = font30, fill = "BLACK")
        draw.text((10, 95), 'Pump 2: "+p2Mode+" : "+p2Status+"', font = font30, fill = "BLACK")
        draw.text((10, 140), 'Pump 3: "+p3Mode+" : "+p3Status+"', font = font30, fill = "BLACK")
        draw.text((10, 185), 'Pump 4: "+p4Mode+" : "+p4Status+"', font = font30, fill = "BLACK")
        self.disp.ShowImage(image)
          
        
    def updateLCDProbe (self, sPH, sEC, sTemp):
        self._log.debug("updateLCDProbe")
     
        # Clear display.
        self.disp.clear()
        self._log.debug("Clear Display")
     
        draw = ImageDraw.Draw(self.image)
        self._log.debug("ImageDraw blank")

        draw.rectangle([(0,0),(320,240)],fill = "WHITE")
        self._log.debug("draw.rectangle 1")
        draw.rectangle([(20,70),(300,130)], fill = "WHITE", outline="BLACK")
        self._log.debug("draw.rectangle 2")          
        draw.rectangle([(20,130),(300,190)], fill = "WHITE", outline="BLACK")
        self._log.debug("draw.rectangle 3")
        draw.rectangle([(20,190),(300,230)], fill = "WHITE", outline="BLACK")

        self._log.debug ("***draw text")

        draw.text((50, 90), 'pH = ' + str(sPH), font = self.font15, fill = "BLACK")
        draw.text((50, 150), 'EC = ' + str(sEC), font = self.font15, fill = "BLACK")
        draw.text((50, 190), 'Temp = ' + str(sTemp), font = self.font15, fill = "BLACK")

        self.image=self.image.rotate(180) 
        self.disp.ShowImage(self.image)
       

    def updateLCD (self, bR1, bR2, bR3, bR4, iPH, iEC, iTemp):
        self._log.debug  ("updateLCD")
        self.disp = ST7789.ST7789()
        # Initialize library.
        disp.Init()

        # Clear display.
        disp.clear()

        # image = Image.new('RGB', (disp.width,disp.height), (255,255,255)) 
        image = Image.new('RGB', (self.disp.height,self.disp.width), (255,255,255)) 

        draw = ImageDraw.Draw(image)

        draw.rectangle([(0,0),(320,240)],fill = "WHITE")

        if(bR1):
            draw.rectangle([(20,10),(90,70)], fill = "GREEN", outline="BLACK")
        else:
            draw.rectangle([(20,10),(90,70)], fill = "RED", outline="BLACK")
        if(bR2):
            draw.rectangle([(90,10),(160,70)], fill = "GREEN", outline="BLACK")
        else:
            draw.rectangle([(90,10),(160,70)], fill = "RED", outline="BLACK")
        if(bR3):
            draw.rectangle([(160,10),(230,70)], fill = "GREEN", outline="BLACK")
        else:
            draw.rectangle([(160,10),(230,70)], fill = "RED", outline="BLACK")
        if(bR4):
            draw.rectangle([(230,10),(300,70)], fill = "GREEN", outline="BLACK")        
        else:
            draw.rectangle([(230,10),(300,70)], fill = "RED", outline="BLACK")

        draw.rectangle([(20,70),(300,130)], fill = "WHITE", outline="BLACK")
        draw.rectangle([(20,130),(300,190)], fill = "WHITE", outline="BLACK")
        draw.rectangle([(20,190),(300,230)], fill = "WHITE", outline="BLACK")

        self._log.debug  ("***draw text")
        draw.text((50,40), 'R1', font = self.font15, fill = "BLACK")
        draw.text((120, 40), 'R2', font = self.font15, fill = "BLACK")
        draw.text((190, 40), 'R3', font = self.font15, fill = "BLACK")
        draw.text((260, 40), 'R4', font = self.font15, fill = "BLACK")

        draw.text((50, 90), 'pH = ' + str(iPH), font = self.font30, fill = "BLACK")
        draw.text((50, 150), 'EC = ' + str(iEC), font = self.font30, fill = "BLACK")
        draw.text((50, 190), 'Temp = ' + str(iTemp), font = self.font30, fill = "BLACK")

        image=image.rotate(180) 
        self.disp.ShowImage(image)


class LCD:
   
    def __init__(self, _log):
        self._log = _log 
        self.lcd = liquidcrystal_i2c.LiquidCrystal_I2C(0x27, 1, numlines=4)


    def updateLCD (self, r1, r2, r3, r4):
        self._log.debug  ("updateLCD")
        self.lcd.printline(0, "Pump 1 status = " + str(r1) + " ")
        self.lcd.printline(1, "Pump 2 status = " + str(r2) + " ")
        self.lcd.printline(2, "Pump 3 status = " + str(r3) + " ")
        self.lcd.printline(3, "Pump 4 status = " + str(r4) + " ")
  
    def displayOn (self):
        self.lcd.backlight()
        self._log.debug  ("Turned ON display backlight")
          
    def displayOff (self):
        self.lcd.noBacklight()
        self._log.debug  ("Turned OFF display backlight")
