import numpy as np

from models.dynamics import F_2D, apply_constraints
from filters.kalman_filter import kf_step
from simulation.simulator import simulate_2D, measure_2D
from plots.plot_results import plot_trajectory

# CONFIG
dt = 0.1
steps = 200

# SIMULATION
true_states = simulate_2D(steps, dt)
measurements = measure_2D(true_states)

# MODEL
A = F_2D(dt)

H = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0]
])

Q = np.eye(4) * 0.1
R_mat = np.eye(2) * (1.5**2)

# INITIAL STATE
x_est = np.array([0, 0, 8, 0])
P = np.eye(4)

estimates = []

# RUN KF
for k in range(steps):
    x_est, P = kf_step(x_est, P, measurements[k], A, H, Q, R_mat)

    # Apply constraint to estimate
    x_est[1] = apply_constraints(x_est[1])

    estimates.append(x_est.copy())

estimates = np.array(estimates)

# OUTPUT
print("Final estimated state:", x_est)

# PLOT
plot_trajectory(true_states, estimates)
