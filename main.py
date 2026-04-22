import numpy as np

from models.dynamics import F_1D, H_1D
from filters.kalman_filter import kf_step
from plots.plot_results import plot_position, plot_velocity

# CONFIG

dt = 0.1
steps = 100

# TRUE SYSTEM

x_true = []
x, v = 0, 10

for _ in range(steps):
    x += v * dt
    x_true.append([x, v])

x_true = np.array(x_true)

# MEASUREMENTS (NOISE)

z = x_true[:, 0] + np.random.randn(steps) * 1.5

# MODEL

A = F_1D(dt)
print("A =", A)
print("Type of A =", type(A))
print("Shape of A =", np.shape(A))
H = H_1D()

Q = np.eye(2) * 0.1
R = np.array([[1.5**2]])


# INITIAL STATE

x_est = np.array([0, 8])
P = np.eye(2)

estimates = []

# RUN KF

for k in range(steps):
    x_est, P = kf_step(x_est, P, z[k], A, H, Q, R)
    estimates.append(x_est.copy())

estimates = np.array(estimates)

# OUTPUT (TERMINAL)

print("Final estimated state:", x_est)

# OUTPUT (PLOTS)

plot_position(x_true, estimates)
plot_velocity(x_true, estimates)
