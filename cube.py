from math import cos, sin


### Zoom out if animation is flickering ###

# Screen constants
screen_width = 150
screen_height = 150
frames = 3000

# Shape constants
R1 = 1  # Radius of circle
R2 = 2  # Radius of rotation
K2 = 5  # Distance of object from eye
K1 = screen_width * K2 * 3 / (8 * (R1 + R2))  # Distance of eye from screen

L = 1.5  # Cube length

# Increments
l_spacing = 0.07
phi_spacing = 0.02
a_spacing = 0.08
b_spacing = 0.03

# A, B and phi rotate the x, z and y axes respectively
A = B = phi = 1

# Clear screen and return cursor to home position
print("\x1b[2J")

# Main loop
for i in range(frames):
    # Reset output and zbuffer
    output = [[" "] * screen_width for _ in range(screen_height)]
    zbuffer = [[0] * screen_width for _ in range(screen_height)]

    cosB, sinB = cos(B), sin(B)
    cosA, sinA = cos(A), sin(A)
    cosphi, sinphi = cos(phi), sin(phi)

    # Width, centred at (0, 0)
    w = -L / 2
    while w < L / 2:
        w += l_spacing

        # Length, centred at (0, 0)
        l = -L / 2
        while l < L / 2:
            l += l_spacing

            # Height, centred at (0, 0)
            h = -L / 2
            while h < L / 2:
                h += l_spacing

                # Point of 3D cube
                cubex = w
                cubey = l
                cubez = h

                # Point = [cosB(xcosphi-zsinphi) - sinB(ycosA-sinA*(xsinphi+zcosphi),
                #          sinB(xcosphi-zsinphi) + cosB(ycosA-sinA*(xsinphi+zcosphi),
                #          ysinA+cosA(xsinphi+zcosphi)]

                # Point rotated on y axis (phi), x axis(A), z axis (B)
                x = cosB * (cubex * cosphi - cubez * sinphi) - sinB * (
                    cubey * cosA - sinA * (cubex * sinphi + cubez * cosphi)
                )
                y = sinB * (cubex * cosphi - cubez * sinphi) + cosB * (
                    cubey * cosA - sinA * (cubex * sinphi + cubez * cosphi)
                )
                z = cubey * sinA + cosA * (cubex * sinphi + cubez * cosphi)

                # Add 1/2 screen since projection is centered at (0, 0)
                # and the eye is also at (0, 0)
                xp = int(screen_width / 2 + K1 * x / (z + K2))
                yp = int(screen_height / 2 - K1 * y / (z + K2))

                # Scale original cube point into unit vector
                factor = (w * w + l * l + h * h) ** 0.5
                cubex = w / factor
                cubey = l / factor
                cubez = h / factor

                # Rotate unit vector
                x = cosB * (cubex * cosphi - cubez * sinphi) - sinB * (
                    cubey * cosA - sinA * (cubex * sinphi + cubez * cosphi)
                )
                y = sinB * (cubex * cosphi - cubez * sinphi) + cosB * (
                    cubey * cosA - sinA * (cubex * sinphi + cubez * cosphi)
                )
                z = cubey * sinA + cosA * (cubex * sinphi + cubez * cosphi)

                # Luminance, calculated with -normal_x - 2 * normal_z
                # since light source is at (-1, 0, -2)
                Lu = -x - 2 * z
                ooz = 1 / (z + K2)

                # L ranges from -sqrt(2) to +sqrt(2)
                # Don't plot if L < 0 as it is shining away from eye
                if Lu > 0:
                    # print(Lu)
                    # Check in z-buffer if there a pixel closer to the eye, with smaller z
                    if ooz > zbuffer[xp][yp]:
                        zbuffer[xp][yp] = ooz
                        luminance_index = (
                            Lu * 5
                        )  # L is not in the range 0..11 (5*sqrt(5) = 11.2)

                        # Plot corresponding luminance
                        output[xp][yp] = ".,-~:;=!*#$@"[int(luminance_index)]

                # output[xp][yp] = "."

    # Return cursor to home position
    print("\x1b[H")

    # Print output matrix
    print("\n".join("".join(output[i]) for i in range(screen_height)))

    # A, B and phi are incremented together
    # so the torus rotates around the x, z and y axes together
    A += a_spacing
    B += b_spacing
    phi += phi_spacing
