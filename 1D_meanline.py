import numpy as np
import pandas as pd

# ----------------------------
# Geometry and constants
# ----------------------------
r_tip_in = 23e-3
r_hub_in = 7.82e-3
r_tip_out = 33e-3
r_hub_out = 18.31e-3
r_m = 28.443e-3   # mean radius
A_in = np.pi*(r_tip_in**2 - r_hub_in**2)

beta2 = np.deg2rad(49.13)  # outlet blade angle

gamma = 1.4
R = 287.0
cp = 1005.0
T0_in = 300.0
p0_in = 101325.0
rho = p0_in/(R*T0_in)

# ----------------------------
# Operating point (baseline)
# ----------------------------
N = 70000.0          # rpm
m = 0.20             # kg/s
omega = 2*np.pi*(N/60.0)
U = omega * r_m      # blade speed
V_ax = m/(rho*A_in)  # axial velocity
V_theta1 = 0.0

# ----------------------------
# Function to compute PR
# ----------------------------
def PR_from_params(slip=0.92, eta_c=0.76):
    # velocity triangle
    V_theta2_ideal = U - V_ax/np.tan(beta2)
    V_theta2 = slip * V_theta2_ideal
    
    # enthalpy rise (Euler)
    delta_h = U*(V_theta2 - V_theta1)
    
    # temperature rise
    delta_T = delta_h / cp
    
    # PR using isentropic efficiency
    T02s_over_T01 = 1 + eta_c * delta_T / T0_in
    PR = T02s_over_T01**(gamma/(gamma-1))
    
    return PR, V_theta2_ideal, V_theta2, delta_h, delta_T

# ----------------------------
# Baseline case
# ----------------------------
baseline = (0.92, 0.76)  # (slip, eta_c)
PR_base, Vt2i, Vt2, dh, dT = PR_from_params(*baseline)

print("Baseline PR =", PR_base)


RoationalSpeeds = [70000,60000,50000,4000]
mass_flowrates = [0.20,0.30]
rows = []
for Ns in RoationalSpeeds:
    for mdot in mass_flowrates :
        V_ax = mdot/(rho*A_in)
        omega = 2*np.pi*(Ns/60.0)
        U = omega * r_m 
        PRs , *_ = PR_from_params(slip=0.85, eta_c=0.76)
        rows.append({"Rotational_Speed(RPM)" : Ns,
                    "mass_flowrate" : mdot,
                    "PR": round(PRs,4)})
df_mdot = pd.DataFrame(rows)

df_mdot.to_csv("Mass_flowrate vs Pr_at_given_RPM", index=False)
    

# ----------------------------
# Sensitivity: slip factor σ
# ----------------------------
slips = np.linspace(0.85, 0.98, 6)
rows = []
for s in slips:
    PR, *_ = PR_from_params(slip=s, eta_c=baseline[1])
    rows.append({"sigma": round(s,3),
                 "PR": round(PR,4),
                 "%ΔPR_vs_baseline": round(100*(PR/PR_base-1),2)})
df_slip = pd.DataFrame(rows)
df_slip.to_csv("Slip_vs_Pr")

# ----------------------------
# Sensitivity: efficiency η_c
# ----------------------------
etas = np.linspace(0.65, 0.82, 8)
rows = []
for eta in etas:
    PR, *_ = PR_from_params(slip=baseline[0], eta_c=eta)
    rows.append({"eta_c": round(eta,3),
                 "PR": round(PR,4),
                 "%ΔPR_vs_baseline": round(100*(PR/PR_base-1),2)})
df_eta = pd.DataFrame(rows)
df_eta.to_csv("Eta_vs_Pr")
