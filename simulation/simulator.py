import numpy as np
from models.dynamics import circular_motion, circular_velocity

def simulate_circular(steps, dt, R, omega):
    theta = 0.0
    data = []

    for _ in range(steps):
        x, y = circular_motion(theta, R)
        vx, vy = circular_velocity(theta, omega, R)

        data.append([x, y, vx, vy])
        theta += omega * dt

    return np.array(data)


def measure_2D(true_states):
    # Add Gaussian noise
    return true_states[:, :2] + np.random.randn(len(true_states), 2) * 1.5
