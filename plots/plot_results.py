import matplotlib.pyplot as plt

def plot_trajectory(true, est):
    plt.figure()

    plt.plot(true[:, 0], true[:, 1], label="True Path")
    plt.plot(est[:, 0], est[:, 1], '--', label="Estimated Path")

    plt.xlabel("X position")
    plt.ylabel("Y position")
    plt.title("EKF tracking with beacons on constrained path")

    plt.legend()
    plt.grid()

    plt.show()
