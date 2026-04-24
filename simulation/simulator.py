import numpy as np

# True Motion

def simulate_2D(steps, dt):
    x, y = 0, 0
    vx, vy = 10, 0.5

    data = []

    for _ in range(steps):
        x += vx * dt
        y += vy * dt
        data.append([x, y, vx, vy])

    return np.array(data)


# Beacon Measurements

def measure_beacons(states, beacons):
    measurements = []

    for state in states:
        z = []
        for bx, by in beacons:
            dist = np.sqrt((state[0] - bx)**2 + (state[1] - by)**2)
            noisy_dist = dist + np.random.randn() * 1.5
            z.append(noisy_dist)
        measurements.append(z)

    return np.array(measurements)
