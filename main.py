# import stuff here
import serial
# from tkinter import *
import _thread
import matplotlib
# matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.backend_bases import key_press_handler
import matplotlib.animation as animation
from matplotlib import style
style.use("ggplot")
# from matplotlib.widgets import Slider
# from matplotlib.widgets import TextBox

###
# Program: Arduino communication
# Author: Jordan Martin
# Version: 0.2
# Date Created: 8 March 2019
# Description: Used to communicate between the arduinos and the computer... will eventually graph real time data
# Last Edited By: Jordan Martin
# Last Edited: 10 March 2019
# Reason Edited: Working on live graph with arduino data... live graphs working, adding arduino data to base off of
###
#global variables here
# root = Tk()
x = [0, 1]
y = [0, 1]

# custom classes/functions here
class ArduinoCommunicator(): # class to communicate with plugged in arduino through serial monitor
    def __init__(self, port):
        self.ser = serial.Serial(port, 9600)

    def readData(self):
        return self.ser.readline().decode('utf-8')

    def isAvailable(self):
        return self.ser.isOpen()

    def writeData(self, data):
        return self.ser.write(data.encode('utf-8'))

    def kill(self):
        self.ser.close()

class Graph(): # graph and GUI class for real time graphs
    ts = [1, 2, 3]
    xDat = []
    yDat = []
    def __init__(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(1, 1, 1)
        # self.ax.set_ylim([0, 50])
        # self.line, = self.ax.plot(self.xDat, self.yDat)

    def animate(self, i, x, y):
        datIn = arduino.readData()
        nx = float(datIn[0:datIn.index(",")])
        ny = float(datIn[datIn.index(",")+1:])
        print(nx)
        print(ny)
        x.append(nx)
        y.append(ny)
        self.ax.clear()
        self.ax.plot(x, y)

def main(): # main function to run
    #execute code here
    liveGraph = Graph()
    arduino = ArduinoCommunicator("/dev/ttyUSB0"); # set up arduino on corresponding port
    ani = animation.FuncAnimation(liveGraph.fig, liveGraph.animate, fargs=(x, y), interval=25)
    plt.show()

main(); # run main function
