import numpy as np

# SIMULATION

def simulate_2D(steps, dt):
    R = 50       # left radius
    rho = 20     # right radius
    d = 100      # center distance
    v = 10

    data = []

    # segment lengths
    L1 = np.pi * R          # left half circle
    L2 = d                  # top straight
    L3 = np.pi * rho        # right half circle
    L4 = d                  # bottom straight

    total = L1 + L2 + L3 + L4
    s_vals = np.linspace(0, total, steps)

    for s in s_vals:

        if s < L1:
            # LEFT ARC (top → bottom)
            theta = np.pi/2 - s / R
            x = R * np.cos(theta)
            y = R * np.sin(theta)
            vx = -v * np.sin(theta)
            vy =  v * np.cos(theta)

        elif s < L1 + L2:
            # BOTTOM STRAIGHT (connects smoothly)
            s2 = s - L1
            x = s2
            y = -R
            vx = v
            vy = 0

        elif s < L1 + L2 + L3:
            # RIGHT ARC (bottom → top)
            s3 = s - (L1 + L2)
            theta = -np.pi/2 + s3 / rho
            x = d + rho * np.cos(theta)
            y = rho * np.sin(theta)
            vx = -v * np.sin(theta)
            vy =  v * np.cos(theta)

        else:
            # TOP STRAIGHT (connects back to start)
            s4 = s - (L1 + L2 + L3)
            x = d - s4
            y = R
            vx = -v
            vy = 0

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
