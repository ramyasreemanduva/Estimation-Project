import numpy as np
from simulation.simulator import get_track_geometry
# ... other imports ...

dt = 0.01 # 100 Hz [cite: 20]
true_states, inner, outer = get_track_geometry(dt)

# Initial State must match first true state exactly to prevent spiraling [cite: 41, 47]
x_est = true_states[0].copy()
P = np.eye(4) * 0.01 

# Process Noise Q: Keep very small to enforce track constraints [cite: 87, 88]
Q = np.diag([1e-8, 1e-8, 1e-6, 1e-6]) 
# R Variance: based on 1.5m standard deviation [cite: 19]
R = np.eye(3) * (1.5**2) 

estimates = []
for k in range(len(measurements)):
    x_est, P = ekf_predict(x_est, P, Q, dt)
    x_est, P = ekf_update_multi(x_est, P, measurements[k], beacons, R)
    estimates.append(x_est.copy())

plot_trajectory(true_states, np.array(estimates), beacons, inner, outer)
