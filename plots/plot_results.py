import matplotlib.pyplot as plt
import numpy as np

def plot_trajectory(true_states, estimates, beacons, inner=None, outer=None):
    """
    Generates the comprehensive visual analysis required for the ELE8101 project.
    Validates 2D tracking, lateral constraints, velocity, and estimation error.
    """
    # Ensure inputs are numpy arrays
    true_states = np.asarray(true_states)
    estimates = np.asarray(estimates)
    time = np.arange(len(estimates)) * 0.01  # Assuming 100 Hz sampling [cite: 20]

    # --- FIGURE 1: 2D TRAJECTORY & BEACON PLACEMENT ---
    plt.figure(figsize=(10, 6))
    if inner is not None:
        plt.plot(inner[0], inner[1], 'k-', alpha=0.4, linewidth=1, label='Inner Bound (r=461m)')
    if outer is not None:
        plt.plot(outer[0], outer[1], 'k-', alpha=0.4, linewidth=1, label='Outer Bound (R=501m)')
    
    # Plot estimated path (True path removed to emphasize filter performance)
    plt.plot(estimates[:, 0], estimates[:, 1], 'r--', label='EKF Estimated Path')
    
    # Plot Beacons b1, b2, b3 [cite: 37]
    plt.scatter(beacons[:, 0], beacons[:, 1], c='red', marker='o', s=80, label='Beacons')
    for i, b in enumerate(beacons):
        plt.text(b[0]+5, b[1]+5, f'$b_{i+1}$', color='red', fontweight='bold')

    plt.title("Figure 1: EKF Tracking and Track Geometry")
    plt.xlabel("X Position (m)")
    plt.ylabel("Y Position (m)")
    plt.axis('equal') 
    plt.legend()
    plt.grid(True)

    # --- FIGURE 2: LATERAL POSITION (Constraint Validation) ---
    # Calculates distance from the estimate to the nearest point on the true centerline
    lat_positions = []
    for i in range(len(estimates)):
        # Find the minimum distance to any point on the ground truth path
        distances = np.sqrt((true_states[:, 0] - estimates[i, 0])**2 + 
                            (true_states[:, 1] - estimates[i, 1])**2)
        lat_positions.append(np.min(distances))
    
    lateral_deviation = np.array(lat_positions)

    plt.figure(figsize=(10, 4))
    plt.plot(time, lateral_deviation, 'k-', linewidth=1.5, label='Lateral Position ($y_t$)')
    
    # Bounds based on constant lane width of 4m (B-r=4m) [cite: 14, 17]
    plt.axhline(y=2, color='r', linestyle='--', label='Upper Bound (+2m)')
    plt.axhline(y=-2, color='r', linestyle='--', label='Lower Bound (-2m)')
    
    plt.title("Figure 2: Lateral Position Over Time (Validation of Fig 3)")
    plt.xlabel("Time (s)")
    plt.ylabel("Lateral Position, $y_t$ (m)")
    plt.ylim(-3, 3) 
    plt.legend(loc='upper right')
    plt.grid(True)

    # --- FIGURE 3: VELOCITY ANALYSIS ---
    # Velocity magnitude must be approx 10m/s and never exceed 25m/s 
    est_vel = np.sqrt(estimates[:, 2]**2 + estimates[:, 3]**2)
    plt.figure(figsize=(10, 4))
    plt.plot(time, est_vel, label='Estimated Velocity')
    plt.axhline(y=10, color='g', linestyle='--', label='Target Velocity (10m/s)')
    plt.axhline(y=25, color='r', linestyle=':', label='Max Velocity Limit (25m/s)') 
    
    plt.title("Figure 3: Vehicle Velocity Profile")
    plt.xlabel("Time (s)")
    plt.ylabel("Velocity (m/s)")
    plt.ylim(0, 30)
    plt.legend()
    plt.grid(True)

    # --- FIGURE 4: LONGITUDINAL POSITION (Distance Traveled) ---
    # Vehicle must move clockwise/forward only 
    dx = np.diff(estimates[:, 0], prepend=estimates[0, 0])
    dy = np.diff(estimates[:, 1], prepend=estimates[0, 1])
    longitudinal_pos = np.cumsum(np.sqrt(dx**2 + dy**2))

    plt.figure(figsize=(10, 4))
    plt.plot(time, longitudinal_pos, 'g-', label='Distance Traveled')
    plt.title("Figure 4: Longitudinal Position (Progress Along Track)")
    plt.xlabel("Time (s)")
    plt.ylabel("Distance (m)")
    plt.grid(True)

    # --- FIGURE 5: ESTIMATION ERROR (RMSE Analysis) ---
    # Provides the technical analysis of estimator performance [cite: 50]
    pos_error = np.sqrt((true_states[:, 0] - estimates[:, 0])**2 + 
                        (true_states[:, 1] - estimates[:, 1])**2)
    plt.figure(figsize=(10, 4))
    plt.plot(time, pos_error, color='purple', label='Position Error')
    plt.title("Figure 5: Estimation Euclidean Error (m)")
    plt.xlabel("Time (s)")
    plt.ylabel("Error (m)")
    plt.grid(True)

    plt.show()
