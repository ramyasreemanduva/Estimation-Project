import matplotlib.pyplot as plt
import numpy as np

def plot_trajectory(true_states, estimates, beacons, inner=None, outer=None):
    # Ensure inputs are numpy arrays to avoid indexing errors
    true_states = np.asarray(true_states)
    estimates = np.asarray(estimates)
    time = np.arange(len(estimates)) * 0.01  # 100 Hz frequency [cite: 20]

    # --- FIGURE 1: 2D TRACK PLOT ---
    plt.figure(figsize=(10, 6))
    
    # Plot Boundaries (r=461, R=501) 
    if inner is not None:
        plt.plot(inner[0], inner[1], 'k-', alpha=0.7, linewidth=2, label='Inner Bound')
    if outer is not None:
        plt.plot(outer[0], outer[1], 'k-', alpha=0.7, linewidth=2, label='Outer Bound')
    
    # Plot Estimated Path (True path removed as requested)
    plt.plot(estimates[:, 0], estimates[:, 1], 'r--', label='Estimated Path')
    
    # Plot and Name Beacons [cite: 37, 42]
    plt.scatter(beacons[:, 0], beacons[:, 1], c='red', marker='o', s=100, label='Beacons')
    for i, b in enumerate(beacons):
        plt.text(b[0] + 2, b[1] + 2, f'$b_{i+1}$', color='red', fontweight='bold')

    plt.title("Figure 1: EKF tracking with beacons on constrained circular path")
    plt.xlabel("X position")
    plt.ylabel("Y position")
    plt.axis('equal') # Keeps circles from looking like ovals
    plt.legend()
    plt.grid(True)
    # Note: plt.show() is called at the very end of the function

    # --- FIGURE 2: LATERAL POSITION (Matches Figure 3 in Coursework) ---
    # Calculates distance to the nearest point on the track centerline
    lat_positions = []
    for i in range(len(estimates)):
        distances = np.sqrt((true_states[:, 0] - estimates[i, 0])**2 + 
                            (true_states[:, 1] - estimates[i, 1])**2)
        lat_positions.append(np.min(distances))
    
    lateral_deviation = np.array(lat_positions)

    plt.figure(figsize=(10, 4))
    plt.plot(time, lateral_deviation, 'k-', linewidth=1.5, label='Lateral Position')
    
    # Bounds: Track width is 4m, so +/- 2m from center [cite: 14, 17]
    plt.axhline(y=2, color='r', linestyle='--', label='Upper bound')
    plt.axhline(y=-2, color='r', linestyle='--', label='Lower bound')
    
    plt.title("Figure 3: Lateral Position Over Time")
    plt.xlabel("Time (s)")
    plt.ylabel("Lateral position, $y_t$")
    plt.ylim(-3, 3) 
    plt.legend(loc='upper right')
    plt.grid(True)

    # --- FIGURE 3: VELOCITY ANALYSIS ---
    est_vel = np.sqrt(estimates[:, 2]**2 + estimates[:, 3]**2)
    plt.figure(figsize=(10, 4))
    plt.plot(time, est_vel, label='Estimated Velocity')
    # Max speed constraint: 25 m/s 
    plt.axhline(y=25, color='r', linestyle=':', label='Max Limit (25m/s)') 
    plt.title("Vehicle Velocity Over Time")
    plt.xlabel("Time (s)")
    plt.ylabel("Velocity (m/s)")
    plt.legend()
    plt.grid(True)

    # --- FIGURE 4: POSITION ERROR ---
    pos_error = np.sqrt((true_states[:, 0] - estimates[:, 0])**2 + 
                        (true_states[:, 1] - estimates[:, 1])**2)
    plt.figure(figsize=(10, 4))
    plt.plot(time, pos_error, color='purple', label='RMSE')
    plt.title("Estimation Error (Euclidean Distance)")
    plt.xlabel("Time (s)")
    plt.ylabel("Error (m)")
    plt.grid(True)

    # Display all windows at once
    plt.show()
