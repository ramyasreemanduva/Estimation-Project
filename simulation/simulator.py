import numpy as np

def get_track_geometry(dt=0.01):
    # Project Parameters: R=50, r=46, rho=20, d=100
    R_out, r_in, rho_mid, d = 50, 46, 20, 100
    R_mid = (R_out + r_in) / 2 # Centerline 48m
    
    # Tangent Angle: alpha = arcsin((R_mid - rho_mid) / d)
    # This angle is where the straight line leaves the circle
    alpha = np.arcsin((R_mid - rho_mid) / d)
    
    A = np.array([R_out, 0])    # Center of left arc
    B = np.array([R_out + d, 0]) # Center of right arc
    v_target = 10.0 # Target speed
    ds = v_target * dt

    def generate_path(R_val, rho_val):
        # Calculate precise segment lengths
        len_arc_A = (np.pi + 2*alpha) * R_val
        len_arc_B = (np.pi - 2*alpha) * rho_val
        len_str = np.sqrt(d**2 - (R_val - rho_val)**2)
        total_len = len_arc_A + len_arc_B + (2 * len_str)
        
        path = []
        dist = 0
        while dist < total_len:
            if dist < len_arc_A: # Left Circular Arc
                theta = (np.pi/2 + alpha) + (dist / R_val)
                x, y = A[0] + R_val * np.cos(theta), A[1] + R_val * np.sin(theta)
                vx, vy = -v_target * np.sin(theta), v_target * np.cos(theta)
            elif dist < (len_arc_A + len_str): # Bottom Tangent Straight
                s = (dist - len_arc_A) / len_str
                p1 = A + R_val * np.array([np.cos(1.5*np.pi - alpha), np.sin(1.5*np.pi - alpha)])
                p2 = B + rho_val * np.array([np.cos(1.5*np.pi - alpha), np.sin(1.5*np.pi - alpha)])
                pos = p1 + s * (p2 - p1)
                x, y, vx, vy = pos[0], pos[1], v_target * np.cos(-alpha), v_target * np.sin(-alpha)
            elif dist < (len_arc_A + len_str + len_arc_B): # Right Circular Arc
                s_arc = dist - (len_arc_A + len_str)
                theta = (1.5*np.pi - alpha) + (s_arc / rho_val)
                x, y = B[0] + rho_val * np.cos(theta), B[1] + rho_val * np.sin(theta)
                vx, vy = -v_target * np.sin(theta), v_target * np.cos(theta)
            else: # Top Tangent Straight
                s = (dist - (len_arc_A + len_str + len_arc_B)) / len_str
                p1 = B + rho_val * np.array([np.cos(0.5*np.pi + alpha), np.sin(0.5*np.pi + alpha)])
                p2 = A + R_val * np.array([np.cos(0.5*np.pi + alpha), np.sin(0.5*np.pi + alpha)])
                pos = p1 + s * (p2 - p1)
                x, y, vx, vy = pos[0], pos[1], -v_target * np.cos(alpha), -v_target * np.sin(alpha)
            path.append([x, y, vx, vy])
            dist += ds
        return np.array(path)

    # Static boundaries for visualization
    def get_bounds(Rv, rhov):
        tl = np.linspace(0.5*np.pi + alpha, 1.5*np.pi - alpha, 100)
        tr = np.linspace(1.5*np.pi - alpha, 2.5*np.pi + alpha, 100)
        return np.concatenate([A[0]+Rv*np.cos(tl), B[0]+rhov*np.cos(tr)]), \
               np.concatenate([A[1]+Rv*np.sin(tl), B[1]+rhov*np.sin(tr)])

    return generate_path(R_mid, rho_mid), get_bounds(r_in, 18), get_bounds(R_out, 22)

def measure_beacons(states, beacons):
    return np.array([[np.sqrt((s[0]-b[0])**2 + (s[1]-b[1])**2) + np.random.normal(0, 1.5) for b in beacons] for s in states])
