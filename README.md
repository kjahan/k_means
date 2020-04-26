K-Means
=======

## General description
 
This project is a Python implementation of k-means clustering algorithm.

## Requirements

You should setup the conda environment (i.e. kmeans) using the environment.yml file:

`conda env create -f environment.yml`

## Activate conda environment:

`conda activate kmeans`

(Run `unset PYTHONPATH` on Mac OS)


## Input

A list of points in two-dimensional space where each point is represented by a latitude/longitude pair.

## Output

The clusters of points.  By default we stores the computed clusters into a csv file: `output.csv`.  You can specify your output filename using `--output` argument option.

## How to run:

`python run.py --input YOUR_LOC_FILE --clusters CLUSTERS_NO`

Note that the runner expects the location file be in `data` folder.

## Technical details

This project is an implementation of k-means algorithm. It starts with a random point and then chooses k-1 other points as the farthest from the previous ones successively. It uses these k points as cluster centroids and then joins each point of the input to the cluster with the closest centroid.

Next, it recomputes the new centroids by calculating the means of obtained clusters and repeats the first step again by finding which cluster each point belongs to.

The program repeats these two steps until the cluster centroids converge and do not change anymore. See the following link to read more about this project and see some real examples of running k-means algorithm:

[K-Means algorithm description](http://www.kazemjahanbakhsh.com/codes/k-means.html)

# To deactivate the conda environment:

`conda deactivate`
