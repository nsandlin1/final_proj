# helpful: prometheus.io/docs/prometheus/latest/querying/api/

from requests import get
import tkinter as tk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from itertools import count

WIDTH = 600
HEIGHT = 400

PROMETHEUS_QUERY = 'http://192.168.1.191:9090/api/v1/query'

# basic class representing tk window
class Window(tk.Tk):
    def __init__(self, *args, **kwargs):
        # initialize master window with arbitrary *args **kwargs
        tk.Tk.__init__(self, *args, **kwargs)
        self.type = "temperature"
        self.basic()

    def basic(self):
        
        # possibly needed? Don't think so
        # figure = Figure()

        b1 = tk.Button(self, text="Temperature", command=self.plot_temperature)
        b1.place(x=510, y=150)
        b2 = tk.Button(self, text="Humidity", command=self.plot_humidity)
        b2.place(x=517, y=205)

    def plot_temperature(self):
        self.clear()
        self.basic()
        self.label = tk.Label(self, text="Temperature Graph") # specify
        self.label.pack(pady=17)
        
        self.plot("temperature")

    def plot_humidity(self):
        self.clear()
        self.basic()
        self.label = tk.Label(self, text="Humidity Graph") # specify
        self.label.pack(pady=17)

        self.plot("humidity")

    def clear(self):
        try: 
            plt.close() # close current figure
        except: print('no'); pass

        for i in self.winfo_children():
            i.destroy()

    def plot(self, type): 

        # subwindow containing live temperature graph of prometheus metrics
        # if type == "temperature":
        #     label = tk.Label(self, text="Temperature Graph")
        # if type == "humidity":
        #     label = tk.Label(self, text="Humidity Graph")
        # update window

        # convenient organizational tool for creation of subplots and multi-plot management
        # returns figure and array of axes objects (the ladder not used)
        self.fig, _ = plt.subplots(figsize=(5, 3)) #figsize=(5, 3)
        # axis.set(), _
        
        # configure plot style
        plt.style.use('fivethirtyeight')

        # lists for storage of time-interval (X) and metric(Y)
        x_values = []
        y_values = []

        # special count object is standard itertool object allowing incrementation (and maybe decrementation)
        # this is usefule is keeping a running count
        # in this case it increments by 15, which represents the 15 seconds that pass between data-pull-requests
        # from prometheus
        index = count(start=0, step=15)

        # animate is standard method used in animation of matplotlib plots
        def animate(i):
            # next() function increments custom count object by specified interval
            x_values.append(next(index)) # append n-1 + 15 to n slot of x_values
            # get function pulls data from specified url with params keyword performing metric query
            # in this case it makes a query request from prometheus for latest temperature_data metric
            if type == "temperature":
                data = get(PROMETHEUS_QUERY, params={'query': "temperature_data"})
            if type == "humidity":
                data = get(PROMETHEUS_QUERY, params={'query': "humdity_data"})
            
            data = data.json() # convert data to json string
            #print(data['data']) # debugging
            y_values.append(data['data']['result'][0]['value'][1]) # get data value
            
            # plt.cla() is necessary to wipe subwindow and replot. This allows a steady line color to be maintained.
            plt.cla()
            # plot x and y values
            plt.plot(x_values, y_values)

        # FuncAnimation animates function. returns nothing (that i need at least)
        _ = FuncAnimation(self.fig, animate, interval=15000, blit=False) # first: plt.gcf()

        # initialize canvas and insert graph into it
        canvas = FigureCanvasTkAgg(self.fig, master=self)
        # update canvas ... window.plot(*args, **kwargs) is depricated?
        canvas.draw()
        
        # insert vanilla matplotlib toolbar into canvas
        toolbar = NavigationToolbar2Tk(canvas, self)
        # toolbar.update similar to plt.plot and canvas.draw above
        toolbar.update()

        # simply returns canvas widget... used to distance tk widget and implementation of FigureCanvasTkAgg
        # object. thus requres implementation as if two individual and unrelated packages
        canvas.get_tk_widget().pack(side=tk.LEFT)

# instantiate root window and run tkinter mainloop
root = Window()
root.geometry("{}x{}".format(WIDTH, HEIGHT))
root.mainloop()