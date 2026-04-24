import numpy as np

# SIMULATION

import numpy as np

import numpy as np

def simulate_2D(steps, dt):

    R = 50      # left curve
    rho = 20    # right curve
    d = 100     # horizontal distance
    v = 10

    data = []

    # arc lengths
    L1 = np.pi * R        # left half-circle
    L2 = d                # top straight
    L3 = np.pi * rho      # right half-circle
    L4 = d                # bottom straight

    total = L1 + L2 + L3 + L4

    s_vals = np.linspace(0, total, steps)

    for s in s_vals:

        if s < L1:
            # LEFT BIG ARC (center A = (0,0))
            theta = np.pi/2 - s / R

            x = R * np.cos(theta)
            y = R * np.sin(theta)

            vx = -v * np.sin(theta)
            vy = v * np.cos(theta)

        elif s < L1 + L2:
            # TOP STRAIGHT
            s2 = s - L1

            x = R + s2
            y = 0

            vx = v
            vy = 0

        elif s < L1 + L2 + L3:
            # RIGHT SMALL ARC (center B = (d,0))
            s3 = s - (L1 + L2)
            theta = np.pi/2 - s3 / rho

            x = d + rho * np.cos(theta)
            y = rho * np.sin(theta)

            vx = -v * np.sin(theta)
            vy = v * np.cos(theta)

        else:
            # BOTTOM STRAIGHT
            s4 = s - (L1 + L2 + L3)

            x = d + rho - s4
            y = 0

            vx = -v
            vy = 0

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
