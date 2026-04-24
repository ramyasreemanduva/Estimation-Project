import numpy as np

# SIMULATION

def simulate_2D(steps, dt):

    R = 50
    d = 100
    v = 10

    data = []

    theta = np.pi/2
    x, y = -d/2, 0

    for k in range(steps):

        seg = k % 4

        if seg == 0:
            x = -d/2 + R * np.cos(theta)
            y = R * np.sin(theta)

            vx = -v * np.sin(theta)
            vy = v * np.cos(theta)

            theta -= v / R * dt

        elif seg == 1:
            x += v * dt
            vx = v
            vy = 0

        elif seg == 2:
            x = d/2 + R * np.cos(theta)
            y = R * np.sin(theta)

            vx = -v * np.sin(theta)
            vy = v * np.cos(theta)

            theta -= v / R * dt

        else:
            x -= v * dt
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
