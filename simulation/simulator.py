import numpy as np

def get_track_geometry(steps, dt=0.01):
    # ELE8101 Specs: R=50, r=46 (Width = 4m)
    R_out, r_in, rho_mid, d = 50, 46, 20, 100
    R_mid = (R_out + r_in) / 2 # Centerline (48m)
    
    A = np.array([50, 0])
    B = np.array([150, 0])

    def gen_loop(R_val, rho_val, total_steps):
        # Divide steps to maintain constant velocity
        s = total_steps // 4
        
        # 1. Top Straight (B to A)
        x_top = np.linspace(B[0], A[0], s)
        y_top = np.full_like(x_top, R_val)
        
        # 2. Left Arc (A) - Clockwise from 90 to 270 degrees
        t_l = np.linspace(np.pi/2, 1.5*np.pi, s)
        x_l = A[0] + R_val * np.cos(t_l)
        y_l = A[1] + R_val * np.sin(t_l)
        
        # 3. Bottom Straight (A to B)
        x_btm = np.linspace(A[0], B[0], s)
        y_btm = np.full_like(x_btm, -R_val)
        
        # 4. Right Arc (B) - Clockwise from 270 to 90 degrees
        # Note: Must use rho_val to match geometry
        t_r = np.linspace(1.5*np.pi, 2.5*np.pi, s)
        x_r = B[0] + rho_val * np.cos(t_r)
        y_r = B[1] + rho_val * np.sin(t_r)
        
        return np.concatenate([x_top, x_l, x_btm, x_r]), np.concatenate([y_top, y_l, y_btm, y_r])

    return gen_loop(R_mid, 20, steps), gen_loop(r_in, 18, steps), gen_loop(R_out, 22, steps)

def measure_beacons(states, beacons):
    # Standard deviation 1.5m 
    return np.array([[np.sqrt((s[0]-b[0])**2 + (s[1]-b[1])**2) + np.random.normal(0, 1.5) for b in beacons] for s in states])
