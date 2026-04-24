import numpy as np

# Circular Motion 

def circular_motion(theta, R):
    x = R * np.cos(theta)
    y = R * np.sin(theta)
    return x, y

# Circular Velocity 

def circular_velocity(theta, omega, R):
    vx = -R * omega * np.sin(theta)
    vy = R * omega * np.cos(theta)
    return vx, vy

# State Transition 

def F_2D(dt):
    return np.array([
        [1, 0, dt, 0],
        [0, 1, 0, dt],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])


# Lane Constraint

def apply_constraints(y):
    return np.clip(y, -2, 2)

# NEW: Beacons 

def get_beacons():
    return np.array([
        [-20, 10],
        [50, -10],
        [120, 15]
    ])


# Nonlinear Measurement Function

def h(x, beacon):
    dx = x[0] - beacon[0]
    dy = x[1] - beacon[1]
    return np.array([np.sqrt(dx**2 + dy**2)])

# Jacobian of Measurement

def H_jacobian(x, beacon):
    dx = x[0] - beacon[0]
    dy = x[1] - beacon[1]

    r = np.sqrt(dx**2 + dy**2)

    return np.array([
        [dx/r, dy/r, 0, 0]
    ])
