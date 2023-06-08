import os
import argparse
import pandas as pd
from src.clustering import KMeans
from src.point import Point

def main(dataset_fn, output_fn, clusters_no):
    # Read location data from csv file and store each location as a Point object
    df = pd.read_csv(dataset_fn)
    geo_locs = [Point(float(row['LAT']), float(row['LON'])) for _, row in df.iterrows()]

    # Run k-means clustering
    model = KMeans(geo_locs, clusters_no)
    flag = model.fit(True)
    if flag == -1:
        print("The number of points is less than the number of clusters!")
    else:
        # Save clustering results as a list of lists where each list represents one cluster
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
