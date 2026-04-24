import numpy as np

# SIMULATION

import numpy as np

def simulate_2D(steps, dt):

    R = 50        # curve radius
    d = 100       # straight length
    v = 10        # velocity

    data = []

    # lengths of each segment
    L_straight = d
    L_curve = np.pi * R   # half circle

    total_length = 2*L_straight + 2*L_curve

    # distance traveled along track
    s_vals = np.linspace(0, total_length, steps)

    for s in s_vals:

        if s < L_straight:
            # Top straight (left → right)
            x = -d/2 + s
            y = R

            vx = v
            vy = 0

        elif s < L_straight + L_curve:
            # Right semicircle
            s_curve = s - L_straight
            theta = np.pi/2 - s_curve / R

            x = d/2 + R * np.cos(theta)
            y = R * np.sin(theta)

            vx = -v * np.sin(theta)
            vy = v * np.cos(theta)

        elif s < 2*L_straight + L_curve:
            # Bottom straight (right → left)
            s_line = s - (L_straight + L_curve)

            x = d/2 - s_line
            y = -R

            vx = -v
            vy = 0

        else:
            # Left semicircle
            s_curve = s - (2*L_straight + L_curve)
            theta = -np.pi/2 - s_curve / R

            x = -d/2 + R * np.cos(theta)
            y = R * np.sin(theta)

            vx = -v * np.sin(theta)
            vy = v * np.cos(theta)

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
