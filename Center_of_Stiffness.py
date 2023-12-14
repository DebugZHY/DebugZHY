import numpy as np

A = 1
x = np.array([1, 2, 3, 4, 5, 6, 7, 8])
y = np.array([1, 2, 3, 4, 5, 6, 7, 8])

# Get number of quadrilaterals

mod_num = int(len(x) / 4)

x_Iy_total = 0
y_Ix_total = 0
Iy_total = 0
Ix_total = 0

for i in range(mod_num):
    x_coords = x[i * 4: i * 4 + 4]
    y_coords = y[i * 4: i * 4 + 4]

    Ix = 0
    Iy = 0

    # Calculate centroid
    x_centroid = np.mean(x_coords)
    y_centroid = np.mean(y_coords)

    # Calculate moment of inertia
    x_coords = np.append(x_coords, x_coords[0])
    y_coords = np.append(y_coords, y_coords[0])

    for j in range(4):
        Ix += (y_coords[i + 1] * x_coords[i] - y_coords[i] * x_coords[i + 1]) * (
                y_coords[i] ** 2 + y_coords[i] * y_coords[i + 1] + y_coords[i + 1] ** 2) / 12
        Ix -= A * y_centroid ** 2
        Iy += (y_coords[i + 1] * x_coords[i] - y_coords[i] * x_coords[i + 1]) * (
                x_coords[i] ** 2 + x_coords[i] * x_coords[i + 1] + x_coords[i + 1] ** 2) / 12
        Iy -= A * x_centroid ** 2

    Ix_total += Ix
    Iy_total += Iy
    x_Iy_total += x_centroid * Iy
    y_Ix_total += y_centroid * Ix

# Get center of stiffness
x_center = x_Iy_total / Iy_total
y_center = y_Ix_total / Ix_total
