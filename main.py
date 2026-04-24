import numpy as np
from simulation.simulator import get_track_geometry, measure_beacons
from filters.kalman_filter import ekf_predict, ekf_update_multi
from models.dynamics import get_beacons
from plots.plot_results import plot_trajectory

dt = 0.01 # 100 Hz frequency [cite: 20]
true_states = get_track_geometry(dt)
beacons = get_beacons() # Placed outside lane region [cite: 18]
measurements = measure_beacons(true_states, beacons)

# INITIALIZATION: Must match true_states[0] exactly
x_est = true_states[0].copy()
P = np.eye(4) * 0.1 

# TUNING: Low Q forces the filter to trust the smooth 10m/s model
Q = np.diag([1e-7, 1e-7, 1e-5, 1e-5]) 
R = np.eye(len(beacons)) * (1.5**2) # Standard deviation 1.5m [cite: 19]

estimates = []
for k in range(len(measurements)):
    x_est, P = ekf_predict(x_est, P, Q, dt)
    x_est, P = ekf_update_multi(x_est, P, measurements[k], beacons, R)
    estimates.append(x_est.copy())

# Convert to array for plot_results.py
estimates = np.array(estimates)
plot_trajectory(true_states, estimates, beacons)
