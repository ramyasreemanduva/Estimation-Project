import numpy as np
from simulation.simulator import get_track_geometry, measure_beacons
from filters.kalman_filter import ekf_predict, ekf_update_multi
from models.dynamics import get_beacons
from plots.plot_results import plot_trajectory

dt = 0.01 
steps = 8000 # Increased steps to lower velocity to 10m/s 
paths = get_track_geometry(steps, dt)
true_path = paths[0]
true_states = np.column_stack([true_path[0], true_path[1], 
                               np.gradient(true_path[0], dt), 
                               np.gradient(true_path[1], dt)])

beacons = get_beacons()
measurements = measure_beacons(true_states, beacons)

x_est = true_states[0].copy()
P = np.eye(4) * 0.1
# VERY LOW Q ensures smooth estimated velocity and lateral position
Q = np.diag([0.0001, 0.0001, 0.001, 0.001]) 
R = np.eye(len(beacons)) * (1.5**2) 

estimates = []
for k in range(len(measurements)):
    x_est, P = ekf_predict(x_est, P, Q, dt)
    x_est, P = ekf_update_multi(x_est, P, measurements[k], beacons, R)
    estimates.append(x_est.copy())

plot_trajectory(true_states, np.array(estimates), beacons, paths[1], paths[2])
