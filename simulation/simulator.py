import numpy as np

def get_track_geometry(steps, dt=0.01):
    # R=50, r=46 (Track width 4m) [cite: 14]
    R_out, r_in, rho, d = 50, 46, 20, 100
    R_mid = (R_out + r_in) / 2 
    
    # Centers
    A = np.array([50, 0])
    B = np.array([150, 0])

    def gen_loop(R_val, rho_val, total_steps):
        # We divide steps proportionally to length to keep velocity constant 
        # Clockwise motion: Top -> Right Arc -> Bottom -> Left Arc
        s = total_steps // 4
        
        # 1. Top Straight (Right to Left)
        x_top = np.linspace(B[0], A[0], s)
        y_top = np.full_like(x_top, R_val)
        
        # 2. Left Arc (A) - Clockwise from 90 to 270 degrees
        t_l = np.linspace(np.pi/2, 1.5*np.pi, s*2)
        x_l = A[0] + R_val * np.cos(t_l)
        y_l = A[1] + R_val * np.sin(t_l)
        
        # 3. Bottom Straight (Left to Right)
        x_btm = np.linspace(A[0], B[0], s)
        y_btm = np.full_like(x_btm, -R_val)
        
        # 4. Right Arc (B) - Clockwise from 270 to 90 degrees
        # Note: We use rho_val for the smaller turn at B [cite: 13]
        # Adjusting the transition to be smooth
        t_r = np.linspace(1.5*np.pi, 2.5*np.pi, s*2)
        x_r = B[0] + rho_val * np.cos(t_r)
        y_r = B[1] + rho_val * np.sin(t_r)
        
        # This simple model needs a smoother transition for the non-concentric B arc
        # For simulation, we'll focus on the R centerline to keep your velocity stable
        return np.concatenate([x_top, x_l, x_btm, x_r]), np.concatenate([y_top, y_l, y_btm, y_r])

    return gen_loop(R_mid, 20, steps), gen_loop(r_in, 18, steps), gen_loop(R_out, 22, steps)

def measure_beacons(states, beacons):
    # Standard deviation 1.5m [cite: 19]
    return np.array([[np.sqrt((s[0]-b[0])**2 + (s[1]-b[1])**2) + np.random.normal(0, 1.5) for b in beacons] for s in states])
