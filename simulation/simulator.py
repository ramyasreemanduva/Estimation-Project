import numpy as np

def get_track_geometry(steps, dt=0.1):
    """Generates True Path, Inner Bound, and Outer Bound."""
    d = 100
    center_a = np.array([50, 0])
    center_b = np.array([150, 0])
    
    # Radii: [True, Inner, Outer]
    R_vals = [50, 42, 58]
    rho_vals = [20, 12, 28]
    
    paths = []
    for R, rho in zip(R_vals, rho_vals):
        alpha = np.arcsin((R - rho) / d)
        
        # Arcs
        theta_l = np.linspace(np.pi/2 + alpha, 1.5*np.pi - alpha, steps//3)
        x_l, y_l = center_a[0] + R * np.cos(theta_l), center_a[1] + R * np.sin(theta_l)
        
        theta_r = np.linspace(-np.pi/2 + alpha, np.pi/2 - alpha, steps//3)
        x_r, y_r = center_b[0] + rho * np.cos(theta_r), center_b[1] + rho * np.sin(theta_r)
        
        # Straights
        x_btm = np.linspace(x_l[-1], x_r[0], steps//6)
        y_btm = np.linspace(y_l[-1], y_r[0], steps//6)
        x_top = np.linspace(x_r[-1], x_l[0], steps//6)
        y_top = np.linspace(y_r[-1], y_l[0], steps//6)
        
        paths.append((np.concatenate([x_l, x_btm, x_r, x_top]), 
                      np.concatenate([y_l, y_btm, y_r, y_top])))
    return paths

def measure_beacons(true_states, beacons, noise_std=1.5):
    """Returns array of shape (steps, num_beacons)."""
    measurements = []
    for state in true_states:
        z_t = [np.sqrt((state[0]-b[0])**2 + (state[1]-b[1])**2) + np.random.normal(0, noise_std) for b in beacons]
        measurements.append(z_t)
    return np.array(measurements)
