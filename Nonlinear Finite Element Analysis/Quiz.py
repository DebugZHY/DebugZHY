import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def read_xlsx(filepath):
    df = pd.read_excel(filepath, sheet_name='Sheet1')
    t = df.iloc[:, 0].tolist()
    A = df.iloc[:, 1].tolist()
    return t, A

def Newmark_beta(t, P, m, zeta, Tn, beta=1/4, gamma=1/2):
    # Initial calculation
    # Assume zero initial displacement and velocity
    U = np.zeros(len(t))
    V = np.zeros(len(t))
    A = np.zeros(len(t))
    # Get time step dt
    dt = t[1] - t[0]
    # Get damping coefficient c
    c = 4 * np.pi * zeta * m / Tn
    # Get stiffness k
    k = 4 * np.pi ** 2 * m / Tn ** 2
    # Get initial acceleration
    A[0] = (P[0] - c * V[0] - k * U[0]) / m
    k_bar = k + gamma * c / (beta * dt) + m / (beta * dt ** 2)
    a = m / (beta * dt) + gamma * c / beta
    b = m / (2 * beta) + dt * (gamma / (2 * beta) - 1) * c
    for i in range(0, len(t) - 1):
        dPi = P[i + 1] - P[i]
        dPi_bar = dPi + a * V[i] + b * A[i]
        dUi = dPi_bar / k_bar
        dVi = gamma * dUi / (beta * dt) - gamma * V[i] / beta + dt * (1 - gamma / (2 * beta)) * A[i]
        dAi = dUi / (beta * dt ** 2) - V[i] / (beta * dt) - A[i] / (2 * beta)
        U[i + 1] = U[i] + dUi
        V[i + 1] = V[i] + dVi
        A[i + 1] = A[i] + dAi
    return U, V, A

# Read ground motion data
t, A_g = read_xlsx("El-centrol ground motion (PGA=0.1g).xlsx")
# Assume mass m = 1kg
m = 1
# Convert acceleration unit from mm/s^2 to m/s^2
A_g = [i / 1000 for i in A_g]
# Get excitation forces
P = [i * m for i in A_g]
# Damping ratio zeta = 0.05
zeta = 0.05
# Vibration period Tn = 1s
Tn = 1
U, V, A = Newmark_beta(t, P, m, zeta, Tn, beta=1/4, gamma=1/2)
# Plot Time history at Tn = 1s
plt.figure(figsize=(10, 4))
plt.plot(t, U, linewidth=1)
plt.xlabel('Time (s)')
plt.ylabel('Displacement (m)')
plt.title('Time history of displacement at Tn = 1s')
plt.savefig('Time history of displacement at Tn = 1s.png', dpi=300)
plt.close()

plt.figure(figsize=(10, 4))
plt.plot(t, V, linewidth=1)
plt.xlabel('Time (s)')
plt.ylabel('Velocity (m/s)')
plt.title('Time history of velocity at Tn = 1s')
plt.savefig('Time history of velocity at Tn = 1s.png', dpi=300)
plt.close()

plt.figure(figsize=(10, 4))
plt.plot(t, A, linewidth=1)
plt.xlabel('Time (s)')
plt.ylabel('Acceleration (m/s^2)')
plt.title('Time history of acceleration at Tn = 1s')
plt.savefig('Time history of acceleration at Tn = 1s.png', dpi=300)
plt.close()

# Pseudo-acceleration response spectrum
Tns = np.linspace(0, 10, 501)
Sd = np.zeros_like(Tns)
PSa = np.zeros_like(Tns)
idx = 0
for Tn in Tns:
    print(Tn)
    omega_n = 2 * np.pi / Tn
    U, V, A = Newmark_beta(t, P, m, zeta, Tn, beta=1/4, gamma=1/2)
    Sd[idx] = max(abs(U))
    PSa[idx] = Sd[idx] * omega_n ** 2
    idx += 1

plt.figure(figsize=(10, 4))
plt.plot(Tns, PSa, linewidth=1)
plt.xlabel('Period (s)')
plt.ylabel('Pseudo-acceleration (m/s^2)')
plt.title('Response spectrum')
plt.savefig('Pseudo-acceleration response spectrum', dpi=300)

