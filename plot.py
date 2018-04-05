import csv

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_the_stupid_dataset_in_glorious_3d(dataset_name='agriculturalland'):
    # Load data from csv
    raw = [row for row in csv.reader(open('datasets/{}.csv'.format(dataset_name)))]
    xkeys, raw = raw[0][1:], raw[1:]
    ykeys = [row[0] for row in raw]
    data = np.array([[float(x) for x in row[1:]] for row in raw])

    # Load colors from metadata
    colors = [row.strip() for row in open('datasets/{}.metadata'.format(dataset_name))]
    colors = [row.split() for row in colors if row.startswith('<color ')]
    colors = [row[1:4] for row in colors]
    colors = [tuple(int(x[3:-1])/255 for x in row) for row in colors]

    # Numpy-ize the data
    _x = np.arange(data.shape[0])
    _y = np.arange(data.shape[1])
    _xx, _yy = np.meshgrid(_x, _y)
    xs, ys = _xx.ravel(), _yy.ravel()
    zs = data[xs, ys]

    # https://stackoverflow.com/questions/18602660/matplotlib-bar3d-clipping-problems
    def get_camera(axis):
        r = np.square(np.max([axis.get_xlim(), axis.get_ylim()], 1)).sum()
        theta, phi = np.radians((90-axis.elev, axis.azim))

        x = r * np.sin(theta) * np.cos(phi)
        y = r * np.sin(theta) * np.sin(phi)
        return np.array((x, y))

    def get_distances(view):
        distances  = []
        a = np.array((xs, ys))
        for i in range(len(xs)):
            distance = (a[0, i] - view[0])**2 + (a[1, i] - view[1])**2
            distances.append(np.sqrt(distance))
        return distances

    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')
    bars = [ax.bar3d(x-.5, y-.5, 0, .7, .7, z, picker=1, zsort='max', color=colors[x]) for x, y, z in zip(xs, ys, zs)]

    plt.xticks(np.arange(len(xkeys)), xkeys)
    plt.yticks(np.arange(len(ykeys)), ykeys)

    def on_draw(event):
        camera = get_camera(ax)
        z_order = get_distances(camera)
        if ax.elev > 0:
            z_order = max(z_order) - z_order
        for bar, z_val in zip(bars, z_order):
            bar._sort_zpos = z_val
        # closest z order in picked -> red
        # else -> black
    on_draw(None)

    picked = []
    highlight = None

    def on_press(event):
        nonlocal picked
        nonlocal highlight

        if not picked:
            return

        if highlight:
            highlight.set_edgecolor('none')

        if ax.elev > 0:
            highlight = max(picked, key=lambda a: a._sort_zpos)
        else:
            highlight = min(picked, key=lambda a: a._sort_zpos)

        highlight.set_edgecolor('black')

        picked = []
        fig.canvas.draw()

    def on_pick(event):
        nonlocal picked
        picked.append(event.artist)

    fig.canvas.mpl_connect('draw_event', on_draw)
    fig.canvas.mpl_connect('button_press_event', on_press)
    fig.canvas.mpl_connect('pick_event', on_pick)

    plt.show()
