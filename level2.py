import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.pyplot import MultipleLocator

months = ["Jaunary", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
years = []
grid = {}
color_bar = {
   1: (0.37,0.31,0.64),
   2:(0.2,0.53,0.74),
   3:(0.4,0.76,0.65),
   4:(0.67,0.87,0.64),  
   5:(0.9,0.96,0.6),
   6:(1.0,0.88,0.55),
   7:(0.99,0.68,0.38),
   8:(0.96,0.43,0.26),
   9:(0.84,0.24,0.31),
   10:(0.62,0.0,0.26)
}

df = pd.read_csv("temperature_daily.csv")
df_bg = df
df_bg.index = pd.to_datetime(df["date"])
df = df.set_index([df.index.year, df.index.month, df.index.day])
df.index.names = ["year", "month", "day"]
df = df.loc[([x for x in range (2008, 2018)]), :]
df_bg = df_bg.groupby(by=[df_bg.index.year, df_bg.index.month]).agg({"max_temperature": "max", "min_temperature": "min"})
df_bg = df_bg.loc[([x for x in range(2008, 2018)]), :]
max_temp = df_bg["max_temperature"].unstack()
min_temp = df_bg["min_temperature"].unstack()

fig = plt.figure(figsize=(10, 8))
gs = fig.add_gridspec(1, 2, width_ratios=[10, 1])
gs0 = gs[0].subgridspec(12, 10, hspace=0, wspace=0)
gs1 = gs[1].subgridspec(10, 1)

ax = fig.add_subplot(gs[0])
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.spines["top"].set_visible(False)
ax.spines["bottom"].set_visible(False)
ax.set_yticks([x for x in range(1, 13)])
ax.set_yticklabels(months)
ax.invert_yaxis()
ax.set_ylabel("Month")
ax.set_xticks([x for x in range(41)])
ax.xaxis.set_major_locator(MultipleLocator(4))
years = [0 ,0] + [x for x in range(2008, 2018)]
ax.set_xticklabels(years)
ax.set_xlabel("Years")

for i in range(12):
    for j in range(10):
        try:
            ax = fig.add_subplot(gs0[i, j])
            ax.set_facecolor(color_bar[int(max_temp.iat[j, i]/4)+1])
            ax.plot(df.loc[2008+j, i+1]["max_temperature"], color="green")
            ax.plot(df.loc[2008+j, i+1]["min_temperature"], color="blue")
            ax.set_xticks([])
            ax.set_yticks([])
            grid[ax] = (j, i)
        except:
            ax.patch.set_alpha(0)
            ax.set_xticks([])
            ax.set_yticks([])
fig.suptitle("Max Temperature Heatmap")

ax = plt.gca()
annot = ax.annotate("", xy=(0,0), xytext=(10, 10) ,xycoords="figure pixels", textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"))
annot.set_visible(False)

ax = fig.add_subplot(gs1[:, 0])
arr = np.zeros([10, 1, 3], dtype=float)
for i in range(10):
    for j in range(3):
        arr[i][0][j] = color_bar[i+1][j]
ax.imshow(arr, extent=[0, 1, 40, 0])
ax.set_xticks([])

def hover(event):
    global ax
    global annot
    if event.inaxes in grid:
        cur_x = grid[event.inaxes][0]
        cur_y = grid[event.inaxes][1]
        annot.xy = (event.x, event.y)
        text = "Date:{} - {}, Max: {}, Min: {}"\
            .format(cur_x+2008, cur_y+1, max_temp.iat[cur_x, cur_y], min_temp.iat[cur_x, cur_y])
        annot.set_text(text)
        annot.set_visible(True)
        plt.draw()
    else:
        annot.set_visible(False)
        plt.draw()

def on_click(event):
    global annot
    if fig._suptitle.get_text() == "Max Temperature Heatmap":
        fig.clf()
        ax = fig.add_subplot(gs[0])
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.spines["top"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.set_yticks([x for x in range(1, 13)])
        ax.set_yticklabels(months)
        ax.invert_yaxis()
        ax.set_ylabel("Month")
        ax.set_xticks([x for x in range(41)])
        ax.xaxis.set_major_locator(MultipleLocator(4))
        years = [0 ,0] + [x for x in range(2008, 2018)]
        ax.set_xticklabels(years)
        ax.set_xlabel("Year")

        grid.clear()
        for i in range(12):
            for j in range(10):
                try:
                    ax = fig.add_subplot(gs0[i, j])
                    ax.set_facecolor(color_bar[int(min_temp.iat[j, i]/4)+1])
                    ax.plot(df.loc[2008+j, i+1]["max_temperature"], color="green")
                    ax.plot(df.loc[2008+j, i+1]["min_temperature"], color="blue")
                    ax.set_xticks([])
                    ax.set_yticks([])
                    grid[ax] = (j, i)
                except:
                    ax.patch.set_alpha(0)
                    ax.set_xticks([])
                    ax.set_yticks([])
                    
        ax = fig.add_subplot(gs1[:, 0])
        arr = np.zeros([10, 1, 3], dtype=float)
        for i in range(10):
            for j in range(3):
                arr[i][0][j] = color_bar[i+1][j]
        ax.imshow(arr, extent=[0, 1, 40, 0])
        ax.set_xticks([]) 
        fig.suptitle("Min Temperature Heatmap")

        ax = plt.gca()
        annot = ax.annotate("", xy=(0,0), xytext=(10, 10) ,xycoords="figure pixels", textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"))
        annot.set_visible(False)

        plt.draw()
    else:        
        fig.clf()
        ax = fig.add_subplot(gs[0])
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.spines["top"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.set_yticks([x for x in range(1, 13)])
        ax.set_yticklabels(months)
        ax.invert_yaxis()
        ax.set_ylabel("Month")
        ax.set_xticks([x for x in range(41)])
        ax.xaxis.set_major_locator(MultipleLocator(4))
        years = [0 ,0] + [x for x in range(2008, 2018)]
        ax.set_xticklabels(years)
        ax.set_xlabel("Year")

        grid.clear()
        for i in range(12):
            for j in range(10):
                try:
                    ax = fig.add_subplot(gs0[i, j])
                    ax.set_facecolor(color_bar[int(max_temp.iat[j, i]/4)+1])
                    ax.plot(df.loc[2008+j, i+1]["max_temperature"], color="green")
                    ax.plot(df.loc[2008+j, i+1]["min_temperature"], color="blue")
                    ax.set_xticks([])
                    ax.set_yticks([])
                    grid[ax] = (j, i)
                except:
                    ax.patch.set_alpha(0)
                    ax.set_xticks([])
                    ax.set_yticks([])
                    
        ax = plt.gca()
        annot = ax.annotate("", xy=(0,0), xytext=(10, 10) ,xycoords="figure pixels", textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"))
        annot.set_visible(False)

        ax = fig.add_subplot(gs1[:, 0])
        arr = np.zeros([10, 1, 3], dtype=float)
        for i in range(10):
            for j in range(3):
                arr[i][0][j] = color_bar[i+1][j]
        ax.imshow(arr, extent=[0, 1, 40, 0])
        ax.set_xticks([]) 

        fig.suptitle("Max Temperature Heatmap")

        ax = plt.gca()
        annot = ax.annotate("", xy=(0,0), xytext=(10, 10) ,xycoords="figure pixels", textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"))
        annot.set_visible(False)

        plt.draw()

fig.canvas.mpl_connect("motion_notify_event", hover)
plt.connect("button_press_event", on_click)
plt.show()