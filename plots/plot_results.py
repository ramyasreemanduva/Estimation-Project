import matplotlib.pyplot as plt
import numpy as np

def plot_trajectory(true_states, estimates, beacons, inner, outer):
    time = np.arange(len(estimates)) * 0.01
    
    # FIG 1: Track Performance (As seen in your image)
    plt.figure(figsize=(12, 7))
    plt.plot(inner[0], inner[1], 'k', alpha=0.2, label='Lane Bounds')
    plt.plot(outer[0], outer[1], 'k', alpha=0.2)
    plt.plot(true_states[:,0], true_states[:,1], 'b-', alpha=0.4, label='True Trajectory')
    plt.plot(estimates[:,0], estimates[:,1], 'r--', linewidth=1.5, label='EKF Estimate')
    plt.scatter(beacons[:,0], beacons[:,1], c='red', marker='o', label='Beacons')
    for i, b in enumerate(beacons): plt.text(b[0]+2, b[1]+2, f'$b_{i+1}$', color='red')
    plt.axis('equal'); plt.grid(True, alpha=0.3); plt.legend()
    plt.title("Figure 1: Tracking Performance on Asymmetric Track")

    # FIG 2: Lateral Position Validation (yt)
    yt = [np.min(np.sqrt((true_states[:,0]-e[0])**2 + (true_states[:,1]-e[1])**2)) for e in estimates]
    plt.figure(figsize=(10, 4))
    plt.plot(time, yt, 'k', label='Lateral position $y_t$')
    plt.axhline(y=2.0, color='r', linestyle='--', label='Bound (2m)')
    plt.ylim(-0.1, 3); plt.grid(True); plt.ylabel("yt (m)")
    plt.title("Figure 2: Lateral Deviation Check")

    # FIG 3: Velocity Constraint
    speed = np.sqrt(estimates[:,2]**2 + estimates[:,3]**2)
    plt.figure(figsize=(10, 4))
    plt.plot(time, speed, label='Estimated Speed')
    plt.axhline(y=10, color='g', linestyle='--', label='Target (10m/s)')
    plt.axhline(y=25, color='r', linestyle=':', label='Max limit')
    plt.ylim(0, 30); plt.grid(True); plt.ylabel("Velocity (m/s)")
    plt.show()
