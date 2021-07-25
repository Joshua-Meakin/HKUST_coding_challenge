from os import terminal_size
from numpy.core.arrayprint import dtype_short_repr
from matplotlib.widgets import Button
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

months = ["Jaunary", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

df = pd.read_csv("temperature_daily.csv")
df.index = pd.to_datetime(df["date"])
df = df.groupby(by=[df.index.month, df.index.year]).agg({"max_temperature": "max", "min_temperature": "min"})
max_temp = df["max_temperature"].unstack()
min_temp = df["min_temperature"].unstack()
max_temp.index.names = ["Month"]
max_temp.index = months
min_temp.index.names = ["Month"]
min_temp.index = months
fig = plt.figure()
ax = sns.heatmap(max_temp, linewidths=6)
ax.set_xlabel("Year")
ax.set_title("Max Temperature Heatmap")
annot = ax.annotate("", xy=(0,0),xytext=(10, 10), textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"))
annot.set_visible(False)

def hover(event):
    if event.xdata is not None and event.ydata is not None:
        cur_x, cur_y = int(event.xdata), int(event.ydata)
        if cur_x <= 20 and cur_x >= 0 and cur_y <= 12 and cur_y >= 0:
            annot.xy = (event.xdata, event.ydata)
            text = "Date:{} - {}, Max: {}, Min: {}"\
                .format(cur_x + 1997, cur_y + 1, max_temp.iat[cur_y, cur_x], min_temp.iat[cur_y, cur_x])
            annot.set_text(text)
            annot.set_visible(True) 
            plt.draw()
            if event.xdata - cur_x < 0.2 or event.xdata - cur_x > 0.8 or event.ydata - cur_y < 0.2 or event.ydata - cur_y > 0.8:
                annot.set_visible(False)
                plt.draw()
        else:
            annot.set_visible(False) 
            plt.draw()

def on_leave(event):
   annot.set_visible(False)
   plt.draw() 

def on_click(event):
    global ax
    global annot
    if ax.get_title() == "Max Temperature Heatmap":
        plt.clf() 
        ax = sns.heatmap(min_temp, linewidths=6)
        ax.set_title("Min Temperature Heatmap")
        ax.set_xlabel("Year")
        annot = ax.annotate("", xy=(0,0),xytext=(10, 10), textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"))
        annot.set_visible(False)
        plt.draw() 
    else:
        plt.clf() 
        ax = sns.heatmap(max_temp, linewidths=6)
        ax.set_title("Max Temperature Heatmap")
        ax.set_xlabel("Year")
        annot = ax.annotate("", xy=(0,0),xytext=(10, 10), textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"))
        annot.set_visible(False)
        plt.draw() 

fig.canvas.mpl_connect("motion_notify_event", hover)
fig.canvas.mpl_connect("axes_leave_event", on_leave)
fig.canvas.mpl_connect("figure_leave_event", on_leave)
plt.connect("button_press_event", on_click)
plt.show()

