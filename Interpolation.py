# Comparison including C2 clamped cubic spline and CSV export of all curves.
# One plot (default styles), and one CSV with columns: x, pchip, pchip_scaled_1p5, akima, makima, spline_c2.

import os
import numpy as np
import matplotlib.pyplot as plt

# ---- Data ---------------------------------------------------------------

# ---- Normal-strength steel ----------------------------------------------
# Strain data with supplements at 30 deg, 45 deg, and 60 deg
# x = np.array([0.0, 0.523598776, 0.785398163, 1.047197551, 1.570796327])
# y = np.array([0.20374133, 0.201621979, 0.20195055, 0.16582927, 0.189997039])
# Strain data with supplements at 20 deg, 45 deg, and 70 deg
# x = np.array([0.0, 0.34906585, 0.785398163, 1.221730476, 1.570796327])
# y = np.array([0.20374133, 0.198331755, 0.20195055, 0.175640779, 0.189997039])
# Strain data with supplements at 20 deg, 40 deg, 50 deg, and 70 deg
# x = np.array([0.0, 0.34906585, 0.698131701, 0.872664626, 1.221730476, 1.570796327])
# y = np.array([0.20374133, 0.198331755, 0.189825468, 0.186766117, 0.175640779, 0.189997039])
# Plastic modulus data with supplements at 30 deg, 45 deg, and 60 deg
# x = np.array([0.0, 0.523598776, 0.785398163, 1.047197551, 1.570796327])
# y = np.array([400.220041, 413.6111575, 489.9533313, 549.9819832, 575.2530383])
# Plastic modulus data with supplements at 20 deg, 45 deg, and 70 deg
# x = np.array([0.0, 0.34906585, 0.785398163, 1.221730476, 1.570796327])
# y = np.array([400.220041, 364.5102618, 489.9533313, 552.142702, 575.2530383])
# Plastic modulus data with supplements at 20 deg, 40 deg, 50 deg, and 70 deg
x = np.array([0.0, 0.34906585, 0.698131701, 0.872664626, 1.221730476, 1.570796327])
y = np.array([400.220041, 364.5102618, 539.2277855, 510.8498646, 552.142702, 575.2530383])

# ---- Stainless steel ----------------------------------------------------
# Strain data with supplements at 30 deg, 45 deg, and 60 deg
# x = np.array([0.0, 0.523598776, 0.785398163, 1.047197551, 1.570796327])
# y = np.array([0.310005236, 0.459798788, 0.771704915, 0.737875478, 0.314548435])
# Strain data with supplements at 20 deg, 45 deg, and 70 deg
# x = np.array([0.0, 0.34906585, 0.785398163, 1.221730476, 1.570796327])
# y = np.array([0.310005236, 0.354536259, 0.771704915, 0.46234593, 0.314548435])
# Strain data with supplements at 20 deg, 40 deg, 50 deg, and 70 deg
# x = np.array([0.0, 0.34906585, 0.698131701, 0.872664626, 1.221730476, 1.570796327])
# y = np.array([0.310005236, 0.354536259, 0.695615527, 0.804814703, 0.46234593, 0.314548435])
# Plastic modulus data with supplements at 30 deg, 45 deg, and 60 deg
# x = np.array([0.0, 0.523598776, 0.785398163, 1.047197551, 1.570796327])
# y = np.array([599.0243539, 415.5526317, 239.6308333, 241.6718306, 780.3138203])
# Plastic modulus data with supplements at 20 deg, 45 deg, and 70 deg
# x = np.array([0.0, 0.34906585, 0.785398163, 1.221730476, 1.570796327])
# y = np.array([599.0243539, 523.7349493, 239.6308333, 398.3446336, 780.3138203])
# Plastic modulus data with supplements at 20 deg, 40 deg, 50 deg, and 70 deg
# x = np.array([0.0, 0.34906585, 0.698131701, 0.872664626, 1.221730476, 1.570796327])
# y = np.array([599.0243539, 523.7349493, 286.4861348, 238.3823514, 398.3446336, 780.3138203])

# ---- PCHIP (Fritsch–Carlson) slopes -----------------------------------
def fritsch_carlson_slopes(x, y):
    h = np.diff(x)
    d = np.diff(y) / h
    n = len(x)
    m = np.zeros(n)
    m[0] = 0.0   # clamped endpoints
    m[-1] = 0.0
    for i in range(1, n-1):
        if d[i-1] == 0.0 or d[i] == 0.0 or np.sign(d[i-1]) != np.sign(d[i]):
            m[i] = 0.0
        else:
            w1 = 2*h[i] + h[i-1]
            w2 = h[i] + 2*h[i-1]
            m[i] = (w1 + w2) / (w1/d[i-1] + w2/d[i])
    return m

# ---- Akima / Modified Akima slopes -------------------------------------
def akima_like_slopes(x, y, modified=False, clamp_ends=True):
    n = len(x)
    h = np.diff(x)
    delta = np.diff(y) / h  # length n-1
    # Extrapolate secants for end handling
    d0   = 2*delta[0]   - delta[1]
    dm1  = 2*d0         - delta[0]
    dn   = 2*delta[-1]  - delta[-2]
    dn1  = 2*dn         - delta[-1]
    d_ext = np.concatenate(([dm1, d0], delta, [dn, dn1]))

    m = np.zeros(n)
    for i in range(n):
        s_im2 = d_ext[i]
        s_im1 = d_ext[i+1]
        s_i   = d_ext[i+2]
        s_ip1 = d_ext[i+3]
        if modified:
            # makima weights
            w1 = abs(s_ip1 - s_i) + 0.5*abs(s_ip1 + s_i)
            w2 = abs(s_im1 - s_im2) + 0.5*abs(s_im1 + s_im2)
        else:
            # original Akima
            w1 = abs(s_ip1 - s_i)
            w2 = abs(s_im1 - s_im2)
        den = w1 + w2
        if den != 0:
            m[i] = (w1*s_im1 + w2*s_i) / den
        else:
            m[i] = 0.0  # flat-run special case
    if clamp_ends:
        m[0] = 0.0
        m[-1] = 0.0
    return m

# ---- Hermite evaluator used by PCHIP/Akima families --------------------
def hermite_eval(xq, x, y, m, lambda_factor=1.0):
    xq = np.atleast_1d(xq)
    n = len(x)
    yq = np.empty_like(xq, dtype=float)
    for k, xv in enumerate(xq):
        i = np.searchsorted(x, xv) - 1
        i = np.clip(i, 0, n-2)
        hi = x[i+1] - x[i]
        t = (xv - x[i]) / hi
        h00 = (1 + 2*t) * (1 - t)**2
        h10 = t * (1 - t)**2
        h01 = t**2 * (3 - 2*t)
        h11 = t**2 * (t - 1)
        yq[k] = (h00 * y[i] + h10 * hi * (lambda_factor*m[i]) +
                 h01 * y[i+1] + h11 * hi * (lambda_factor*m[i+1]))
    return yq if len(yq) > 1 else yq.item()

# ---- C2 clamped cubic spline (build & evaluate) ------------------------
def clamped_cubic_spline_evaluator(x, y, s0=0.0, sN=0.0):
    n = len(x)
    h = np.diff(x)
    A = np.zeros((n, n))
    b = np.zeros(n)
    # left clamp
    A[0,0] = 2*h[0]; A[0,1] = h[0]
    b[0]   = 6*((y[1]-y[0])/h[0] - s0)
    # interior
    for i in range(1, n-1):
        A[i,i-1] = h[i-1]
        A[i,i]   = 2*(h[i-1] + h[i])
        A[i,i+1] = h[i]
        b[i]     = 6*((y[i+1]-y[i])/h[i] - (y[i]-y[i-1])/h[i-1])
    # right clamp
    A[-1,-2] = h[-1]; A[-1,-1] = 2*h[-1]
    b[-1]    = 6*(sN - (y[-1]-y[-2])/h[-1])
    M = np.linalg.solve(A, b)  # second derivatives at nodes

    def eval_spline(xq):
        xq = np.atleast_1d(xq)
        vals = np.empty_like(xq, dtype=float)
        for k, xv in enumerate(xq):
            i = np.searchsorted(x, xv) - 1
            i = np.clip(i, 0, n-2)
            hi = x[i+1]-x[i]
            a = (x[i+1]-xv)/hi
            b_ = (xv-x[i])/hi
            vals[k] = (M[i]*a**3 + M[i+1]*b_**3)*hi**2/6 \
                      + (y[i] - M[i]*hi**2/6)*a \
                      + (y[i+1] - M[i+1]*hi**2/6)*b_
        return vals if len(vals) > 1 else vals[0]

    return eval_spline

# ---- Build methods ------------------------------------------------------
m_pchip  = fritsch_carlson_slopes(x, y)
m_akima  = akima_like_slopes(x, y, modified=False, clamp_ends=True)
m_makima = akima_like_slopes(x, y, modified=True,  clamp_ends=True)
S_c2     = clamped_cubic_spline_evaluator(x, y, s0=0.0, sN=0.0)

# ---- Evaluate on dense grid --------------------------------------------
xx = np.linspace(x[0], x[-1], 100)
yy_pchip        = hermite_eval(xx, x, y, m_pchip, 1.0)
yy_pchip_scaled = hermite_eval(xx, x, y, m_pchip, 1.5)   # example λ=1.5
yy_akima        = hermite_eval(xx, x, y, m_akima, 1.0)
yy_makima       = hermite_eval(xx, x, y, m_makima, 1.0)
yy_spline       = S_c2(xx)

# ---- Plot ---------------------------------------------------------------
plt.figure(figsize=(7, 4.5))
plt.plot(xx, yy_pchip,        label="PCHIP (λ=1.0)")
plt.plot(xx, yy_pchip_scaled, label="PCHIP scaled (λ=1.5)")
plt.plot(xx, yy_akima,        label="Akima (original, clamped ends)")
plt.plot(xx, yy_makima,       label="Modified Akima (makima, clamped ends)")
plt.plot(xx, yy_spline,       label="C2 Clamped Cubic Spline")
plt.scatter(x, y, marker='o', label="Data points")
plt.xlabel("x (radians)")
plt.ylabel("y")
plt.title("Interpolation Comparison (clamped ends f'(0)=f'(π/2)=0)")
plt.grid(True)
plt.legend(loc="best")
plt.show()

# ---- Save CSV (one x column, each method as its own y column) ----------
out = np.column_stack([xx, yy_pchip, yy_pchip_scaled, yy_akima, yy_makima, yy_spline])
header = "x,pchip,y_pchip_scaled_1p5,akima,makima,spline_c2"
csv_path = os.path.join(os.getcwd(), "interp_results.csv")
np.savetxt(csv_path, out, delimiter=",", header=header, comments="", fmt="%.9f")
