
import numpy as np

def F_1D(dt):
    A = np.array([
        [1, dt],
        [0, 1]
    ])
    return A

def H_1D():
    H = np.array([[1, 0]])
    return H
