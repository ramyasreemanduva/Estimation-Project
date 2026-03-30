import numpy as np

def simulate_motion(T=10, dt=0.1):
    t = np.arange(0, T, dt)
    x = 10 * t  # simple constant velocity motion
    return t, x
