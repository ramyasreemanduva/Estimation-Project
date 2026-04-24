import numpy as np

# Circular Motion Simulation

def simulate_2D(steps, dt):
    R = 50          # radius
    omega = 0.2     # angular speed
    theta = 0

    data = []

    for _ in range(steps):
        # Position
        x = R * np.cos(theta)
        y = R * np.sin(theta)

        # Velocity (important for state)
        vx = -R * omega * np.sin(theta)
        vy = R * omega * np.cos(theta)

        data.append([x, y, vx, vy])

        # Move angle forward
        theta += omega * dt

    return np.array(data)


# Beacon Measurements

def measure_beacons(states, beacons):
    measurements = []

    for state in states:
        z = []
        for bx, by in beacons:
            dist = np.sqrt((state[0] - bx)**2 + (state[1] - by)**2)
            noisy_dist = dist + np.random.randn() * 1.0  # reduced noise
            z.append(noisy_dist)
        measurements.append(z)

    return np.array(measurements)
