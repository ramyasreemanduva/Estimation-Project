import numpy as np
from models.dynamics import get_beacons
from filters.kalman_filter import ekf_predict, ekf_update_multi
from simulation.simulator import get_track_geometry, measure_beacons # Updated import
from plots.plot_results import plot_trajectory

# CONFIG 
dt = 0.01
steps = 1500

# SIMULATION 
# Get the full geometry: True Path, Inner Bound, and Outer Bound
paths = get_track_geometry(steps, dt)
true_path_coords = paths[0]  # (x, y) tuple for true path
inner_bound = paths[1]       # (x, y) tuple for inner wall
outer_bound = paths[2]       # (x, y) tuple for outer wall

# We need true_states in [x, y, vx, vy] format for the EKF
vx = np.gradient(true_path_coords[0], dt)
vy = np.gradient(true_path_coords[1], dt)
true_states = np.column_stack([true_path_coords[0], true_path_coords[1], vx, vy])

beacons = get_beacons()
measurements = measure_beacons(true_states, beacons)

# INITIAL STATE
# Starting at (0, 50) to match the graph in your coursework
x_est = np.array([0, 50, 10, 0]) 
P = np.eye(4) * 0.1

Q = np.diag([0.01, 0.01, 0.1, 0.1])
R = np.eye(len(beacons)) * (1.5**2)

estimates = []

# EKF LOOP
for k in range(steps):
    x_est, P = ekf_predict(x_est, P, Q, dt)
    
    # Ensure you are passing the measurement for the current timestep
    x_est, P = ekf_update_multi(
        x_est, P, measurements[k], beacons, R
    )
    estimates.append(x_est.copy())

estimates = np.array(estimates)

print("Final state estimate:", x_est)

# PLOTTING
# Pass the boundaries to your plot function so they appear on the graph
plot_trajectory(true_states, estimates, beacons, inner_bound, outer_bound)
