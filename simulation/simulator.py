import numpy as np

def get_track_geometry(dt=0.01):
    # Parameters from problem statement [cite: 13, 14]
    R_out, r_in, rho_mid, d = 50, 46, 20, 100
    R_mid = (R_out + r_in) / 2 # Centerline 
    
    # Calculate Tangent Angle alpha for smooth connectivity 
    alpha = np.arcsin((R_mid - rho_mid) / d)
    
    A = np.array([R_out, 0]) # Center A [cite: 31]
    B = np.array([R_out + d, 0]) # Center B [cite: 32]
    v_target = 10.0 # Target velocity around 10 m/s 
    ds = v_target * dt # Distance per step [cite: 20]

    def generate_full_path(R_val, rho_val):
        # Precise segment lengths to maintain 10 m/s 
        len_arc_A = (np.pi + 2*alpha) * R_val
        len_arc_B = (np.pi - 2*alpha) * rho_val
        len_str = np.sqrt(d**2 - (R_val - rho_val)**2)
        total_len = len_arc_A + len_arc_B + (2 * len_str)
        
        path = []
        dist = 0
        while dist < total_len:
            if dist < len_arc_A: # Left Arc [cite: 37]
                theta = (np.pi/2 + alpha) + (dist / R_val)
                x, y = A[0] + R_val * np.cos(theta), A[1] + R_val * np.sin(theta)
                vx, vy = -v_target * np.sin(theta), v_target * np.cos(theta)
            elif dist < (len_arc_A + len_str): # Bottom Straight 
                s = (dist - len_arc_A) / len_str
                p1 = A + R_val * np.array([np.cos(1.5*np.pi - alpha), np.sin(1.5*np.pi - alpha)])
                p2 = B + rho_val * np.array([np.cos(1.5*np.pi - alpha), np.sin(1.5*np.pi - alpha)])
                pos = p1 + s * (p2 - p1)
                vx, vy = v_target * np.cos(-alpha), v_target * np.sin(-alpha)
                x, y = pos[0], pos[1]
            elif dist < (len_arc_A + len_str + len_arc_B): # Right Arc [cite: 38]
                s_arc = dist - (len_arc_A + len_str)
                theta = (1.5*np.pi - alpha) + (s_arc / rho_val)
                x, y = B[0] + rho_val * np.cos(theta), B[1] + rho_val * np.sin(theta)
                vx, vy = -v_target * np.sin(theta), v_target * np.cos(theta)
            else: # Top Straight 
                s = (dist - (len_arc_A + len_str + len_arc_B)) / len_str
                p1 = B + rho_val * np.array([np.cos(0.5*np.pi + alpha), np.sin(0.5*np.pi + alpha)])
                p2 = A + R_val * np.array([np.cos(0.5*np.pi + alpha), np.sin(0.5*np.pi + alpha)])
                pos = p1 + s * (p2 - p1)
                vx, vy = -v_target * np.cos(alpha), -v_target * np.sin(alpha)
                x, y = pos[0], pos[1]
            path.append([x, y, vx, vy])
            dist += ds
        return np.array(path)

    # Static boundaries for Figure 1 visualization [cite: 14, 26]
    def get_bounds(R_v, rho_v):
        t_l = np.linspace(0.5*np.pi + alpha, 1.5*np.pi - alpha, 100)
        t_r = np.linspace(1.5*np.pi - alpha, 2.5*np.pi + alpha, 100)
        return np.concatenate([A[0]+R_v*np.cos(t_l), B[0]+rho_v*np.cos(t_r)]), \
               np.concatenate([A[1]+R_v*np.sin(t_l), B[1]+rho_v*np.sin(t_r)])

    return generate_full_path(R_mid, rho_mid), get_bounds(r_in, 18), get_bounds(R_out, 22)
