import numpy as np

def circular_motion(theta, R):
    x = R * np.cos(theta)
    y = R * np.sin(theta)
    return x, y

def circular_velocity(theta, omega, R):
    vx = -R * omega * np.sin(theta)
    vy = R * omega * np.cos(theta)
    return vx, vy

def F_2D(dt):
    return np.array([
        [1, 0, dt, 0],
        [0, 1, 0, dt],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])
