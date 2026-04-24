import numpy as np

# TRUE TRACK

def simulate_2D(steps, dt):

    R = 50
    rho = 20
    d = 100
    v = 10

    # ---------- LEFT ARC ----------
    theta_left = np.linspace(np.pi/2, -np.pi/2, steps//3)
    x_left = R * np.cos(theta_left)
    y_left = R * np.sin(theta_left)

    # ---------- RIGHT ARC ----------
    theta_right = np.linspace(-np.pi/2, np.pi/2, steps//3)
    x_right = d + rho * np.cos(theta_right)
    y_right = rho * np.sin(theta_right)

    # ---------- CONNECTING STRAIGHTS ----------
    # bottom straight (end of left arc → start of right arc)
    x_bottom = np.linspace(x_left[-1], x_right[0], steps//6)
    y_bottom = np.linspace(y_left[-1], y_right[0], steps//6)

    # top straight (end of right arc → start of left arc)
    x_top = np.linspace(x_right[-1], x_left[0], steps//6)
    y_top = np.linspace(y_right[-1], y_left[0], steps//6)

    # ---------- COMBINE ----------
    x = np.concatenate([x_left, x_bottom, x_right, x_top])
    y = np.concatenate([y_left, y_bottom, y_right, y_top])

    # ---------- VELOCITY ----------
    vx = np.gradient(x, dt)
    vy = np.gradient(y, dt)

    return np.column_stack([x, y, vx, vy])

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
