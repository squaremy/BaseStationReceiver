# import stuff here
import serial
import _thread
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
style.use("ggplot")

import tkinter as tk
from tkinter import ttk
from tkinter import *

###
# Program: Arduino communication
# Author: Jordan Martin
# Version: 1.0
# Date Created: 8 March 2019
# Description: Used to communicate between the arduinos and the computer... will eventually graph real time data
# Last Edited By: Jordan Martin
# Last Edited: 12 March 2019
# Reason Edited: Weird data sort of filtered... added checksum
###
#global variables here
x = [] # list of x values
y = [] # list of y values
altitude = [] # list of altitudes
timestamp = [] # list of timestamps
LARGE_FONT = ("Verdana", 12)

# custom classes/functions here
class ArduinoCommunicator(): # class to communicate with plugged in arduino through serial monitor
    def __init__(self, port):
        self.ser = serial.Serial(port, 9600) # start arduino on given port with serial monitor on 9600 baud

    def readData(self):
        return self.ser.readline().decode('utf-8') # read incoming line in utf-8 format

    def isAvailable(self):
        return self.ser.isOpen() # return if serial monitor is open

    def writeData(self, data):
        return self.ser.write(data.encode('utf-8')) # write given data in utf-8 format

    def kill(self):
        self.ser.close() # close serial monitor

class Graph(): # graph and GUI class for real time graphs
    def __init__(self): # constructor
        self.fig = plt.figure() # create figure window
        self.ax = self.fig.add_subplot(211) # add axes to figure
        self.altAx = self.fig.add_subplot(212)

    def animate(self, i, x, y):
        datIn = arduino.readData() # receive data from arduino
        print(datIn) # log data to computer printout
        if "AX:" in datIn and "AY:" in datIn and "AZ:" in datIn and "*" in datIn: # check if the message isn't garbled and is location
            # FIND VELOCITY VECTOR
            xAccel = float(datIn[datIn.index("AX:")+3:datIn.index("AY:")])
        elif "PA:" in datIn and "TS:" in datIn and "*" in datIn: # check if message isn't garbled and is altitude
            nAlt = float(datIn[datIn.index("PA:")+3:datIn.index("TS:")]) # get new altitude
            ts = float(datIn[datIn.index("TS:")+3:datIn.index("*")]) # get new timestamp
            print(nAlt) # log altitude
            print(ts) # log timestamp
            altitude.append(nAlt) # add new altitude to altitude list
            timestamp.append(ts) # add timestamp to timestamp list
            self.altAx.clear() # clear prev alt graph
            self.altAx.plot(timestamp, altitude) # plot new alt graph

class LocationGraph():
    def __init__(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)

    def checkIfGoodLocation(self, x, y):
        if(len(x) > 1 and len(y) > 1):
            distToLoc = sqrt((x[len(x)-1] - x[len(x)-2])**2 + (y[len(y)-1] - y[len(y)-2])**2)
            if(distToLoc > 1):
                x.pop()
                y.pop()
                return False
            return True
        return True

    def animate(self, i, x, y):
        datIn = arduino.readData() # receive data from arduino
        print(datIn) # log data to computer printout
        if "LX:" in datIn and "LY:" in datIn and "*" in datIn: # check if the message isn't garbled and is location
            # NOTE: -- chop off last dec to decrease accuracy (it was too accurate... moving while sitting still)
            nx = float(datIn[datIn.index("LX:")+3:datIn.index("LY:")-1]) # get the new x coord of the location
            ny = float(datIn[datIn.index("LY:")+3:datIn.index("*")-1]) # get y coord
            print(nx) # log x coord
            print(ny) # log y coord
            x.append(nx) # add new x coord to x values
            y.append(ny) # add new y coord to y values
            goodLoc = checkIfGoodLocation(x, y) # TODO: test
            print(goodLoc) # TODO: test
            # self.ax.clear()
            self.ax.plot(x, y) # plot x and y data as lines

class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Base Station")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (StartPage, PageOne, PageThree, PageFour):
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
        button = ttk.Button(self, text="Control Page",
                            command=lambda: controller.show_frame(PageOne))
        button.pack()
        button2 = ttk.Button(self, text="Visit Page 2",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()
        button3 = ttk.Button(self, text="Graph Page",
                            command=lambda: controller.show_frame(PageThree))
        button3.pack()
        button4 = ttk.Button(self, text="Graph Page 2",
                            command=lambda: controller.show_frame(PageFour))
        button4.pack()

class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Control Page!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack(side=TOP)
        button2 = Button(self, text="SYNC RADIO", font=("Verdana", 24), width=10, command=lambda:controller.sync())
        button2.place(relx=0.25, rely=0.35, anchor=CENTER)
        button3 = Button(self, text="ARM", font=("Verdana", 24), width=10, command=lambda:controller.arm())
        button3.place(relx=0.25, rely=0.7, anchor=CENTER)
        button4 = Button(self, text="LAUNCH", font=("Verdana", 24), width=10, command=lambda:controller.launch())
        button4.place(relx=0.75, rely=0.35, anchor=CENTER)
        button5 = Button(self, text="ABORT", font=("Verdana", 24), width=10, command=lambda:controller.abort())
        button5.place(relx=0.75, rely=0.7, anchor=CENTER)

class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        print("testing")

class PageThree(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graph Page!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()
        canvas = FigureCanvasTkAgg(liveGraph.fig, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

class PageFour(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graph Page!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()
        canvas = FigureCanvasTkAgg(locGraph.fig, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

def main(): # main function to run
    #execute code here
    ani = animation.FuncAnimation(liveGraph.fig, liveGraph.animate, fargs=(x, y), interval=15) # handles making it in "real time"
    app = Application()
    app.mainloop()
    # plt.show() # show graph

# arduino = ArduinoCommunicator("/dev/ttyUSB0"); # set up arduino on corresponding port
liveGraph = Graph() # create graph
locGraph = LocationGraph()
main(); # run main function
# NOTE: should be able to just stick this into tkinter to add buttons for rocket tests/launches
