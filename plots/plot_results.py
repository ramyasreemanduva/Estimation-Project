import matplotlib.pyplot as plt
import numpy as np

def plot_trajectory(true_states, estimates, beacons, inner, outer):
    time = np.arange(len(estimates)) * 0.01 # [cite: 20]
    
    # Figure 1: Path
    plt.figure(figsize=(10, 5))
    plt.plot(inner[0], inner[1], 'gray', alpha=0.5, label='Lane Bounds') [cite: 17]
    plt.plot(outer[0], outer[1], 'gray', alpha=0.5)
    plt.plot(estimates[:,0], estimates[:,1], 'r--', label='EKF Estimate')
    plt.scatter(beacons[:,0], beacons[:,1], c='red', label='Beacons') [cite: 18, 37]
    plt.axis('equal'); plt.legend(); plt.grid(True)

    # Figure 2: Lateral Position Validation (Matches coursework Fig 3) [cite: 72]
    # Calculate yt as distance from current estimate to center of lane
    yt = [np.min(np.sqrt((true_states[:,0]-e[0])**2 + (true_states[:,1]-e[1])**2)) for e in estimates]
    plt.figure(figsize=(10, 4))
    plt.plot(time, yt, 'k', label='Lateral position, $y_t$') [cite: 60]
    plt.axhline(y=2, color='r', linestyle='--', label='Bound (2m)') [cite: 14, 63]
    plt.ylim(-0.5, 3); plt.grid(True); plt.ylabel("Lateral position, $y_t$ (m)"); plt.xlabel("Time (s)") [cite: 60, 69]

    # Figure 3: Velocity Constraint Validation 
    speed = np.sqrt(estimates[:,2]**2 + estimates[:,3]**2)
    plt.figure(figsize=(10, 4))
    plt.plot(time, speed, label='Estimated Speed')
    plt.axhline(y=10, color='g', linestyle='--', label='Target (10m/s)') [cite: 16]
    plt.axhline(y=25, color='r', linestyle=':', label='Max limit (25m/s)') [cite: 16]
    plt.ylim(0, 30); plt.grid(True); plt.ylabel("Velocity (m/s)") [cite: 16]
    plt.show()
