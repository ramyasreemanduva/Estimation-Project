import numpy as np

# SIMULATION

def simulate_2D(steps, dt):
    # Track parameters
    R = 50.0      # left (big) radius
    rho = 20.0    # right (small) radius
    d = 100.0     # distance between arc centers
    v = 10.0

    # Centers
    A = np.array([0.0, 0.0])   # left center
    B = np.array([d, 0.0])     # right center

    # Lengths of segments
    L1 = np.pi * R      # left semicircle
    L2 = d              # top straight
    L3 = np.pi * rho    # right semicircle
    L4 = d              # bottom straight
    total = L1 + L2 + L3 + L4

    s_vals = np.linspace(0, total, steps)

    data = []

    for s in s_vals:

        if s < L1:
            # LEFT semicircle (top -> bottom)
            theta = np.pi/2 - s / R
            x = A[0] + R * np.cos(theta)
            y = A[1] + R * np.sin(theta)

            vx = -v * np.sin(theta)
            vy =  v * np.cos(theta)

        elif s < L1 + L2:
            # BOTTOM straight (left -> right)
            s2 = s - L1
            x = s2
            y = -R

            vx = v
            vy = 0

        elif s < L1 + L2 + L3:
            # RIGHT semicircle (bottom -> top)
            s3 = s - (L1 + L2)
            theta = -np.pi/2 + s3 / rho

            x = B[0] + rho * np.cos(theta)
            y = B[1] + rho * np.sin(theta)

            vx = -v * np.sin(theta)
            vy =  v * np.cos(theta)

        else:
            # TOP straight (right -> left)
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
