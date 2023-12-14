import matplotlib.pyplot as plt
import numpy as np

#A polar plot example
theta = [0, np.pi / 6, np.pi / 3, np.pi / 2, 2 * np.pi / 3, 5 * np.pi / 6, np.pi,
         7 * np.pi / 6, 4 * np.pi / 3, 3 * np.pi / 2, 5 * np.pi / 3, 11 * np.pi / 6, 2 * np.pi, 13 * np.pi / 6,
         0]
r = [40.82482905, 35.35533906, 40.82482905, 35.35533906, 40.82482905, 35.35533906, 40.82482905,
     35.35533906, 40.82482905, 35.35533906, 40.82482905, 35.35533906, 40.82482905, 35.35533906,
     40.82482905]
fig = plt.figure()
ax = fig.add_subplot(111, polar=True)
ax.plot(theta, r, color='r', linewidth=3)
ax.grid(True)
plt.show()






