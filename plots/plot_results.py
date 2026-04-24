import matplotlib.pyplot as plt
import numpy as np

def plot_trajectory(true_states, estimates, beacons, inner, outer):
    time = np.arange(len(estimates)) * 0.01
    
    # Figure 1: Tracking Performance with Boundaries [cite: 37, 58]
    plt.figure(figsize=(10, 6))
    plt.plot(inner[0], inner[1], 'gray', alpha=0.5, label='Inner Bound (r=46m)')
    plt.plot(outer[0], outer[1], 'gray', alpha=0.5, label='Outer Bound (R=50m)')
    plt.plot(estimates[:,0], estimates[:,1], 'r--', label='EKF Estimate')
    plt.scatter(beacons[:,0], beacons[:,1], c='red', label='Beacons')
    plt.axis('equal'); plt.legend(); plt.grid(True); plt.title("Figure 1: Boundary Validation")

    # Figure 2: Lateral Position Validation [cite: 72, 91]
    # yt calculated as distance to centerline
    yt = [np.min(np.sqrt((true_states[:,0]-e[0])**2 + (true_states[:,1]-e[1])**2)) for e in estimates]
    plt.figure(figsize=(10, 4))
    plt.plot(time, yt, 'k', label='Lateral position, $y_t$')
    plt.axhline(y=2, color='r', linestyle='--', label='Road Bound (2m)')
    plt.ylim(-0.5, 3); plt.grid(True); plt.ylabel("Position (m)"); plt.title("Figure 2: Lateral Analysis")

    # Figure 3: Velocity Validation 
    speed = np.sqrt(estimates[:,2]**2 + estimates[:,3]**2)
    plt.figure(figsize=(10, 4))
    plt.plot(time, speed, label='Estimated Speed')
    plt.axhline(y=25, color='r', linestyle=':', label='Max Limit (25m/s)')
    plt.ylim(0, 30); plt.grid(True); plt.ylabel("Velocity (m/s)"); plt.title("Figure 3: Velocity Profile")
    plt.show()
