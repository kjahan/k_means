K-Means
=======

K-Means Clustering Algortihm

## General description
 
This code is a Python implementation of k-means clustering algorithm.

## Input

A list of points in the plane where each point is represented by a latitude/longitude pair.

## Output

The clusters of points.

## Technical details

This project is an implementation of k-means algorithm. It starts with a random point and then chooses k-1 other points as the farthest from the previous ones successively. It uses these k points as cluster centroids and then joins each point of the input to the cluster with the closest centroid. Next, it recomputes the new centroids by computing the means of obtained clusters and repeats the first step again by finding to which cluster each point belongs. The program repeats these two steps until the clusters converge and do not change anymore. View the following link to read more about this project and see some real examples of running k-means algorithm:

	http://www.kazemjahanbakhsh.com/codes/k-means.html
