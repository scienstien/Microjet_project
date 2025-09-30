import numpy as np

# ---- Known geometry ----
r_tip_in = 23e-3     # m
r_hub_in = 7.82e-3   # m
r_tip_out = 33e-3    # m
r_hub_out = 18.31e-3 # m
b_in = r_tip_in - r_hub_in
b_out = r_tip_out - r_hub_out
rm = 0.02844         # mean radius [m]

beta1 = np.deg2rad(90.0)    # inlet blade angle
beta2 = np.deg2rad(49.13)   # outlet blade angle

# Gas properties
gamma = 1.4
R = 287.0
cp = gamma * R / (gamma - 1)

# Inlet conditions
T0_in = 300.0   # K
p0_in = 1e5     # Pa
rho_in = p0_in / (R * T0_in)


def compressor_point(N_rpm, m_dot):
    # Geometry
    A_in = np.pi * (r_tip_in**2 - r_hub_in**2)
    A_out = np.pi * (r_tip_out**2 - r_hub_out**2)
    
   
    V_ax = m_dot / (rho_in * A_in)
    
    U = 2*np.pi * (N_rpm/60) * rm
    
    V_theta1 = 0.0
    
    V_theta2 = U - V_ax/np.tan(beta2)
    

    delta_h = U*(V_theta2 - V_theta1)
    delta_T = delta_h / cp
    
    # Pressure ratio (the assumed issentropic efficiency is 0.75, theoretically  it could upto to 0.9, but we will test it for multiple values)
    eta_c = 0.75
    PR = (1 + eta_c*delta_T/T0_in)**(gamma/(gamma-1))
    
    return {
        "N_rpm": N_rpm,
        "m_dot": m_dot,
        "U": U,
        "V_ax": V_ax,
        "V_theta2": V_theta2,
        "delta_h": delta_h,
        "delta_T": delta_T,
        "PR": PR
    }


N_list = [70000]        # rpm
m_list = [0.2]             # kg/s

for N in N_list:
    for m in m_list:
        result = compressor_point(N, m)
        print(result)
