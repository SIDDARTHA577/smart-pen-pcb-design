# Smart Pen Rev G — Final USB Differential Interface Validation
**Document ID:** RPT-REVG-P3C-USB-VALIDATION  
**Project:** Smart Pen Hardware Architecture Revision G  
**Variant:** Four-Layer Evaluation Candidate (`output/RevG/variants/FourLayer_Candidate/SmartPen.kicad_pcb`)  
**Git Branch:** `engineering/revg-production`  
**Base Commit:** `f76aab08831da7bf26516d4a1a39215d754e0d73`  
**Date:** November 16, 2026  
**Status:** Schematic & Physical USB Path Audited; Impedance Labeled as Prototype Validation Assumption  

---

## 1. Executive Summary

This report delivers the comprehensive electrical and physical routing validation of the USB 2.0 interface on the Smart Pen Revision G four-layer candidate. The complete data path—from the reversible USB Type-C receptacle `J_USB` through transient voltage suppressor `U_ESD` and series damping resistors `R7`/`R8` to microcontroller `U1` (ESP32-C3FH4X)—has been audited down to physical pad coordinates, pin assignments, net polarities, CC termination, and layer transitions.

The physical routing satisfies all electrical DRC rules with **0 violations**. However, because the differential pair splits layers (`/USB_DM_CORE` on `B.Cu` vs `/USB_DP_CORE` on `In2.Cu`) due to board density constraints, nominal $90\,\Omega$ differential coupling is decoupled over this section. For USB 2.0 Full-Speed (12 Mbps), the short physical trace length ($\approx 30\text{ mm}$) places the signal well within the lumped-element regime, ensuring functional digital operation. In strict accordance with engineering handoff standards, differential impedance is formally designated as a design assumption requiring physical prototype validation rather than a measured metric.

---

## 2. Complete End-to-End Signal Chain Audit

```
 [J_USB: Type-C] ===> [U_ESD: USBLC6-2SC6] ===> [R7 / R8: 22Ω] ===> [U1: ESP32-C3]
  (TYPE-C-31-M-12)      (TVS Diode Array)         (Damping)          (SoC USB Core)
   Pads 5,6,7,8          Pads 1, 2, 3              0402 SMD           Pads 25, 26
```

### 2.1 Reversible USB-C Receptacle (`J_USB: TYPE-C-31-M-12`)
- **Physical Position:** $X = 78.400\text{ mm}, Y = 4.600\text{ mm}$ (Mounted on `F.Cu`, side-facing).
- **Pin Assignments & Net Polarity:**
  - **Pads 1 & 12:** `/GND` (Ground return).
  - **Pads 2 & 11:** `/USB_VBUS` (+5.0V bus input).
  - **Pad 4:** `/USB_CC1` (Configuration Channel 1).
  - **Pad 9:** `/USB_CC2` (Configuration Channel 2).
  - **Pads 5 & 7:** `/USB_DM_PORT` (USB D− A-side Pad 5 @ $77.65, 3.10$, B-side Pad 7 @ $78.65, 3.10$). Both pads are tied directly together on copper to ensure plug reversibility.
  - **Pads 6 & 8:** `/USB_DP_PORT` (USB D+ A-side Pad 6 @ $78.15, 3.10$, B-side Pad 8 @ $79.15, 3.10$). Both pads are tied directly together on copper to ensure plug reversibility.
  - **Pads 3 & 10:** SBU2 and SBU1 (Unconnected NC, not used in USB 2.0 Full-Speed).
  - **Pads 13, 14, 15, 16:** Mechanical shell retention tabs directly bonded to solid PCB `/GND`.

### 2.2 USB Type-C CC Configuration Resistors (`R5`, `R6`)
- In accordance with the USB Type-C Cable and Connector Specification (Revision 2.1) for Upstream Facing Ports (UFP / Device mode):
  - **`R5` ($5.10\text{ k}\Omega \pm 1\%$, 0402):** Connected from `/USB_CC1` (Pad 4) to `/GND`.
  - **`R6` ($5.10\text{ k}\Omega \pm 1\%$, 0402):** Connected from `/USB_CC2` (Pad 9) to `/GND`.
- **Validation:** Independent $5.1\text{ k}\Omega$ pull-downs advertise the Smart Pen as a $5\text{V}$ standard device sink to any connected USB-C host or PD supply, successfully requesting $500\text{ mA}$ standard power without initiating unsupported PD contracts.

### 2.3 Electrostatic Discharge Protection (`U_ESD: USBLC6-2SC6`)
- **Component:** STMicroelectronics `USBLC6-2SC6` (SOT-23-6 package).
- **Physical Position:** $X = 72.000\text{ mm}, Y = 4.490\text{ mm}$ (Directly adjacent to `J_USB`).
- **Pinout Mapping:**
  - **Pad 1 (I/O 1):** Net `/USB_DP_PORT` @ $(71.050, 3.190)$
  - **Pad 2 (I/O 2):** Net `/USB_DM_PORT` @ $(72.000, 3.190)$
  - **Pad 3 (GND):** Net `/GND` @ $(72.950, 3.190)$
- **Protection Rating:** IEC 61000-4-2 Level 4 ($\pm 15\text{ kV}$ air discharge, $\pm 8\text{ kV}$ contact discharge). Ultra-low line capacitance ($3.5\text{ pF}$ max) prevents capacitive loading of data edges.

### 2.4 Series Damping & Source Termination Resistors (`R7`, `R8`)
- **`R7` ($22.0\,\Omega \pm 1\%$, 0402):** Connects between `/USB_DM_PORT` (Pad 1 @ $72.500, 7.975$) and `/USB_DM_CORE` (Pad 2 @ $72.500, 7.025$).
- **`R8` ($22.0\,\Omega \pm 1\%$, 0402):** Connects between `/USB_DP_PORT` (Pad 1 @ $71.600, 7.975$) and `/USB_DP_CORE` (Pad 2 @ $71.600, 7.025$).
- **Purpose:** Together with the ESP32-C3 internal output impedance ($\approx 20\text{--}25\,\Omega$), the $22\,\Omega$ series resistors provide matched source termination to the nominal $90\,\Omega$ differential transmission target, suppressing edge ringing and reflections.

### 2.5 Microcontroller Host Connection (`U1: ESP32-C3FH4X`)
- **Physical Position:** $X = 42.880\text{ mm}, Y = 4.835\text{ mm}$ (QFN-32).
- **Pin Assignment & Polarity Verification:**
  - **Pad 25 (GPIO18 / USB_D−):** Connected to net `/USB_DM_CORE` @ $(44.630, 7.235)$.
  - **Pad 26 (GPIO19 / USB_D+):** Connected to net `/USB_DP_CORE` @ $(44.130, 7.235)$.
- **Polarity Match:** Confirmed 100% compliant with Espressif ESP32-C3 Technical Reference Manual (Section 26: USB Serial/JTAG Controller).

---

## 3. Physical Routing Geometry & Layer Transitions

Detailed trace inspection reveals the exact layer distribution and routing coordinates:

| Signal Net | Section | Routing Layer | Track Width | Coordinate Span |
| :--- | :--- | :---: | :---: | :--- |
| `/USB_DM_PORT` | J_USB $\rightarrow$ U_ESD | F.Cu | $0.180\text{ mm}$ | $(77.650, 3.100) \rightarrow (78.650, 0.550)$ |
| `/USB_DM_PORT` | Longitudinal run | B.Cu | $0.180\text{ mm}$ | $(72.000, 0.550) \rightarrow (78.650, 0.550)$ |
| `/USB_DM_PORT` | U_ESD $\rightarrow$ R7 | In2.Cu / F.Cu | $0.180\text{ mm}$ | $(72.000, 0.550) \rightarrow (73.200, 8.500) \rightarrow R7$ |
| `/USB_DP_PORT` | J_USB $\rightarrow$ U_ESD | F.Cu | $0.180\text{ mm}$ | $(78.150, 3.100) \rightarrow (79.150, 1.200)$ |
| `/USB_DP_PORT` | Longitudinal run | B.Cu | $0.180\text{ mm}$ | $(71.050, 1.200) \rightarrow (78.150, 1.200) \rightarrow (71.600, 8.500) \rightarrow R8$ |
| **`/USB_DM_CORE`**| **R7 $\rightarrow$ U1 Pin 25** | **B.Cu & F.Cu** | **$0.150\text{ mm}$** | **$X = 52.00\text{ to }69.20\text{ mm}$ on B.Cu @ $Y = 6.000\text{ mm}$** |
| **`/USB_DP_CORE`**| **R8 $\rightarrow$ U1 Pin 26** | **In2.Cu & F.Cu**| **$0.180\text{ mm}$** | **$X = 54.00\text{ to }70.50\text{ mm}$ on In2.Cu @ $Y = 7.200\text{ mm}$** |

### Critical Finding: Core Trace Layer Split
- Between $X \approx 54\text{ mm}$ and $X \approx 70\text{ mm}$:
  - `/USB_DM_CORE` runs on **Layer 4 (`B.Cu`)** at $Y = 6.000\text{ mm}$.
  - `/USB_DP_CORE` runs on **Layer 3 (`In2.Cu`)** at $Y = 7.200\text{ mm}$.
- **Electromagnetic Consequence:** Because D+ and D− are routed on separate layers separated by a $0.210\text{ mm}$ dielectric and $1.20\text{ mm}$ lateral offset, true differential coupling is absent over this $16\text{ mm}$ span.

---

## 4. Transmission Line & Impedance Analysis

### 4.1 Theoretical Impedance Model (JLCPCB 4-Layer 7628 Stackup)
Using standard IPC-2141 microstrip and stripline formulas for the specified stackup:
- Outer Dielectric Height: $H_1 = H_3 = 0.2104\text{ mm}$ ($\epsilon_r = 4.4$, FR-4).
- Copper Thickness: $T = 0.035\text{ mm}$ ($1\text{ oz}$).
- **Single-Ended Microstrip (F.Cu or B.Cu referenced to In1/In2):**
  $$Z_0 = \frac{87}{\sqrt{\epsilon_r + 1.41}} \ln\left(\frac{5.98 H}{0.8 W + T}\right)$$
  - For $W = 0.180\text{ mm}, H = 0.210\text{ mm} \implies Z_0 \approx 64\,\Omega$.
- **Edge-Coupled Differential Microstrip Target:**
  - Standard USB specification mandates $Z_{\text{diff}} = 90\,\Omega \pm 10\%$ ($81\,\Omega \text{ to } 99\,\Omega$).
  - Achieving $Z_{\text{diff}} \approx 90\,\Omega$ on this stackup requires $W \approx 0.16\text{ mm}, S \approx 0.18\text{ mm}$ referenced to a continuous ground plane.

### 4.2 Lumped-Element vs. Transmission Line Regime
The ESP32-C3 integrated USB Serial/JTAG controller operates strictly in **USB 2.0 Full-Speed (12 Mbps)** mode (it does NOT support High-Speed 480 Mbps):
- **Data Bit Period:** $T_{\text{bit}} = \frac{1}{12\text{ MHz}} \approx 83.3\text{ ns}$.
- **Rise / Fall Time ($10\%\text{--}90\%$):** $t_r \approx 4\text{ to } 20\text{ ns}$ (typically $10\text{ ns}$).
- **Signal Knee Frequency:** $f_{\text{knee}} = \frac{0.5}{t_r} \approx \frac{0.5}{10\text{ ns}} = 50\text{ MHz}$.
- **Effective Dielectric Constant:** $\epsilon_{\text{eff}} \approx 3.2 \implies v = \frac{c}{\sqrt{\epsilon_{\text{eff}}}} \approx 167\text{ mm/ns}$.
- **Signal Transition Distance (Rise Time Distance):**
  $$l_{\text{trans}} = v \times t_r = 167\text{ mm/ns} \times 10\text{ ns} = 1670\text{ mm}$$
- **Critical Transmission Line Threshold ($\frac{1}{10}$ rise distance):**
  $$l_{\text{crit}} = \frac{l_{\text{trans}}}{10} \approx 167\text{ mm}$$

### 4.3 Engineering Verdict
- **Total Physical Trace Length:** Approximately $32\text{ mm}$.
- Because the total trace length ($32\text{ mm}$) is **less than one-fifth of the critical transmission line length ($167\text{ mm}$)**, the USB connection operates entirely in the **lumped-element regime**.
- In the lumped-element regime, transmission line reflections and differential uncoupling do not cause significant phase distortion or bit errors at 12 Mbps. Functional USB enumeration, firmware flashing, and UART console logging will operate reliably.
- **Prototype Validation Mandate:** In compliance with professional engineering standards:
  - **NO EYE DIAGRAM HAS BEEN MEASURED.**
  - **NO PHYSICAL TDR IMPEDANCE PROFILING HAS BEEN PERFORMED.**
  - In a digital-only deliverables scope, $90\,\Omega$ differential compliance is classified as a **design assumption** that must be experimentally confirmed on physical prototypes in Phase 5.
