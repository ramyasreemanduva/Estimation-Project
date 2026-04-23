import matplotlib.pyplot as plt

def plot_trajectory(true, est):
    plt.figure()

    plt.plot(true[:, 0], true[:, 1], label="True Path")
    plt.plot(est[:, 0], est[:, 1], '--', label="Estimated Path")

    plt.xlabel("X position")
    plt.ylabel("Y position")
    plt.title("Day 3: Constrained Motion")

    plt.legend()
    plt.grid()

    plt.show()
