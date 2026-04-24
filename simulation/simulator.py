import numpy as np

# TRUE TRACK

def simulate_2D(steps, dt):

    # ---- Key shape points from your diagram ----
    path_points = np.array([
        [-15, -45],   # bottom-left
        [10, 45],     # top-left
        [120, 30],    # top-right
        [120, 0],     # right arc start
        [120, -20],   # right arc bottom
        [90, -20],    # lower right straight
        [-15, -45]    # close loop
    ])

    # ---- Interpolate smooth path ----
    pts = []
    for i in range(len(path_points) - 1):
        p1 = path_points[i]
        p2 = path_points[i + 1]

        for t in np.linspace(0, 1, steps // (len(path_points)-1)):
            pt = p1 + t * (p2 - p1)
            pts.append(pt)

    pts = np.array(pts)

    # ---- Add curved arcs manually ----
    theta = np.linspace(np.pi/2, -np.pi/2, 200)

    # Left big arc
    left_arc = np.column_stack([
        50 * np.cos(theta),
        50 * np.sin(theta)
    ])

    # Right small arc
    right_arc = np.column_stack([
        100 + 20 * np.cos(theta),
        20 * np.sin(theta)
    ])

    # ---- Combine everything ----
    full_path = np.vstack([
        left_arc,
        pts,
        right_arc
    ])

    # ---- Compute velocity ----
    velocities = np.gradient(full_path, axis=0) / dt

    return np.hstack([full_path, velocities])


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
