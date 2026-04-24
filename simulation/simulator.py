import numpy as np

def get_track_geometry(dt=0.01):
    # Parameters: R=50, r=46 (4m lane), rho=20, d=100
    R_out, r_in, rho_mid, d = 50, 46, 20, 100
    R_mid = (R_out + r_in) / 2 
    
    # Tangent Angle alpha ensures smooth connection between arcs and straights
    alpha = np.arcsin((R_mid - rho_mid) / d)
    
    A = np.array([R_out, 0])
    B = np.array([R_out + d, 0])
    v_target = 10.0 
    ds = v_target * dt

    def generate_path(R_val, rho_val):
        len_arc_A = (np.pi + 2*alpha) * R_val
        len_arc_B = (np.pi - 2*alpha) * rho_val
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

    # Static boundaries for Figure 1 plotting
    def get_static_bounds(R_v, rho_v):
        tl = np.linspace(0.5*np.pi + alpha, 1.5*np.pi - alpha, 100)
        tr = np.linspace(1.5*np.pi - alpha, 2.5*np.pi + alpha, 100)
        return np.concatenate([A[0]+R_v*np.cos(tl), B[0]+rho_v*np.cos(tr)]), \
               np.concatenate([A[1]+R_v*np.sin(tl), B[1]+rho_v*np.sin(tr)])

    return generate_path(R_mid, rho_mid), get_static_bounds(r_in, 18), get_static_bounds(R_out, 22)

# THE MISSING FUNCTION
def measure_beacons(states, beacons):
    """Simulates range measurements with 1.5m noise."""
    return np.array([[np.sqrt((s[0]-b[0])**2 + (s[1]-b[1])**2) + np.random.normal(0, 1.5) for b in beacons] for s in states])
