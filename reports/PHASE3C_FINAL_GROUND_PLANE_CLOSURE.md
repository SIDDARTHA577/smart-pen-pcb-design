# Smart Pen Rev G — Final Ground-Plane and SPI Routing Closure
**Document ID:** RPT-REVG-P3C-GND-CLOSURE  
**Project:** Smart Pen Hardware Architecture Revision G  
**Variant:** Four-Layer Evaluation Candidate (`output/RevG/variants/FourLayer_Candidate/SmartPen.kicad_pcb`)  
**Git Branch:** `engineering/revg-production`  
**Base Commit:** `f76aab08831da7bf26516d4a1a39215d754e0d73`  
**Date:** November 16, 2026  
**Status:** Geometric & Return-Path Audit Complete; Architectural Resolutions Formulated  

---

## 1. Executive Summary

This report delivers the authoritative geometric and signal return-path audit of the four-layer Smart Pen Revision G candidate PCB (`output/RevG/variants/FourLayer_Candidate/SmartPen.kicad_pcb`). While the board achieves complete physical routing closure with **0 KiCad DRC violations, 0 unconnected pads, 0 schematic parity errors, and 0 footprint library mismatches**, an in-depth electromagnetic audit reveals an electrical integrity trade-off:
1. **Internal Layer 1 (`In1.Cu`) Ground Reference Interruption:** 82 signal segments (77 `/SD_MISO`, 5 `/SD_MOSI`) traverse `In1.Cu` (the designated primary GND reference plane) across $X = 40.60\text{ mm}$ to $X = 58.65\text{ mm}$, cutting an $18\text{ mm}$ slot directly below the 2.4 GHz RF matching network and U.FL antenna connector `J_RF`.
2. **Internal Layer 2 (`In2.Cu`) Power Plane Fragmentation:** 34 signal segments traverse `In2.Cu` (the $+3.3\text{V}$ power plane), including USB differential traces and power distribution sub-nets.
3. **Bottom Layer (`B.Cu`) Saturation:** 10 parallel longitudinal bus traces occupy the bottom layer, creating an impermeable barrier to simple single-layer rerouting on an ultra-narrow $9.20\text{ mm}$ board width.

This document details the electromagnetic return-path consequences, empirical layer-shift experiments, and defensible architectural solutions for Phase 4.

---

## 2. Layer Stackup & Baseline Net Allocation

The four-layer candidate utilizes the standard $1.60\text{ mm}$ core-and-prepreg stackup (JLCPCB JLC04161H-7628 equivalent):

| Layer | Type | Nominal Thickness | Copper Weight | Primary Intended Function | Actual Routing Utilization |
| :--- | :--- | :---: | :---: | :--- | :--- |
| **F.Cu (L1)** | Signal / Mixed | $0.035\text{ mm}$ (1 oz) | Top Component Pads & High-Speed Traces | 178 track segments; SMD pads for U1, U2, U3, U4, J_USB, J_SD, J_RF |
| *Dielectric 1* | Prepreg 7628 | $0.210\text{ mm}$ | $\epsilon_r \approx 4.4$ | High-frequency microstrip reference dielectric | Reference plane height $H_1 = 0.210\text{ mm}$ |
| **In1.Cu (L2)**| Plane / Mixed | $0.035\text{ mm}$ (1 oz) | **Continuous GND Reference Plane** | **GND Copper Pour + 82 Signal Segments** (77 `/SD_MISO`, 5 `/SD_MOSI`) |
| *Dielectric 2* | Core FR4 | $1.065\text{ mm}$ | $\epsilon_r \approx 4.5$ | Structural core separation | Core height $H_2 = 1.065\text{ mm}$ |
| **In2.Cu (L3)**| Plane / Mixed | $0.035\text{ mm}$ (1 oz) | **Continuous +3.3V Power Plane** | **3.3V Copper Pour + 34 Signal Segments** (`/3V3_RF`, `/USB_DP_CORE`, etc.) |
| *Dielectric 3* | Prepreg 7628 | $0.210\text{ mm}$ | $\epsilon_r \approx 4.4$ | Bottom microstrip reference dielectric | Reference plane height $H_3 = 0.210\text{ mm}$ |
| **B.Cu (L4)** | Signal / Mixed | $0.035\text{ mm}$ (1 oz) | Bottom Escape Traces & Secondary GND Pour | 51 track segments; 10 longitudinal bus lines; GND flood |

---

## 3. Detailed Physical Inspection of Internal Layer 1 (`In1.Cu`)

### 3.1 Trace Distribution on In1.Cu
Inspection of the board database confirms that `In1.Cu` contains exactly 82 track segments:
- **Net `/SD_MISO`:** 77 track segments, width $w = 0.150\text{ mm}$.
- **Net `/SD_MOSI`:** 5 track segments, width $w = 0.150\text{ mm}$.

Bounding box of `In1.Cu` signal routing:
$$\text{X-Span: } 40.600\text{ mm to } 58.650\text{ mm} \quad (\Delta X = 18.050\text{ mm})$$
$$\text{Y-Span: } 1.150\text{ mm to } 5.500\text{ mm} \quad (\Delta Y = 4.350\text{ mm})$$

### 3.2 Proximity to 2.4 GHz RF Matching Network and J_RF
The high-frequency 2.4 GHz frontend components reside on `F.Cu` in the immediate vicinity of this slot:
- **Microcontroller U1 (ESP32-C3FH4X) RF Pin (Pin 1 / LNA_IN):** $(40.480, 6.585)$
- **Series Inductor L2 (`LQP03TN2N4B02D`):** $(52.200, 5.300)$
- **Shunt Capacitor C8 (`GRM0335C1H1R5BA01D`):** $(52.500, 3.600)$
- **Shunt Capacitor C9 (`GRM0335C1H1R5BA01D`):** $(54.050, 3.550)$
- **Coaxial Receptacle J_RF (`U.FL-R-SMT-1(10)`):** $(54.850, 5.150)$
- **Feedline Net `/RF_OUT`:** Microstrip from L2 Pad 2 $(52.480, 5.300)$ to J_RF Pad 1 $(54.850, 5.150)$.

Direct euclidean distance measurements from the RF components on F.Cu to the `/SD_MISO` track segments on `In1.Cu` yield:
- **Distance to Shunt Capacitor C8:** **$0.500\text{ mm}$**
- **Distance to Shunt Capacitor C9:** **$0.550\text{ mm}$**
- **Distance to U.FL Receptacle J_RF Center Pin:** **$0.680\text{ mm}$**
- **Distance to Matching Inductor L2:** **$1.200\text{ mm}$**
- **Distance to `/RF_OUT` Feedline Corridor:** **$1.200\text{ mm}$**

```
F.Cu (L1):             [L2]----/RF_OUT---->[J_RF: (54.85, 5.15)]
                         |                     | (Ground Pads)
Prepreg Dielectric:   ========================================== H = 0.210 mm
                         :                     :
In1.Cu (L2):        ---GND--- [==== /SD_MISO SLOT ====] ---GND---
                               ^ (Distance to J_RF: 0.68 mm!)
```

### 3.3 Electromagnetic & Signal Integrity Return-Path Impact

1. **RF Ground Return Current Diversion:** At 2.4 GHz ($\lambda \approx 12.5\text{ cm}$), return currents in the ground plane travel directly underneath the signal trace within a narrow corridor ($\approx 3 \times$ trace width). The ground pads of `J_RF` (Pads 2 & 3 @ $X = 53.400$ and $X = 56.300$) must return high-frequency current back to U1's thermal ground pad (EPAD @ $X = 42.880, Y = 4.835$). Because `/SD_MISO` slices a continuous void across $X = 54.25\text{ mm}$ to $X = 57.30\text{ mm}$, RF return currents cannot take the path of minimum loop inductance. Instead, currents are forced around the perimeter of the slot, introducing parasitic series inductance ($\Delta L \approx 1\text{--}2\text{ nH}$), which alters the complex load impedance presented to U1's LNA/PA.
2. **Cross-Domain Noise Injection:** MicroSD SPI transfers operate at 20–25 MHz with edge rise/fall times $t_r \approx 1.5\text{--}2.5\text{ ns}$. High-frequency Fourier harmonics extend well above 500 MHz. Capacitive and inductive coupling between the `/SD_MISO` slot and the RF feedline injects transient switching spikes into the RF receive chain, degrading receiver sensitivity and increasing packet error rate (PER).
3. **Power Plane Discontinuities on In2.Cu:** `In2.Cu` (+3.3V plane) contains 34 track segments. While less sensitive than the RF ground plane, signals crossing these plane splits experience reference shifts, requiring displacement current through inter-plane capacitance ($C_{\text{plane}} \approx 15\text{ pF/in}^2$).

---

## 4. Empirical Rerouting Investigations & Technical Blockers

To determine whether the smallest safe correction could reroute `/SD_MISO` and `/SD_MOSI` off `In1.Cu`, automated sandbox routing experiments were executed using native KiCad 10 tools on an exact replica of the project workspace.

### 4.1 Trial A: Shifting `/SD_MOSI` from In1.Cu to B.Cu
- **Hypothesis:** Net `/SD_MOSI` has only 5 segments on In1.Cu between via $(41.130, 1.650)$ and via $(58.650, 3.350)$. Both vias are already through-hole `F.Cu -> B.Cu`.
- **Experimental Result:** Moving these 5 segments to `B.Cu` produced **9 DRC violations** (6 `tracks_crossing`, 3 `clearance`).
- **Root Cause:** On B.Cu, `/SD_SCK` runs horizontally at $Y = 1.150\text{ mm}$ and `/CHG_STAT` runs at $Y = 1.800\text{ mm}$ and $Y = 2.300\text{ mm}$. Between $X = 41.450$ and $X = 43.600$, the `/SD_MOSI` trajectory intersects the via pad of `/3V3_RTC` @ $(42.130, 1.800)$ and crosses `/CHG_STAT`, creating unavoidable shorts without shifting surrounding nets.

### 4.2 Trial B: Shifting `/SD_MISO` from In1.Cu to B.Cu
- **Hypothesis:** Move `/SD_MISO` (77 segments) from `In1.Cu` to `B.Cu`.
- **Experimental Result:** Produced **32 DRC violations** (multiple dead shorts: `shorting_items` with `/CHG_STAT` and `/VBAT_SW`, plus `tracks_crossing`).
- **Root Cause:** `/SD_MISO` originates at U1 Pin 13 / via $(41.630, 1.200)$ and terminates at J_SD Pad 5 / via $(57.300, 5.500)$. To traverse from $Y = 1.200\text{ mm}$ to $Y = 5.500\text{ mm}$ on `B.Cu`, the trace must cross two continuous longitudinal power/status tracks:
  1. `/CHG_STAT` running at $Y = 1.800\text{ mm}$ from $X = 44.0\text{ mm}$ to $X = 66.05\text{ mm}$.
  2. `/VBAT_SW` running at $Y = 4.400\text{ mm}$ from $X = 40.5\text{ mm}$ to $X = 62.96\text{ mm}$.
  No single-layer crossing is physically possible on B.Cu without intersecting these active nets.

### 4.3 Trial C: Shifting `/SD_MISO` from In1.Cu to In2.Cu (+3.3V Plane)
- **Hypothesis:** Move `/SD_MISO` to `In2.Cu` to restore `In1.Cu` as a pure GND plane.
- **Experimental Result:** Produced **365 DRC violations**, including 8 unconnected nets and severe thermal starvation.
- **Root Cause:** `In2.Cu` already carries localized escape routing for `/3V3_RTC`, `/SD_CS`, `/3V3_RF`, `/VSYS_RAW`, and `/USB_DP_CORE`. `/SD_MISO` directly collided with `/3V3_RTC` near U1 and severed copper supply channels to the 3.3V pour.

### 4.4 Synthesis: Why a 4-Layer 9.2 mm Board Forces This Bottleneck
The Smart Pen PCB geometry is exceptionally constrained:
- **Aspect Ratio:** $84.00\text{ mm} \times 9.20\text{ mm}$ (Length-to-Width ratio $> 9:1$).
- **Net Count:** 46 active routed electrical nets.
- **Longitudinal Freeway:** B.Cu already carries 10 parallel bus traces: `/UART_TX`, `/UART_RX`, `/XTAL_N`, `/RF_LNA`, `/USB_DM_CORE`, `/VBAT_SW`, `/CHG_STAT`, `/SD_SCK`, `/3V3`, `/BOOT9`.
- **Component Congestion:** F.Cu is saturated by U1 (QFN-32), U2, U3, U4, J_USB, J_SD, J_RF, and passives.

Because `F.Cu` and `B.Cu` are saturated, any multi-pin bus traversing the length of the board (such as the 4-signal MicroSD SPI bus) is forced to borrow routing space from the internal planes (`In1.Cu` and `In2.Cu`). Blindly pushing traces across layers without modifying component placement immediately violates KiCad 10 design rules.

---

## 5. Architectural Recommendations for Phase 4

In accordance with project instructions ("Do not restart PCB routing from zero... If a safe four-layer solution is infeasible, document the exact blocker instead of entering another indefinite routing loop"), two clear paths are presented for Phase 4:

### Option 1 (Primary Engineering Recommendation): Transition to 6-Layer Stackup
- **Stackup Architecture:**
  - L1 (Top): Signal (Components, RF microstrip, short escapes)
  - L2 (In1): **Solid GND Reference Plane (100% continuous, zero signal traces)**
  - L3 (In2): High-Speed Digital Signal Routing (MicroSD SPI, USB differential)
  - L4 (In3): Low-Speed Signal / Peripheral Routing (I2C, GPIO, Status)
  - L5 (In4): **Solid Power Plane (+3.3V and battery rails)**
  - L6 (Bottom): Ground Flood / Shielding / Local Escapes
- **Benefits:**
  - Completely restores `In1.Cu` as an unbroken ground plane under the RF front-end, eliminating the 18 mm slot.
  - Keeps USB and SPI digital return currents isolated from the RF reference.
  - Easily accommodates standard $1.60\text{ mm}$ total board thickness at standard fab vendors (e.g. JLCPCB JLC06161H-7628).
  - Cost Delta: Moderate (~$15–$25 additional tooling cost per prototype batch, negligible in production volume).

### Option 2 (Alternate 4-Layer Recommendation): Strategic Floorplan Revision
- If a four-layer stackup must be preserved:
  1. **Mirror / Flip `J_SD` Pinout:** Reorienting the FFC connector or daughterboard pinout allows SPI traces to escape on the opposite side of the board ($Y < 2.0\text{ mm}$), away from the RF matching network ($Y > 5.0\text{ mm}$).
  2. **Relocate Series Resistors / Diode D4:** Moving D4 longitudinally creates surface routing space on F.Cu for `/SD_MISO`, removing it from `In1.Cu`.

---

## 6. Verification Status of Candidate PCB

The candidate PCB file (`output/RevG/variants/FourLayer_Candidate/SmartPen.kicad_pcb`) remains fully verified and preserved in its zero-error baseline state:
- **KiCad DRC Violations:** **0**
- **Unconnected Pads:** **0**
- **Schematic Parity Discrepancies:** **0**
- **Footprint Library Mismatches:** **0**
- **Native DRC Exit Code:** `0`
- **Native ERC Exit Code:** `0`

The board is electrically complete and manufacturable, with the ground-plane slot formally characterized as a documented technical risk for client and Phase 4 review.
