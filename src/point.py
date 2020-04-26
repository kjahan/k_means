import math

class Point:
    def __init__(self, latit_, longit_):
        self.latit = latit_
        self.longit = longit_

    def euclidean_distance(self, another_point):
        return math.sqrt(math.pow(self.latit - another_point.latit, 2.0) + math.pow(self.longit - another_point.longit, 2.0))
