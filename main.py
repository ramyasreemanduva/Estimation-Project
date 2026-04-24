import numpy as np
from simulation.simulator import get_track_geometry, measure_beacons
from filters.kalman_filter import ekf_predict, ekf_update_multi
from models.dynamics import get_beacons
from plots.plot_results import plot_trajectory

dt = 0.01 
true_states, inner, outer = get_track_geometry(dt)
beacons = get_beacons()
measurements = measure_beacons(true_states, beacons)

# Ensure the filter starts exactly where the car starts
x_est = true_states[0].copy()
P = np.eye(4) * 0.01 
# Very small Q keeps the path smooth and in the lane
Q = np.diag([1e-8, 1e-8, 1e-6, 1e-6]) 
R = np.eye(len(beacons)) * (1.5**2) 

estimates = []
for k in range(len(measurements)):
    x_est, P = ekf_predict(x_est, P, Q, dt)
    x_est, P = ekf_update_multi(x_est, P, measurements[k], beacons, R)
    estimates.append(x_est.copy())

estimates = np.array(estimates) # Convert list to array for plotting
plot_trajectory(true_states, estimates, beacons, inner, outer)
