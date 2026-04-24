import numpy as np

# TRUE TRACK

def simulate_2D(steps, dt):

    R = 50.0
    rho = 20.0
    d = 100.0
    v = 10.0

    # Circle centers
    A = np.array([0.0, 0.0])
    B = np.array([d, 0.0])

    # ---------- Correct tangent angle ----------
    alpha = np.arcsin((R - rho) / d)

    # ---------- Tangent points ----------
    TL = A + R * np.array([ np.sin(alpha),  np.cos(alpha)])
    TR = B + rho * np.array([ np.sin(alpha),  np.cos(alpha)])

    BL = A + R * np.array([-np.sin(alpha), -np.cos(alpha)])
    BR = B + rho * np.array([-np.sin(alpha), -np.cos(alpha)])

    # ---------- Segment lengths ----------
    L_left = np.pi * R
    L_top = np.linalg.norm(TR - TL)
    L_right = np.pi * rho
    L_bottom = np.linalg.norm(BL - BR)

    total_length = L_left + L_top + L_right + L_bottom

    s_vals = np.linspace(0, total_length, steps)

    data = []

    for s in s_vals:

        # ---------- LEFT ARC ----------
        if s < L_left:
            theta_start = np.arctan2(TL[1], TL[0])
            theta = theta_start - s / R

            x = R * np.cos(theta)
            y = R * np.sin(theta)

            vx = -v * np.sin(theta)
            vy =  v * np.cos(theta)

        # ---------- TOP STRAIGHT ----------
        elif s < L_left + L_top:
            t = (s - L_left) / L_top
            pos = TL + t * (TR - TL)

            x, y = pos
            direction = (TR - TL) / L_top

            vx, vy = v * direction

        # ---------- RIGHT ARC ----------
        elif s < L_left + L_top + L_right:
            theta_start = np.arctan2(TR[1], TR[0] - d)
            theta = theta_start - (s - (L_left + L_top)) / rho

            x = d + rho * np.cos(theta)
            y = rho * np.sin(theta)

            vx = -v * np.sin(theta)
            vy =  v * np.cos(theta)

        # ---------- BOTTOM STRAIGHT ----------
        else:
            t = (s - (L_left + L_top + L_right)) / L_bottom
            pos = BR + t * (BL - BR)

            x, y = pos
            direction = (BL - BR) / L_bottom

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
