import matplotlib.pyplot as plt

def plot_trajectory(true_states, estimates, beacons, inner=None, outer=None):
    plt.figure(figsize=(12, 6))
    
    # Plot Boundaries (The Track Walls)
    if inner: plt.plot(inner[0], inner[1], 'k-', alpha=0.8, linewidth=2)
    if outer: plt.plot(outer[0], outer[1], 'k-', alpha=0.8, linewidth=2)
    
    # Plot Paths
    
    plt.plot(estimates[:, 0], estimates[:, 1], '--', label='Estimated Path', linewidth=1.5)
    
    # Plot Beacons
    plt.scatter(beacons[:, 0], beacons[:, 1], c='red', marker='o', label='Beacons')
    for i, b in enumerate(beacons):
        plt.text(b[0]+2, b[1]+2, f'b{i+1}', color='red', fontweight='bold')

    plt.title("EKF tracking with beacons on constrained path")
    plt.xlabel("X position")
    plt.ylabel("Y position")
    plt.legend()
    plt.grid(True)
    plt.axis('equal') # Crucial for circular look
    plt.show()
