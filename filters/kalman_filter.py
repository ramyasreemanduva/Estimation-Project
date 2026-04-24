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

def ekf_update(x, P, z, beacon, R):

    # Difference between state and beacon
    dx = x[0] - beacon[0]
    dy = x[1] - beacon[1]

    # Predicted measurement 
    r = np.sqrt(dx**2 + dy**2)

    # Jacobian matrix
    H = H_jacobian(x, beacon)

    # Innovation 
    y = z - r

    # Innovation covariance
    S = H @ P @ H.T + R

    # Kalman Gain
    K = P @ H.T @ np.linalg.inv(S)

    # Update state
    x = x + (K * y).flatten()

    # Update covariance
    P = (np.eye(4) - K @ H) @ P

    return x, P
