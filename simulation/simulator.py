import numpy as np

# SIMULATION

def simulate_2D(steps, dt):

    R = 48
    omega = 10 / R

    data = []

    theta_vals = np.linspace(0, 2*np.pi, steps)

    for theta in theta_vals:

        x = R * np.cos(theta)
        y = R * np.sin(theta)

        vx = -R * omega * np.sin(theta)
        vy = R * omega * np.cos(theta)

        data.append([x, y, vx, vy])

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
