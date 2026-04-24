import numpy as np
import matplotlib.pyplot as plt

def plot_analysis(true_states, estimates, dt=0.01):
    # 1. Convert to numpy array for slicing
    estimates = np.array(estimates)
    time = np.arange(len(estimates)) * dt

    # 2. Longitudinal Calculation
    true_speed = np.sqrt(true_states[:,2]**2 + true_states[:,3]**2)
    est_speed = np.sqrt(estimates[:,2]**2 + estimates[:,3]**2)
    long_rmse = np.sqrt(np.mean((true_speed - est_speed)**2))

    # 3. Lateral Calculation (yt)
    lat_errors = []
    for i in range(len(estimates)):
        dist_to_path = np.sqrt((true_states[:,0] - estimates[i,0])**2 + 
                               (true_states[:,1] - estimates[i,1])**2)
        lat_errors.append(np.min(dist_to_path))
    
    lat_errors = np.array(lat_errors)
    lat_rmse = np.sqrt(np.mean(lat_errors**2))

    # 4. Plotting
    plt.figure(figsize=(10, 8))
    
    plt.subplot(2, 1, 1)
    plt.plot(time, est_speed, 'r', label='Estimated Speed')
    plt.plot(time, true_speed, 'b', alpha=0.3, label='True Speed')
    plt.ylabel("Velocity (m/s)")
    plt.legend()
    plt.title(f"Longitudinal Analysis (RMSE: {long_rmse:.4f})")

    plt.subplot(2, 1, 2)
    plt.plot(time, lat_errors, 'k', label='Lateral Deviation ($y_t$)')
    plt.axhline(y=2.0, color='r', linestyle='--', label='Bound (2m)')
    plt.ylabel("Lateral Error (m)")
    plt.xlabel("Time (s)")
    plt.legend()
    plt.title(f"Lateral Analysis (RMSE: {lat_rmse:.4f})")

    plt.tight_layout()
    plt.show()

    # --- THIS IS THE CRITICAL FIX ---
    return long_rmse, lat_rmse
def plot_trajectory(true_states, estimates, beacons, inner=None, outer=None):
    plt.figure(figsize=(12, 6))
    
    # Plot Boundaries (The Track Walls)
    if inner: plt.plot(inner[0], inner[1], 'k-', alpha=0.8, linewidth=2)
    if outer: plt.plot(outer[0], outer[1], 'k-', alpha=0.8, linewidth=2)
    
    # Plot Paths
    
    plt.plot(estimates[:, 0], estimates[:, 1], '--', label='Estimated Path', linewidth=1.5)
    
    # Plot Beacons
    plt.scatter(beacons[:, 0], beacons[:, 1], c='red', marker='o', label='Beacons')
    for i, b in enumerate(beacons):
        plt.text(b[0]+2, b[1]+2, f'b{i+1}', color='red', fontweight='bold')

    plt.title("EKF tracking with beacons on constrained path")
    plt.xlabel("X position")
    plt.ylabel("Y position")
    plt.legend()
    plt.grid(True)
    plt.axis('equal') # Crucial for circular look
    plt.show()
