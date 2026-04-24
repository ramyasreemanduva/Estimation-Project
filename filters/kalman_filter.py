import numpy as np
from models.dynamics import H_jacobian

# EKF Prediction

def ekf_predict(x, P, Q, dt):
    # State transition 
    A = np.array([
        [1, 0, dt, 0],
        [0, 1, 0, dt],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])

    # Predict state
    x = A @ x

    # Predict covariance
    P = A @ P @ A.T + Q

    return x, P


# EKF Update (Nonlinear)

def ekf_update_multi(x, P, z_all, beacons, R):

    H_list = []
    y_list = []

    for i, beacon in enumerate(beacons):
        dx = x[0] - beacon[0]
        dy = x[1] - beacon[1]

        r = np.sqrt(dx**2 + dy**2) + 1e-6  # avoid divide by zero

        # Jacobian row
        H_i = [dx/r, dy/r, 0, 0]
        H_list.append(H_i)

        # error
        y_i = z_all[i] - r
        y_list.append(y_i)

    # Convert to arrays
    H = np.array(H_list)
    y = np.array(y_list).reshape(-1, 1)

    # Covariance
    S = H @ P @ H.T + R

    # Kalman Gain
    K = P @ H.T @ np.linalg.inv(S)

    # Update
    x = x + (K @ y).flatten()
    P = (np.eye(4) - K @ H) @ P

    return x, P


