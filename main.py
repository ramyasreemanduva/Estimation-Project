import numpy as np
from simulation.simulator import get_track_geometry, measure_beacons
from filters.kalman_filter import ekf_predict, ekf_update_multi
from models.dynamics import get_beacons
from plots.plot_results import plot_trajectory

dt = 0.01 # 100 Hz frequency [cite: 20]
true_states, inner, outer = get_track_geometry(dt)
beacons = get_beacons() # Beacons cannot be inside lane region [cite: 18]
measurements = measure_beacons(true_states, beacons) # Noise std dev 1.5m [cite: 19]

x_est = true_states[0].copy()
P = np.eye(4) * 0.1
Q = np.diag([1e-7, 1e-7, 1e-5, 1e-5]) # Low Q to trust model [cite: 46]
R = np.eye(len(beacons)) * (1.5**2) # Measurement noise variance [cite: 19]

estimates = []
for k in range(len(measurements)):
    x_est, P = ekf_predict(x_est, P, Q, dt)
    x_est, P = ekf_update_multi(x_est, P, measurements[k], beacons, R)
    estimates.append(x_est.copy())

plot_trajectory(true_states, np.array(estimates), beacons, inner, outer)
