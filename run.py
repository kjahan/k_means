import argparse
import pandas as pd

from clustering import Clustering
from point import Point

def main(fn, clusters_no):
    geo_locs = []
    #read location data from csv file and store each location as a Point(latit,longit) object
    df = pd.read_csv(fn)
    for index, row in df.iterrows():
        loc_ = Point(float(row['LAT']), float(row['LON']))  #tuples for location
        geo_locs.append(loc_)
    #run k_means clustering
    cluster = Clustering(geo_locs, clusters_no)
    flag = cluster.k_means(False)
    if flag == -1:
        print("Error in arguments!")
    else:
        #clustering results is a list of lists where each list represents one cluster
        print("Clustering results:")
        cluster.print_clusters(cluster.clusters)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run k-means for location data",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--input', type=str, default='NYC_Free_Public_WiFi_03292017.csv',
                        dest='inputfile', help='input location file name')
    parser.add_argument('--clusters', type=int, default=8, dest='clusters', help='number of clusters')
    args = parser.parse_args()
    fn = "data/" + args.inputfile
    main(fn, args.clusters)
