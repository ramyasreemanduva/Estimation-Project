import matplotlib.pyplot as plt
import numpy as np

def plot_trajectory(true_states, estimates, beacons, inner=None, outer=None):
    time = np.arange(len(estimates)) * 0.01
    
    # 1. 2D TRACK
    plt.figure(figsize=(10, 5))
    plt.plot(inner[0], inner[1], 'k-', alpha=0.3, label='Lane Bounds')
    plt.plot(outer[0], outer[1], 'k-', alpha=0.3)
    plt.plot(estimates[:, 0], estimates[:, 1], 'r--', label='EKF Estimate')
    plt.scatter(beacons[:, 0], beacons[:, 1], c='red', label='Beacons')
    plt.axis('equal')
    plt.legend()
    plt.title("Figure 1: Track Layout")

    # 2. LATERAL POSITION (The 'Fig 3' Plot) [cite: 72]
    # Calculated as distance from centerline
    lat_pos = [np.min(np.sqrt((true_states[:,0]-e[0])**2 + (true_states[:,1]-e[1])**2)) for e in estimates]
    plt.figure(figsize=(10, 4))
    plt.plot(time, lat_pos, 'k', label='Lateral Position $y_t$')
    plt.axhline(y=2, color='r', linestyle='--', label='Upper Bound') # [cite: 14]
    plt.axhline(y=-2, color='r', linestyle='--', label='Lower Bound')
    plt.ylim(-3, 3); plt.grid(True); plt.legend()
    plt.title("Figure 2: Lateral Position Validation")

    # 3. VELOCITY 
    speed = np.sqrt(estimates[:, 2]**2 + estimates[:, 3]**2)
    plt.figure(figsize=(10, 4))
    plt.plot(time, speed, label='Estimated Speed')
    plt.axhline(y=10, color='g', linestyle='--', label='Target (10m/s)')
    plt.axhline(y=25, color='r', linestyle=':', label='Max Limit (25m/s)')
    plt.ylim(0, 30); plt.grid(True); plt.legend()
    plt.title("Figure 3: Velocity Constraint Check")

    # 4. LONGITUDINAL POSITION 
    dist = np.cumsum(np.sqrt(np.diff(estimates[:, 0], prepend=estimates[0,0])**2 + 
                             np.diff(estimates[:, 1], prepend=estimates[0,1])**2))
    plt.figure(figsize=(10, 4))
    plt.plot(time, dist, 'b')
    plt.title("Figure 4: Longitudinal Progress")
    plt.ylabel("Distance (m)"); plt.xlabel("Time (s)")

    plt.show()
