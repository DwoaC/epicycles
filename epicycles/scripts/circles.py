from epicycles import Circle, Circles, series
from math import pi

import matplotlib.animation as animation
from matplotlib import pyplot as plt
import numpy as np

def add_two_circles():
    circles = Circles()
    circles.append(Circle(
        radius=1,
        frequency=1,
    ))
    circles.append(Circle(
        radius=0.5,
        frequency=2
    ))
    circles.draw()

def add_two_waves_equal_funk():
    cs = series(
        10,
        radius_func=lambda i: 1/((2*i)+1),
        frequency_func=lambda i: (2*i)+1)
    cs2 = series(
        10,
        radius_func=lambda i: 1/((2*i)+1),
        frequency_func=lambda i: -(2*i)+1,
        phase_func=lambda i: pi/2
    )
    cs = cs + cs2
    cs.draw()

def square():
    cs = series(
        3,
        radius_func=lambda i: [0.2, 1, 0.2, 0.3, 0.01, 0.01][i],
        frequency_func=lambda i: [1, -1, 3, -5, 7, -10][i],
        phase_func=lambda i: [0, 0, pi, pi][i])
    cs.draw()


def animate():
    fig = plt.figure()
    ax = fig.add_subplot(111, autoscale_on=False, xlim=(-2, 2), ylim=(-2, 2))

    line, = ax.plot([], [], '-', lw=1)
    # title, = ax.set_title('')
    def init():
        line.set_data([], [])
        # title.set_data('')
        return [line]

    def animate(t):
        cs = series(2, radius_func=lambda i: [1, 0.3][i],
                    frequency_func=lambda i: [1, -t][i],
                    phase_func=lambda i: [0, pi/2][i],
                    num_cycles=10)

        line.set_data(cs.combined_x,
                      cs.combined_y)
        # title.set_data(str(t))
        return [line]

    ani = animation.FuncAnimation(fig, animate, frames=np.arange(1, 2, step=0.001),
                                  interval=1, blit=True, init_func=init)
    plt.show()

if __name__=='__main__':
    add_two_circles()