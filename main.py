import numpy as np

from models.dynamics import F_2D
from filters.kalman_filter import kf_step
from simulation.simulator import simulate_circular, measure_2D
from plots.plot_results import plot_trajectory

# CONFIG

dt = 0.1
steps = 200
R = 50
omega = 0.2

# SIMULATION

true_states = simulate_circular(steps, dt, R, omega)
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
x_est = np.array([R, 0, 0, 5])  # imperfect initial guess
P = np.eye(4)

estimates = []

# RUN KF
for k in range(steps):
    x_est, P = kf_step(x_est, P, measurements[k], A, H, Q, R_mat)
    estimates.append(x_est.copy())

estimates = np.array(estimates)

# OUTPUT

print("Final estimated state:", x_est)

# PLOT

plot_trajectory(true_states, estimates)
