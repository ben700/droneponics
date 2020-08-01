#!/usr/bin/python
# -*- coding:utf-8 -*-
import time
import sys
import os
picdir = '/home/pi/droneponics/pic/'
libdir = '/home/pi/droneponics/lib/'
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
import time
from waveshare_2inch_LCD import ST7789
from PIL import Image,ImageDraw,ImageFont

logging.basicConfig(level=logging.INFO)
print(picdir)

def updateLCD (bR1, bR2, bR3, bR4, iPH, iEC, iTemp):
    print ("2inch LCD Module")
    disp = ST7789.ST7789()
    # Initialize library.
    disp.Init()

    # Clear display.
    disp.clear()

    # image = Image.new('RGB', (disp.width,disp.height), (255,255,255)) 
    image = Image.new('RGB', (disp.height,disp.width), (255,255,255)) 

    draw = ImageDraw.Draw(image)

    font30 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 30)
    font15 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 15)

    
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
    
    
    print ("***draw line")
    #draw.line([(20,20),(300,20)], fill = "BLUE",width = 5)
    #draw.line([(20,80),(300,80)], fill = "BLUE",width = 5)
    #draw.line([(20,20),(20,80)], fill = "BLUE",width = 5)
    #draw.line([(300,20),(300,80)], fill = "BLUE",width = 5)

    
    print ("***draw text")
    draw.text((50,40), 'R1', font = font15, fill = "BLACK")
    draw.text((120, 40), 'R2', font = font15, fill = "BLACK")
    draw.text((190, 40), 'R3', font = font15, fill = "BLACK")
    draw.text((260, 40), 'R4', font = font15, fill = "BLACK")

    draw.text((50, 90), 'pH = ' + str(iPH), font = font30, fill = "BLACK")
    draw.text((50, 150), 'EC = ' + str(iEC), font = font30, fill = "BLACK")
    draw.text((50, 190), 'Temp = ' + str(iTemp), font = font30, fill = "BLACK")

    image=image.rotate(180) 
    disp.ShowImage(image)
    time.sleep(10)

    # read bmp file 
    bmp = Image.open(os.path.join(picdir, 'LCD_2inch.bmp'))	
    image.paste(bmp, (0,0))  
    image=image.rotate(180)
    disp.ShowImage(image)

try:
    updateLCD (True, True, False, False, 7.0, 400, 25)

