import numpy as np
import matplotlib.pyplot as plt

# Example values at these angles (you can replace these with your actual data)
# ER70S-6_T8
# angles_deg = np.array([0, 30, 45, 60, 90])
# y_values = np.array([0.185895501,0.165971958,0.165944359,0.135981698,0.145903397])

# ER70S-6_T3
# angles_deg = np.array([0, 30, 45, 60, 90])
# y_values = np.array([0.165735143,0.145749884,0.145717026,0.125768753,0.125723658])

# ER110S-G_Huang
# angles_deg = np.array([0, 30, 45, 60, 90])
# y_values = np.array([0.06482547,0.064960695,0.064954922,0.054998115,0.054926346])

# ER100S-G
# angles_deg = np.array([0, 30, 45, 60, 90])
# y_values = np.array([0.089399415,0.094149123,0.093320792,0.096520285,0.078552097])

# ER110S-G Chen
# angles_deg = np.array([0, 30, 45, 60, 90])
# y_values = np.array([0.102854599,0.095435297,0.10403766,0.097073188,0.101424641])

# ER120S-G
# angles_deg = np.array([0, 30, 45, 60, 90])
# y_values = np.array([0.101066286,0.101993881,0.089713349,0.08825753,0.067383244])

# ER304
# angles_deg = np.array([0, 30, 45, 60, 90])
# y_values = np.array([0.457386125,0.493077525,0.650995841,0.59405003,0.454479495])

# ER308L
# angles_deg = np.array([0, 30, 45, 60, 90])
# y_values = np.array([0.363275124,0.374317833,0.468319356,0.48139733,0.386234228])

# ER316L
# angles_deg = np.array([0, 30, 45, 60, 90])
# y_values = np.array([0.252981641,0.310311662,0.434397901,0.379057895,0.299816493])

# ER110S-G-H1 Weber
# angles_deg = np.array([0, 22.5, 45, 67.5, 90])
# y_values = np.array([0.106360019,0.099343765,0.097355599,0.089399221,0.085319108])

# ER110S-G-H2 Weber
# angles_deg = np.array([0, 22.5, 45, 67.5, 90])
# y_values = np.array([0.106238675,0.092205653,0.08919152,0.093233238,0.090169157])

# ER110S-G-L1 Weber
# angles_deg = np.array([0, 22.5, 45, 67.5, 90])
# y_values = np.array([0.088316827,0.074258422,0.082283705,0.088325156,0.096365002])

# ER110S-G-L2 Weber
angles_deg = np.array([0, 22.5, 45, 67.5, 90])
y_values = np.array([0.080153921,0.064069498,0.046088307,0.036075499,0.059148544])

# Convert angles to radians
angles_rad = np.radians(angles_deg)

# Construct the matrix A based on the equation
A = np.vstack([
    np.ones_like(angles_rad),  # a0 term
    np.cos(2 * angles_rad),  # a1 term
    np.cos(4 * angles_rad),  # a2 term
    np.cos(6 * angles_rad),  # a3 term
    np.cos(8 * angles_rad)  # a4 term
]).T

# Solve for the parameters a0, a1, a2, a3, a4
params = np.linalg.lstsq(A, y_values, rcond=None)[0]

# Extract fitted parameters
a0, a1, a2, a3, a4 = params

# Print the parameters
print(f"Fitted parameters: a0 = {a0}, a1 = {a1}, a2 = {a2}, a3 = {a3}, a4 = {a4}")

# Plot the data and the fitted curve
angles_fine = np.linspace(0, np.pi / 2, 500)  # Fine angles for smooth curve
fitted_values = a0 + a1 * np.cos(2 * angles_fine) + a2 * np.cos(4 * angles_fine) + a3 * np.cos(6 * angles_fine) + a4 * np.cos(8 * angles_fine)

plt.figure(figsize=(8, 6))
plt.scatter(angles_deg, y_values, color='red', label='Data points')
plt.plot(np.degrees(angles_fine), fitted_values, label='Fitted curve', color='blue')
plt.xlabel('Angle (degrees)')
plt.ylabel('Fitted Values')
plt.title('Fitting Function to Angle Data')
plt.legend()
plt.grid(True)
plt.show()
