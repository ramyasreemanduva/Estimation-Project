import numpy as np

def F_matrix(dt):
    return np.array([
        [1,0,dt,0],
        [0,1,0,dt],
        [0,0,1,0],
        [0,0,0,1]
    ])

def propagate(x, dt):
    return F_matrix(dt) @ x
