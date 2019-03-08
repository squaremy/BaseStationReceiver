# import stuff here
import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from tkinter import *

#global variables here
root = Tk()

# custom classes/functions here
class ArduinoCommunicator():
    def __init__(self, port):
        self.ser = serial.Serial(port, 115200)

    def readData(self):
        return self.ser.readline().decode('utf-8')

    def isAvailable(self):
        return self.ser.isOpen()

    def writeData(self, data):
        return self.ser.write(data.encode('utf-8'))

    def kill(self):
        self.ser.close()

class Graph():
    def __init__(self, x, y):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.ax.set_ylim([0, 50])
        self.xDat = x
        self.yDat = y
        self.line, = self.ax.plot(self.xDat, self.yDat)

    def animate(self, x, y):
        x = self.xDat+1
        y = 10*x
        self.xDat.append(x)
        self.yDat.append(y)
        self.line.set_xdata(self.xDat)
        self.line.set_ydata(self.yDat)
        return self.line,

def main():
    #execute code here
    # arduino = ArduinoCommunicator("PORT HERE");
    liveGraph = Graph([0, 1, 2], [0, 10, 20])
    ani = animation.FuncAnimation(liveGraph.fig, liveGraph.animate, fargs=(x,, y,), interval=50, blit=True)
    plt.show()

main();
