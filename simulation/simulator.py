import numpy as np

def get_track_geometry(steps, dt=0.01):
    # R=50, r=46 per user request (Track width 4m) [cite: 14]
    R_out, r_in, rho, d = 50, 46, 20, 100
    R_mid = (R_out + r_in) / 2 
    center_a, center_b = np.array([50, 0]), np.array([150, 0])

    def gen_path(R, r_s, n_steps):
        # Clockwise logic 
        t_r = np.linspace(np.pi/2, -np.pi/2, n_steps // 3)
        x_r, y_r = center_b[0] + r_s * np.cos(t_r), center_b[1] + r_s * np.sin(t_r)
        x_btm = np.linspace(x_r[-1], center_a[0], n_steps // 6)
        y_btm = np.full_like(x_btm, -R)
        t_l = np.linspace(1.5*np.pi, 0.5*np.pi, n_steps // 3)
        x_l, y_l = center_a[0] + R * np.cos(t_l), center_a[1] + R * np.sin(t_l)
        x_top = np.linspace(x_l[-1], x_r[0], n_steps // 6)
        y_top = np.full_like(x_top, R)
        return np.concatenate([x_top, x_r, x_btm, x_l]), np.concatenate([y_top, y_r, y_btm, y_l])

    return gen_path(R_mid, rho, steps), gen_path(r_in, rho-2, steps), gen_path(R_out, rho+2, steps)

def measure_beacons(states, beacons):
    # Sensor noise standard deviation 1.5m [cite: 19]
    return np.array([[np.sqrt((s[0]-b[0])**2 + (s[1]-b[1])**2) + np.random.normal(0, 1.5) for b in beacons] for s in states])
