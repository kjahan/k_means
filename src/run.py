import os
import argparse
import pandas as pd

from src.clustering import KMeans
from src.point import Point

def main(dataset_fn, output_fn, clusters_no):
    geo_locs = []
    # read location data from csv file and store each location as a Point(latit,longit) object
    df = pd.read_csv(dataset_fn)
    for index, row in df.iterrows():
        loc_ = Point(float(row['LAT']), float(row['LON']))  #tuples for location
        geo_locs.append(loc_)
    # run k_means clustering
    model = KMeans(geo_locs, clusters_no)
    flag = model.fit(True)
    if flag == -1:
        print("No of points are less than cluster number!")
    else:
        # save clustering results is a list of lists where each list represents one cluster
        model.save(output_fn)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run k-means for location data",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--input', type=str, default='NYC_Free_Public_WiFi_03292017.csv',
                        dest='input', help='input location file name')
    parser.add_argument('--output', type=str, default='output.csv', dest='output', 
                        help='clusters output file name')
    parser.add_argument('--clusters', type=int, default=8, dest='clusters', help='number of clusters')
    args = parser.parse_args()
    input_fn = os.path.join("data", args.input)
    output_fn = args.output
    main(input_fn, output_fn, args.clusters)
