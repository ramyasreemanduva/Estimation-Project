import numpy as np
from simulation.simulator import get_track_geometry, measure_beacons
from filters.kalman_filter import ekf_predict, ekf_update_multi
from models.dynamics import get_beacons
from plots.plot_results import plot_analysis

# --- 1. Simulation Setup ---
dt = 0.01 
# Unpack the geometry. (We get true_states, inner, and outer from the simulator)
true_states, inner_bounds, outer_bounds = get_track_geometry(dt)
beacons = get_beacons()
measurements = measure_beacons(true_states, beacons)

# --- 2. EKF Initialization ---
# CRITICAL: Start exactly at the true starting point to prevent the initial lateral spike
x_est = true_states[0].copy()
P = np.eye(4) * 0.01 

# Tuning Parameters: 
# Low Q forces the filter to trust the constant 10m/s physics model over noisy sensors
Q = np.diag([1e-8, 1e-8, 1e-6, 1e-6]) 
# R uses the 1.5m standard deviation provided in the project specs
R = np.eye(len(beacons)) * (1.5**2) 

# --- 3. Main EKF Loop ---
estimates = []
for k in range(len(measurements)):
    # Step 1: Predict the next state based on physics
    x_est, P = ekf_predict(x_est, P, Q, dt)
    # Step 2: Update the state based on noisy beacon distance measurements
    x_est, P = ekf_update_multi(x_est, P, measurements[k], beacons, R)
    # Store the result
    estimates.append(x_est.copy())

# Convert the list of estimates to a NumPy array for mathematical slicing
estimates = np.array(estimates)

# --- 4. Plotting and Analysis ---
# Call the plot_analysis function, which generates the graphs and returns the RMSE metrics
long_rmse, lat_rmse = plot_analysis(true_states, estimates, dt)

# Print the final validation metrics to the terminal
print("--- ELE8101 Project Validation Complete ---")
print(f"Longitudinal RMSE (Velocity): {long_rmse:.4f} m/s")
print(f"Lateral RMSE (Cross-Track):   {lat_rmse:.4f} m")
if lat_rmse < 2.0:
    print("Status: SUCCESS (Vehicle remained inside the 4m lane)")
else:
    print("Status: FAILED (Vehicle breached the lane boundaries)")
