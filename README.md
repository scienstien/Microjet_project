# Microjet Engine Prototype — Radial Compressor Design & Meanline Analysis

This repository contains the early-stage work for a microjet engine prototype developed by two very stubborn students who decided that “can we build one?” was a perfectly reasonable question.

The first iteration focuses on the component that ruins your life first in any gas turbine:  
**the radial compressor.**

This repo includes:
- The **SolidWorks impeller model**
- The **1-D meanline analysis code** (`1D_meanline.py`)
- The **performance calculations**
- Notes on the physics and assumptions behind the model
- Early plots and results

This is not a polished product. It’s documentation of a side quest.

---

# 1. Project Background

Small-scale jet engines are gaining relevance in India and globally — UAVs, experimental propulsion systems, rapid prototyping, etc.  
The question was never “should we build one?”  
The question quickly became: **how far can we get with a disciplined first iteration?**

A self-sustaining turbine on the first attempt is a fantasy, so iteration 1 is **electrically driven**.  
This lets us isolate compressor performance without the chaos of combustion stability.

The impeller and diffuser were designed in SolidWorks during the 3rd semester, refined over several months, then analyzed using classical 1-D meanline compressor theory.

---

# 2. Geometry Extraction

All meanline calculations start from *actual* CAD dimensions.  
From the model:

| Parameter | Value |
|----------|--------|
| Inlet tip radius \(r_{tip,in}\) | 23 mm |
| Inlet hub radius \(r_{hub,in}\) | 7.82 mm |
| Outlet tip radius \(r_{tip,out}\) | 33 mm |
| Outlet hub radius \(r_{hub,out}\) | 18.31 mm |
| Mean radius \(r_m\) | 28.44 mm |
| Blade outlet angle \(\beta_2\) | 49.13° |
| Number of blades | 12 |

These values feed directly into the velocity triangle and Euler work calculations.

---

# 3. What the Meanline Model Computes

Meanline analysis compresses 3-D compressor flow physics into a set of 1-D relationships at a reference radius.

The workflow:

1. Compute **meridional (axial) velocity**  
   \[
   V_{ax} = rac{\dot{m}}{ho A_{in}}
   \]

2. Use the blade outlet angle to compute the required **tangential flow**:  
   \[
   V_{	heta2,ideal} = U - rac{V_{ax}}{	aneta_2}
   \]

3. Apply a **slip factor** \(\sigma\) (finite blade count correction):  
   Stanitz correlation for 12 blades gives \(\sigma pprox 0.83\).  
   \[
   V_{	heta2} = \sigma V_{	heta2,ideal}
   \]

4. Use **Euler’s turbine equation** to compute specific work:  
   \[
   \Delta h_0 = U(V_{	heta2} - V_{	heta1})
   \]

5. Convert to **total temperature rise**:  
   \[
   \Delta T_0 = rac{\Delta h_0}{c_p}
   \]

6. Convert to **pressure ratio** using an isentropic efficiency \(\eta_c\):  
   \[
   PR = \left(1 + \eta_crac{\Delta T_0}{T_{0,in}}ight)^{rac{\gamma}{\gamma - 1}}
   \]

---

# 4. Why the Code Looks the Way It Does

The script `1D_meanline.py` is intentionally minimal:

- No CFD  
- No empirical loss models  
- No diffuser matching  
- No clearance leakage modeling *(to be added in Iteration 2)*  

This version focuses solely on:

- Slip factor  
- Blade geometry  
- Axial velocity set by mass flow  
- Induced work from Euler  
- Pressure ratio from thermodynamics

This keeps the physics transparent and the debugging tolerable.

---

# 5. Baseline Results

Using:  
- \(N = 50{,}000\) rpm  
- \(\dot{m} = 0.25\) kg/s  
- \(\sigma = 0.83\)  
- \(\eta_c = 0.76\)

We obtain:

- Blade speed \(U pprox 149\) m/s  
- Axial velocity \(V_{ax} pprox 30.8\) m/s  
- Outlet tangential velocity \(V_{	heta2} pprox 42.3\) m/s  
- Specific work \(\Delta h_0 pprox 6300\) J/kg  
- Temperature rise \(\Delta T_0 pprox 6.3\) K  
- Stage pressure ratio ≈ **1.03**

---

# 6. Sensitivity Analysis

### Slip factor variation
Range: 0.85 → 0.98  
Effect: PR shifts by a few percent.

### Isentropic efficiency variation
Range: 0.65 → 0.82  
Effect: PR increases ~1–2%.

---

# 7. What This Repository *Is* and *Is Not*

**This repo *is*:**
- A transparent first-iteration design  
- Actual geometry + actual math  
- A clean baseline for future optimization  
- A record of how the compressor behaves before CFD

**This repo is *not*:**
- A complete engine  
- CFD-grade accurate  
- A final compressor  
- A self-sustaining turbine

---

# 8. License

MIT. Use it however you want.

---

# 9. Contact

If you're building microjets, compressors, or turbomachinery and want to compare notes, feel free to reach out.
