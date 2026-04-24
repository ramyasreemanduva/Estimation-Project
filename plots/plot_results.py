import numpy as np
import matplotlib.pyplot as plt

def plot_analysis(true_states, estimates, dt=0.01):
    # Ensure estimates is a NumPy array to allow slicing [:, index]
    estimates = np.array(estimates)
    time = np.arange(len(estimates)) * dt

    # --- LONGITUDINAL ANALYSIS (Velocity) ---
    # Total Speed = sqrt(vx^2 + vy^2)
    true_speed = np.sqrt(true_states[:,2]**2 + true_states[:,3]**2)
    est_speed = np.sqrt(estimates[:,2]**2 + estimates[:,3]**2)

    # --- LATERAL ANALYSIS (Cross-Track Error) ---
    # Calculation: Distance from estimate to the nearest point on the centerline
    lat_error = []
    for i in range(len(estimates)):
        # Calculate Euclidean distance to all points on the true path
        dx = true_states[:,0] - estimates[i,0]
        dy = true_states[:,1] - estimates[i,1]
        dist = np.sqrt(dx**2 + dy**2)
        lat_error.append(np.min(dist))
    
    lat_error = np.array(lat_error)

    # --- PLOTTING ---
    plt.figure(figsize=(10, 8))

    # Top Plot: Longitudinal (Speed)
    plt.subplot(2, 1, 1)
    plt.plot(time, est_speed, 'r', label='Estimated Speed')
    plt.plot(time, true_speed, 'b', alpha=0.3, label='True Speed')
    plt.axhline(y=10, color='g', linestyle='--', label='Target (10m/s)')
    plt.ylabel("Velocity (m/s)")
    plt.title("Longitudinal Analysis: Speed Tracking")
    plt.legend()
    plt.grid(True)

    # Bottom Plot: Lateral (Lane Deviation)
    plt.subplot(2, 1, 2)
    plt.plot(time, lat_error, 'k', label='Lateral Deviation ($y_t$)')
    plt.axhline(y=2.0, color='r', linestyle='--', label='Lane Bound (2m)')
    plt.ylabel("Lateral Error (m)")
    plt.xlabel("Time (s)")
    plt.title("Lateral Analysis: Cross-Track Deviation")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()
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
