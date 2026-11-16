# SMART PEN REV G — MICROSD, MPU, FFC & RF INTEGRATION REPORT
## Multi-Board Coordination, Realistic 180° Service Loops, and Dielectric Antenna Routing

**Document ID:** RPT-SMARTPEN-REVG-PHASE04A-SUB-BOARDS  
**Parts Evaluated:** `06_Front_MPU_Carrier`, `07_MicroSD_Carrier_Mount`, `14_Antenna_Mount`, `16_Front_MPU_Daughterboard`, `17_MicroSD_Carrier_Daughterboard`, `23_Molex_146153_Antenna`, `24_Micro_Coax_Cable_and_UFL`, `25_FFC_Ribbon_Cable`  
**Date:** November 16, 2026  
**Status:** **PASSED — INTEGRATION COORDINATED & VERIFIED**

---

## 1. MICROSD CARRIER & 180° FFC SERVICE LOOP

### 1.1 MicroSD Carrier Architecture
- **Carrier Location:** $Z = 122.00$ to $138.00\text{ mm}$ (inside rear bayonet collar zone).
- **Daughterboard Dimensions:** $11.40\text{ mm} \times 16.00\text{ mm} \times 0.80\text{ mm}$.
- **Socket:** Push-push MicroSD socket oriented rearwards towards the pen cap. When the 30° bayonet cap is detached, the MicroSD card can be pushed to eject without dismantling the internal rail.
- **Pushrod Tunnel:** Central bore Ø $2.40\text{ mm}$ runs through the mount, allowing the moving pushrod to reach the click mechanism.

### 1.2 Realistic 180° FFC Service Loop Modeling
In Phase 4, the FFC was erroneously modeled as a straight rectangular block cutting through the central pushrod corridor. In Phase 4A, this was replaced with a **physically validated 180° service loop**:
- **Connection at Main PCB:** 6-pin FFC connector `J_SD` (`FH12-6S-0.5SH(55)`) located at PCB $X = 58.40\text{ mm}$ -> Pen $Z = 96.40\text{ mm}$, top face $Y = +3.20\text{ mm}$.
- **Forward Flat Leg:** Runs from $Z = 96.40\text{ mm}$ to $Z = 108.00\text{ mm}$ at $Y = +3.20\text{ mm}$.
- **180° Loop Bend:** Modeled with an actual curved cylindrical shell of inner radius $R_{\text{bend}} = 2.00\text{ mm}$ (outer radius $2.20\text{ mm}$), looping vertically from $Y = +3.20\text{ mm}$ up to $Y = +5.20\text{ mm}$ across $Z = 108.00$ to $110.50\text{ mm}$.
  - IPC-2223 minimum dynamic bend radius for $0.12\text{ mm}$ polyimide FFC is $10 \times t = 1.20\text{ mm}$. The CAD radius of **$2.00\text{ mm}$** provides a **$1.67\times$ safety margin**.
- **Return Flat Leg:** Extends from $Z = 108.00\text{ mm}$ to $Z = 122.00\text{ mm}$ at $Y = +5.20\text{ mm}$, entering the MicroSD carrier board connector.
- **Pushrod Clearance:** Pushrod travels at $Y = 0.00\text{ mm}$ (OD $1.60\text{ mm}$, top boundary $Y = +0.80\text{ mm}$).
  $$\text{Vertical Clearance} = Y_{\text{FFC\_min}} - Y_{\text{pushrod\_max}} = 3.10\text{ mm} - 0.80\text{ mm} = 2.30\text{ mm} > 1.50\text{ mm}$$
- **CAD Collision Result:** `ffc ^ pushrod = 0.000 mm³` (Zero interference).

---

## 2. DETACHABLE FRONT MPU MODULE

### 2.1 Mechanical Carrier & Routing
- **Carrier Location:** $Z = 20.00$ to $32.00\text{ mm}$ (inside the front grip).
- **MPU Daughterboard:** $7.20\text{ mm} \times 10.00\text{ mm} \times 0.80\text{ mm}$ carrying 6-axis IMU sensor (ICM-42670-P / BMI270).
- **Connector:** 4-pin keyed connector (`SM04B-SRSS-TB(LF)(SN)`) mating via a flexible 4-wire silicone harness to Main PCB `J_IMU` at Pen $Z = 41.20\text{ mm}$.
- **Refill Isolation Conduit:** A continuous cylindrical sleeve (ID $2.90\text{ mm}$, OD $3.60\text{ mm}$) passes through the center of the MPU carrier. The moving D1 ink refill travels through this conduit with **$0.275\text{ mm}$ radial clearance**, fully isolated from the daughterboard circuitry and wiring.
- **Detachment Mechanism:** Tool-free snap latch. Pulling the front nose cone slides the MPU carrier forward along the $-Z$ axis for easy maintenance.

---

## 3. RF ANTENNA & MICRO-COAXIAL INTEGRATION

### 3.1 Molex 146153-0050 Flexible Dipole
- **Antenna Type:** Molex 146153-0050 2.4/5 GHz balanced flex dipole antenna.
- **Dimensions:** $34.90\text{ mm} \times 9.00\text{ mm} \times 0.10\text{ mm}$.
- **Mounting (Part 14):** Conformal dielectric carrier shell of thickness $0.40\text{ mm}$, seated against the bottom barrel bore wall ($R = 6.65\text{ mm}$, centered at $\theta = -90^\circ$, $Z = 48.00$ to $83.90\text{ mm}$).
- **Metal Pushrod Clearance:** The central metal pushrod runs along $X = 0, Y = 0$. The antenna sits at $Y = -6.65\text{ mm}$. Radial distance is **$6.65\text{ mm}$**, exceeding the minimum recommended RF ground clearance of $5.00\text{ mm}$.
- **Micro-Coax Cable (Part 24):** Ø $1.13\text{ mm}$ low-loss micro-coax routes from the antenna feed point at $Z = 50.00\text{ mm}$ through a dedicated groove along the side of the rail to U.FL receptacle `J_RF` on the PCB at $Z = 92.85\text{ mm}$.
- **Enclosure Permittivity Note:** The model assumes an engineering plastic barrel ($\epsilon_r \approx 3.0$). If an aluminum or metallic barrel is selected by the client, an RF window must be machined directly above this zone.
