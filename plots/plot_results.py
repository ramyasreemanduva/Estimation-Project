import matplotlib.pyplot as plt
import numpy as np

def plot_trajectory(true_states, estimates, beacons, inner=None, outer=None):
    """
    Comprehensive visual analysis for ELE8101.
    Validates 2D tracking, lateral constraints, velocity, and longitudinal progress.
    """
    true_states = np.asarray(true_states)
    estimates = np.asarray(estimates)
    # dt = 0.01 (100 Hz) as specified in datasheet [cite: 20]
    time = np.arange(len(estimates)) * 0.01 

    # --- FIGURE 1: 2D TRACK & BEACONS ---
    plt.figure(figsize=(10, 6))
    if inner is not None:
        plt.plot(inner[0], inner[1], 'k-', alpha=0.5, label='Inner Bound (r=46m)')
    if outer is not None:
        plt.plot(outer[0], outer[1], 'k-', alpha=0.5, label='Outer Bound (R=50m)')
    
    plt.plot(estimates[:, 0], estimates[:, 1], 'r--', linewidth=1.5, label='EKF Estimate')
    
    # Label Beacons numerically b1, b2, b3 [cite: 37]
    plt.scatter(beacons[:, 0], beacons[:, 1], c='red', marker='o', s=100, label='Beacons')
    for i, b in enumerate(beacons):
        plt.text(b[0]+2, b[1]+2, f'$b_{{{i+1}}}$', color='red', fontweight='bold')

    plt.title("Figure 1: Vehicle Tracking and Beacon Placement")
    plt.xlabel("X Position (m)")
    plt.ylabel("Y Position (m)")
    plt.axis('equal') 
    plt.legend()
    plt.grid(True)

    # --- FIGURE 2: LATERAL POSITION (Constraint Validation) ---
    # Validation that vehicle stays within +/- 2m of centerline [cite: 14, 17]
    lat_errors = []
    for i in range(len(estimates)):
        dists = np.sqrt((true_states[:, 0] - estimates[i, 0])**2 + 
                        (true_states[:, 1] - estimates[i, 1])**2)
        lat_errors.append(np.min(dists))
    
    plt.figure(figsize=(10, 4))
    plt.plot(time, lat_errors, 'k-', label='Lateral Position ($y_t$)')
    plt.axhline(y=2, color='r', linestyle='--', label='Upper Bound (+2m)')
    plt.axhline(y=-2, color='r', linestyle='--', label='Lower Bound (-2m)')
    plt.title("Figure 2: Lateral Position Over Time (Lane Keeping)")
    plt.ylabel("Lateral Position, $y_t$ (m)")
    plt.xlabel("Time (s)")
    plt.ylim(-3, 3)
    plt.legend()
    plt.grid(True)

    # --- FIGURE 3: VELOCITY ANALYSIS ---
    # Max speed limit: 25 m/s 
    speed = np.sqrt(estimates[:, 2]**2 + estimates[:, 3]**2)
    plt.figure(figsize=(10, 4))
    plt.plot(time, speed, label='Estimated Velocity')
    plt.axhline(y=10, color='g', linestyle='--', label='Target (10m/s)')
    plt.axhline(y=25, color='r', linestyle=':', label='Max Limit (25m/s)')
    plt.title("Figure 3: Velocity Constraint Validation")
    plt.ylabel("Velocity (m/s)")
    plt.xlabel("Time (s)")
    plt.ylim(0, 30)
    plt.legend()
    plt.grid(True)

    # --- FIGURE 4: LONGITUDINAL POSITION ---
    # Cumulative distance traveled along the track
    dx = np.diff(estimates[:, 0], prepend=estimates[0, 0])
    dy = np.diff(estimates[:, 1], prepend=estimates[0, 1])
    dist_traveled = np.cumsum(np.sqrt(dx**2 + dy**2))

    plt.figure(figsize=(10, 4))
    plt.plot(time, dist_traveled, 'b-', label='Progress along track')
    plt.title("Figure 4: Longitudinal Position Over Time")
    plt.ylabel("Distance Traveled (m)")
    plt.xlabel("Time (s)")
    plt.grid(True)

    plt.show()
