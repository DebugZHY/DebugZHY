# Read the Excel file
# 2% damping 结果
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df = pd.read_excel(r'D:\PycharmProjects\DebugZHY\02damping_mc1_node68_displacement.xlsx')

dataz = df.iloc[2:, 6]
dataz = pd.to_numeric(dataz, errors='coerce')
# Plotting the curve line
plt.figure(figsize=(10,7))
plt.plot(range(len(dataz)), dataz, marker='o', markersize=5)
dataz_fft = np.fft.fft(dataz - np.mean(dataz))
plt.plot(range(len(dataz_fft)), np.abs(dataz_fft), marker='o', markersize=5)
plt.xlabel('Time:1/20s')
plt.ylabel('Displacement(m)')
plt.title('Time-history of Displacement at Reference Node')
#plt.show()
plt.savefig('02damping_mc1_node68_displacement.png', format="png")
plt.close()

np.fft.fft(dataz)

df = pd.read_excel(r'D:\PycharmProjects\DebugZHY\02damping_mc1_node68_velocity.xlsx')
dataz = df.iloc[:, 6]
dataz = pd.to_numeric(dataz, errors='coerce')
# Plotting the curve line
plt.figure(figsize=(10,7))
plt.plot(range(len(dataz)), dataz, marker='o', markersize=5)
plt.xlabel('Time:1/20s')
plt.ylabel('Velocity(m/s)')
plt.title('Time-history of Velocity at Reference Node')
#plt.show()
plt.savefig('02damping_mc1_node68_velocity.png', format="png")
plt.close()
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






