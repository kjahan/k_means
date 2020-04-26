import random as rand
import math
import numpy as np
import matplotlib.pyplot as plt
import csv

from src.point import Point

class KMeans:
    def __init__(self, geo_locs_, k_):
        self.geo_locations = geo_locs_
        self.k = k_
        self.clusters = None  # clusters of nodes
        self.means = []     # means of clusters
        self.debug = False  # debug flag

    def next_random(self, index, points, clusters):
        # this method returns the next random node
        # pick next node that has the maximum distance from other nodes
        dist = {}
        for point_1 in points:
            if self.debug:
                print("point_1: {} {}".format(point_1.latit, point_1.longit))
            #compute this node distance from all other points in cluster
            for cluster in clusters.values():
                point_2 = cluster[0]
                if self.debug:
                    print("point_2: {} {}".format(point_2.latit, point_2.longit))
                if point_1 not in dist:
                    dist[point_1] = math.sqrt(math.pow(point_1.latit - point_2.latit,2.0) + math.pow(point_1.longit - point_2.longit,2.0))       
                else:
                    dist[point_1] += math.sqrt(math.pow(point_1.latit - point_2.latit,2.0) + math.pow(point_1.longit - point_2.longit,2.0))
        if self.debug:
            for key, value in dist.items():
                print("({}, {}) ==> {}".format(key.latit, key.longit, value))
        #now let's return the point that has the maximum distance from previous nodes
        count_ = 0
        max_ = 0
        for key, value in dist.items():
            if count_ == 0:
                max_ = value
                max_point = key
                count_ += 1
            else:
                if value > max_:
                    max_ = value
                    max_point = key
        return max_point

    def initial_means(self, points):
        # compute the initial means
        # pick the first node at random
        point_ = rand.choice(points)
        if self.debug:
            print("point#0: {} {}".format(point_.latit, point_.longit))
        clusters = dict()
        clusters.setdefault(0, []).append(point_)
        points.remove(point_)
        #now let's pick k-1 more random points
        for i in range(1, self.k):
            point_ = self.next_random(i, points, clusters)
            if self.debug:
                print("point#{}: {} {}".format(i, point_.latit, point_.longit))
            #clusters.append([point_])
            clusters.setdefault(i, []).append(point_)
            points.remove(point_)
        # compute mean of clusters
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
                #print "compute: point(%f,%f)" % (point.latit, point.longit)
                mean_point.latit += point.latit
                mean_point.longit += point.longit
                cnt += 1.0
            mean_point.latit = mean_point.latit/cnt
            mean_point.longit = mean_point.longit/cnt
            means.append(mean_point)
        return means

    def assign_points(self, points):
        # assign nodes to the cluster with the smallest mean
        if self.debug:
            print("assign points")
        clusters = dict()
        for point in points:
            dist = []
            if self.debug:
                print("point({},{})".format(point.latit, point.longit))
            #find the best cluster for this node
            for mean in self.means:
                dist.append(math.sqrt(math.pow(point.latit - mean.latit,2.0) + math.pow(point.longit - mean.longit,2.0)))
            #let's find the smallest mean
            if self.debug:
                print(dist)
            cnt_ = 0
            index = 0
            min_ = dist[0]
            for d in dist:
                if d < min_:
                    min_ = d
                    index = cnt_
                cnt_ += 1
            if self.debug:
                print("index: {}".format(index))
            clusters.setdefault(index, []).append(point)
        return clusters

    def update_means(self, means, threshold):
        # compare current means with the previous ones to see if we have to stop
        for i in range(len(self.means)):
            mean_1 = self.means[i]
            mean_2 = means[i]
            if self.debug:
                print("mean_1({},{})".format(mean_1.latit, mean_1.longit))
                print("mean_2({},{})".format(mean_2.latit, mean_2.longit))          
            if math.sqrt(math.pow(mean_1.latit - mean_2.latit,2.0) + math.pow(mean_1.longit - mean_2.longit,2.0)) > threshold:
                return False
        return True

    def save(self, filename="output.csv"):
        # save clusters into a csv file
        with open(filename, mode='w') as csv_file:
            writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['latitude', 'longitude', 'cluster_id'])
            cluster_id = 0
            for cluster in self.clusters.values():
                for point in cluster:
                    writer.writerow([point.latit, point.longit, cluster_id])
                cluster_id += 1

    def print_clusters(self, clusters=None):
        if not clusters:
            clusters = self.clusters
        # debug function: print cluster points
        cluster_id = 0
        for cluster in clusters.values():
            print("nodes in cluster #{}".format(cluster_id))
            cluster_id += 1
            for point in cluster:
                print("point({},{})".format(point.latit, point.longit))

    def print_means(self, means):
        # print means
        for point in means:
            print("{} {}".format(point.latit, point.longit))

    def fit(self, plot_flag):
        # Run k_means algorithm
        if len(self.geo_locations) < self.k:
            return -1   #error
        points_ = [point for point in self.geo_locations]
        #compute the initial means
        self.initial_means(points_)
        stop = False
        iterations = 1
        print("Starting K-Means...")
        while not stop:
            # assignment step: assign each node to the cluster with the closest mean
            points_ = [point for point in self.geo_locations]
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
                self.means = []
                self.means = means
            iterations += 1
        print("K-Means is completed in {} iterations. Check outputs.csv for clustering results!".format(iterations))
        self.clusters = clusters
        #plot cluster for evluation
        if plot_flag:
            fig = plt.figure()
            ax = fig.add_subplot(111)
            markers = ['o', 'd', 'x', 'h', 'H', 7, 4, 5, 6, '8', 'p', ',', '+', '.', 's', '*', 3, 0, 1, 2]
            colors = ['r', 'k', 'b', [0,0,0], [0,0,1], [0,1,0], [0,1,1], [1,0,0], [1,0,1], [1,1,0], [1,1,1]]
            cnt = 0
            for cluster in clusters.values():
                latits = []
                longits = []
                for point in cluster:
                    latits.append(point.latit)
                    longits.append(point.longit)
                ax.scatter(longits, latits, s=60, c=colors[cnt], marker=markers[cnt])
                cnt += 1
            plt.show()
        return 0