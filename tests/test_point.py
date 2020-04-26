import pytest

from src.point import Point

def test_euclidean_distance():
	point_1 = Point(10, 100)
	point_2 = Point(1, 10)
	assert point_1.euclidean_distance(point_2) == pytest.approx(90.44, 0.01)
