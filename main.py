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
from math import *
from math import sqrt
from time import sleep

###
# Program: Arduino communication
# Author: Jordan Martin
# Version: 1.0
# Date Created: 8 March 2019
# Description: Used to communicate between the arduinos and the computer... will eventually graph real time data
# Last Edited By: Jordan Martin
# Last Edited: 8 May 2019
# Reason Edited: Added radio testing
###
#global variables here
LARGE_FONT = ("Verdana", 12)
curPage = 0

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
    altitude = [0]
    altTs = [0]
    acceleration = [[0, -9.8, 0, 9.8]]
    velocity = [[10, 20, 0, 22.36]]
    velTs = [0]
    x = []
    y = []
    distance = [[0, 0]]
    trajDeltaAlt = [[0, 0]]
    curTrajPos = 0
    curDatPos = 0
    def __init__(self): # constructor
        self.velFig = plt.figure(1) # create figure window
        self.velAx = self.velFig.add_subplot(211) # add axes to figure
        self.altAx = self.velFig.add_subplot(212) # add second axes
        self.trajFig = plt.figure(2)
        self.trajAx = self.trajFig.add_subplot(111)
        self.locFig = plt.figure(3)
        self.locAx = self.locFig.add_subplot(111)

    def checkIfGoodLocation(self, x, y):
        if(len(x) > 1 and len(y) > 1):
            distToLoc = sqrt((x[len(x)-1] - x[len(x)-2])**2 + (y[len(y)-1] - y[len(y)-2])**2)
            if(distToLoc > 1):
                x.pop()
                y.pop()
                return False
            return True
        return True

    def predictRemaindingTrajectory(self):
        if len(self.trajDeltaAlt) > 1 and len(self.distance) > 1:
            # vx = self.velocity[len(self.velocity)-1][0]
            # vy = self.velocity[len(self.velocity)-1][1]
            # print(self.trajDeltaAlt[self.curTrajPos][1])
            # print(self.trajDeltaAlt[self.curTrajPos-1][1])
            theta = atan2((self.trajDeltaAlt[self.curTrajPos][0] - self.trajDeltaAlt[self.curTrajPos-1][0]), (self.distance[self.curTrajPos][0] - self.distance[self.curTrajPos-1][0]))
            vx = self.velocity[self.curTrajPos][3] * cos(theta)
            vy = self.velocity[self.curTrajPos][3] * sin(theta)
            # print(vy)
                # vy = (self.trajDeltaAlt[self.curTrajPos][0] - self.trajDeltaAlt[self.curTrajPos-1][0]) / (self.trajDeltaAlt[self.curTrajPos][1] - self.trajDeltaAlt[self.curTrajPos-1][1])
                # vx = (self.distance[self.curTrajPos][0] - self.distance[self.curTrajPos-1][0]) / (self.distance[self.curTrajPos][1] - self.distance[self.curTrajPos-1][1])
            t = (self.distance[self.curTrajPos][0] - self.distance[0][0]) / vx
            newAlt = self.trajDeltaAlt[self.curTrajPos][0] + vy * t - 0.5 * 9.8 * t**2
            while newAlt > 0:
                newDist = self.distance[self.curTrajPos][0] + vx * t
                newAlt = self.trajDeltaAlt[self.curTrajPos][0] + vy * t - 0.5 * 9.8 * t**2
                self.distance.append([newDist, t])
                self.trajDeltaAlt.append([newAlt, t])
                t += 0.025

    def updateTrajectory(self):
        if(self.trajDeltaAlt[self.curTrajPos][0] >= 0):
            self.trajAx.clear()
            self.predictRemaindingTrajectory()
            x = []
            for i in self.distance:
                x.append(i[0])
            y = []
            for i in self.trajDeltaAlt:
                y.append(i[0])
            self.trajAx.plot(x, y)

    def animate(self, i):
        datIn = arduino.readData()
        # print(datIn) # log data to computer printout
        if "AX:" in datIn and "AY:" in datIn and "AZ:" in datIn and "TS:" in datIn and "*" in datIn and (curPage == 3 or curPage == 5): # check if the message isn't garbled and is location
            # FIND VELOCITY VECTOR
            xAccel = float(datIn[datIn.index("AX:")+3:datIn.index("AY:")])
            yAccel = float(datIn[datIn.index("AY:")+3:datIn.index("AZ:")]) - 9.8
            zAccel = float(datIn[datIn.index("AZ:")+3:datIn.index("TS:")])
            ts = float(datIn[datIn.index("TS:")+3:datIn.index("*")])
            self.velTs.append(ts)
            mag = sqrt(xAccel**2 + yAccel**2 + zAccel**2)
            accel = [xAccel, yAccel, zAccel, mag]
            self.acceleration.append(accel)
            if len(self.acceleration) > 1:
                vx = 0.5 * (self.velTs[len(self.velTs)-1] - self.velTs[len(self.velTs)-2]) * (self.acceleration[len(self.acceleration)-1][0] + self.acceleration[len(self.acceleration)-2][0]) + self.velocity[len(self.velocity)-1][0]
                vy = 0.5 * (self.velTs[len(self.velTs)-1] - self.velTs[len(self.velTs)-2]) * (self.acceleration[len(self.acceleration)-1][1] + self.acceleration[len(self.acceleration)-2][1]) + self.velocity[len(self.velocity)-1][1]
                vz = 0.5 * (self.velTs[len(self.velTs)-1] - self.velTs[len(self.velTs)-2]) * (self.acceleration[len(self.acceleration)-1][2] + self.acceleration[len(self.acceleration)-2][2]) + self.velocity[len(self.velocity)-1][2]
                print(vy)
                mag = sqrt(vx**2 + vy**2 + vz**2)
                newVel = [vx, vy, vz, mag]
                self.velocity.append(newVel)
            velMag = []
            for i in self.velocity:
                velMag.append(i[3])
            self.velAx.clear()
            self.velAx.plot(self.velTs, velMag)
        elif "PA:" in datIn and "TS:" in datIn and "*" in datIn and (curPage == 3 or curPage == 5): # check if message isn't garbled and is altitude
            nAlt = float(datIn[datIn.index("PA:")+3:datIn.index("TS:")]) # get new altitude
            ts = float(datIn[datIn.index("TS:")+3:datIn.index("*")]) # get new timestamp
            temp = str(ts)
            if len(temp) < 4:
                self.altitude.append(nAlt) # add new altitude to altitude list
                self.altTs.append(ts) # add timestamp to timestamp list
            if len(self.velocity) > 1 and len(self.velTs) > 1 and len(self.altitude) > 1 and len(temp) < 4:
                xyVel = []
                for i in self.velocity:
                    xyVel.append(sqrt(i[0]**2 + i[1]**2))
                    # print(xyVel[len(xyVel)-1])
                # deltaAlt = self.altitude[len(self.altitude)-1] - self.altitude[0]
                # self.trajDeltaAlt.append([deltaAlt, ts])
                # print(self.distance[len(self.distance)-1][0])
                newDist = 0.5 * (self.velTs[len(self.velTs)-1] - self.velTs[len(self.velTs)-2]) * (xyVel[len(xyVel)-1]+xyVel[len(xyVel)-2]) + self.distance[self.curTrajPos][0]
                while((len(self.distance)-1) > self.curTrajPos):
                    self.distance.pop()
                while((len(self.trajDeltaAlt)-1) > self.curTrajPos):
                    self.trajDeltaAlt.pop()
                self.distance.append([newDist, ts])
                self.trajDeltaAlt.append([nAlt, ts])
                self.curTrajPos += 1
                self.trajAx.clear()
                x = []
                for i in self.distance:
                    x.append(i[0])
                y = []
                for i in self.trajDeltaAlt:
                    y.append(i[0])
                self.trajAx.plot(x, y)
                self.updateTrajectory()
            self.altAx.clear() # clear prev alt graph
            self.altAx.plot(self.altTs, self.altitude) # plot new alt graph
        elif "LX:" in datIn and "LY:" in datIn and "*" in datIn: # check if the message isn't garbled and is location
            # NOTE: -- chop off last dec to decrease accuracy (it was too accurate... moving while sitting still)
            nx = float(datIn[datIn.index("LX:")+3:datIn.index("LY:")-1]) # get the new x coord of the location
            ny = float(datIn[datIn.index("LY:")+3:datIn.index("*")-1]) # get y coord
            self.x.append(nx) # add new x coord to x values
            self.y.append(ny) # add new y coord to y values
            goodLoc = checkIfGoodLocation(self.x, self.y) # TODO: test
            print(goodLoc) # TODO: test
            # self.ax.clear()
            self.locAx.plot(self.x, self.y) # plot x and y data as lines

class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Base Station")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, PageThree, PageFour, PageFive):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage, 0)

    def show_frame(self, cont, page):
        global curPage
        curPage = page
        frame = self.frames[cont]
        frame.tkraise()

    def sync(self):
        datIn = ""
        while(arduino.isAvailable() and "SYNCED" not in datIn):
            datIn = arduino.readData()
            arduino.writeData("SYNC_NOW")

    def arm(self):
        datIn = ""
        while(arduino.isAvailable() and "ARMED" not in datIn):
            datIn = arduino.readData()
            arduino.writeData("ARM")

    def launch(self):
        datIn = ""
        while(arduino.isAvailable() and "STARTING_COUNTDOWN" not in datIn):
            datIn = arduino.readData()
            arduino.writeData("LAUNCH")

    def abort(self):
        datIn = ""
        while(arduino.isAvailable() and "ABORTED" not in datIn):
            datIn = arduino.readData()
            arduino.writeData("ABORT")

    def deployChute(self):
        datIn = ""
        while(arduino.isAvailable() and "DEPLOYING_CHUTE" not in datIn):
            datIn = arduino.readData()
            arduino.writeData("DEPLOY_CHUTE")

    def toggleCamera(self):
        datIn = ""
        while(arduino.isAvailable() and "TOGGLED_CAMERA" not in datIn):
            datIn = arduino.readData()
            arduino.writeData("TOGGLE_CAMERA")

    def writeToSD(self):
        datIn = ""
        while(arduino.isAvailable() and "SD_WRITTEN" not in datIn):
            datIn = arduino.readData()
            arduino.writeData("WRITE_SD")

    def receiveGraphData(self):
        datIn = ""
        while(arduino.isAvailable() and "GRAPH_DATA_SENT" not in datIn):
            datIn = arduino.readData()
            arduino.writeData("REQUESTING_GRAPH_DATA")

    def toggleBuzzer(self):
        datIn = ""
        while(arduino.isAvailable() and "BUZZER_TOGGLED" not in datIn):
            datIn = arduino.readData()
            arduino.writeData("TOGGLE_BUZZER")


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button = ttk.Button(self, text="Control Page",
                            command=lambda: controller.show_frame(PageOne, 1))
        button.pack()
        button2 = ttk.Button(self, text="Test Page",
                            command=lambda: controller.show_frame(PageTwo, 2))
        button2.pack()
        button3 = ttk.Button(self, text="Graph Page",
                            command=lambda: controller.show_frame(PageThree, 3))
        button3.pack()
        button4 = ttk.Button(self, text="Graph Page 2",
                            command=lambda: controller.show_frame(PageFour, 4))
        button4.pack()
        button5 = ttk.Button(self, text="Graph Page 3",
                            command=lambda: controller.show_frame(PageFive, 5))
        button5.pack()

class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Control Page!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage, 0))
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
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Test Page!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage, 0))
        button1.pack(side=TOP)
        button2 = Button(self, text="DEPLOY PARACHUTE", font=("Verdana", 24), width=17, command=lambda:controller.deployChute())
        button2.place(relx=0.25, rely=0.35, anchor=CENTER)
        button3 = Button(self, text="TOGGLE CAMERA", font=("Verdana", 24), width=15, command=lambda:controller.toggleCamera())
        button3.place(relx=0.75, rely=0.35, anchor=CENTER)
        button4 = Button(self, text="WRITE TO SD", font=("Verdana", 24), width=11, command=lambda:controller.writeToSD())
        button4.place(relx=0.15, rely=0.7, anchor=CENTER)
        button5 = Button(self, text="RECEIVE GRAPH DATA", font=("Verdana", 24), width=18, command=lambda:controller.receiveGraphData())
        button5.place(relx=0.5, rely=0.7, anchor=CENTER)
        button6 = Button(self, text="TOGGLE BUZZER", font=("Verdana", 24), width=15, command=lambda:controller.toggleBuzzer())
        button6.place(relx=0.85, rely=0.7, anchor=CENTER)

class PageThree(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graph Page!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage, 0))
        button1.pack()
        canvas = FigureCanvasTkAgg(liveGraph.velFig, self)
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
                            command=lambda: controller.show_frame(StartPage, 0))
        button1.pack()
        canvas = FigureCanvasTkAgg(liveGraph.locFig, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

class PageFive(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graph Page!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage, 0))
        button1.pack()
        canvas = FigureCanvasTkAgg(liveGraph.trajFig, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

liveGraph = Graph() # create graph
arduino = ArduinoCommunicator("/dev/ttyUSB0"); # set up arduino on corresponding port
app = Application()
ani = animation.FuncAnimation(liveGraph.trajFig, liveGraph.animate, interval=15)
app.mainloop()
# NOTE: should be able to just stick this into tkinter to add buttons for rocket tests/launches
