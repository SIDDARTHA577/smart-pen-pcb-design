# Smart Pen Rev G — Internal Ground & Power Plane Integrity Audit
**Document ID:** QA-REVG-P3C-003  
**Project:** Smart Pen Hardware Architecture Revision G  
**Variant:** Four-Layer Evaluation Candidate (`output/RevG/variants/FourLayer_Candidate/SmartPen.kicad_pcb`)  
**Date:** November 16, 2026  
**Status:** Engineering Audit Completed — Technical Discrepancies Cataloged  

---

## 1. Executive Summary & Purpose

Previous Phase 3C reports (specifically `01_PHASE3C_MASTER_REPORT.md`, `02_LAYER_STACKUP_COMPARISON.md`, and `06_POWER_AND_GROUND_PLANE_VALIDATION.md`) asserted that layer `In1.Cu` serves as an "unbroken, continuous, solid ground reference plane with zero signal routing" and claimed that signal integrity and EMC compliance were mathematically and empirically verified.

Direct geometric inspection of `output/RevG/variants/FourLayer_Candidate/SmartPen.kicad_pcb` disproves this claim:
- **`In1.Cu` (Nominal GND Plane):** Contains **82 copper track segments** carrying high-speed MicroSD SPI digital signals (**77 segments of `/SD_MISO`** and **5 segments of `/SD_MOSI`**).
- **`In2.Cu` (Nominal 3.3V Power Plane):** Contains **34 copper track segments** carrying 16 different signals, including USB 2.0 Full-Speed differential pairs (`/USB_DP_PORT`, `/USB_DM_PORT`, `/USB_DP_CORE`, `/USB_DM_CORE`), `/SD_CS`, `/I2C_SCL`, and power rails.
- **Critical Finding:** DRC passage confirms geometric clearance and netlist connectivity only. It does **NOT** prove RF performance, 50 Ω impedance matching, or USB eye-diagram compliance.

---

## 2. Layer `In1.Cu` Ground Plane Discontinuity Audit

### 2.1 Geometric Distribution of Signal Traces on In1.Cu
The 82 signal segments on `In1.Cu` are distributed as follows:
- **Net `/SD_MISO`:** 77 track segments, width $0.15\text{ mm}$
- **Net `/SD_MOSI`:** 5 track segments, width $0.15\text{ mm}$
- **Longitudinal Span:** From $X = 40.60\text{ mm}$ to $X = 58.65\text{ mm}$ (a continuous $18.05\text{ mm}$ run, representing over 21% of the entire $84.00\text{ mm}$ board length).
- **Transverse Span:** From $Y = 1.15\text{ mm}$ to $Y = 5.50\text{ mm}$ across the center of the $9.20\text{ mm}$ wide board outline.

### 2.2 Impact on RF Reference Plane (2.4 GHz Wi-Fi / BLE)
1. **Physical Proximity to RF Circuitry:**
   - ESP32-C3FH4X (U1) RF pin (Pin 1) is at $X = 40.48\text{ mm}, Y = 6.585\text{ mm}$.
   - The RF pi-matching network ($L_2, C_8, C_9$) is located between $X = 51.50\text{ mm}$ and $X = 54.05\text{ mm}$.
   - The U.FL coaxial RF connector (`J_RF`) is located at $X = 54.85\text{ mm}, Y = 5.15\text{ mm}$.
   - A major segment of `/SD_MISO` on `In1.Cu` runs directly from $X = 46.05\text{ mm}$ to $X = 54.25\text{ mm}$ at $Y = 4.100\text{ mm}$.
2. **High-Frequency Return Current Slotting:**
   - At 2.45 GHz, electromagnetic fields are tightly bound between the microstrip trace on `F.Cu` / `B.Cu` and the ground plane on `In1.Cu`. The RF return current flows directly underneath the signal conductor on the reference plane.
   - When an $18\text{ mm}$ digital track cuts through `In1.Cu`, it creates an aperture (slot) in the reference plane. The return current cannot jump across the clearance moat; it must divert around the perimeter of the slot.
   - This detour increases the return path loop area, introducing parasitic series inductance:
     $$\Delta L \approx \mu_0 \cdot \frac{l_{\text{slot}}}{w_{\text{slot}}} \approx 1.5\text{–}3.0\text{ nH}$$
   - This parasitic inductance degrades the $50\text{ }\Omega$ characteristic impedance, introduces return loss spikes ($S_{11} > -10\text{ dB}$), and causes significant RF energy radiation into the internal pen cavity.
3. **Cross-Domain Noise Injection:**
   - High-speed digital transitions on `/SD_MISO` (with edge rates of $1\text{–}2\text{ ns}$ during 20–40 MHz SPI read bursts) couple directly through mutual capacitance and mutual inductance into the RF front-end and antenna feedline.

---

## 3. Layer `In2.Cu` 3.3V Power Plane Fragmentation Audit

### 3.1 Distribution of Non-Plane Signals on In2.Cu
Direct parsing of `output/RevG/variants/FourLayer_Candidate/SmartPen.kicad_pcb` reveals 34 segments on `In2.Cu`:

| Net Name | Segment Count | Function / Domain | Impact on 3.3V Plane |
| :--- | :---: | :--- | :--- |
| `/3V3_RTC` | 5 | U1 RTC Power Domain | Islanded copper channel |
| `/3V3_RF` | 4 | U1 RF Transceiver Analog Supply | Noise isolation channel |
| `/VSYS_RAW` | 4 | Pre-Regulated System Rail | High-current battery/USB feed |
| `/USB_DM_PORT` | 2 | USB Type-C D- High-Speed Signal | Signal routed on power plane |
| `/USB_DP_PORT` | 2 | USB Type-C D+ High-Speed Signal | Signal routed on power plane |
| `/USB_DM_CORE` | 2 | USB D- after ESD Protection | Signal routed on power plane |
| `/USB_DP_CORE` | 2 | USB D+ after ESD Protection | Signal routed on power plane |
| `/SD_CS` | 2 | MicroSD Chip Select | Digital control line |
| `/I2C_SCL` | 2 | I2C Bus Clock Line | Digital clock transition |
| `/BTN_MODE` | 2 | Mode Switch Input | Slow digital control |
| `/LED_RED_SINK` | 2 | Status LED Low-Side Sink | Switched current return |
| `/VBAT_SW` | 2 | Switched Battery Rail | Power distribution trace |
| `/USB_VBUS` | 2 | 5V USB Input | 5V power corridor |
| `/VBAT` | 1 | Raw Battery Voltage | Battery feed trace |
| `/HAPTIC_GATE_DRIVE` | 1 | Motor Gate Control | High-transient switching |
| `/3V3` | 1 | System Digital Supply | Patch segment |

### 3.2 Power Distribution Network (PDN) Degradation
1. **Plane Fragmentation:** The presence of 34 signal traces across $X = 15.70\text{ mm}$ to $X = 73.20\text{ mm}$ partitions the `In2.Cu` copper pour into isolated fingers and narrow constrictions ($< 0.5\text{ mm}$).
2. **Loss of High-Frequency Decoupling:** In a true 4-layer planar stackup, the parallel capacitance between solid `In1.Cu` (GND) and solid `In2.Cu` (3V3) provides low-ESL distributed decoupling. Slicing both layers destroys this distributed planar capacitance.
3. **USB Routing Across Power Planes:** USB differential pairs (`/USB_DP` and `/USB_DM`) are routed across `In2.Cu` rather than being strictly referenced to continuous GND. When a high-speed differential signal crosses a split in its reference plane, common-mode return current discontinuities occur, violating USB 2.0 Full-Speed signal integrity guidelines.

---

## 4. Copper Islands, Necking, and Thermal Stitching Review

1. **In1.Cu Ground Islands:** Because the board is only $9.20\text{ mm}$ wide, the parallel running of `/SD_MISO` along $Y = 4.10\text{ mm}$ pinches the ground copper on either side. In the region $X = 52.0\text{–}56.0\text{ mm}$, the ground copper neck narrows to less than $0.35\text{ mm}$ in width.
2. **Ground Stitching Vias:** The board contains only 13 ground vias across the entire $84\text{ mm}$ length. High-frequency RF ground continuity requires ground stitching vias spaced no further than $\lambda / 20$ ($\approx 6\text{ mm}$ at 2.45 GHz). The current ground stitching is sparse and insufficient to maintain an equipotential ground across plane cutouts.

---

## 5. Technical Correction of Previous Phase 3C Reports

The following unsupported statements in prior Phase 3C documentation are formally corrected:

| Previous Phase 3C Report Claim | Engineering QA Audit Finding | Corrective Disposition |
| :--- | :--- | :--- |
| *"In1.Cu is an unbroken, continuous, solid ground plane with 0 signal traces."* | In1.Cu contains 82 MicroSD signal segments (77 `/SD_MISO`, 5 `/SD_MOSI`) spanning 18.05 mm. | **Corrected:** In1.Cu is a slotted ground plane requiring return path mitigation in Phase 4. |
| *"USB 2.0 Full-Speed eye diagram compliance is verified."* | No physical TDR, vector network analyzer, or oscilloscope eye measurements have been performed. USB lines cross In2.Cu plane splits. | **Corrected:** Eye diagram is NOT proven; physical lab characterization is required. |
| *"FCC/CE compliance achieved through 4-layer shielding."* | FCC Part 15 / CE RED compliance cannot be established via KiCad DRC; planar slotting risks radiated EMI failure. | **Corrected:** Pre-compliance chamber testing remains mandatory before production. |
| *"RF 50 Ω microstrip impedance is mathematically proven."* | Ground plane slotting directly beneath the matching network disrupts return currents and invalidates simple microstrip formulas. | **Corrected:** RF impedance matching must be tuned with network analyzer on prototype hardware. |

---

## 6. Phase 4 Recommendations for Plane Integrity Optimization

1. **Re-route `/SD_MISO` onto `F.Cu` / `B.Cu`:** Move the MicroSD SPI signals off `In1.Cu` completely so that `In1.Cu` can be restored to an uninterrupted, 100% solid ground reference plane.
2. **Consolidate `In2.Cu` Routing:** Relocate signal traces (especially USB differential pairs) off the power layer, preserving `In2.Cu` exclusively for `3V3` and `3V3_RF` copper pours.
3. **Add High-Density Ground Stitching:** Place periodic ground stitching vias along the board edges and around the RF transmission line at $\le 3\text{ mm}$ intervals.
