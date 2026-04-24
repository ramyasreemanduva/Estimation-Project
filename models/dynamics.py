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
    """Returns beacon positions located outside the lane region."""
    # Placed outside the R=50 and r=46 boundaries
    return np.array([
        [20, 70],   # b1 [cite: 37]
        [20, -70],  # b2 [cite: 37]
        [180, 0]    # b3 [cite: 37]
    ])

def H_jacobian(x, beacon):
    """Linearizes the range measurement function for the EKF."""
    dx = x[0] - beacon[0]
    dy = x[1] - beacon[1]
    dist = np.sqrt(dx**2 + dy**2) + 1e-6
    return np.array([[dx/dist, dy/dist, 0, 0]])
