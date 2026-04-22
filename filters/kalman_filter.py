import numpy as np

def kf_step(x, P, z, A, H, Q, R):
    # Predict
    x = A @ x
    P = A @ P @ A.T + Q

    # Update
    S = H @ P @ H.T + R
    K = P @ H.T @ np.linalg.inv(S)

    x = x + (K @ (z - H @ x)).flatten()
    P = (np.eye(len(x)) - K @ H) @ P

    return x, P

