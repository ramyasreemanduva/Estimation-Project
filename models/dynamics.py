import numpy as np

#STATE TRANSITION MODEL

def F_2D(dt):
    return np.array([
        [1, 0, dt, 0],
        [0, 1, 0, dt],
        [0, 0, 1,  0],
        [0, 0, 0,  1]
    ])
#MEASUREMENT JACOBIAN
def H_jacobian(x, beacon):
    x = x.reshape(-1, 1)
    px, py = x[0, 0], x[1, 0]
    bx, by = beacon

    dx = px - bx
    dy = py - by
    r = np.sqrt(dx**2 + dy**2)
 # Avoid division by zero
    if r < 1e-6:
        r = 1e-6
 return np.array([[dx/r, dy/r, 0, 0]])
# BEACON POSITIONS
def get_beacons():
    return np.array([
        [0, 20],
        [100, -20],
        [200, 20]
    ])
