import numpy as np

def F_2D(dt):
    """State transition matrix for constant velocity model."""
    return np.array([
        [1, 0, dt, 0],
        [0, 1, 0, dt],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])

def get_beacons():
    """Returns beacon positions (must be outside the lane region)."""
    # Placed arbitrarily outside the R=50 and r=46 bounds [cite: 18, 37]
    return np.array([
        [0, 60],    # b1 [cite: 37]
        [0, -60],   # b2 [cite: 37]
        [160, 0]    # b3 [cite: 37]
    ])

def H_jacobian(x, beacon):
    """Linearizes the range measurement function[cite: 41]."""
    dx = x[0] - beacon[0]
    dy = x[1] - beacon[1]
    dist = np.sqrt(dx**2 + dy**2) + 1e-6
    return np.array([[dx/dist, dy/dist, 0, 0]])
