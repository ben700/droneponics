ome python code for the raspberry to run this display.

uses good old PythonImagingLibrary
can load any Image
allows image manipulation and drawing
can fetch images from the internet
demo code shows some search results from duckduckgo.com
References
Here is the waveshare Wiki page with the somewhat useful info's you may need. Unfortunately I am missing info about the memory layout just to know where I can expect to write a bit for a certain pixel. It also lacks timing infos, the code does a lot of delay's and there is a busy pin to read from but when and how I use which ??? The code also contains initialization code that is copied to the display and you will get no glue what it is. And no the PDF document about the display does not reveal this either.

After some experimentation, I can get a refresh rate of about 2fps for a complete image refresh, with the partial update function. The pixels do not completely reset, I guess you need to do the long refresh cycle which inverts everything a view times to get completely clean display back.

Update:

Extensive explanation of the Waveshare example code...



Connections to Raspberry
I used a Pi3 but it should work with any.

Search the web for "Raspberry pinout" e.g. this one and match with the waveshare doc, or simply use this table..

e-Paper  RaspberryPi<br>3.3V     3.3V (pin1)<br>GND      GND  (pin6)<br>DIN      MOSI (pin19)<br>CLK      SCLK (pin23)<br>CS       CE0  (pin24)<br>DC       BCM25(pin22)<br>RST      BCM17(pin11)<br>BUSY     BCM24(pin18)
The Code
There is the main.py which runs the fancy stuff and there is EPD_driver.py which is a stripped down version of the interfacing code provided py waveshare. I thrown out almost everything which did not just copy an image to the display - it.. eh.. well they tried, but putting the frame together is much easier done on the Pi and the copied over with a single command.

Just download the attached paperDisp.zip. Then run the code with "python main.py". You will need to install at least PIL and GPIO phyton libs like this.

sudo apt-get install python-requests python-pil python-rpi.gpio
Also make sure the SPI is enabled, edit /boot/config.txt and uncomment the line

dtparam=spi=on
main.py - this does init the display, gets some data from a duckduckgo search and displays that along with the current time. (instructables messed up the code, use the attached zip file)

#!/usr/bin/python<br>import spidev as SPI   # where the display connects

import Image, ImageDraw, ImageFont  # PIL - PythonImageLibrary

import time, datetime, sys, signal, urllib, requests
from EPD_driver import EPD_driver
def handler(signum, frame):
    print 'SIGTERM'
    sys.exit(0)
signal.signal(signal.SIGTERM, handler)
bus = 0 
device = 0
disp = EPD_driver(spi = SPI.SpiDev(bus, device))
print "disp size : %dx%d"%(disp.xDot, disp.yDot)
print '------------init and Clear full screen------------'
disp.Dis_Clear_full()
disp.delay()
# display part
disp.EPD_init_Part()
disp.delay()
imagenames = [] 
search = "http://api.duckduckgo.com/?q=Cat&format=json&pretty=1"
if search:
    req = requests.get(search)
    if req.status_code == 200:
        for topic in req.json()["RelatedTopics"]:
            if "Topics" in topic:
                for topic2 in topic["Topics"]:
                    try:
                        url = topic2["Icon"]["URL"]
                        text = topic2["Text"]
                        if url:
                            imagenames.append( (url,text) )
                    except:
                        # print topic
                        pass
            try:
                url = topic["Icon"]["URL"]
                if url:
                    imagenames.append( url )
            except:
                # print topic
                pass
    else:
        print req.status_code
# font for drawing within PIL
myfont10 = ImageFont.truetype("amiga_forever/amiga4ever.ttf", 8)
myfont28 = ImageFont.truetype("amiga_forever/amiga4ever.ttf", 28)
# mainimg is used as screen buffer, all image composing/drawing is done in PIL,
# the mainimg is then copied to the display (drawing on the disp itself is no fun)
mainimg = Image.new("1", (296,128))
name = ("images/downloaded.png", "bla")
skip = 0
while 1:
    for name2 in imagenames:
        print '---------------------'
        skip = (skip+1)%7
        try:
            starttime = time.time()
            if skip==0 and name2[0].startswith("http"):
                name = name2
                urllib.urlretrieve(name[0], "images/downloaded.png")
                name = ("images/downloaded.png", name2[1])
            im = Image.open(name[0])
            print name, im.format, im.size, im.mode
            im.thumbnail((296,128))
            im = im.convert("1") #, dither=Image.NONE)
            # print 'thumbnail', im.format, im.size, im.mode
            loadtime = time.time()
            print 't:load+resize:', (loadtime - starttime)
            draw = ImageDraw.Draw(mainimg)
            # clear
            draw.rectangle([0,0,296,128], fill=255)
            # copy to mainimg
            ypos = (disp.xDot - im.size[1])/2
            xpos = (disp.yDot - im.size[0])/2
            print 'ypos:', ypos, 'xpos:', xpos
            mainimg.paste(im, (xpos,ypos))
            # draw info text
            ts = draw.textsize(name[1], font=myfont10)
            tsy = ts[1]+1
            oldy = -1
            divs = ts[0]/250
            for y in range(0, divs):
                newtext = name[1][(oldy+1)*len(name[1])/divs:(y+1)*len(name[1])/divs]
                # print divs, oldy, y, newtext
                oldy = y
                draw.text((1, 1+y*tsy), newtext, fill=255, font=myfont10)
                draw.text((1, 3+y*tsy), newtext, fill=255, font=myfont10)
                draw.text((3, 3+y*tsy), newtext, fill=255, font=myfont10)
                draw.text((3, 1+y*tsy), newtext, fill=255, font=myfont10)
                draw.text((2, 2+y*tsy), newtext, fill=0, font=myfont10)
            #draw time
            now = datetime.datetime.now()
            tstr = "%02d:%02d:%02d"%(now.hour,now.minute,now.second)
            # draw a shadow, time
            tpx = 36
            tpy = 96
            for i in range(tpy-4, tpy+32, 2):
                draw.line([0, i, 295, i], fill=255)
            draw.text((tpx-1, tpy  ), tstr, fill=0, font=myfont28)
            draw.text((tpx-1, tpy-1), tstr, fill=0, font=myfont28)
            draw.text((tpx  , tpy-1), tstr, fill=0, font=myfont28)
            draw.text((tpx+2, tpy  ), tstr, fill=0, font=myfont28)
            draw.text((tpx+2, tpy+2), tstr, fill=0, font=myfont28)
            draw.text((tpx  , tpy+2), tstr, fill=0, font=myfont28)
            draw.text((tpx  , tpy  ), tstr, fill=255, font=myfont28)
            del draw
            im = mainimg.transpose(Image.ROTATE_90)
            drawtime = time.time()
            print 't:draw:', (drawtime - loadtime)
            listim = list(im.getdata())
            # print im.format, im.size, im.mode, len(listim)
            listim2 = []
            for y in range(0, im.size[1]):
                for x in range(0, im.size[0]/8):
                    val = 0
                    for x8 in range(0, 8):
                        if listim[(im.size[1]-y-1)*im.size[0] + x*8 + (7-x8)] > 128:
                            # print x,y,x8,'ON'
                            val = val | 0x01 << x8
                        else:
                            # print x,y,x8,'OFF'
                            pass
                    # print val
                    listim2.append(val)
            for x in range(0,1000):
                listim2.append(0)
            # print len(listim2)
            convtime = time.time()
            print 't:conv:', (convtime - loadtime)
            ypos = 0
            xpos = 0
            disp.EPD_Dis_Part(xpos, xpos+im.size[0]-1, ypos, ypos+im.size[1]-1, listim2) # xStart, xEnd, yStart, yEnd, DisBuffer
            # disp.delay()
            uploadtime = time.time()
            print 't:upload:', (uploadtime - loadtime)
        except IOError as ex:
            print 'IOError', str(ex)</p>
