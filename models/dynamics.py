import numpy as np

# State Transition

def F_2D(dt):
    return np.array([
        [1, 0, dt, 0],
        [0, 1, 0, dt],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])


# Beacons (outside track)

def get_beacons():
    return np.array([
    [0, -50], # b1
   [0, 50],  # b2
   [140, -40] # b3
 ])


# Lane Constraint

def apply_track_constraint(x, y):
    r = np.sqrt(x**2 + y**2)

    # keep inside [46, 50]
    r = np.clip(r, 46, 50)

    angle = np.arctan2(y, x)

    x_new = r * np.cos(angle)
    y_new = r * np.sin(angle)

    return x_new, y_new

# Jacobian for EKF

def H_jacobian(x, beacon):
    dx = x[0] - beacon[0]
    dy = x[1] - beacon[1]

    r = np.sqrt(dx**2 + dy**2) + 1e-6

    return np.array([[dx/r, dy/r, 0, 0]])
