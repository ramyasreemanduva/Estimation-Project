import matplotlib.pyplot as plt
import numpy as np

def plot_trajectory(true_states, estimates, beacons, inner, outer):
    time = np.arange(len(estimates)) * 0.01
    
    # FIG 1: Track and Estimation
    plt.figure(figsize=(12, 7))
    plt.plot(inner[0], inner[1], 'k', alpha=0.15, label='Lane Bounds')
    plt.plot(outer[0], outer[1], 'k', alpha=0.15)
    plt.plot(true_states[:,0], true_states[:,1], 'b-', alpha=0.3, label='True Path')
    plt.plot(estimates[:,0], estimates[:,1], 'r--', label='EKF Estimate')
    plt.scatter(beacons[:,0], beacons[:,1], c='red', label='Beacons')
    plt.axis('equal'); plt.grid(True, alpha=0.2); plt.legend()
    plt.title("Figure 1: Corrected Tracking on Asymmetric Track")

    # FIG 2: Lateral Position Validation (Constraint < 2m)
    yt = [np.min(np.sqrt((true_states[:,0]-e[0])**2 + (true_states[:,1]-e[1])**2)) for e in estimates]
    plt.figure(figsize=(10, 4))
    plt.plot(time, yt, 'k', label='Lateral position $y_t$')
    plt.axhline(y=2.0, color='r', linestyle='--', label='Bound (2m)')
    plt.ylim(-0.1, 3); plt.grid(True); plt.ylabel("yt (m)")
    plt.title("Figure 2: Lateral Deviation Constraint")

    # FIG 3: Velocity Validation (Target 10m/s)
    speed = np.sqrt(estimates[:,2]**2 + estimates[:,3]**2)
    plt.figure(figsize=(10, 4))
    plt.plot(time, speed, label='Estimated Speed')
    plt.axhline(y=10, color='g', linestyle='--', label='Target')
    plt.axhline(y=25, color='r', linestyle=':', label='Max Limit')
    plt.ylim(0, 30); plt.grid(True); plt.ylabel("Velocity (m/s)")
    plt.title("Figure 3: Velocity Profile")
    plt.show()
    
