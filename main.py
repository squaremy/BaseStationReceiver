# import stuff here
import serial
from tkinter import *
# import _thread
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.backend_bases import key_press_handler
import matplotlib.animation as animation
from matplotlib import style
style.use("ggplot")
from matplotlib.widgets import Slider
from matplotlib.widgets import TextBox

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
    ts = []
    xDat = []
    yDat = []
    def __init__(self, master, x, y):
        master.columnconfigure(0, weight=1)
        master.rowconfigure(1, weight=1)
        self.master = master
        self.master.title("Base Station")
        self.master.geometry("800x600")
        self.master.attributes("-zoomed", False)
        # self.fig = plt.figure()
        # self.ax = self.fig.add_subplot(1, 1, 1)
        # self.ax.set_ylim([0, 50])
        self.xDat = x
        self.yDat = y
        # self.line, = self.ax.plot(self.xDat, self.yDat)
        self.plotGraph(1)
        self.createGraph()
        self.master.bind("<Escape>", self.end_fullscreen)

    def end_fullscreen(self, event=None):
        self.state = False
        sys.exit()

    def animate(self, x, y):
        x = self.xDat+1
        y = 10*x
        self.xDat.append(x)
        self.yDat.append(y)
        self.line.set_xdata(self.xDat)
        self.line.set_ydata(self.yDat)
        return self.line,

    def createGraph(self):
        self.frame = Frame(self.master)
        self.frame.grid(column=0,row=1,columnspan=4, rowspan=3, sticky=N+W+E+S)
        self.f = Figure( figsize=(8, 7), dpi=80 )
        self.ax0 = self.f.add_axes([.05, .625, .4, .35], frameon=False, label='X Orientation')
        self.ax0.set_xlabel( 'Latitude' )
        self.ax0.set_ylabel( 'Longitude' )
        self.ax0.grid(color='r', linestyle='-', linewidth=2)
        self.ax1 = self.f.add_axes([.55, .625, .4, .35], frameon=False, label='Y Orientation')
        self.ax1.set_xlabel('Time (ms)')
        self.ax1.set_ylabel('Degree')
        self.sliderAxis = self.f.add_axes([.075, .525, .325, .025])
        self.sliderAxis1 = self.f.add_axes([.6, .525, .325, .025])
        self.sliderAxis2 = self.f.add_axes([.35, .025, .325, .025])
        self.canvas = FigureCanvasTkAgg(self.f, master=self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)
        self.toolbar = NavigationToolbar2TkAgg(self.canvas, self.frame)
        self.slider = Slider(self.sliderAxis, "Latitude", -180, 180, valinit=0, valstep=1)
        self.slider.on_changed(self.plotGraph)
        self.slider1 = Slider(self.sliderAxis1, "Longitude", -180, 180, valinit=0, valstep=1)
        self.slider1.on_changed(self.plotGraph)
        self.toolbar.update()

    def plotGraph(self, val):
        xData = []
        yData = []
        for i in range(0,len(self.ts)):
            xData.append(self.slider.val)
            yData.append(self.slider1.val)
        # arduino.writeData("Lat:" + str(self.slider.val))
        # arduino.writeData("Lng:" + str(self.slider1.val))
        self.line, = self.ax0.plot(self.ts,xData)
        self.line.set_color("blue")
        self.line1, = self.ax1.plot(self.ts,yData)
        self.line1.set_color("blue")
        self.addOrientationData()
        self.l, = self.ax0.plot(self.ts, self.ox)
        self.l.set_color("black")
        self.l1, = self.ax1.plot(self.ts, self.oy)
        self.l1.set_color("black")
        self.canvas.draw()

def main():
    #execute code here
    liveGraph = Graph(root, [0, 1, 2], [0, 10, 20])
    # ani = animation.FuncAnimation(liveGraph.fig, liveGraph.animate, fargs=(x,, y,), interval=50, blit=True)
    # plt.show()
    root.mainloop()

# arduino = ArduinoCommunicator("PORT HERE");
main();
