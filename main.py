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
# Version: 0.2
# Date Created: 8 March 2019
# Description: Used to communicate between the arduinos and the computer... will eventually graph real time data
# Last Edited By: Jordan Martin
# Last Edited: 11 March 2019
# Reason Edited: Successfully parses arduino data in the format xx.xxx,yy.yyy and animates the graph
###
#global variables here
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

    def animate(self, i, x, y):
        datIn = arduino.readData()
        print(datIn)
        if "," in datIn:
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
    ani = animation.FuncAnimation(liveGraph.fig, liveGraph.animate, fargs=(x, y), interval=25)
    plt.show()

arduino = ArduinoCommunicator("/dev/ttyUSB0"); # set up arduino on corresponding port
main(); # run main function
