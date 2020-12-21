
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTk, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import tkinter as tk
from tkinter import ttk
from numpy import *
from math import *

LARGE_FONT= ("Verdana", 12)
style.use("ggplot")

f = Figure(figsize=(5,5), dpi=100)
a = f.add_subplot(111)


def animate(i):
    print("in animate")
    pullData = open("/home/pi/droneponics/GUI/example/sampleText.txt","r").read()
    dataList = pullData.split('\n')
    xList = []
    yList = []
    for eachLine in dataList:
        if len(eachLine) > 1:
            x, y = eachLine.split(',')
            xList.append(int(x))
            yList.append(int(y))
            print("x = " + str(x) + " y = " + str(y))

    a.clear()
    a.plot(xList, yList)

    
            

class SeaofBTCapp(tk.Tk):
    

    def __init__(self, *args, **kwargs):
        print("SeaofBTCapp __init__")        
        tk.Tk.__init__(self, *args, **kwargs)

        
        img = tk.PhotoImage(file='/home/pi/droneponics/pic/favicon.ico')
        
       # tk.Tk.iconbitmap(self, default="/home/pi/droneponics/pic/favicon.ico")
        
        tk.Tk.wm_title(self, "Sea of BTC client")
        
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        container.tk.call('wm', 'iconphoto', self._w, img)
       
        self.frames = {}

        for F in (StartPage, PageOne, PageTwo, PageThree):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button = ttk.Button(self, text="Visit Page 1",
                            command=lambda: controller.show_frame(PageOne))
        button.pack()

        button2 = ttk.Button(self, text="Visit Page 2",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()

        button3 = ttk.Button(self, text="Graph Page",
                            command=lambda: controller.show_frame(PageThree))
        button3.pack()


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text="Page Two",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page Two!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text="Page One",
                            command=lambda: controller.show_frame(PageOne))
        button2.pack()


class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        print("PageThree __init__")        
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graph Page!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()
        
        f = Figure(figsize=(5,4), dpi=100)
        
        
        a = f.add_subplot(111)
        
        
        x = np.arange(0,4*np.pi-1,0.1)   # start,stop,step
        y = np.sin(x)
        z = np.cos(x)
        a.plot(x,y,x,z)
        a.xlabel('x values from 0 to 4pi')  # string must be enclosed with quotes '  '
        a.ylabel('sin(x) and cos(x)')
        a.title('Plot of sin and cos from 0 to 4pi')
        a.legend(['sin(x)', 'cos(x)'])      # legend entries as seperate strings in a list
        a.show()
        
        #t = arange(0.0,3.0,0.01)
        #print (math.sin(math.pi))
        #print (math.sin(2*math.pi*t))
        #s = sin(2*math.pi*t)

        #a.plot(t,s)
        
        
        
        print("pre FigureCanvasTk")
        #canvas = FigureCanvasTk(f, self)
        #canvas.draw()
        #canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        print("post FigureCanvasTk")
        
        #toolbar = NavigationToolbar2Tk(canvas, self)
        #toolbar.update()
        #canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


app = SeaofBTCapp()
print("pre animation")
ani = animation.FuncAnimation(f, animate, interval=1000)
print("post animation")
app.mainloop()
