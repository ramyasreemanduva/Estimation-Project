import numpy as np
from simulation.simulator import get_track_geometry, measure_beacons
from plots.plot_results import plot_trajectory

# CONFIG 
dt = 0.01
steps = 10000 # Increased steps to accommodate the 10m/s speed over a full lap

# GEOMETRY
paths = get_track_geometry(steps, dt)
true_x, true_y = paths[0]
inner_bound, outer_bound = paths[1], paths[2]

# Prepare true_states [x, y, vx, vy]
vx = np.gradient(true_x, dt)
vy = np.gradient(true_y, dt)
true_states = np.column_stack([true_x, true_y, vx, vy])

# Beacons must be outside the lane region [cite: 18, 42]
beacons = np.array([
    [0, 60],   # Above left arc
    [0, -60],  # Below left arc
    [160, 0]   # Right of small arc
])

measurements = measure_beacons(true_states, beacons)

# EKF INITIALIZATION
x_est = np.array([true_x[0], true_y[0], vx[0], vy[0]])
P = np.eye(4) * 0.1
Q = np.diag([0.01, 0.01, 0.1, 0.1])
R = np.eye(len(beacons)) * (1.5**2) # Noise variance 

estimates = []

# EKF LOOP
for k in range(len(true_states)):
    # Predict and Update (assumes your kalman_filter.py is correctly implemented)
    # ... x_est, P = ekf_predict(...)
    # ... x_est, P = ekf_update_multi(...)
    estimates.append(x_est.copy())

estimates = np.array(estimates)
plot_trajectory(true_states, estimates, beacons, inner_bound, outer_bound)
