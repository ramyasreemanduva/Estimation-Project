import numpy as np
from models.dynamics import F_2D, H_jacobian

def ekf_predict(x, P, Q, dt):
    A = F_2D(dt)
    x = A @ x
    P = A @ P @ A.T + Q
    return x, P

def ekf_update_multi(x, P, z_all, beacons, R_mat):
    H_list, y_list = [], []
    for i, b in enumerate(beacons):
        H_i = H_jacobian(x, b)
        dist_pred = np.sqrt((x[0]-b[0])**2 + (x[1]-b[1])**2)
        H_list.append(H_i[0])
        y_list.append(z_all[i] - dist_pred)

    H = np.array(H_list)
    y = np.array(y_list).reshape(-1, 1)
    S = H @ P @ H.T + R_mat
    K = P @ H.T @ np.linalg.inv(S)
    x = x + (K @ y).flatten()
    P = (np.eye(4) - K @ H) @ P
    return x, P
