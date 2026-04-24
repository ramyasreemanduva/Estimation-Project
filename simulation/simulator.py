import numpy as np

def get_track_geometry(steps, dt=0.01):
    # ELE8101 Specs (Modified to R=50, r=46 as requested)
    R_outer = 50  
    r_inner = 46   
    rho_mid = 20   
    d = 100        
    
    R_center = (R_outer + r_inner) / 2  # Centerline at 48m
    rho_outer = rho_mid + 2
    rho_inner = rho_mid - 2
    
    center_a = np.array([R_outer, 0]) 
    center_b = np.array([R_outer + d, 0]) 

    def generate_path_coords(R, rho, total_steps):
        alpha = np.arcsin((R - rho) / d)
        # Segments for clockwise motion 
        # Top Straight
        theta_start = np.pi/2 + alpha
        theta_end = np.pi/2 - alpha
        
        # Right Arc (B)
        theta_r = np.linspace(np.pi/2 - alpha, -np.pi/2 + alpha, total_steps // 3)
        x_r = center_b[0] + rho * np.cos(theta_r)
        y_r = center_b[1] + rho * np.sin(theta_r)
        
        # Left Arc (A)
        theta_l = np.linspace(1.5*np.pi - alpha, 0.5*np.pi + alpha, total_steps // 3)
        x_l = center_a[0] + R * np.cos(theta_l)
        y_l = center_a[1] + R * np.sin(theta_l)
        
        # Connecting Straights
        x_btm = np.linspace(x_r[-1], x_l[0], total_steps // 6)
        y_btm = np.linspace(y_r[-1], y_l[0], total_steps // 6)
        x_top = np.linspace(x_l[-1], x_r[0], total_steps // 6)
        y_top = np.linspace(y_l[-1], y_r[0], total_steps // 6)
        
        return np.concatenate([x_top, x_r, x_btm, x_l]), \
               np.concatenate([y_top, y_r, y_btm, y_l])

    return generate_path_coords(R_center, rho_mid, steps), \
           generate_path_coords(r_inner, rho_inner, steps), \
           generate_path_coords(R_outer, rho_outer, steps)

def measure_beacons(true_states, beacons, noise_std=1.5):
    measurements = []
    for state in true_states:
        # Distance measurement with 1.5m std dev
        z_t = [np.sqrt((state[0]-b[0])**2 + (state[1]-b[1])**2) + np.random.normal(0, noise_std) for b in beacons]
        measurements.append(z_t)
    return np.array(measurements)
