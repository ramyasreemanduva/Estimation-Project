import numpy as np
from simulation.simulator import get_track_geometry, measure_beacons
from filters.kalman_filter import ekf_predict, ekf_update_multi
from models.dynamics import get_beacons
from plots.plot_results import plot_trajectory

dt = 0.01 # [cite: 20]
true_states, inner, outer = get_track_geometry(dt)

beacons = get_beacons()
measurements = measure_beacons(true_states, beacons)

# Initial State: Start at first true position
x_est = true_states[0].copy()
P = np.eye(4) * 0.1 

# TUNING: These values are critical for Figure 3 performance [cite: 91]
# Make Q very small so the filter ignores measurement jitter
Q = np.diag([1e-6, 1e-6, 1e-4, 1e-4]) 
R = np.eye(len(beacons)) * (1.5**2) # [cite: 19]

estimates = []
for k in range(len(measurements)):
    x_est, P = ekf_predict(x_est, P, Q, dt)
    x_est, P = ekf_update_multi(x_est, P, measurements[k], beacons, R)
    estimates.append(x_est.copy())

plot_trajectory(true_states, np.array(estimates), beacons, inner, outer)
