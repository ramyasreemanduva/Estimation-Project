import matplotlib.pyplot as plt
# Position Plot
def plot_position(x_true, estimates):
    plt.figure()
    plt.plot(x_true[:, 0], label="True Position")
    plt.plot(estimates[:, 0], label="Estimated Position")
    plt.xlabel("Time step")
    plt.ylabel("Position")
    plt.title("Day 1: Position Estimation")
    plt.legend()
    plt.grid()
    plt.show()

# Velocity Plot
def plot_velocity(x_true, estimates):
    plt.figure()
    plt.plot(x_true[:, 1], label="True Velocity")
    plt.plot(estimates[:, 1], label="Estimated Velocity")
    plt.xlabel("Time step")
    plt.ylabel("Velocity")
    plt.title("Day 1: Velocity Estimation")
    plt.legend()
    plt.grid()
    plt.show()
