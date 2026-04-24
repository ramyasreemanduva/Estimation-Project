import numpy as np

# SIMULATION

def simulate_2D(steps, dt):
    R = 50.0
    rho = 20.0
    d = 100.0
    v = 10.0

    A = np.array([0.0, 0.0])
    B = np.array([d, 0.0])

    # --- Compute common external tangent angle ---
    # sin(alpha) = (R - rho) / d
    alpha = np.arcsin((R - rho) / d)  # slope angle of the straight

    # Tangent points on left circle (A) and right circle (B)
    # Top tangent points
    TL = A + R * np.array([ np.sin(alpha),  np.cos(alpha)])
    TR = B + rho * np.array([ np.sin(alpha),  np.cos(alpha)])

    # Bottom tangent points
    BL = A + R * np.array([-np.sin(alpha), -np.cos(alpha)])
    BR = B + rho * np.array([-np.sin(alpha), -np.cos(alpha)])

    # Segment lengths
    L1 = np.pi * R          # left arc
    L2 = np.linalg.norm(TR - TL)  # top straight
    L3 = np.pi * rho        # right arc
    L4 = np.linalg.norm(BL - BR)  # bottom straight

    total = L1 + L2 + L3 + L4
    s_vals = np.linspace(0, total, steps)

    data = []

    for s in s_vals:

        if s < L1:
            # LEFT ARC: from TL -> BL (clockwise)
            theta0 = np.arctan2(TL[1]-A[1], TL[0]-A[0])
            theta = theta0 - s / R

            x = A[0] + R * np.cos(theta)
            y = A[1] + R * np.sin(theta)

            vx = -v * np.sin(theta)
            vy =  v * np.cos(theta)

        elif s < L1 + L2:
            # TOP STRAIGHT: TL -> TR
            s2 = (s - L1) / L2
            pos = TL + s2 * (TR - TL)

            x, y = pos
            dir_vec = (TR - TL) / L2
            vx, vy = v * dir_vec

        elif s < L1 + L2 + L3:
            # RIGHT ARC: TR -> BR (clockwise)
            theta0 = np.arctan2(TR[1]-B[1], TR[0]-B[0])
            theta = theta0 - (s - (L1 + L2)) / rho

            x = B[0] + rho * np.cos(theta)
            y = B[1] + rho * np.sin(theta)

            vx = -v * np.sin(theta)
            vy =  v * np.cos(theta)

        else:
            # BOTTOM STRAIGHT: BR -> BL
            s4 = (s - (L1 + L2 + L3)) / L4
            pos = BR + s4 * (BL - BR)

            x, y = pos
            dir_vec = (BL - BR) / L4
            vx, vy = v * dir_vec

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
