import numpy as np

def get_track_geometry(dt=0.01):
    # Parameters for R=50, r=46 (Coursework width = 4m)
    R_out, r_in, rho_mid, d = 50, 46, 20, 100
    R_mid = (R_out + r_in) / 2 # 48m centerline
    v_target = 10.0 # Target longitudinal velocity 
    ds = v_target * dt # Distance per step
    
    A, B = np.array([50, 0]), np.array([150, 0])
    states = []
    curr_dist = 0
    total_len = (2 * d) + (np.pi * R_mid) + (np.pi * rho_mid)
    
    while curr_dist < total_len:
        if curr_dist < d: # Top Straight (Moving Clockwise)
            x, y = 150 - curr_dist, R_mid
            vx, vy = -v_target, 0
        elif curr_dist < (d + np.pi * R_mid): # Left Arc (Center A)
            s_arc = curr_dist - d
            theta = np.pi/2 + (s_arc / R_mid)
            x, y = A[0] + R_mid * np.cos(theta), A[1] + R_mid * np.sin(theta)
            vx, vy = -v_target * np.sin(theta), v_target * np.cos(theta)
        elif curr_dist < (2*d + np.pi * R_mid): # Bottom Straight
            s_str = curr_dist - (d + np.pi * R_mid)
            x, y = 50 + s_str, -R_mid
            vx, vy = v_target, 0
        else: # Right Arc (Center B)
            s_arc = curr_dist - (2*d + np.pi * R_mid)
            theta = 1.5*np.pi + (s_arc / rho_mid)
            x, y = B[0] + rho_mid * np.cos(theta), B[1] + rho_mid * np.sin(theta)
            vx, vy = -v_target * np.sin(theta), v_target * np.cos(theta)
            
        states.append([x, y, vx, vy])
        curr_dist += ds
        
    def gen_bound(R_val, rho_val):
        t_l = np.linspace(0.5*np.pi, 1.5*np.pi, 100)
        t_r = np.linspace(1.5*np.pi, 2.5*np.pi, 100)
        return np.concatenate([np.linspace(150, 50, 50), 50+R_val*np.cos(t_l), 
                               np.linspace(50, 150, 50), 150+rho_val*np.cos(t_r)]), \
               np.concatenate([np.full(50, R_val), R_val*np.sin(t_l), 
                               np.full(50, -R_val), rho_val*np.sin(t_r)])

    return np.array(states), gen_bound(r_in, 18), gen_bound(R_out, 22)

def measure_beacons(states, beacons):
    return np.array([[np.sqrt((s[0]-b[0])**2 + (s[1]-b[1])**2) + np.random.normal(0, 1.5) for b in beacons] for s in states])
