import numpy as np

# SIMULATION

def simulate_2D(steps, dt):

    R = 50
    rho = 20
    d = 100
    v = 10

    data = []

    # angle of straight segments (approx from diagram)
    alpha = np.deg2rad(20)

    # segment lengths
    L1 = np.pi * R
    L2 = d
    L3 = np.pi * rho
    L4 = d

    total = L1 + L2 + L3 + L4
    s_vals = np.linspace(0, total, steps)

    for s in s_vals:

        if s < L1:
            # LEFT ARC
            theta = np.pi/2 - s / R
            x = R * np.cos(theta)
            y = R * np.sin(theta)

            vx = -v * np.sin(theta)
            vy =  v * np.cos(theta)

        elif s < L1 + L2:
            # TOP SLOPED STRAIGHT
            s2 = s - L1
            x = R + s2 * np.cos(alpha)
            y = s2 * np.sin(alpha)

            vx = v * np.cos(alpha)
            vy = v * np.sin(alpha)

        elif s < L1 + L2 + L3:
            # RIGHT ARC (shifted correctly)
            s3 = s - (L1 + L2)
            theta = np.pi/2 - s3 / rho

            cx = d
            cy = rho * np.sin(alpha)

            x = cx + rho * np.cos(theta)
            y = cy + rho * np.sin(theta)

            vx = -v * np.sin(theta)
            vy =  v * np.cos(theta)

        else:
            # BOTTOM SLOPED STRAIGHT
            s4 = s - (L1 + L2 + L3)
            x = d - s4 * np.cos(alpha)
            y = -s4 * np.sin(alpha)

            vx = -v * np.cos(alpha)
            vy = -v * np.sin(alpha)

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
