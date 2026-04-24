import numpy as np
from models.dynamics import get_beacons
from filters.kalman_filter import ekf_predict, ekf_update_multi
from simulation.simulator import get_track_geometry, measure_beacons
from plots.plot_results import plot_trajectory

# CONFIG
dt, steps = 0.01, 1500

# GEOMETRY
paths = get_track_geometry(steps, dt)
true_x, true_y = paths[0]
inner_bound, outer_bound = paths[1], paths[2]

# Prepare true_states [x, y, vx, vy]
vx, vy = np.gradient(true_x, dt), np.gradient(true_y, dt)
true_states = np.column_stack([true_x, true_y, vx, vy])

beacons = get_beacons()
measurements = measure_beacons(true_states, beacons)

# EKF INITIALIZATION
x_est = np.array([true_x[0], true_y[0], vx[0], vy[0]])
P = np.eye(4) * 0.1
Q = np.diag([0.01, 0.01, 0.1, 0.1])
R = np.eye(len(beacons)) * (1.5**2)

estimates = []

# EKF LOOP
for k in range(len(true_states)):
    x_est, P = ekf_predict(x_est, P, Q, dt)
    x_est, P = ekf_update_multi(x_est, P, measurements[k], beacons, R)
    estimates.append(x_est.copy())
    from plots.analysis import perform_analysis
    long_rmse, lat_rmse = perform_analysis(true_states, estimates, dt)

print(f"Project Validation:")
print(f"Longitudinal RMSE: {long_rmse:.4f} m/s")
print(f"Lateral RMSE: {lat_rmse:.4f} m")

plot_trajectory(true_states, np.array(estimates), beacons, inner_bound, outer_bound)
