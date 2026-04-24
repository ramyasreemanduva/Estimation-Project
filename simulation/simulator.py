import numpy as np

# SIMULATION

import numpy as np

def simulate_2D(steps, dt):

    R = 50.0
    rho = 20.0
    d = 100.0
    v = 10.0

    A = np.array([0.0, 0.0])
    B = np.array([d, 0.0])

    # -------- Correct tangent angle --------
    alpha = np.arcsin((R - rho) / d)

    # -------- Tangent points --------
    TL = A + R * np.array([ np.sin(alpha),  np.cos(alpha)])
    TR = B + rho * np.array([ np.sin(alpha),  np.cos(alpha)])

    BL = A + R * np.array([-np.sin(alpha), -np.cos(alpha)])
    BR = B + rho * np.array([-np.sin(alpha), -np.cos(alpha)])

    # -------- Segment lengths --------
    L1 = np.pi * R
    L2 = np.linalg.norm(TR - TL)
    L3 = np.pi * rho
    L4 = np.linalg.norm(BR - BL)

    total = L1 + L2 + L3 + L4
    s_vals = np.linspace(0, total, steps)

    data = []

    for s in s_vals:

        # ---------- LEFT ARC ----------
        if s < L1:
            theta0 = np.arctan2(TL[1], TL[0])
            theta = theta0 - s / R

            x = R * np.cos(theta)
            y = R * np.sin(theta)

            vx = -v * np.sin(theta)
            vy =  v * np.cos(theta)

        # ---------- TOP SLOPED STRAIGHT ----------
        elif s < L1 + L2:
            s2 = (s - L1) / L2
            pos = TL + s2 * (TR - TL)

            x, y = pos
            direction = (TR - TL) / L2

            vx, vy = v * direction

        # ---------- RIGHT ARC ----------
        elif s < L1 + L2 + L3:
            theta0 = np.arctan2(TR[1], TR[0] - d)
            theta = theta0 - (s - (L1 + L2)) / rho

            x = d + rho * np.cos(theta)
            y = rho * np.sin(theta)

            vx = -v * np.sin(theta)
            vy =  v * np.cos(theta)

        # ---------- BOTTOM SLOPED STRAIGHT ----------
        else:
            s4 = (s - (L1 + L2 + L3)) / L4
            pos = BR + s4 * (BL - BR)

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
