from random import random

from compas.colors import Color
from compas.geometry import Point
from compas.geometry import Vector

from compas_viewer import Viewer

viewer = Viewer()

for x in range(5):
    for y in range(5):
        viewer.add(Vector(0, 0, 1), anchor=Point(x, y, 0), linescolor=Color.from_i(random()))

viewer.show()
