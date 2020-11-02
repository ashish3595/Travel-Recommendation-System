datafrom sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
import time

import matplotlib.pyplot as plt

data = pd.read_csv("flickr_dataset_dbscan.csv")
#data = pd.read_csv(r'\home\ashish\Desktop\Major_Project\flickr_dataset.csv')

data = data[["Latitude", "Longitude"]]
data = data.as_matrix().astype("float32", copy = False)

print np.std(data[0:, 0])   #Standard deviation along the latitude
print np.std(data[0:, 1])   #Standard deviation along the longitude

stscaler = StandardScaler().fit(data)
data = stscaler.transform(data)


start_time = time.time()
dbsc = DBSCAN(eps = .001, min_samples = 10).fit(data)

print("--- %s seconds ---" % (time.time() - start_time))

labels = dbsc.labels_
core_samples = np.zeros_like(labels, dtype = bool)
core_samples[dbsc.core_sample_indices_] = True

n_clusters = len(set(labels))

print n_clusters, labels

unique_labels = set(labels)
colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
for k, col in zip(unique_labels, colors):
    if k == -1:
        # Black used for noise.
        col = 'k'

    class_member_mask = (labels == k)

    xy = data[class_member_mask & core_samples]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col, markeredgecolor='k', markersize=14)

    xy = data[class_member_mask & ~core_samples]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col, markeredgecolor='k', markersize=6)

plt.title('Estimated number of clusters: %d' % n_clusters)
plt.show()