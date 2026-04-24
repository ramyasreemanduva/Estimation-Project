import numpy as np

# SIMULATION

def simulate_2D(steps, dt):

    R = 50.0
    rho = 20.0
    d = 100.0
    v = 10.0

    data = []

    # Angle that creates the slanted connection
    alpha = np.arctan2(30, d)   # 30 ≈ R - rho

    theta_vals = np.linspace(0, 2*np.pi, steps)

    for theta in theta_vals:

        if theta < np.pi:
            # LEFT BIG ARC
            t = theta
            x = R * np.cos(t)
            y = R * np.sin(t)

            vx = -v * np.sin(t)
            vy =  v * np.cos(t)

        elif theta < np.pi + alpha:
            # TOP SLOPED STRAIGHT
            t = (theta - np.pi) / alpha

            x = R + t * d
            y = t * (R - rho)

            vx = v * np.cos(alpha)
            vy = v * np.sin(alpha)

        elif theta < 2*np.pi - alpha:
            # RIGHT SMALL ARC
            t = (theta - (np.pi + alpha)) / (np.pi - 2*alpha)
            ang = np.pi/2 - t*np.pi

            x = d + rho * np.cos(ang)
            y = rho * np.sin(ang)

            vx = -v * np.sin(ang)
            vy =  v * np.cos(ang)

        else:
            # BOTTOM SLOPED STRAIGHT
            t = (theta - (2*np.pi - alpha)) / alpha

            x = d - t * d
            y = -t * (R - rho)

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
