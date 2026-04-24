import numpy as np
from models.dynamics import get_beacons
from filters.kalman_filter import ekf_predict, ekf_update_multi
from simulation.simulator import simulate_2D, measure_beacons
from plots.plot_results import plot_trajectory


# CONFIG 

dt = 0.01
steps = 2000


# SIMULATION

true_states = simulate_2D(steps, dt)
beacons = get_beacons()
measurements = measure_beacons(true_states, beacons)


# INITIAL STATE

x_est = np.array([48, 0, 0, 10])
P = np.eye(4)

Q = np.diag([0.01, 0.01, 0.1, 0.1])
R = np.eye(len(beacons)) * (1.5**2)

estimates = []


# EKF LOOP

for k in range(steps):

    x_est, P = ekf_predict(x_est, P, Q, dt)

    x_est, P = ekf_update_multi(
        x_est, P, measurements[k], beacons, R
    )

    estimates.append(x_est.copy())

estimates = np.array(estimates)

print("Final state:", x_est)

plot_trajectory(true_states, estimates)
