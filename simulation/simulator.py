import numpy as np

def get_track_geometry(dt=0.01):
    # Parameters: R=50, r=46 (Width=4m), rho=20, d=100
    R_out, r_in, rho_mid, d = 50, 46, 20, 100
    R_mid = (R_out + r_in) / 2 # 48m centerline
    
    alpha = np.arcsin((R_mid - rho_mid) / d)
    A = np.array([R_out, 0])
    B = np.array([R_out + d, 0])
    
    # Locked target velocity for smooth physics
    v_target = 10.0 
    ds = v_target * dt

    def generate_continuous_path(R_val, rho_val):
        # The correct arc sizes: Large circle A is smaller than a half circle, B is larger
        len_arc_A = (np.pi - 2*alpha) * R_val
        len_arc_B = (np.pi + 2*alpha) * rho_val
        len_str = np.sqrt(d**2 - (R_val - rho_val)**2)
        total_len = len_arc_A + len_arc_B + (2 * len_str)
        
        path = []
        dist = 0
        while dist < total_len:
            if dist < len_arc_A: 
                theta = (np.pi/2 + alpha) + (dist / R_val)
                x, y = A[0] + R_val * np.cos(theta), A[1] + R_val * np.sin(theta)
                vx, vy = -v_target * np.sin(theta), v_target * np.cos(theta)
            elif dist < (len_arc_A + len_str): 
                s = (dist - len_arc_A) / len_str
                p1 = A + R_val * np.array([np.cos(1.5*np.pi - alpha), np.sin(1.5*np.pi - alpha)])
                p2 = B + rho_val * np.array([np.cos(1.5*np.pi - alpha), np.sin(1.5*np.pi - alpha)])
                pos = p1 + s * (p2 - p1)
                x, y, vx, vy = pos[0], pos[1], v_target * np.cos(-alpha), v_target * np.sin(-alpha)
            elif dist < (len_arc_A + len_str + len_arc_B): 
                s_arc = dist - (len_arc_A + len_str)
                theta = (1.5*np.pi - alpha) + (s_arc / rho_val)
                x, y = B[0] + rho_val * np.cos(theta), B[1] + rho_val * np.sin(theta)
                vx, vy = -v_target * np.sin(theta), v_target * np.cos(theta)
            else: 
                s = (dist - (len_arc_A + len_str + len_arc_B)) / len_str
                p1 = B + rho_val * np.array([np.cos(0.5*np.pi + alpha), np.sin(0.5*np.pi + alpha)])
                p2 = A + R_val * np.array([np.cos(0.5*np.pi + alpha), np.sin(0.5*np.pi + alpha)])
                pos = p1 + s * (p2 - p1)
                x, y, vx, vy = pos[0], pos[1], -v_target * np.cos(alpha), -v_target * np.sin(alpha)
            
            path.append([x, y, vx, vy])
            dist += ds
        return np.array(path)

    def get_synced_bounds(Rv, rhov):
        al_bound = np.arcsin((Rv - rhov) / d)
        tl = np.linspace(0.5*np.pi + al_bound, 1.5*np.pi - al_bound, 100)
        tr = np.linspace(1.5*np.pi - al_bound, 2.5*np.pi + al_bound, 100)
        
        x_l, y_l = A[0] + Rv*np.cos(tl), A[1] + Rv*np.sin(tl)
        x_r, y_r = B[0] + rhov*np.cos(tr), B[1] + rhov*np.sin(tr)
        
        return np.concatenate([x_l, [x_r[0]], x_r, [x_l[0]]]), \
               np.concatenate([y_l, [y_r[0]], y_r, [y_l[0]]])

    return generate_continuous_path(R_mid, rho_mid), get_synced_bounds(r_in, 18), get_synced_bounds(R_out, 22)

def measure_beacons(states, beacons):
    return np.array([[np.sqrt((s[0]-b[0])**2 + (s[1]-b[1])**2) + np.random.normal(0, 1.5) for b in beacons] for s in states])
