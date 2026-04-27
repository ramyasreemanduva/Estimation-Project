import numpy as np
from models.dynamics import F_2D, H_jacobian

def ekf_predict(x, P, Q, dt):
    A = F_2D(dt)
    x = A @ x
    P = A @ P @ A.T + Q
    return x, P

def ekf_update_multi(x, P, z_all, beacons, R_mat):

    x = x.reshape(-1, 1)

    H_list = []
    y_list = []

    for i, b in enumerate(beacons):
        H_i = H_jacobian(x, b)

        dx = x[0, 0] - b[0]
        dy = x[1, 0] - b[1]
        dist_pred = np.sqrt(dx**2 + dy**2)

        if dist_pred < 1e-6:
            dist_pred = 1e-6

        H_list.append(H_i[0])
        y_list.append(z_all[i] - dist_pred)

    H = np.vstack(H_list)
    y = np.array(y_list).reshape(-1, 1)

    S = H @ P @ H.T + R_mat
    K = P @ H.T @ np.linalg.inv(S)

    x = x + K @ y
    P = (np.eye(4) - K @ H) @ P

    # 🚨 ADD THIS (MOST IMPORTANT CHANGE)
    x = apply_constraints(x)

    return x.flatten(), P
def apply_constraints(x):

    # Lane bounds (4m width)
    x[1, 0] = np.clip(x[1, 0], -2.0, 2.0)

    # Lateral velocity constraint
    x[3, 0] = np.clip(x[3, 0], -0.55, 0.55)

    # No backward motion
    x[2, 0] = max(x[2, 0], 0.0)

    return x
