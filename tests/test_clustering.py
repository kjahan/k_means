import pytest

from src.point import Point
from src.clustering import KMeans

@pytest.fixture
def clusters_mock():
	return {0: [Point(1,2), Point(3,4)], 1: [Point(10,100)]}

@pytest.fixture
def kmeans_mock():
	model = KMeans([], 3)
	model.means = [Point(11,121), Point(-9,33)]
	return model

def test_compute_means(clusters_mock, kmeans_mock):
	means = kmeans_mock.compute_means(clusters_mock)
	print(kmeans_mock.print_means(means))
	assert len(means) == 2
	mean_1, mean_2 = means[0], means[1]
	assert mean_1.latit == 2 and mean_1.longit == 3
	assert mean_2.latit == 10 and mean_2.longit == 100

def test_passed_update_means(kmeans_mock):
	means = [Point(11.002,121), Point(-9,33.001)]
	threshold = 0.01
	assert kmeans_mock.update_means(means,threshold)

def test_failed_update_means(kmeans_mock):
	means = [Point(11.01,121), Point(-9,33.2)]
	threshold = 0.01
	assert not kmeans_mock.update_means(means,threshold)
