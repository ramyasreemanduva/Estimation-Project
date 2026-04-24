import numpy as np

def get_track_geometry(steps, dt=0.1):
    """
    Generates the true trajectory, inner bound, and outer bound.
    """
    # Geometry Constants
    d = 100
    center_a = np.array([50, 0])
    center_b = np.array([150, 0])
    
    # Radii for: [True Path, Inner Bound, Outer Bound]
    # Adjust widths (5.0) to match your coursework visual preference
    R_vals = [50, 45, 55]    # Large circle radii
    rho_vals = [20, 15, 25]  # Small circle radii
    
    paths = []

    for R, rho in zip(R_vals, rho_vals):
        alpha = np.arcsin((R - rho) / d)
        
        # Left Arc
        theta_l = np.linspace(np.pi/2 + alpha, 1.5*np.pi - alpha, steps//3)
        x_l = center_a[0] + R * np.cos(theta_l)
        y_l = center_a[1] + R * np.sin(theta_l)
        
        # Right Arc
        theta_r = np.linspace(-np.pi/2 + alpha, np.pi/2 - alpha, steps//3)
        x_r = center_b[0] + rho * np.cos(theta_r)
        y_r = center_b[1] + rho * np.sin(theta_r)
        
        # Straights
        x_btm = np.linspace(x_left[-1], x_right[0], steps//6)
        y_btm = np.linspace(y_left[-1], y_right[0], steps//6)
        x_top = np.linspace(x_right[-1], x_left[0], steps//6)
        y_top = np.linspace(y_right[-1], y_left[0], steps//6)
        
        paths.append((np.concatenate([x_l, x_btm, x_r, x_top]), 
                      np.concatenate([y_l, y_btm, y_r, y_top])))

    # paths[0] is True, paths[1] is Inner, paths[2] is Outer
    return paths

def measure_beacons(state, beacons, noise_std=1.5):
    """Calculates noisy range measurements from the vehicle to beacons."""
    z = []
    for bx, by in beacons:
        dist = np.sqrt((state[0] - bx)**2 + (state[1] - by)**2)
        z.append(dist + np.random.normal(0, noise_std))
    return np.array(z)
