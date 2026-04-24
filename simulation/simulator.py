import numpy as np
from models.dynamics import apply_track_constraint

# Vehicle Simulation 

def simulate_2D(steps, dt):

    R_center = 48
    omega = 10 / R_center  # v = r*omega

    theta = 0
    data = []

    for _ in range(steps):

        # lateral motion (small)
        lateral = np.clip(np.random.randn() * 0.3, -2, 2)

        r_actual = R_center + lateral

        x = r_actual * np.cos(theta)
        y = r_actual * np.sin(theta)

        # apply constraint
        x, y = apply_track_constraint(x, y)

        vx = -r_actual * omega * np.sin(theta)
        vy = r_actual * omega * np.cos(theta)

        data.append([x, y, vx, vy])

        theta += omega * dt

    return np.array(data)

# Beacon Measurements

def measure_beacons(states, beacons):

    measurements = []

    for state in states:
        z = []
        for bx, by in beacons:
            dist = np.sqrt((state[0] - bx)**2 + (state[1] - by)**2)
            z.append(dist + np.random.randn() * 1.5)
        measurements.append(z)

    return np.array(measurements)
