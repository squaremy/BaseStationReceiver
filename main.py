# import stuff here
import serial
import _thread
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.backend_bases import key_press_handler
import matplotlib.animation as animation
from matplotlib import style
style.use("ggplot")

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

    def checkIfGoodLocation(self, x, y):
        if(len(x) > 1 and len(y) > 1):
            distToLoc = sqrt((x[len(x)-1] - x[len(x)-2])**2 + (y[len(y)-1] y[len(y)-2])**2)
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
        elif "PA:" in datIn and "TS:" in datIn and "*" in datIn: # check if message isn't garbled and is altitude
            nAlt = float(datIn[datIn.index("PA:")+3:datIn.index("TS:")]) # get new altitude
            ts = float(datIn[datIn.index("TS:")+3:datIn.index("*")]) # get new timestamp
            print(nAlt) # log altitude
            print(ts) # log timestamp
            altitude.append(nAlt) # add new altitude to altitude list
            timestamp.append(ts) # add timestamp to timestamp list
            self.altAx.clear() # clear prev alt graph
            self.altAx.plot(timestamp, altitude) # plot new alt graph

def main(): # main function to run
    #execute code here
    liveGraph = Graph() # create graph
    ani = animation.FuncAnimation(liveGraph.fig, liveGraph.animate, fargs=(x, y), interval=15) # handles making it in "real time"
    plt.show() # show graph

arduino = ArduinoCommunicator("/dev/ttyUSB0"); # set up arduino on corresponding port
main(); # run main function
# NOTE: should be able to just stick this into tkinter to add buttons for rocket tests/launches
