import matplotlib.pyplot as plt
import numpy as np

def plot_trajectory(true_states, estimates, beacons, inner=None, outer=None):
    # ... existing array setup ...
    time = np.arange(len(true_states)) * 0.01

    # --- UPDATED LATERAL CALCULATION ---
    # We find the distance to the center path for every estimated point
    # true_states[:, 0:2] contains the (x, y) of the centerline
    lat_positions = []
    for i in range(len(estimates)):
        # Find the distance from the estimate to every point on the true path
        distances = np.sqrt((true_states[:, 0] - estimates[i, 0])**2 + 
                            (true_states[:, 1] - estimates[i, 1])**2)
        # The lateral deviation is the minimum distance found
        lat_positions.append(np.min(distances))
    
    lateral_deviation = np.array(lat_positions)

    # --- FIGURE 2: LATERAL POSITION (Constraint Validation) ---
    plt.figure(figsize=(10, 4))
    plt.plot(time, lateral_deviation, 'k-', linewidth=1.5, label='Lateral Deviation')
    
    #so bounds are +/- 2m from center
    plt.axhline(y=2, color='r', linestyle='--', label='Outer Wall (+2m)') 
    plt.axhline(y=-2, color='r', linestyle='--', label='Inner Wall (-2m)')
    
    plt.title("Lateral Position Over Time (Constraint Validation)")
    plt.xlabel("Time (s)")
    plt.ylabel("Lateral Deviation (m)")
    plt.ylim(-3, 3) 
    plt.legend(loc='upper right')
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
