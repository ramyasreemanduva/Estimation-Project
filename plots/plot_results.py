import matplotlib.pyplot as plt
import numpy as np

def plot_trajectory(true_states, estimates, beacons, inner, outer):
    time = np.arange(len(estimates)) * 0.01
    
    # Figure 1: Track validation
    plt.figure(figsize=(10, 6))
    plt.plot(inner[0], inner[1], 'gray', alpha=0.3, label='Lane Bounds')
    plt.plot(outer[0], outer[1], 'gray', alpha=0.3)
    plt.plot(estimates[:,0], estimates[:,1], 'r--', label='EKF Estimate')
    plt.scatter(beacons[:,0], beacons[:,1], c='red', label='Beacons')
    plt.axis('equal'); plt.grid(True); plt.legend()
    plt.title("Figure 1: Final Geometry Tracking")

    # Figure 2: Lateral Position Validation (Matches Fig 3 in Coursework)
    yt = [np.min(np.sqrt((true_states[:,0]-e[0])**2 + (true_states[:,1]-e[1])**2)) for e in estimates]
    plt.figure(figsize=(10, 4))
    plt.plot(time, yt, 'k', label='Lateral position, $y_t$')
    plt.axhline(y=2.0, color='r', linestyle='--', label='Bound (2m)')
    plt.ylim(-0.5, 3); plt.grid(True); plt.ylabel("yt (m)")
    plt.title("Figure 2: Lateral Constraint Validation")

    # Figure 3: Velocity Profile
    speed = np.sqrt(estimates[:,2]**2 + estimates[:,3]**2)
    plt.figure(figsize=(10, 4))
    plt.plot(time, speed, label='Estimated Speed')
    plt.axhline(y=10, color='g', linestyle='--', label='Target (10m/s)')
    plt.axhline(y=25, color='r', linestyle=':', label='Max Limit (25m/s)')
    plt.ylim(0, 30); plt.grid(True); plt.ylabel("Velocity (m/s)")
    plt.title("Figure 3: Velocity Profile")
    plt.show()
