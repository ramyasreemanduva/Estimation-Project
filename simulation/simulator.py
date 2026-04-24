import numpy as np

# TRUE TRACK

dimport numpy as np

# TRUE TRACK
def simulate_2D(steps, dt):
    # Constants based on diagram
    R = 50      # Large radius
    rho = 20    # Small radius
    d = 100     # Distance between centers A and B
    
    # To match the first image, we need the path to start at (0, 50)
    # The center of the left circle is at (50, 0)
    center_a = np.array([50, 0])
    center_b = np.array([50 + d, 0])

    # Angle where the tangent lines touch the circles
    # sin(alpha) = (R - rho) / d
    alpha = np.arcsin((R - rho) / d)

    # ---------- LEFT ARC (Outer curve) ----------
    # Sweeps from top tangent point to the far left, then to bottom tangent
    theta_left = np.linspace(np.pi/2 + alpha, 1.5*np.pi - alpha, steps//3)
    x_left = center_a[0] + R * np.cos(theta_left)
    y_left = center_a[1] + R * np.sin(theta_left)

    # ---------- RIGHT ARC (Small curve) ----------
    # Sweeps around the tip on the right
    theta_right = np.linspace(-np.pi/2 + alpha, np.pi/2 - alpha, steps//3)
    x_right = center_b[0] + rho * np.cos(theta_right)
    y_right = center_b[1] + rho * np.sin(theta_right)

    # ---------- CONNECTING STRAIGHTS ----------
    # Bottom straight (end of left arc to start of right arc)
    x_bottom = np.linspace(x_left[-1], x_right[0], steps//6)
    y_bottom = np.linspace(y_left[-1], y_right[0], steps//6)

    # Top straight (end of right arc to start of left arc)
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
    # Using the beacon positions from the diagram (approximate based on red dots)
    # b1 is bottom left, b2 is top left, b3 is bottom right
    for state in states:
        z = []
        for bx, by in beacons:
            dist = np.sqrt((state[0] - bx)**2 + (state[1] - by)**2)
            # Adding noise as per EKF requirements
            z.append(dist + np.random.normal(0, 1.5))
        measurements.append(z)

    return np.array(measurements)

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
