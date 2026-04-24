import numpy as np
import matplotlib.pyplot as plt

def plot_analysis(true_states, estimates, beacons, inner, outer, dt=0.01):
    estimates = np.array(estimates)
    time = np.arange(len(estimates)) * dt

    # --- 1. Calculations ---
    # Velocity
    true_speed = np.sqrt(true_states[:,2]**2 + true_states[:,3]**2)
    est_speed = np.sqrt(estimates[:,2]**2 + estimates[:,3]**2)
    long_rmse = np.sqrt(np.mean((true_speed - est_speed)**2))

    # Lateral (yt)
    lat_errors = []
    for i in range(len(estimates)):
        dist_to_path = np.sqrt((true_states[:,0] - estimates[i,0])**2 + 
                               (true_states[:,1] - estimates[i,1])**2)
        lat_errors.append(np.min(dist_to_path))
    
    lat_errors = np.array(lat_errors)
    lat_rmse = np.sqrt(np.mean(lat_errors**2))

    # --- 2. Plotting ---
    # FIGURE 1: 2D Track Mapping
    plt.figure(figsize=(10, 6))
    plt.plot(inner[0], inner[1], 'k', alpha=0.2, label='Lane Bounds')
    plt.plot(outer[0], outer[1], 'k', alpha=0.2)
    plt.plot(true_states[:,0], true_states[:,1], 'b-', alpha=0.4, label='True Path')
    plt.plot(estimates[:,0], estimates[:,1], 'r--', label='EKF Estimate')
    plt.scatter(beacons[:,0], beacons[:,1], c='red', label='Beacons')
    plt.axis('equal')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.title("Figure 1: 2D Track and EKF Estimation")
    plt.show() # Shows the first window

    # FIGURE 2 & 3: Longitudinal and Lateral Analysis
    plt.figure(figsize=(10, 8))
    
    # Top Plot (Speed)
    plt.subplot(2, 1, 1)
    plt.plot(time, est_speed, 'r', label='Estimated Speed')
    plt.plot(time, true_speed, 'b', alpha=0.3, label='True Speed')
    plt.ylabel("Velocity (m/s)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.title(f"Figure 2: Longitudinal Analysis (RMSE: {long_rmse:.4f})")

    # Bottom Plot (Lateral)
    plt.subplot(2, 1, 2)
    plt.plot(time, lat_errors, 'k', label='Lateral Deviation ($y_t$)')
    plt.axhline(y=2.0, color='r', linestyle='--', label='Lane Bound (2m)')
    plt.ylabel("Lateral Error (m)")
    plt.xlabel("Time (s)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.title(f"Figure 3: Lateral Analysis (RMSE: {lat_rmse:.4f})")

    plt.tight_layout()
    plt.show() # Shows the second window

    return long_rmse, lat_rmse
