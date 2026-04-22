import numpy as np
 def circular_motion(theta, R):
    x = R * np.cos(theta)
    y = R * np.sin(theta)
    return x, y
