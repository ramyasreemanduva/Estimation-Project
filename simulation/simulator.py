import numpy as np

import numpy as np

def get_track_geometry(dt=0.01):
    # Parameters for R=50, r=46 logic
    R_out, r_in, rho_mid, d = 50, 46, 20, 100
    R_mid = (R_out + r_in) / 2 # Centerline at 48m
    
    # Tangent Angle: alpha = arcsin((R-rho)/d)
    alpha = np.arcsin((R_mid - rho_mid) / d)
    
    A = np.array([R_out, 0])    # Center A [cite: 38]
    B = np.array([R_out + d, 0]) # Center B [cite: 38]
    v_target = 10.0 # Target velocity 
    ds = v_target * dt

    # Exact segment lengths
    len_arc_A = (np.pi + 2*alpha) * R_mid
    len_arc_B = (np.pi - 2*alpha) * rho_mid
    len_str = np.sqrt(d**2 - (R_mid - rho_mid)**2)
    total_len = len_arc_A + len_arc_B + (2 * len_str)
    
    states = []
    dist = 0
    while dist < total_len:
        if dist < len_arc_A: # Left Arc
            theta = (np.pi/2 + alpha) + (dist / R_mid)
            x, y = A[0] + R_mid * np.cos(theta), A[1] + R_mid * np.sin(theta)
            vx, vy = -v_target * np.sin(theta), v_target * np.cos(theta)
        elif dist < (len_arc_A + len_str): # Bottom Straight
            s = (dist - len_arc_A) / len_str
            p1 = A + R_mid * np.array([np.cos(1.5*np.pi - alpha), np.sin(1.5*np.pi - alpha)])
            p2 = B + rho_mid * np.array([np.cos(1.5*np.pi - alpha), np.sin(1.5*np.pi - alpha)])
            pos = p1 + s * (p2 - p1)
            vx, vy = v_target * np.cos(-alpha), v_target * np.sin(-alpha)
            x, y = pos[0], pos[1]
        elif dist < (len_arc_A + len_str + len_arc_B): # Right Arc
            s_arc = dist - (len_arc_A + len_str)
            theta = (1.5*np.pi - alpha) + (s_arc / rho_mid)
            x, y = B[0] + rho_mid * np.cos(theta), B[1] + rho_mid * np.sin(theta)
            vx, vy = -v_target * np.sin(theta), v_target * np.cos(theta)
        else: # Top Straight
            s = (dist - (len_arc_A + len_str + len_arc_B)) / len_str
            p1 = B + rho_mid * np.array([np.cos(0.5*np.pi + alpha), np.sin(0.5*np.pi + alpha)])
            p2 = A + R_mid * np.array([np.cos(0.5*np.pi + alpha), np.sin(0.5*np.pi + alpha)])
            pos = p1 + s * (p2 - p1)
            vx, vy = -v_target * np.cos(alpha), -v_target * np.sin(alpha)
            x, y = pos[0], pos[1]
            
        states.append([x, y, vx, vy])
        dist += ds
        
    return np.array(states)
    # Static boundaries for plotting Figure 1 [cite: 18]
    def get_bounds(R_v, rho_v):
        t_l = np.linspace(0.5*np.pi + alpha, 1.5*np.pi - alpha, 100)
        t_r = np.linspace(1.5*np.pi - alpha, 2.5*np.pi + alpha, 100)
        return np.concatenate([A[0]+R_v*np.cos(t_l), B[0]+rho_v*np.cos(t_r)]), \
               np.concatenate([A[1]+R_v*np.sin(t_l), B[1]+rho_v*np.sin(t_r)])

    return generate_full_path(R_mid, rho_mid), get_bounds(r_in, 18), get_bounds(R_out, 22)

def measure_beacons(states, beacons):
    # Standard deviation 1.5m as per datasheet [cite: 19]
    return np.array([[np.sqrt((s[0]-b[0])**2 + (s[1]-b[1])**2) + np.random.normal(0, 1.5) for b in beacons] for s in states])
