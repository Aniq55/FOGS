import numpy as np
import pickle

data = np.load("/home/chri6578/Documents/aniq/FOGS/data/PEMSBAY/pems_bay.npz")
X = data['data']

speed = X[..., 0]  # first channel
mean = speed.mean(axis=0)

with open("/home/chri6578/Documents/aniq/FOGS/data/PEMSBAY/PEMSBAY_flow_count.pkl", "wb") as f:
    pickle.dump(mean, f)