import sys                  #imports
import tkinter
def main():
    root= tkinter.Tk()      #Setup root
    root.title('Reminder')
    root.resizable(width=False, height=False)
    root.mainloop()         #Culprit
if __name__ == '_ _main_ _': 
    main()

root.mainloop()             #Culprit
