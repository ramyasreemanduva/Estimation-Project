def simulate_2D(steps, dt):

    R = 50
    d = 100
    v = 10

    data = []

    # Total segments
    segments = [
        "left_curve",
        "top_straight",
        "right_curve",
        "bottom_straight"
    ]

    theta = np.pi/2

    x, y = -d/2, 0

    for k in range(steps):

        seg = k % 4

        if seg == 0:  # left curve
            x = -d/2 + R * np.cos(theta)
            y = R * np.sin(theta)

            vx = -v * np.sin(theta)
            vy = v * np.cos(theta)

            theta -= v / R * dt

        elif seg == 1:  # top straight
            x += v * dt
            vx = v
            vy = 0

        elif seg == 2:  # right curve
            x = d/2 + R * np.cos(theta)
            y = R * np.sin(theta)

            vx = -v * np.sin(theta)
            vy = v * np.cos(theta)

            theta -= v / R * dt

        else:  # bottom straight
            x -= v * dt
            vx = -v
            vy = 0

        data.append([x, y, vx, vy])

    return np.array(data)
