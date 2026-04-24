import numpy as np

# TRUE TRACK

import numpy as np

def simulate_2D(steps, dt):

    R = 50.0
    rho = 20.0
    d = 100.0
    v = 10.0

    # ---------- Build centerline track ----------
    pts = []

    # 1. LEFT ARC (big circle)
    theta1 = np.linspace(np.pi/2, -np.pi/2, steps//4)
    x1 = R * np.cos(theta1)
    y1 = R * np.sin(theta1)

    # 2. BOTTOM STRAIGHT (slanted)
    x2 = np.linspace(x1[-1], d, steps//4)
    y2 = np.linspace(y1[-1], -20, steps//4)

    # 3. RIGHT ARC (small circle)
    theta3 = np.linspace(-np.pi/2, np.pi/2, steps//4)
    x3 = d + rho * np.cos(theta3)
    y3 = rho * np.sin(theta3)

    # 4. TOP STRAIGHT (slanted)
    x4 = np.linspace(x3[-1], x1[0], steps//4)
    y4 = np.linspace(y3[-1], y1[0], steps//4)

    # Combine path
    x = np.concatenate([x1, x2, x3, x4])
    y = np.concatenate([y1, y2, y3, y4])

    # ---------- Compute velocity ----------
    vx = np.gradient(x, dt)
    vy = np.gradient(y, dt)

    states = np.column_stack([x, y, vx, vy])

    return states


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
