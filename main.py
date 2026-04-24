import numpy as np
from simulation.simulator import get_track_geometry, measure_beacons
from filters.kalman_filter import ekf_predict, ekf_update_multi
from models.dynamics import get_beacons
from plots.plot_results import plot_trajectory

dt, steps = 0.01, 5000 
paths = get_track_geometry(steps, dt)
true_states = np.column_stack([paths[0][0], paths[0][1], np.gradient(paths[0][0], dt), np.gradient(paths[0][1], dt)])

beacons = get_beacons()
measurements = measure_beacons(true_states, beacons)

x_est = true_states[0].copy()
P = np.eye(4) * 0.1
Q = np.diag([0.001, 0.001, 0.01, 0.01]) 
R = np.eye(len(beacons)) * (1.5**2) # Variance 

estimates = []
for k in range(steps):
    x_est, P = ekf_predict(x_est, P, Q, dt)
    x_est, P = ekf_update_multi(x_est, P, measurements[k], beacons, R)
    estimates.append(x_est.copy())

plot_trajectory(true_states, np.array(estimates), beacons, paths[1], paths[2])
