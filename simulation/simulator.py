import numpy as np

# SIMULATION

def simulate_2D(steps, dt):

    R = 48        # center radius
    v = 10        # velocity
    omega = v / R

    theta = 0
    data = []

    for _ in range(steps):

        # Smooth circular motion
        x = R * np.cos(theta)
        y = R * np.sin(theta)

        vx = -v * np.sin(theta)
        vy = v * np.cos(theta)

        data.append([x, y, vx, vy])

        theta += omega * dt

    return np.array(data)

# MEASUREMENTS 

def measure_beacons(states, beacons):

    measurements = []

    for state in states:
        z = []
        for bx, by in beacons:
            dist = np.sqrt((state[0] - bx)**2 + (state[1] - by)**2)
            z.append(dist + np.random.randn() * 1.5)
        measurements.append(z)

    return np.array(measurements)
