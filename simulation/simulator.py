import numpy as np
def simulate_1D(steps, dt):
    x, v = 0, 10
    data = []
    for _ in range(steps):
        x += v * dt
        data.append([x, v])
    return np.array(data)

def measure_1D(true):
    return true[:,0] + np.random.randn(len(true))*1.5
