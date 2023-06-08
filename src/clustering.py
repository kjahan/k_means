import random
import math
import numpy as np
import matplotlib.pyplot as plt
import csv

from src.point import Point

class KMeans:
    def __init__(self, geo_locs, k):
        self.geo_locations = geo_locs
        self.k = k
        self.clusters = None
        self.means = []
        self.debug = False

    def next_random(self, index, points, clusters):
        # This method returns the next random node
        # Pick the next node that has the maximum distance from other nodes
        dist = {}
        for point_1 in points:
            if self.debug:
                print(f"point_1: {point_1.latit} {point_1.longit}")
            # Compute the distance of this node from all other points in the cluster
            for cluster in clusters.values():
                point_2 = cluster[0]
                if self.debug:
                    print(f"point_2: {point_2.latit} {point_2.longit}")
                if point_1 not in dist:
                    dist[point_1] = math.sqrt((point_1.latit - point_2.latit) ** 2 + (point_1.longit - point_2.longit) ** 2)
                else:
                    dist[point_1] += math.sqrt((point_1.latit - point_2.latit) ** 2 + (point_1.longit - point_2.longit) ** 2)
        if self.debug:
            for key, value in dist.items():
                print(f"({key.latit}, {key.longit}) ==> {value}")
        # Now let's return the point that has the maximum distance from previous nodes
        max_point = max(dist, key=dist.get)
        return max_point

    def initial_means(self, points):
        # Compute the initial means
        # Pick the first node at random
        point_ = random.choice(points)
        if self.debug:
            print(f"point#0: {point_.latit} {point_.longit}")
        clusters = {0: [point_]}
        points.remove(point_)
        # Now let's pick k-1 more random points
        for i in range(1, self.k):
            point_ = self.next_random(i, points, clusters)
            if self.debug:
                print(f"point#{i}: {point_.latit} {point_.longit}")
            clusters[i] = [point_]
            points.remove(point_)
        # Compute mean of clusters
        self.means = self.compute_means(clusters)
        if self.debug:
            print("initial means:")
            self.print_means(self.means)

    def compute_means(self, clusters):
        means = []
        for cluster in clusters.values():
            mean_point = Point(0.0, 0.0)
            cnt = 0.0
            for point in cluster:
                mean_point.latit += point.latit
                mean_point.longit += point.longit
                cnt += 1.0
            mean_point.latit /= cnt
            mean_point.longit /= cnt
            means.append(mean_point)
        return means

    def assign_points(self, points):
        # Assign nodes to the cluster with the smallest mean
        if self.debug:
            print("assign points")
        clusters = {}
        for point in points:
            dist = []
            if self.debug:
                print(f"point({point.latit},{point.longit})")
            # Find the best cluster for this node
            for mean in self.means:
                dist.append(math.sqrt((point.latit - mean.latit) ** 2 + (point.longit - mean.longit) ** 2))
            # Let's find the smallest mean
            if self.debug:
                print(dist)
            index = dist.index(min(dist))
            clusters.setdefault(index, []).append(point)
        return clusters

    def update_means(self, means, threshold):
        # Compare current means with the previous ones to see if we have to stop
        for mean_1, mean_2 in zip(self.means, means):
            if math.sqrt((mean_1.latit - mean_2.latit) ** 2 + (mean_1.longit - mean_2.longit) ** 2) > threshold:
                return False
        return True

    def save(self, filename="output.csv"):
        # Save clusters into a CSV file
        with open(filename, mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['latitude', 'longitude', 'cluster_id'])
            for cluster_id, cluster in enumerate(self.clusters.values()):
                for point in cluster:
                    writer.writerow([point.latit, point.longit, cluster_id])

    def print_clusters(self, clusters=None):
        if not clusters:
            clusters = self.clusters
        # Debug function: print cluster points
        for cluster_id, cluster in enumerate(clusters.values()):
            print(f"nodes in cluster #{cluster_id}")
            for point in cluster:
                print(f"point({point.latit},{point.longit})")

    def print_means(self, means):
        # Print means
        for point in means:
            print(f"{point.latit} {point.longit}")

    def fit(self, plot_flag):
        # Run k-means algorithm
        if len(self.geo_locations) < self.k:
            return -1   # Error
        points_ = self.geo_locations.copy()
        # Compute the initial means
        self.initial_means(points_)
        stop = False
        iterations = 1
        print("Starting K-Means...")
        while not stop:
            # Assignment step: assign each node to the cluster with the closest mean
            points_ = self.geo_locations.copy()
            clusters = self.assign_points(points_)
            if self.debug:
                self.print_clusters(clusters)
            means = self.compute_means(clusters)
            if self.debug:
                print("means:")
                self.print_means(means)
                print("update mean:")
            stop = self.update_means(means, 0.01)
            if not stop:
                self.means = means
            iterations += 1
        print(f"K-Means completed in {iterations} iterations. Check output.csv for clustering results!")
        self.clusters = clusters
        # Plot cluster for evaluation
        if plot_flag:
            fig = plt.figure()
            ax = fig.add_subplot(111)
            markers = ['o', 'd', 'x', 'h', 'H', 7, 4, 5, 6, '8', 'p', ',', '+', '.', 's', '*', 3, 0, 1, 2]
            colors = ['r', 'k', 'b', [0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1], [1, 0, 0], [1, 0, 1], [1, 1, 0], [1, 1, 1]]
            for cluster_id, cluster in enumerate(clusters.values()):
                latits = []
                longits = []
                for point in cluster:
                    latits.append(point.latit)
                    longits.append(point.longit)
                ax.scatter(longits, latits, s=60, c=colors[cluster_id % len(colors)], marker=markers[cluster_id % len(markers)])
            plt.show()
        return 0
