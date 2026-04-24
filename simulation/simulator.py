import numpy as np

def get_track_geometry(steps, dt=0.1):
    """
    Generates the true trajectory, inner bound, and outer bound.
    Returns: [True Path Tuple, Inner Bound Tuple, Outer Bound Tuple]
    """
    # Geometry Constants from your diagram
    d = 100
    center_a = np.array([50, 0])
    center_b = np.array([150, 0])
    
    # Radii for: [True Path, Inner Bound, Outer Bound]
    R_vals = [50, 40, 60]    # Large circle radii (Adjusted for clear bounds)
    rho_vals = [20, 10, 30]  # Small circle radii (Adjusted for clear bounds)
    
    paths = []

    for R, rho in zip(R_vals, rho_vals):
        # Angle where the tangent lines touch the circles
        alpha = np.arcsin((R - rho) / d)
        
        # ---------- LEFT ARC ----------
        theta_l = np.linspace(np.pi/2 + alpha, 1.5*np.pi - alpha, steps//3)
        x_l = center_a[0] + R * np.cos(theta_l)
        y_l = center_a[1] + R * np.sin(theta_l)
        
        # ---------- RIGHT ARC ----------
        theta_r = np.linspace(-np.pi/2 + alpha, np.pi/2 - alpha, steps//3)
        x_r = center_b[0] + rho * np.cos(theta_r)
        y_r = center_b[1] + rho * np.sin(theta_r)
        
        # ---------- CONNECTING STRAIGHTS ----------
        # Bottom straight (end of left arc to start of right arc)
        x_btm = np.linspace(x_l[-1], x_r[0], steps//6)
        y_btm = np.linspace(y_l[-1], y_r[0], steps//6)
        
        # Top straight (end of right arc to start of left arc)
        x_top = np.linspace(x_r[-1], x_l[0], steps//6)
        y_top = np.linspace(y_r[-1], y_l[0], steps//6)
        
        # Combine all segments for this specific boundary
        full_x = np.concatenate([x_l, x_btm, x_r, x_top])
        full_y = np.concatenate([y_l, y_btm, y_r, y_top])
        
        paths.append((full_x, full_y))

    return paths

def measure_beacons(state, beacons, noise_std=1.5):
    """Calculates noisy range measurements from the vehicle to beacons."""
    z = []
    for bx, by in beacons:
        # state[0] is x, state[1] is y
        dist = np.sqrt((state[0] - bx)**2 + (state[1] - by)**2)
        z.append(dist + np.random.normal(0, noise_std))
    return np.array(z)
