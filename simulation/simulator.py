import numpy as np

# TRUE TRACK

import numpy as np

import numpy as np

def simulate_2D(steps, dt):

    R = 50.0
    rho = 20.0
    d = 100.0
    v = 10.0

    A = np.array([0.0, 0.0])
    B = np.array([d, 0.0])

    # ---------- TRUE tangent angle ----------
    alpha = np.arccos((R - rho) / d)

    # ---------- tangent direction ----------
    dx = np.cos(alpha)
    dy = np.sin(alpha)

    # ---------- tangent points ----------
    TL = np.array([ R*dy,  R*dx])
    BL = np.array([-R*dy, -R*dx])

    TR = np.array([d + rho*dy,  rho*dx])
    BR = np.array([d - rho*dy, -rho*dx])

    # ---------- segment lengths ----------
    L1 = np.pi * R
    L2 = np.linalg.norm(TR - TL)
    L3 = np.pi * rho
    L4 = np.linalg.norm(BL - BR)

    total = L1 + L2 + L3 + L4
    s_vals = np.linspace(0, total, steps)

    data = []

    for s in s_vals:

        # LEFT ARC
        if s < L1:
            theta = np.pi/2 - s / R
            x = R * np.cos(theta)
            y = R * np.sin(theta)

            vx = -v * np.sin(theta)
            vy =  v * np.cos(theta)

        # TOP STRAIGHT
        elif s < L1 + L2:
            t = (s - L1) / L2
            pos = TL + t * (TR - TL)

            x, y = pos
            direction = (TR - TL) / L2
            vx, vy = v * direction

        # RIGHT ARC
        elif s < L1 + L2 + L3:
            theta = np.pi/2 - (s - (L1 + L2)) / rho
            x = d + rho * np.cos(theta)
            y = rho * np.sin(theta)

            vx = -v * np.sin(theta)
            vy =  v * np.cos(theta)

        # BOTTOM STRAIGHT
        else:
            t = (s - (L1 + L2 + L3)) / L4
            pos = BR + t * (BL - BR)

            x, y = pos
            direction = (BL - BR) / L4
            vx, vy = v * direction

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
