import matplotlib.pyplot as plt
import numpy as np

def plot_trajectory(true_states, estimates, beacons, inner, outer):
    time = np.arange(len(estimates)) * 0.01 
    
    # 2D Trajectory
    plt.figure(figsize=(8, 5))
    plt.plot(inner[0], inner[1], 'k', alpha=0.3, label='Lane Bounds')
    plt.plot(outer[0], outer[1], 'k', alpha=0.3)
    plt.plot(estimates[:,0], estimates[:,1], 'r--', label='EKF Estimate')
    plt.scatter(beacons[:,0], beacons[:,1], c='red', marker='o')
    for i, b in enumerate(beacons): plt.text(b[0]+2, b[1]+2, f'$b_{i+1}$', color='red')
    plt.axis('equal'); plt.legend(); plt.grid(True); plt.title("Figure 1: Tracking Performance")

    # Lateral Position (Validation of Figure 3 [cite: 72])
    yt = np.array([np.min(np.sqrt((true_states[:,0]-e[0])**2 + (true_states[:,1]-e[1])**2)) for e in estimates])
    plt.figure(figsize=(8, 3))
    plt.plot(time, yt, 'k', label='Lateral Position $y_t$')
    plt.axhline(y=2, color='r', linestyle='--', label='Bound (2m)') # Width=4m 
    plt.ylim(-0.5, 3); plt.legend(); plt.grid(True); plt.ylabel("Position (m)"); plt.xlabel("Time (s)")

    # Velocity Constraint (Max 25m/s )
    speed = np.sqrt(estimates[:,2]**2 + estimates[:,3]**2)
    plt.figure(figsize=(8, 3))
    plt.plot(time, speed, label='Estimated Speed')
    plt.axhline(y=10, color='g', linestyle='--', label='Target (10m/s)')
    plt.axhline(y=25, color='r', linestyle=':', label='Max limit (25m/s)')
    plt.ylim(0, 30); plt.legend(); plt.grid(True); plt.ylabel("Speed (m/s)")
    plt.show()
