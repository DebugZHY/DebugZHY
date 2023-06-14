import numpy as np
from scipy import interpolate

def max_difference(x1, y1, x2, y2):
    # create a linear interpolation of the first line
    f = interpolate.interp1d(x1, y1)

    # now generate y1 values for x2
    y1_new = f(x2).tolist()

    # calculate differences
    differences = [0]
    for i in range(1, len(y1_new)):
        differences.append(abs((y1_new[i] - y2[i]) / y2[i]))
    # get index of maximum difference
    max_diff = max(differences)
    index = differences.index(max_diff)
    # get the corresponding x and maximum difference
    corresponding_x = x2[index]
    return max_diff, corresponding_x

# example usage:
x1 = [0,-0.0011,-0.00233,-0.0037,-0.00525,-0.007,-0.009,-0.01131,-0.01399,-0.01716,-0.02053,-0.02555,-0.03126,-0.03852,-0.04806,-0.06114,-0.08013,-0.11018,-0.16479,-0.29452]
y1 = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9]
x2 = [0,-0.0012,-0.0024,-0.0037,-0.0052,-0.007,-0.009,-0.0114,-0.0139,-0.0171,-0.0209,-0.0255,-0.0313,-0.0384,-0.0478,-0.061,-0.0797,-0.1089,-0.1617,-0.2717]
y2 = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9]

max_diff, x_value = max_difference(x1, y1, x2, y2)
print(f"Maximum difference is {max_diff} at x = {x_value}")
