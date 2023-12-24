# From https://www.a1k0n.net/2011/07/20/donut-math.html

from math import cos, sin, pi


# Screen constants
screen_width = 35
screen_height = 35
frames = 300

# Shape constants
R1 = 1  # Radius of circle
R2 = 2  # Radius of rotation
K2 = 5  # Distance of object from eye
K1 = screen_width * K2 * 3 / (8 * (R1 + R2))  # Distance of eye from screen

# Increments
theta_spacing = 0.07
phi_spacing = 0.02
a_spacing = 0.08
b_spacing = 0.03

# A and B rotate the x and z axes respectively
A = B = 1

# Clear screen and return cursor to home position
print("\x1b[2J")

# Main loop
for i in range(frames):
    # Reset output and zbuffer
    output = [[" "] * screen_width for _ in range(screen_height)]
    zbuffer = [[0] * screen_width for _ in range(screen_height)]

    cosB, sinB = cos(B), sin(B)
    cosA, sinA = cos(A), sin(A)

    # Theta rotates the point to form a circle of points
    theta = 0
    while theta < 2 * pi:
        theta += theta_spacing

        costheta, sintheta = cos(theta), sin(theta)

        # Phi rotates the circle of points around the y axis (in a circle)
        # to form a torus of points (the donut)
        phi = 0
        while phi < 2 * pi:
            phi += phi_spacing

            cosphi, sinphi = cos(phi), sin(phi)

            # Point of 2D circle
            circlex = R2 + R1 * costheta
            circley = R1 * sintheta

            # Point rotated on y axis (phi), x axis(A), z axis (B)
            x = circlex * (cosB * cosphi + sinA * sinB * sinphi) - circley * cosA * sinB
            y = circlex * (sinB * cosphi - sinA * cosB * sinphi) + circley * cosA * cosB
            z = cosA * circlex * sinphi + circley * sinA
            ooz = 1 / (z + K2)

            # Add 1/2 screen since projection is centered at (0, 0)
            # and the eye is also at (0, 0)
            xp = int(screen_width / 2 + K1 * x * ooz)
            yp = int(screen_height / 2 - K1 * y * ooz)

            # Luminance, calculated with normal_y - normal_z
            # since light source is at (0, 1, -1)
            L = (
                cosphi * costheta * sinB
                - cosA * costheta * sinphi
                - sinA * sintheta
                + cosB * (cosA * sintheta - costheta * sinA * sinphi)
            )

            # L ranges from -sqrt(2) to +sqrt(2)
            # Don't plot if L < 0 as it is shining away from eye
            if L > 0:
                # Check in z-buffer if there a pixel closer to the eye, with smaller z
                if ooz > zbuffer[xp][yp]:
                    zbuffer[xp][yp] = ooz
                    luminance_index = (
                        L * 8
                    )  # L is not in the range 0..11 (8*sqrt(2) = 11.3)

                    # Plot corresponding luminance
                    output[xp][yp] = ".,-~:;=!*#$@"[int(luminance_index)]

    # Return cursor to home position
    print("\x1b[H")

    # Print output matrix
    print("\n".join("".join(output[i]) for i in range(screen_height)))

    # A and B are incremented together
    # so the torus rotates around the x and z axes together
    A += a_spacing
    B += b_spacing
