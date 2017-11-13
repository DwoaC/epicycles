'''
Draw pretty pictures based on epicycles.

The best examples of Epicycles is the spirograph toy.  This module is a toy to
explore using design patterns to implement circles holding circles.

The implementation is optimized for ease of reading but its not terribly inefficient
performance wise.
'''

from math import cos, pi, sin

import logging
from matplotlib import pyplot as plt

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class Circle:
    '''
    Circle represents one line defined by a radius, frequency and phase.

    If Circle has a parent circle that parent defines the center of the child.

    The draw method is called to render the series of circles defined by the
    parent relationship.
    '''
    num_points = 10000

    def __init__(self, radius, frequency, parent=None, phase=0, num_cycles=1):
        self.radius = radius
        self.frequency = frequency
        self.phase = phase
        self.parent = parent
        self.num_cycles = num_cycles

    def __repr__(self):
        return ('{0.__class__.__name__}('
                'radius={0.radius}, '
                'frequency={0.frequency})').format(self)

    def __str__(self):
        return ('('
                'r={0.radius}, '
                'f={0.frequency})').format(self)

    @property
    def period(self):
        _period = []
        for i in range(self.num_points):
            _period.append((i * self.step) + self.phase)
        return _period

    @property
    def step(self):
        return (2 * pi * self.num_cycles) / self.num_points

    @property
    def x(self):
        return self._calc_period_prop(cos)

    @property
    def y(self):
        return self._calc_period_prop(sin)

    @property
    def combined_x(self):
        return self._combinded_period_property('x')

    @property
    def combined_y(self):
        return self._combinded_period_property('y')

    def _combinded_period_property(self, property_name):
        if self.parent is None:
            return getattr(self, property_name)

        return [p + super_p for p, super_p in zip(
            getattr(self, property_name),
            getattr(self.parent, 'combined_' + property_name))]

    def _calc_period_prop(self, func):
        _p = []
        for t in self.period:
            _p.append(func(t * self.frequency) * self.radius)
        return _p

    def draw(self, ax=None):

        if ax is None:
            fig, axes = plt.subplots(2, 2)

        axes[0][0].plot(self.combined_x + [self.combined_x[0]],
                self.combined_y + [self.combined_y[0]], '-')
        axes[0][0].axis('equal')

        # ax.set_title(self.get_title())
        # axes[0][1].scatter(self.period, self.x)
        parent = self
        while parent is not None:
            axes[0][1].plot(parent.x)
            axes[1][0].plot(parent.y)
            parent = getattr(parent, 'parent')

    def get_title(self):
        if self.parent is None:
            return str(self)

        return '{parent}->{child}'.format(
            parent=self.parent.get_title(),
            child=self)


def series(num_circles, radius_func, frequency_func, phase_func=None, num_cycles=1):
    '''
    Factory for defining a series of circles.

    :param num_circles: int.  How many circles in the series
    :param radius_func: func. takes one parameter, i, and returns a float that
    defines the radius of the circle for a given circle in ther series
    :param frequency_func: func, same definition as radius
    :param phase_func: func(optional), same definition as phase
    :param num_cycles: int(optional). overrides the num_cycles parameter passed to circle
    :return: a circles objects
    '''
    circles = Circles()
    sub_c = None
    for i in range(num_circles):
        sub_c = Circle(radius=radius_func(i),
                       frequency=frequency_func(i),
                       phase=0 if phase_func is None else phase_func(i),
                       parent=sub_c,
                       num_cycles=num_cycles)
        circles.append(sub_c)
    return circles


class Circles:
    '''
    List like container class for holding circles.

    Implements the draw method to render the series.
    '''

    def __init__(self, circles=None):
        if circles is None:
            self.circles = []
        else:
            self.circles = circles

    def __add__(self, other):
        other[0].parent = self[-1]
        return Circles(self.circles + other.circles)

    def __getitem__(self, item):
        return self.circles[item]

    def append(self, item):
        item.parent = self.last
        self.circles.append(item)

    @property
    def last(self):
        try:
            return self.circles[-1]
        except IndexError:
            return None

    @property
    def first(self):
        try:
            return self.circles[0]
        except IndexError:
            return None

    def draw(self):
        return self.last.draw()

    def __getattr__(self, item):
        return getattr(self.last, item)

    def __repr__(self):
        return '{0.__class__.__name__}({0.circles})'.format(self)

if __name__ == '__main__':
    c = Circle(radius=1, frequency=1, parent=None)
    c2 = Circle(radius=0.5, frequency=2, parent=c)
    c2.draw()
    cs = series(4, radius_func=lambda i: 1/(2**i), frequency_func=lambda i: 2**i)
    cs = series(4, radius_func=lambda i: 1 / (2 ** i), frequency_func=lambda i: 2 ** i)
    # 1d square wave
    cs = series(80, radius_func=lambda i: 1/((2*i)+1), frequency_func=lambda i: (2*i)+1)
    # 2d square
    cs = series(3, radius_func=lambda i: [0.2, 1, 0.2, 0.3, 0.01, 0.01][i],
                          frequency_func=lambda i: [1, -1, 3, -5, 7, -10][i], phase_func=lambda i: [0, 0, pi, pi][i])

    # 4 nodes
    cs = series(10, radius_func=lambda i: 1 / ((4 * i) + 1), frequency_func=lambda i: (4 * i) + 1)
    # diamond
    cs = series(3, radius_func=lambda i: [0.1, 1, 0.2, 0.9][i], frequency_func=lambda i: [1, -1, 3, -3][i])
    # star
    cs = series(5, radius_func=lambda i: [0.1, 1, 0.3, 0.2, 0.1][i],
                          frequency_func=lambda i: [1, -1, 3, -5, 7][i])
    # tiangle
    cs = series(3, radius_func=lambda i: [0.2, 1, 0.4, 0.7, 0.01, 0.01][i], frequency_func=lambda i: [1, -1, 2, -4, 7, -10][i], phase_func=lambda i: [0 , 0, pi/2, 0][i])

