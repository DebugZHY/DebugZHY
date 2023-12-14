import numpy as np

# rotate the matrix to 90 degree, 180deg, 270 deg and print with comma separated
def rotate_mtx(mtx):
    print("Original Matrix: \n", mtx)
    print("Rotate 90 degree: \n", np.rot90(mtx, 3))
    print("Rotate 180 degree: \n", np.rot90(mtx, 2))
    print("Rotate 270 degree: \n", np.rot90(mtx, 1))

test = np.array([[1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 1],
                 [1, 1, 1, 1, 1, 0],
                 [1, 1, 1, 0, 0, 0],
                 [1, 1, 0, 0, 0, 0]])
rotate_mtx(test)
