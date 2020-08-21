import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np
import time
from math import *

style.use('fivethirtyeight')

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

def animate(i):
    xs = []
    ys = []
    x1 = i*0.03
    y1 = sin(x1)
    x2 = (i+1)*0.03
    y2 = sin(x2)
    xs.append(float(x1))
    ys.append(float(y1))
    xs.append(float(x2))
    ys.append(float(y2))
    print(xs)
    # ax1.clear()
    ax1.plot(xs, ys, "-b")

ani = animation.FuncAnimation(fig, animate, interval=30)
plt.show()
