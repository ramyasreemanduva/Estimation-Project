import numpy as np

from models.dynamics import get_beacons
from filters.kalman_filter import ekf_predict
from simulation.simulator import simulate_2D, measure_beacons
from plots.plot_results import plot_trajectory

# MULTI-BEACON EKF UPDATE

def ekf_update_multi(x, P, z_all, beacons, R):

    H_list = []
    y_list = []

    for i, beacon in enumerate(beacons):
        dx = x[0] - beacon[0]
        dy = x[1] - beacon[1]

        r = np.sqrt(dx**2 + dy**2) + 1e-6  # stability fix

        # Jacobian
        H_i = [dx/r, dy/r, 0, 0]
        H_list.append(H_i)

        # error
        y_i = z_all[i] - r
        y_list.append(y_i)

    H = np.array(H_list)
    y = np.array(y_list).reshape(-1, 1)

    S = H @ P @ H.T + R
    K = P @ H.T @ np.linalg.inv(S)

    x = x + (K @ y).flatten()
    P = (np.eye(4) - K @ H) @ P

    return x, P

# CONFIG

dt = 0.1
steps = 200

# SIMULATION

true_states = simulate_2D(steps, dt)
beacons = get_beacons()
measurements = measure_beacons(true_states, beacons)

# INITIAL STATE

x_est = np.array([50, 0, 0, 10])   # close to circle start
P = np.eye(4)

Q = np.eye(4) * 0.01
R = np.eye(len(beacons)) * (1.0**2)

estimates = []


# RUN EKF

for k in range(steps):

    # Prediction
    x_est, P = ekf_predict(x_est, P, Q, dt)

    # Update (ALL beacons together)
    x_est, P = ekf_update_multi(x_est, P, measurements[k], beacons, R)

    estimates.append(x_est.copy())

estimates = np.array(estimates)

# OUTPUT

print("Final estimated state:", x_est)

# PLOT

plot_trajectory(true_states, estimates)
