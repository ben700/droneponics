
import tkinter as tk
root=tk.Tk()
root.geometry("360x360")

frame=tk.Frame(root,bg='lightblue')
frame.place(relx=0.2,rely=0.2,relheight=0.6,relwidth=0.6)

def pumpPage1():
    label=tk.Label(frame,text='this is the pump 1')
    label.place(relx=0.3,rely=0.4)

def pumpPage2():
    label=tk.Label(frame,text='this is the pump 2')
    label.place(relx=0.3,rely=0.4)

def pumpPage3():
    label=tk.Label(frame,text='this is the pump 3')
    label.place(relx=0.3,rely=0.4)

def pumpPage4():
    label=tk.Label(frame,text='this is the pump 4')
    label.place(relx=0.3,rely=0.4)
    
def pumpPage5():
    label=tk.Label(frame,text='this is the pump 5')
    label.place(relx=0.3,rely=0.4)
    
def pumpPage6():
    label=tk.Label(frame,text='this is the pump 6')
    label.place(relx=0.3,rely=0.4)
    
def pumpPage7():
    label=tk.Label(frame,text='this is the pump 7')
    label.place(relx=0.3,rely=0.4)
    
bt1=tk.Button(root,text='Pump 1',command=pumpPage1)
bt1.grid(row=1,column=0)

bt2=tk.Button(root,text='Pump 2',command=pumpPage2)
bt2.grid(row=1,column=1)

bt3=tk.Button(root,text='Pump 3',command=pumpPage3)
bt3.grid(row=1,column=2)

bt4=tk.Button(root,text='Pump 4',command=pumpPage4)
bt4.grid(row=1,column=3)

bt5=tk.Button(root,text='Pump 5',command=pumpPage5)
bt5.grid(row=2,column=0)

bt6=tk.Button(root,text='Pump 6',command=pumpPage6)
bt6.grid(row=2,column=1)

bt7=tk.Button(root,text='Pump 7',command=pumpPage7)
bt7.grid(row=2,column=2)

root.mainloop()