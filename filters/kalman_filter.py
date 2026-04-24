import numpy as np
from models.dynamics import H_jacobian

# EKF Prediction

def ekf_predict(x, P, Q, dt):
    A = np.array([
        [1, 0, dt, 0],
        [0, 1, 0, dt],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])

    x = A @ x
    P = A @ P @ A.T + Q

    return x, P


# EKF Multi-Beacon Update

def ekf_update_multi(x, P, z_all, beacons, R):

    H_list = []
    y_list = []

    for i, beacon in enumerate(beacons):
        dx = x[0] - beacon[0]
        dy = x[1] - beacon[1]

        r = np.sqrt(dx**2 + dy**2) + 1e-6

        H_list.append([dx/r, dy/r, 0, 0])
        y_list.append(z_all[i] - r)

    H = np.array(H_list)
    y = np.array(y_list).reshape(-1, 1)

    S = H @ P @ H.T + R
    K = P @ H.T @ np.linalg.inv(S)

    x = x + (K @ y).flatten()
    P = (np.eye(4) - K @ H) @ P

    return x, P
