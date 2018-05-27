import random as rand
from clustering import clustering
from point import Point
import csv
import sys
''' input 1st parameter to the number of clusters want to generate within 11 '''
geo_locs = []
#loc_ = Point(0.0, 0.0)  #tuples for location
#geo_locs.append(loc_)
#read the fountains location from the csv input file and store each fountain location as a Point(latit,longit) object
f = open('fountain.csv', 'r')
reader = csv.reader(f, delimiter=",")
for line in reader:
    loc_ = Point(float(line[0]), float(line[1]))  #tuples for location
    geo_locs.append(loc_)
#print len(geo_locs)
#for p in geo_locs:
#    print "%f %f" % (p.latit, p.longit)
#let's run k_means clustering. the second parameter is the no of clusters
try:
    cluster = clustering(geo_locs, int(sys.argv[1]))
except:
    cluster = clustering(geo_locs,5)
flag = cluster.k_means(True)
if flag == -1:
    print("Error in arguments!")
else:
    #the clustering results is a list of lists where each list represents one cluster
    print("clustering results:")
    cluster.print_clusters(cluster.clusters)
