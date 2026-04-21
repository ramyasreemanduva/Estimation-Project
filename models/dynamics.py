import numpy as np

def F_1D(dt):
    return np.array([
        [1, dt],
        [0, 1]
    ])

def H_1D():
    return np.array([[1, 0]])
