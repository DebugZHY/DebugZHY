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
x1 = [8.42803E-4,0.00111,0.00142,0.00178,0.00219,0.00268,0.00327,0.004,0.0049,0.00605,0.00752,0.00947,0.0121,0.01573,0.02092,0.02858,0.04041,0.05954,0.09227,0.15104,0.25773]
y1 = [192,240,288,336,384,432,480,528,576,624,672,720,768,816,864,912,960,1008,1056,1104,1152]
x2 = [0.00111,0.0015,0.00197,0.00255,0.00328,0.0042,0.00543,0.00707,0.00947,0.01283,0.01799,0.02645,0.04006,0.06339,0.11281,0.20426]
y2 = [240,300,360,420,480,540,600,660,720,780,840,900,960,1020,1080,1140]

max_diff, x_value = max_difference(x1, y1, x2, y2)
print(f"Maximum difference is {max_diff} at x = {x_value}")
