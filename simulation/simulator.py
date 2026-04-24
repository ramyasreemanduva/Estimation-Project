import numpy as np

def get_track_geometry(dt=0.01):
    """
    Generates track and true states using a constant velocity stepping method.
    This prevents the velocity spikes seen in previous versions. 
    """
    R_out, r_in, rho_mid, d = 50, 46, 20, 100
    R_mid = (R_out + r_in) / 2 # 48m
    v_target = 10.0 # Target speed 
    ds = v_target * dt # Distance to move per step
    
    A, B = np.array([50, 0]), np.array([150, 0])
    
    states = []
    curr_dist = 0
    
    # Calculate Total Length of Centerline
    # 2 straights + 2 arcs
    total_len = (2 * d) + (np.pi * R_mid) + (np.pi * rho_mid)
    
    # Generate points by moving along the path at exactly 10 m/s
    while curr_dist < total_len:
        # Determine which segment we are in
        if curr_dist < d: # Top Straight
            x, y = B[0] - curr_dist, R_mid
            vx, vy = -v_target, 0
        elif curr_dist < (d + np.pi * R_mid): # Left Arc
            s_arc = curr_dist - d
            theta = np.pi/2 + (s_arc / R_mid)
            x, y = A[0] + R_mid * np.cos(theta), A[1] + R_mid * np.sin(theta)
            vx, vy = -v_target * np.sin(theta), v_target * np.cos(theta)
        elif curr_dist < (2*d + np.pi * R_mid): # Bottom Straight
            s_str = curr_dist - (d + np.pi * R_mid)
            x, y = A[0] + s_str, -R_mid
            vx, vy = v_target, 0
        else: # Right Arc
            s_arc = curr_dist - (2*d + np.pi * R_mid)
            theta = 1.5*np.pi + (s_arc / rho_mid)
            x, y = B[0] + rho_mid * np.cos(theta), B[1] + rho_mid * np.sin(theta)
            vx, vy = -v_target * np.sin(theta), v_target * np.cos(theta)
            
        states.append([x, y, vx, vy])
        curr_dist += ds
        
    # Helper to generate boundary lines for plotting
    def gen_boundary(R_val, rho_val):
        t_l = np.linspace(0.5*np.pi, 1.5*np.pi, 100)
        t_r = np.linspace(1.5*np.pi, 2.5*np.pi, 100)
        return np.concatenate([np.linspace(150, 50, 50), 50+R_val*np.cos(t_l), 
                               np.linspace(50, 150, 50), 150+rho_val*np.cos(t_r)]), \
               np.concatenate([np.full(50, R_val), R_val*np.sin(t_l), 
                               np.full(50, -R_val), rho_val*np.sin(t_r)])

    return np.array(states), gen_boundary(r_in, 18), gen_boundary(R_out, 22)

def measure_beacons(states, beacons):
    # Sensor noise 1.5m standard deviation [cite: 19]
    return np.array([[np.sqrt((s[0]-b[0])**2 + (s[1]-b[1])**2) + np.random.normal(0, 1.5) for b in beacons] for s in states])
    
