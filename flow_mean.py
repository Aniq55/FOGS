import numpy as np
import pickle

data = np.load("/home/chri6578/Documents/aniq/DATA/METRLA/metr_la.npz")
X = data['data']

speed = X[..., 0]  # first channel
mean = speed.mean(axis=0)

with open("/home/chri6578/Documents/aniq/DATA/METRLA/METRLA_flow_count.pkl", "wb") as f:
    pickle.dump(mean, f)