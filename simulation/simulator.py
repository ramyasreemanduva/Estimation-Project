import numpy as np


def get_track_geometry(steps=5000):
    # Parameters provided by user
    R, r, rho, d = 50, 46, 20, 100
    R_center = (R + r) / 2  # Centerline radius = 48m
    
    # Centers A and B
    A = np.array([50, 0])
    B = np.array([150, 0])
    
    # Calculate Tangent Angle (alpha)
    alpha = np.arcsin((R_center - rho) / d)

    def generate_path(R_val, rho_val, n_total):
        # Proportional step distribution based on segment lengths
        n = n_total // 4
        
        # 1. Left Arc (Large turn around A) - Clockwise
        # From Top Tangent to Bottom Tangent
        theta_l = np.linspace(np.pi/2 + alpha, 1.5*np.pi - alpha, n*2)
        x_l = A[0] + R_val * np.cos(theta_l)
        y_l = A[1] + R_val * np.sin(theta_l)
        
        # 2. Bottom Straight (Connecting A to B)
        x_btm = np.linspace(x_l[-1], B[0] + rho_val * np.cos(1.5*np.pi - alpha), n)
        y_btm = np.linspace(y_l[-1], B[1] + rho_val * np.sin(1.5*np.pi - alpha), n)
        
        # 3. Right Arc (Small turn around B) - Clockwise
        theta_r = np.linspace(1.5*np.pi - alpha, 2.5*np.pi + alpha, n)
        x_r = B[0] + rho_val * np.cos(theta_r)
        y_r = B[1] + rho_val * np.sin(theta_r)
        
        # 4. Top Straight (Connecting B back to A)
        x_top = np.linspace(x_r[-1], x_l[0], n)
        y_top = np.linspace(y_r[-1], y_l[0], n)
        
        return np.concatenate([x_l, x_btm, x_r, x_top]), \
               np.concatenate([y_l, y_btm, y_r, y_top])

    # Generate the three paths for visualization and validation
    centerline = generate_path(R_center, rho, steps)
    inner_bound = generate_path(r, rho - 2, steps) # Lane width 4m [cite: 14]
    outer_bound = generate_path(R, rho + 2, steps)
    
    return centerline, inner_bound, outer_bound

def measure_beacons(states, beacons):
    return np.array([[np.sqrt((s[0]-b[0])**2 + (s[1]-b[1])**2) + np.random.normal(0, 1.5) for b in beacons] for s in states])
