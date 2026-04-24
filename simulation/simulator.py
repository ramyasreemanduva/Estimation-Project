import numpy as np

def get_track_geometry(dt=0.01):
    # Parameters for R=50, r=46 per your request
    R_outer, r_inner, rho_mid, d = 50, 46, 20, 100
    R_center = (R_outer + r_inner) / 2 # 48m centerline
    
    # Calculate Track Length to fix Velocity
    # Full lap = Left Arc + Right Arc + 2 * Straights
    arc_l = np.pi * R_center
    arc_r = np.pi * rho_mid
    total_length = arc_l + arc_r + (2 * d)
    
    # To maintain 10 m/s: total_length / (steps * dt) = 10
    # steps = total_length / (10 * dt)
    steps = int(total_length / (10 * dt))
    
    center_a = np.array([R_outer, 0]) 
    center_b = np.array([R_outer + d, 0]) 

    def generate_path(R, rho, num_steps):
        alpha = np.arcsin((R - rho) / d)
        
        # Segment 1: Right Arc (Clockwise)
        t_r = np.linspace(np.pi/2 - alpha, -np.pi/2 + alpha, num_steps // 3)
        x_r, y_r = center_b[0] + rho * np.cos(t_r), center_b[1] + rho * np.sin(t_r)
        
        # Segment 2: Bottom Straight
        x_btm = np.linspace(x_r[-1], center_a[0], num_steps // 6)
        y_btm = np.linspace(y_r[-1], -R, num_steps // 6)
        
        # Segment 3: Left Arc (Clockwise)
        t_l = np.linspace(1.5*np.pi, 0.5*np.pi, num_steps // 3)
        x_l, y_l = center_a[0] + R * np.cos(t_l), center_a[1] + R * np.sin(t_l)
        
        # Segment 4: Top Straight
        x_top = np.linspace(x_l[-1], x_r[0], num_steps // 6)
        y_top = np.linspace(y_l[-1], y_r[0], num_steps // 6)
        
        return np.concatenate([x_top, x_r, x_btm, x_l]), \
               np.concatenate([y_top, y_r, y_btm, y_l])

    return generate_path(R_center, rho_mid, steps), \
           generate_path(r_inner, rho_mid - 2, steps), \
           generate_path(R_outer, rho_mid + 2, steps)

def measure_beacons(true_states, beacons, noise_std=1.5):
    # Standard deviation of 1.5m 
    return np.array([[np.sqrt((s[0]-b[0])**2 + (s[1]-b[1])**2) + 
                      np.random.normal(0, noise_std) for b in beacons] for s in true_states])
