import numpy as np

from models.dynamics import get_beacons
from filters.kalman_filter import ekf_predict, ekf_update
from simulation.simulator import simulate_2D, measure_beacons
from plots.plot_results import plot_trajectory

# CONFIG

dt = 0.1
steps = 100

# SIMULATION

true_states = simulate_2D(steps, dt)
beacons = get_beacons()
measurements = measure_beacons(true_states, beacons)

# INITIAL STATE

x_est = np.array([0, 0, 8, 0])  # initial guess
P = np.eye(4)

Q = np.eye(4) * 0.1
R = np.array([[1.5**2]])

estimates = []

# RUN EKF

for k in range(steps):

    # Prediction
    x_est, P = ekf_predict(x_est, P, Q, dt)

    # Update using all beacons
    for i, beacon in enumerate(beacons):
        z = measurements[k][i]
        x_est, P = ekf_update(x_est, P, z, beacon, R)

    estimates.append(x_est.copy())

estimates = np.array(estimates)


# OUTPUT

print("Final estimated state:", x_est)

# PLOT

plot_trajectory(true_states, estimates)
