import numpy as np
import pandas as pd

dist = np.load("./data/PEMSBAY/pems_bay_spatial_distance.npy")
N = dist.shape[0]

rows = []

for i in range(N):
    for j in range(N):
        if i != j and np.isfinite(dist[i, j]) and dist[i, j] > 0:
            rows.append([i, j, dist[i, j]])

df = pd.DataFrame(rows, columns=["from", "to", "distance"])
df.to_csv("./data/PEMSBAY/PEMSBAY.csv", index=False)

print("Edges:", len(df))