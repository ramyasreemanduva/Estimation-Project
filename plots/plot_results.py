import numpy as np
import matplotlib.pyplot as plt

def perform_analysis(true_states, estimates, dt):
    # --- ADD THIS LINE TO FIX THE ERROR ---
    estimates = np.array(estimates) 
    
    time = np.arange(len(estimates)) * dt
    
    # Now this line will work perfectly
    est_speed = np.sqrt(estimates[:,2]**2 + estimates[:,3]**2)
    true_speed = np.sqrt(true_states[:,2]**2 + true_states[:,3]**2)
    
    # Longitudinal Error (Velocity)
    long_error = true_speed - est_speed
    long_rmse = np.sqrt(np.mean(long_error**2))

    # Lateral Error (Distance to path)
    lat_errors = []
    for i in range(len(estimates)):
        dist_to_path = np.sqrt((true_states[:,0] - estimates[i,0])**2 + 
                               (true_states[:,1] - estimates[i,1])**2)
        lat_errors.append(np.min(dist_to_path))
    
    lat_rmse = np.sqrt(np.mean(np.array(lat_errors)**2))
    
    # Plotting code follows...
    return long_rmse, lat_rmse
    # --- 2. Lateral Analysis (Cross-Track Error) ---
    # Finding distance from estimate to the nearest point on true trajectory
    lat_errors = []
    for i in range(len(estimates)):
        # Euclidean distance to all points in ground truth
        dist_to_path = np.sqrt((true_states[:,0] - estimates[i,0])**2 + 
                               (true_states[:,1] - estimates[i,1])**2)
        lat_errors.append(np.min(dist_to_path))
    
    lat_errors = np.array(lat_errors)
    lat_rmse = np.sqrt(np.mean(lat_errors**2))

    # --- 3. Plotting the Analysis ---
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    # Longitudinal Plot
    ax1.plot(time, est_speed, 'b', label='Estimated Speed')
    ax1.plot(time, true_speed, 'g--', alpha=0.7, label='True Speed')
    ax1.axhline(y=10, color='r', linestyle=':', label='Target (10m/s)')
    ax1.set_title(f"Longitudinal Analysis (RMSE: {long_rmse:.4f} m/s)")
    ax1.set_ylabel("Velocity (m/s)")
    ax1.legend()
    ax1.grid(True)

    # Lateral Plot
    ax2.plot(time, lat_errors, 'k', label='Lateral Deviation ($y_t$)')
    ax2.axhline(y=2.0, color='r', linestyle='--', label='Lane Bound (2m)')
    ax2.set_title(f"Lateral Analysis (RMSE: {lat_rmse:.4f} m)")
    ax2.set_ylabel("Error (m)")
    ax2.set_xlabel("Time (s)")
    ax2.legend()
    ax2.grid(True)

    plt.tight_layout()
    plt.show()
    
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
