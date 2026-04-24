import matplotlib.pyplot as plt
import numpy as np

def plot_trajectory(true_states, estimates, beacons, inner=None, outer=None):
    """
    Generates the 4 primary graphs needed for the technical report.
    """
    time = np.arange(len(true_states)) * 0.01  # dt = 0.01

    # --- FIGURE 1: 2D TRAJECTORY ---
    plt.figure(figsize=(10, 6))
    if inner: plt.plot(inner[0], inner[1], 'k-', alpha=0.5, label='Track Bounds')
    if outer: plt.plot(outer[0], outer[1], 'k-', alpha=0.5)
    
    plt.plot(true_states[:, 0], true_states[:, 1], 'b-', label='True Path')
    plt.plot(estimates[:, 0], estimates[:, 1], 'r--', label='EKF Estimate')
    plt.scatter(beacons[:, 0], beacons[:, 1], c='red', marker='x', label='Beacons')
    
    plt.title("Vehicle Localization (2D Trajectory)")
    plt.xlabel("X Position (m)")
    plt.ylabel("Y Position (m)")
    plt.axis('equal')
    plt.legend()
    plt.grid(True)
    plt.show()

    # FIGURE 2: LATERAL POSITION
    # We calculate deviation from the center of the lane (radius R=50 vs r=46)
    # This is a simplified "unrolled" lateral view
    lateral_error = np.sqrt(estimates[:, 0]**2 + estimates[:, 1]**2) - 50 
    
    plt.figure(figsize=(10, 4))
    plt.plot(time, lateral_error, 'k-', linewidth=1.5)
    plt.axhline(y=2, color='r', linestyle='--', label='Upper Bound') # Width B-r=4m [cite: 14]
    plt.axhline(y=-2, color='r', linestyle='--', label='Lower Bound')
    plt.title("Lateral Position Over Time (Constraint Validation)")
    plt.xlabel("Time (s)")
    plt.ylabel("Lateral Deviation (m)")
    plt.ylim(-3, 3)
    plt.legend()
    plt.grid(True)
    plt.show()

    #  FIGURE 3: VELOCITY ANALYSIS 
    est_vel = np.sqrt(estimates[:, 2]**2 + estimates[:, 3]**2)
    plt.figure(figsize=(10, 4))
    plt.plot(time, est_vel, label='Estimated Velocity')
    plt.axhline(y=25, color='r', linestyle=':', label='Max Limit (25m/s)') # 
    plt.title("Vehicle Velocity Over Time")
    plt.xlabel("Time (s)")
    plt.ylabel("Velocity (m/s)")
    plt.legend()
    plt.grid(True)
    plt.show()

    #  FIGURE 4: POSITION ERROR (RMSE Analysis)
    pos_error = np.sqrt((true_states[:, 0] - estimates[:, 0])**2 + 
                        (true_states[:, 1] - estimates[:, 1])**2)
    plt.figure(figsize=(10, 4))
    plt.plot(time, pos_error, color='purple')
    plt.title("Estimation Error (Euclidean Distance)")
    plt.xlabel("Time (s)")
    plt.ylabel("Error (m)")
    plt.grid(True)
    plt.show()
