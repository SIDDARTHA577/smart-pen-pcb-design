# SMART PEN REVISION G — PHASE 3 PCB ROUTING & LAYOUT PREPARATION
## Layout Strategy, Design Rules, Stack-Up & Manufacturing Constraints

- **Project:** Smart Pen PCB Design
- **Document ID:** `REVG-DOC-RTE-001`
- **Revision:** Rev G Phase 2 Freeze Candidate
- **Author:** Senior KiCad PCB Layout & DFM Engineer

---

## 1. Executive Summary & Objective

This document defines the physical constraints, routing rules, layer stack-up, impedance targets, component layout guidelines, and Design for Manufacturing (DFM) requirements prepared for **Phase 3 (PCB Rerouting & Physical Layout)**.

The overarching design objective is to route the newly validated Rev G schematic into the narrow $11.0\text{ mm} \times 88.0\text{ mm}$ internal rail while preserving 100% mechanical compatibility with the $15.0\text{ mm}$ barrel and removable electronics chassis.

---

## 2. Layer Stack-Up & Substrate Configuration

The Smart Pen Main PCB utilizes a standard, cost-effective 2-layer FR-4 stack-up compatible with JLCPCB / PCBWay standard production:

```
+----------------------------------------------------------------------------------------------------+
|                                    2-LAYER FR-4 STACK-UP SPECIFICATION                             |
+-------+--------------+------------------+------------------+------------------+--------------------+
| Layer | Layer Name   | Material Type    | Copper Thickness | Dielectric H     | Functional Usage   |
+-------+--------------+------------------+------------------+------------------+--------------------+
| L1    | `F.Cu` (Top) | Copper (1 oz)    | 35 µm (1.4 mil)  | -                | Components, Signals|
| -     | Dielectric   | FR-4 Core        | -                | 0.93 mm (36 mil) | Mechanical Base    |
| L2    | `B.Cu` (Bot) | Copper (1 oz)    | 35 µm (1.4 mil)  | -                | Solid Ground Plane |
+-------+--------------+------------------+------------------+------------------+--------------------+
| Total | Board Thick  | FR-4 Standard    | Total: 1.00 mm ± 10% (Required for internal rail slots) |
+-------+--------------+------------------+------------------+------------------+--------------------+
```

### 2.1 Critical Mechanical Thickness Note
- Nominal board thickness must remain strictly **$1.00\text{ mm}$** (not $1.60\text{ mm}$).
- The 3D-printed internal rail (`04_Internal_Rail.step`) features precision card-guide slots designed for $1.0\text{ mm}$ PCB thickness with a $+0.15\text{ mm}$ sliding clearance. A $1.6\text{ mm}$ board will physically fail to slide into the rail.

---

## 3. High-Speed & RF Controlled Impedance Targets

### 3.1 50-Ohm Single-Ended RF Trace (`RF_LNA` to `J_RF`)
- **Target Characteristic Impedance ($Z_0$):** $50\,\Omega \pm 10\%$.
- **Topology:** Coplanar Waveguide with Ground (CPWG) on Top Layer (`F.Cu`).
- **Trace Width ($W$):** $0.45\text{ mm}$ ($17.7\text{ mil}$).
- **Ground Gap ($S$):** $0.20\text{ mm}$ ($7.9\text{ mil}$).
- **Substrate Height ($H$):** $0.93\text{ mm}$ (to Bottom Layer ground plane).
- **Dielectric Constant ($\epsilon_r$):** 4.5 @ 2.4 GHz.
- **Continuous Ground Shielding:** Ground via fence with via-to-via pitch $\le 1.5\text{ mm}$ along the entire length of the RF trace to suppress spurious harmonic radiation and prevent coupling into adjacent digital buses.

### 3.2 90-Ohm Differential USB Data Lines (`USB_DP` / `USB_DM`)
- **Target Differential Impedance ($Z_{diff}$):** $90\,\Omega \pm 10\%$.
- **Trace Width ($W$):** $0.25\text{ mm}$ ($10\text{ mil}$).
- **Differential Spacing ($S$):** $0.20\text{ mm}$ ($8\text{ mil}$).
- **Length Matching:** Intra-pair skew $\le 0.5\text{ mm}$ ($< 3\text{ ps}$ delay skew).
- **Reference Plane:** Unbroken ground plane on `B.Cu` beneath the entire route from `J_USB` through `U_ESD` to ESP32-C3 Pins 25/26. Zero plane splits or cross-talk cuts permitted.

---

## 4. Design Rules & Clearance Constraints

The KiCad design rules file (`output/RevG/SmartPen.kicad_dru`) establishes the manufacturing constraints:

```
+----------------------------------------------------------------------------------------------------+
|                                    PHASE 3 PCB DESIGN RULES MATRIX                                 |
+----------------------------------------+-------------------+-------------------+-------------------+
| Parameter                              | Standard Rule     | Power Rails       | RF / USB Diff     |
+----------------------------------------+-------------------+-------------------+-------------------+
| Minimum Trace Width                    | 0.15 mm (6 mil)   | 0.40 mm (16 mil)  | 0.45 mm (CPWG)    |
| Minimum Clearance (Copper-to-Copper)   | 0.15 mm (6 mil)   | 0.20 mm (8 mil)   | 0.20 mm (8 mil)   |
| Minimum Via Drill Diameter             | 0.30 mm (12 mil)  | 0.35 mm (14 mil)  | 0.30 mm (12 mil)  |
| Minimum Via Annular Ring               | 0.15 mm (6 mil)   | 0.18 mm (7 mil)   | 0.15 mm (6 mil)   |
| Copper-to-Board-Edge Clearance         | 0.30 mm (12 mil)  | 0.50 mm (20 mil)  | 0.50 mm (20 mil)  |
| Solder Mask Expansion                  | 0.05 mm (2 mil)   | 0.05 mm (2 mil)   | 0.05 mm (2 mil)   |
| Minimum Solder Mask Dam                | 0.10 mm (4 mil)   | 0.10 mm (4 mil)   | 0.10 mm (4 mil)   |
| Silk Screen Text Size                  | 0.8 mm x 0.8 mm   | 0.8 mm x 0.8 mm   | 0.8 mm x 0.8 mm   |
| Silk Screen Minimum Thickness          | 0.15 mm (6 mil)   | 0.15 mm (6 mil)   | 0.15 mm (6 mil)   |
+----------------------------------------+-------------------+-------------------+-------------------+
```

---

## 5. Critical Phase 3 Routing Directives

1. **LDO Output Routing (`U4` Pad 5 to `/3V3`):**
   - Connect Pad 5 immediately to bulk ceramic capacitor `C2` ($10\,\mu\text{F}$) using a wide polygon or $0.50\text{ mm}$ trace.
   - Route `/3V3` as a star distribution tree or wide trunk ($0.40\text{ mm}$ to $0.60\text{ mm}$) along the center of the board, branching off to decoupling capacitors at `U1`, `U3`, `J_IMU`, `J_SD`, and `J_TOUCH`.
2. **Power-Path Local Cluster (`Q2`, `D4`, `R26`, `U2`):**
   - Place components within the $72\text{ mm} - 82\text{ mm}$ zone on the top layer.
   - Maintain minimum trace width of $0.40\text{ mm}$ for `/USB_VBUS` and `/VBAT` to handle $500\text{ mA}$ maximum inrush and fault currents without resistive drops.
3. **Solid Ground Plane (`B.Cu`):**
   - Keep the bottom copper layer as unbroken ground plane to the maximum extent possible (> 85% continuous copper coverage).
   - Any signal crossing on the bottom layer must be short ($\le 5\text{ mm}$) and immediately returned to the top layer.
4. **Thermal Relief on ESP32-C3 Center EPAD (Pad 33):**
   - Place a $3 \times 3$ array of thermal vias ($0.3\text{ mm}$ drill, $0.6\text{ mm}$ pad) in the exposed die pad to conduct heat efficiently into the bottom copper plane.
