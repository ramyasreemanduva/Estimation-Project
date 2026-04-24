import numpy as np

# SIMULATION

import numpy as np

def simulate_2D(steps, dt):

    R = 50      # left big radius
    rho = 20    # right small radius
    d = 100
    v = 10

    data = []

    # centers
    A = np.array([0, 0])        # left center
    B = np.array([d, 0])        # right center

    # arc lengths
    L1 = np.pi * R
    L2 = d
    L3 = np.pi * rho
    L4 = d

    total = L1 + L2 + L3 + L4

    s_vals = np.linspace(0, total, steps)

    for s in s_vals:

        if s < L1:
            # LEFT ARC (top → bottom)
            theta = np.pi/2 - s / R

            x = A[0] + R * np.cos(theta)
            y = A[1] + R * np.sin(theta)

            vx = -v * np.sin(theta)
            vy = v * np.cos(theta)

        elif s < L1 + L2:
            # BOTTOM STRAIGHT (left → right)
            s2 = s - L1

            x = A[0] + s2
            y = -R

            vx = v
            vy = 0

        elif s < L1 + L2 + L3:
            # RIGHT ARC (bottom → top)
            s3 = s - (L1 + L2)
            theta = -np.pi/2 + s3 / rho

            x = B[0] + rho * np.cos(theta)
            y = B[1] + rho * np.sin(theta)

            vx = -v * np.sin(theta)
            vy = v * np.cos(theta)

        else:
            # TOP STRAIGHT (right → left)
            s4 = s - (L1 + L2 + L3)

            x = B[0] - s4
            y = R

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
