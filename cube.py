from math import cos, sin, isclose


### Zoom out if animation is flickering ###

# Screen constants
screen_width = 80
screen_height = 80
frames = 3000

# Shape constants
R1 = 1  # Radius of circle
R2 = 2  # Radius of rotation
K2 = 5  # Distance of object from eye
K1 = screen_width * K2 * 3 / (8 * (R1 + R2))  # Distance of eye from screen

L = 1.5  # Cube length

# Increments
l_spacing = 0.05
phi_spacing = 0.05
a_spacing = 0.05
b_spacing = 0.05

# A, B and phi rotate the x, z and y axes respectively
A = B = phi = 1

# Clear screen and return cursor to home position
print("\x1b[2J")


def helper():
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
    ooz = 1 / (z + K2)

    # Add 1/2 screen since projection is centered at (0, 0)
    # and the eye is also at (0, 0)
    xp = int(screen_width / 2 + K1 * x * ooz)
    yp = int(screen_height / 2 - K1 * y * ooz)

    # normal of cube is largest component of (x, y, z)
    sides = [abs(cubex), abs(cubey), abs(cubez)]
    index = max(range(len(sides)), key=lambda i: sides[i])
    normal = [0, 0, 0]
    normal[index] = 1
    cubex, cubey, cubez = normal

    # Rotate normal
    x = cosB * (cubex * cosphi - cubez * sinphi) - sinB * (
        cubey * cosA - sinA * (cubex * sinphi + cubez * cosphi)
    )
    y = sinB * (cubex * cosphi - cubez * sinphi) + cosB * (
        cubey * cosA - sinA * (cubex * sinphi + cubez * cosphi)
    )
    z = cubey * sinA + cosA * (cubex * sinphi + cubez * cosphi)

    # Luminance, calculated with -normal_x - 2 * normal_z
    # since light source is at (1, 0, 2)
    Lu = x + 2 * z

    Lu = abs(Lu)
    # Check in z-buffer if there a pixel closer to the eye, with smaller z
    if ooz > zbuffer[xp][yp]:
        zbuffer[xp][yp] = ooz
        luminance_index = Lu * 5.2  # L is not in the range 0..11 (5.2*sqrt(5) = 11.6)

        # Plot corresponding luminance
        output[xp][yp] = ".,-~:;=!*#$@"[int(luminance_index)]


# Main loop
for i in range(frames):
    # Reset output and zbuffer
    output = [[" "] * screen_width for _ in range(screen_height)]
    zbuffer = [[0] * screen_width for _ in range(screen_height)]

    cosB, sinB = cos(B), sin(B)
    cosA, sinA = cos(A), sin(A)
    cosphi, sinphi = cos(phi), sin(phi)

    # Width goes from -L/2 to L/2
    w = -L / 2
    while isclose(w, L / 2) or w < L / 2:
        # Go the whole plane for both sides
        if isclose(w, L / 2) or isclose(w, -L / 2):
            # Length, centred at (0, 0)
            l = -L / 2
            while isclose(l, L / 2) or l < L / 2:
                # Height, centred at (0, 0)
                h = -L / 2
                while isclose(h, L / 2) or h < L / 2:
                    helper()
                    h += l_spacing
                l += l_spacing
        else:
            # Go only the edges
            l = -L / 2
            h = -L / 2
            while isclose(l, L / 2) or l < L / 2:
                helper()
                l += l_spacing
            while isclose(h, L / 2) or h < L / 2:
                helper()
                h += l_spacing
            while isclose(l, -L / 2) or l > -L / 2:
                helper()
                l -= l_spacing
            while isclose(h, -L / 2) or h > -L / 2:
                helper()
                h -= l_spacing
        w += l_spacing

    # Return cursor to home position
    print("\x1b[H")

    # Print output matrix
    print("\n".join("".join(output[i]) for i in range(screen_height)))

    # A, B and phi are incremented together
    # so the torus rotates around the x, z and y axes together
    A += a_spacing
    B += b_spacing
    phi += phi_spacing
