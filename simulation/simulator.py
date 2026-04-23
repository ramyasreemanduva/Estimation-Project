import numpy as np
from models.dynamics import apply_constraints

def simulate_2D(steps, dt):
    x, y = 0, 0
    vx, vy = 10, 0.5

    data = []

    for _ in range(steps):
        x += vx * dt
        y += vy * dt

        # Apply constraint
        y = apply_constraints(y)

        data.append([x, y, vx, vy])

    return np.array(data)


def measure_2D(true_states):
    return true_states[:, :2] + np.random.randn(len(true_states), 2) * 1.5
