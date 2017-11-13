import unittest
from math import pi

from epicycles.core.epicycles import Circle, Circles


class TestEpicycles(unittest.TestCase):

    def setUp(self):
        self.c = Circle(radius=1, frequency=1, parent=None)
        self.sub_c = Circle(radius=1, frequency=1, parent=self.c)

    def test_period(self):
        self.c.num_points = 2
        self.assertListEqual(self.c.period, [0, pi])
        self.assertEqual(len(self.c.x), self.c.num_points)
        self.assertEqual(len(self.c.combined_x), self.c.num_points)

    def test_circles(self):
        circles = Circles()
        circles.append(Circle(
            radius=1,
            frequency=1,
        ))
        circles.append(Circle(
            radius=0.5,
            frequency=2
        ))
        self.assertEqual(circles.last.parent, circles.first)
        circles.draw()