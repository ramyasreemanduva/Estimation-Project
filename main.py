import numpy as np
from simulation.simulator import get_track_geometry, measure_beacons
from plots.plot_results import plot_trajectory
# from filters.kalman_filter import ekf_predict, ekf_update_multi

dt = 0.01 # 100 Hz [cite: 20]
steps = 6000 # Enough steps for one lap at 10m/s

paths = get_track_geometry(steps, dt)
true_x, true_y = paths[0]
inner_bound, outer_bound = paths[1], paths[2]

vx = np.gradient(true_x, dt)
vy = np.gradient(true_y, dt)
true_states = np.column_stack([true_x, true_y, vx, vy])

# Beacons b1, b2, b3 outside lane region [cite: 18, 37]
beacons = np.array([[20, 60], [20, -60], [180, 0]])
measurements = measure_beacons(true_states, beacons)

x_est = np.array([true_x[0], true_y[0], vx[0], vy[0]])
P = np.eye(4) * 0.1
# Reduced Q to smooth out lateral and velocity estimates
Q = np.diag([0.001, 0.001, 0.01, 0.01]) 
R = np.eye(len(beacons)) * (1.5**2) # [cite: 19]

estimates = []
for k in range(len(true_states)):
    # x_est, P = ekf_predict(x_est, P, Q, dt)
    # x_est, P = ekf_update_multi(x_est, P, measurements[k], beacons, R)
    estimates.append(x_est.copy())

estimates = np.array(estimates)
plot_trajectory(true_states, estimates, beacons, inner_bound, outer_bound)
