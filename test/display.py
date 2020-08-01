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

try:
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
    
    draw.rectangle([(20,20),(90,80)], fill = "BLUE", outline="BLACK")
    draw.rectangle([(90,20),(160,80)], fill = "RED", outline="BLACK")
    draw.rectangle([(160,20),(230,80)], fill = "BLUE", outline="BLACK")
    draw.rectangle([(230,20),(300,80)], fill = "RED", outline="BLACK")


    
    print ("***draw line")
    #draw.line([(20,20),(300,20)], fill = "BLUE",width = 5)
    #draw.line([(20,80),(300,80)], fill = "BLUE",width = 5)
    #draw.line([(20,20),(20,80)], fill = "BLUE",width = 5)
    #draw.line([(300,20),(300,80)], fill = "BLUE",width = 5)

    
    print ("***draw text")
    draw.text((50,50), 'R1', font = font30, fill = "BLACK")
    draw.text((120, 50), 'R2', font = font15, fill = "BLACK")
    draw.text((190, 50), 'R3', font = font15, fill = "BLACK")
    draw.text((260, 50), 'R4', font = font15, fill = "BLACK")

    image=image.rotate(180) 
    disp.ShowImage(image)
    time.sleep(10)

    # read bmp file 
    bmp = Image.open(os.path.join(picdir, 'LCD_2inch.bmp'))	
    image.paste(bmp, (0,0))  
    image=image.rotate(180)
    disp.ShowImage(image)

except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    exit()

