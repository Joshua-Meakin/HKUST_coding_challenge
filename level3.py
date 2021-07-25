import json
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import colors 
from matplotlib.pyplot import MultipleLocator

data = open("HKUST_coauthor_graph.json")
data = json.load(data)

nodes = data["nodes"]
edges = data["edges"]
nodes = pd.DataFrame(nodes)
edges = pd.DataFrame(edges)
nodes = nodes[nodes["dept"] == "CSE"]
nodes = nodes[(nodes["fullname"] != "") & (nodes["id"] != "")]
nodes = nodes[["fullname", "id"]]
edges = edges[["source", "target"]]
edges = edges[(edges["source"].isin(nodes["id"])) & (edges["target"].isin(nodes["id"]))]
nodes = nodes.reset_index(drop=True)
name_list = dict(zip(nodes["id"], nodes["fullname"]))
pos_list = dict(zip(nodes["fullname"], [x for x in range(len(nodes["fullname"]))]))
adj_axis = dict(zip([x for x in range(len(nodes["fullname"]))], nodes["fullname"]))
edges = edges.replace({
    "source": name_list,
    "target": name_list
})
edges = edges.reset_index(drop=True)

fig = plt.figure(figsize=(14, 8))
gs = fig.add_gridspec(nrows=1, ncols=2, width_ratios=[1, 1])
grid = {}

ax = fig.add_subplot(gs[0])
grid[ax] = 0
all_nodes = pd.unique(edges["source"].to_list()+edges["target"].to_list())
coord_name = {}
coord_x = []
coord_y = []
for node in all_nodes:
    coord = (random.randint(0, 100), random.randint(0, 100))
    coord_name[coord] = node
    coord_x.append(coord[0])
    coord_y.append(coord[1])
coord_name_helper = dict(zip(coord_name.values(), coord_name.keys()))

ax.scatter(coord_x, coord_y, marker='o', linewidth=8)
for i in range(len(all_nodes)):
    ax.annotate(text=all_nodes[i], xy=(coord_x[i], coord_y[i]), xytext=(coord_x[i]+1, coord_y[i]+1)) 
for row in edges.itertuples():
    source_node = coord_name_helper[row[1]]
    target_node = coord_name_helper[row[2]]
    ax.plot([source_node[0], target_node[0]], [source_node[1], target_node[1]], "r")
ax.set_xticks([])
ax.set_yticks([])
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.spines["top"].set_visible(False)
ax.spines["bottom"].set_visible(False)

adj = np.zeros(shape=(45, 45))
for row in edges.itertuples():
    adj[pos_list[row[1]], pos_list[row[2]]] = 1
    adj[pos_list[row[1]], pos_list[row[1]]] = 1
    adj[pos_list[row[2]], pos_list[row[2]]] = 1

cmap = colors.ListedColormap(["white", "yellow", "green"])
ax = fig.add_subplot(gs[1])
grid[ax] = 1
ax.imshow(adj, cmap=cmap)
ax.set_xticks([x for x in range(45)])
ax.set_xticklabels(nodes["fullname"], rotation=90)
ax.xaxis.set_major_locator(MultipleLocator(1))
ax.xaxis.set_ticks_position("top")
ax.set_yticks([x for x in range(45)])
ax.set_yticklabels(nodes["fullname"])
ax.yaxis.set_major_locator(MultipleLocator(1))
ax.yaxis.set_ticks_position("right")
ax.grid(b=True, which="both")

def hover(event):
    global adj
    try:
        if grid[event.inaxes] == 0:
            if int(event.xdata) in coord_x and int(event.ydata) in coord_y:
                name = coord_name[(int(event.xdata), int(event.ydata))]
                print(coord_name[name])
        if grid[event.inaxes] == 1:
            cur_x = int(event.xdata)
            cur_y = int(event.ydata)
            pos_list_helper = dict(zip(pos_list.values(), pos_list.keys()))
            if adj[cur_y, cur_x] == 1:
                print(pos_list_helper[cur_y], pos_list_helper[cur_x])
    except:
        pass

fig.canvas.mpl_connect("motion_notify_event", hover)
plt.show()
