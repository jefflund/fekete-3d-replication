import csv

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

raw = [row for row in csv.reader(open('datasets/education.csv'))]
xkeys, raw = raw[0][1:], raw[1:]
ykeys = [row[0] for row in raw]
data = np.array([[float(x) for x in row[1:]] for row in raw])

_x = np.arange(data.shape[0])
_y = np.arange(data.shape[1])
_xx, _yy = np.meshgrid(_x, _y)
x, y = _xx.ravel(), _yy.ravel()

dz = data[x, y]
z = np.zeros_like(dz)
dx = dy = .8

fig = plt.figure(figsize=(8, 8))
ax1 = fig.add_subplot(111, projection='3d')
ax1.bar3d(x, y, z, dx, dy, dz, zsort='min', picker=5)

def on_draw(_):
    # TODO fix z-order
    pass

def on_pick(event):
    print(event.artist)
    event.artist.set_edgecolor('red')
    fig.canvas.draw()


fig.canvas.mpl_connect('draw_event', on_draw)
fig.canvas.mpl_connect('pick_event', on_pick)

plt.show()
