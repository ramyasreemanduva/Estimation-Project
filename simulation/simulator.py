import numpy as np

# SIMULATION

def simulate_2D(steps, dt):
    # Given
    R = 50.0     # outer left radius
    rho = 20.0   # right tight radius
    d = 100.0    # distance A->B
    v = 10.0

    # Centers
    A = np.array([0.0, 0.0])
    B = np.array([d, 0.0])

    # We build a smooth centerline by blending:
    # left big arc (around A, radius ~ R-2)  +  right small arc (around B, radius ~ rho+2)
    # and connect them with *tangent* lines using a parameter t in [0, 2π]
    # This avoids piecewise jumps entirely.

    t_vals = np.linspace(0, 2*np.pi, steps)

    data = []

    for t in t_vals:
        # Blend angle to move from left big arc to right small arc smoothly
        # weight goes from 1 (left) to 0 (right) across half cycle
        w = 0.5*(1 + np.cos(t))   # in [0,1]

        # radii for centerline (mid-lane approx)
        rL = 48.0      # near center of [46,50]
        rR = rho + 2.0 # ~22 (center-ish for right lobe)

        # angles for arcs
        thetaL = t
        thetaR = t + np.pi  # opposite phase to create teardrop asymmetry

        # points on each arc
        pL = A + rL * np.array([np.cos(thetaL), np.sin(thetaL)])
        pR = B + rR * np.array([np.cos(thetaR), np.sin(thetaR)])

        # smooth blend (guarantees continuity)
        x, y = w * pL + (1 - w) * pR

        # approximate velocity via derivative of blend
        # (good enough for EKF; keeps continuity)
        dtheta = 2*np.pi / max(steps-1, 1)
        # next t for finite difference
        t2 = t + dtheta
        w2 = 0.5*(1 + np.cos(t2))
        thetaL2 = t2
        thetaR2 = t2 + np.pi
        pL2 = A + rL * np.array([np.cos(thetaL2), np.sin(thetaL2)])
        pR2 = B + rR * np.array([np.cos(thetaR2), np.sin(thetaR2)])
        x2, y2 = w2 * pL2 + (1 - w2) * pR2

        vx = (x2 - x) / dt
        vy = (y2 - y) / dt

        # normalize speed to ~v (keeps motion realistic)
        speed = np.hypot(vx, vy) + 1e-9
        vx = vx * (v / speed)
        vy = vy * (v / speed)

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
