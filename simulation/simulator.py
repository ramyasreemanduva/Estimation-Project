import numpy as np

def get_track_geometry(steps, dt=0.01):
    # Parameters requested by user
    R_outer = 50   # Outer boundary
    r_inner = 46   # Inner boundary
    rho_mid = 20   # Center of the small arc [cite: 13]
    d = 100        # Distance between centers A and B [cite: 13]
    
    # Calculate centerline for the True Path
    R_center = (R_outer + r_inner) / 2  # 48m
    
    # Lane width is 4m, so bounds are +/- 2m from centerline 
    rho_outer = rho_mid + 2
    rho_inner = rho_mid - 2
    
    center_a = np.array([R_outer, 0]) 
    center_b = np.array([R_outer + d, 0]) 

    def generate_path_coords(R, rho, total_steps):
        alpha = np.arcsin((R - rho) / d)
        
        # Segment 1: Right Arc (Clockwise)
        theta_r = np.linspace(np.pi/2 - alpha, -np.pi/2 + alpha, total_steps // 3)
        x_r = center_b[0] + rho * np.cos(theta_r)
        y_r = center_b[1] + rho * np.sin(theta_r)
        
        # Segment 2: Bottom Straight
        x_btm = np.linspace(x_r[-1], center_a[0] + R * np.cos(1.5*np.pi - alpha), total_steps // 6)
        y_btm = np.linspace(y_r[-1], center_a[1] + R * np.sin(1.5*np.pi - alpha), total_steps // 6)
        
        # Segment 3: Left Arc (Clockwise)
        theta_l = np.linspace(1.5*np.pi - alpha, np.pi/2 + alpha, total_steps // 3)
        x_l = center_a[0] + R * np.cos(theta_l)
        y_l = center_a[1] + R * np.sin(theta_l)
        
        # Segment 4: Top Straight
        x_top = np.linspace(x_l[-1], x_r[0], total_steps // 6)
        y_top = np.linspace(y_l[-1], y_r[0], total_steps // 6)
        
        return np.concatenate([x_r, x_btm, x_l, x_top]), \
               np.concatenate([y_r, y_btm, y_l, y_top])

    true_x, true_y = generate_path_coords(R_center, rho_mid, steps)
    inner_x, inner_y = generate_path_coords(r_inner, rho_inner, steps)
    outer_x, outer_y = generate_path_coords(R_outer, rho_outer, steps)
    
    return (true_x, true_y), (inner_x, inner_y), (outer_x, outer_y)

def simulate_2D(steps, dt=0.01):
    (tx, ty), _, _ = get_track_geometry(steps, dt)
    vx = np.gradient(tx, dt)
    vy = np.gradient(ty, dt)
    return np.column_stack([tx, ty, vx, vy])

def measure_beacons(true_states, beacons, noise_std=1.5):
    measurements = []
    for state in true_states:
        # Standard deviation of 1.5m as per datasheet 
        z_t = [np.sqrt((state[0]-b[0])**2 + (state[1]-b[1])**2) + np.random.normal(0, noise_std) for b in beacons]
        measurements.append(z_t)
    return np.array(measurements)
