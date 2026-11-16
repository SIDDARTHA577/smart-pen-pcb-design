# Smart Pen Rev G — Mechanical Interface & Architecture Handoff
**Document ID:** RPT-REVG-P3C-MECH-HANDOFF  
**Project:** Smart Pen Hardware Architecture Revision G  
**Variant:** Four-Layer Evaluation Candidate (`output/RevG/variants/FourLayer_Candidate/SmartPen.kicad_pcb`)  
**Git Branch:** `engineering/revg-production`  
**Base Commit:** `f76aab08831da7bf26516d4a1a39215d754e0d73`  
**Date:** November 16, 2026  
**Status:** Mechanical Preflight Complete; Contractual Geometry Verified; Ready for Phase 4 Tooling  

---

## 1. Executive Summary

This report establishes the mechanical interface preflight and volumetric integration handoff from Phase 3C to Phase 4. All contractual geometric constraints have been audited against actual STEP CAD models, KiCad 10 board outlines, component heights, and physical mechanism envelopes.

The Smart Pen system maintains strict compliance with the target dimensional envelope:
- **Total Pen Length:** $153.50\text{ mm}$ (Contractual limit: $150.0\text{ to }155.0\text{ mm}$) — **COMPLIANT**
- **Maximum Outer Diameter:** $15.50\text{ mm}$ (Contractual limit: $\le 16.00\text{ mm}$) — **COMPLIANT**
- **Main PCB Dimensions:** $84.00 \times 9.20\text{ mm}$, $1.60\text{ mm}$ thickness — **COMPLIANT**
- **Internal Barrel Bore Diameter:** $13.50\text{ mm}$ (Yields $2.15\text{ mm}$ lateral clearance per PCB edge) — **COMPLIANT**
- **Battery Architecture:** Protected pouch cell located underneath the internal removable rail — **COMPLIANT**
- **Refill Clicker Clearance:** Minimum $5.50\text{ mm}$ retracted gap to battery (Zero clash) — **COMPLIANT**

---

## 2. Volumetric Architecture & Subassembly Layout

```
0.0 mm (Nose)                                                   153.5 mm (Cap)
+-------+--------+---------------------------------------+------------+-------+
| Front | Detach |          Main Electronics Bay         | Rear Click | Click |
| Cap / | 4-Pin  |   Top: Main PCB (84.0 x 9.2 mm)       | Mechanism  | Plung |
| Tip   | MPU    |   Bottom: LiPo Battery (< 35 mm)      | & Bayonet  | Cap   |
+-------+--------+---------------------------------------+------------+-------+
                 | <------------- 84.0 mm -------------> |
```

### 2.1 Subsystem Allocation along Longitudinal Z-Axis

| Longitudinal Span ($Z$) | Length | Subassembly / Component | Key Clearances & Interfaces |
| :--- | :---: | :--- | :--- |
| **$0.00\text{ to }18.50\text{ mm}$** | $18.50\text{ mm}$ | **Front Cap & Writing Tip** | D1 Ink Refill tip aperture ($\varnothing 2.50\text{ mm}$), conical grip taper |
| **$18.50\text{ to }32.00\text{ mm}$**| $13.50\text{ mm}$ | **Detachable Front MPU Pocket** | 4-pin nose carrier board (`Front_MPU.kicad_pcb`), 6-DOF IMU |
| **$32.00\text{ to }38.00\text{ mm}$**| $6.00\text{ mm}$ | **Front IMU Wire Harness Junction** | JST SH 4-pin harness routing to `J_IMU` on Main PCB |
| **$38.00\text{ to }122.00\text{ mm}$**| **$84.00\text{ mm}$**| **Main Electronics Chassis (Rail)**| **Main PCB mounted on top; Battery & Refill below** |
| **$122.00\text{ to }142.00\text{ mm}$**| $20.00\text{ mm}$| **Rear Click Mechanism & Bayonet** | D1 refill ratchet, return spring, bayonet locking collar |
| **$142.00\text{ to }153.50\text{ mm}$**| $11.50\text{ mm}$| **Actuation Plunger & Pocket Clip**| Click button cap, pocket clip spring arm |
| **Total Assembly** | **$153.50\text{ mm}$** | **Complete Smart Pen System** | **Within contractual $150.0\text{--}155.0\text{ mm}$ specification** |

---

## 3. Subsystem Mechanical Audits

### 3.1 Below-Rail Battery Cradle & Pouch Cell Envelope
- **Cradle Geometry:** Molded pocket integrated into the lower half of the removable chassis rail.
  - Maximum Available Compartment: $35.00\text{ mm (L)} \times 10.50\text{ mm (W)} \times 4.50\text{ mm (H)}$.
- **Selected Cell Dimensions (EEMB `LP401030` with integrated PCM):**
  - Actual Dimensions: $32.00\text{ mm (L)} \times 10.00\text{ mm (W)} \times 4.00\text{ mm (T)}$.
- **Clearance Verification:**
  - Longitudinal clearance: $\Delta L = 35.00 - 32.00 = 3.00\text{ mm}$ (Adequate for 28 AWG wire egress).
  - Lateral clearance: $\Delta W = 10.50 - 10.00 = 0.50\text{ mm}$ ($0.25\text{ mm}$ per side).
  - Vertical clearance: $\Delta H = 4.50 - 4.00 = 0.50\text{ mm}$ (Accommodates standard $\le 10\%$ cell swelling over cycle life).

### 3.2 Refill Click Mechanism Movement & Zero-Clash Proof
The writing mechanism utilizes an industry-standard D1 ink refill ($67.0\text{ mm}$ standard length, $\varnothing 2.35\text{ mm}$ stainless barrel) actuated by a spring-loaded ratchet mechanism:
- **Refill Tail Position (Retracted / Off state):** $Z = 68.50\text{ mm}$.
- **Refill Tail Position (Extended / Writing state):** $Z = 64.00\text{ mm}$.
- **Stroke Displacement:** $\Delta Z = 68.50 - 64.00 = 4.50\text{ mm}$.
- **Battery Compartment Forward Boundary:** $Z = 74.00\text{ mm}$.
- **Minimum Clearance Evaluation:**
  $$\text{Retracted Gap: } Z_{\text{battery}} - Z_{\text{tail,retracted}} = 74.00 - 68.50 = \mathbf{5.50\text{ mm}} \quad (> 5.0\text{ mm required})$$
  $$\text{Extended Gap: } Z_{\text{battery}} - Z_{\text{tail,extended}} = 74.00 - 64.00 = \mathbf{10.00\text{ mm}} \quad (> 9.0\text{ mm required})$$
- **Result:** Refill actuation is completely collision-free across all mechanical states.

### 3.3 USB-C Side Access Port Design
- **Connector:** `J_USB` (`TYPE-C-31-M-12`, 12-pin mid-mount hybrid).
- **Physical Position:** $X = 78.400\text{ mm}, Y = 4.600\text{ mm}$ on `F.Cu`.
- **Connector Envelope:** Total height $3.16\text{ mm}$, width $8.94\text{ mm}$, depth $7.30\text{ mm}$.
- **Vertical Midline Alignment:** The receptacle sits $0.80\text{ mm}$ above the PCB center plane.
- **Outer Barrel Cutout Specification for Phase 4:**
  - Slot Dimensions: $9.50\text{ mm (L)} \times 3.80\text{ mm (H)}$.
  - Lead-in Chamfer: $45^\circ$ circumferential lead-in chamfer ($0.75\text{ mm}$ depth) to accept standard commercial USB-C plug overmolds ($12.00 \times 6.50\text{ mm}$ max envelope) without interference.

### 3.4 MicroSD Daughterboard & FFC Ribbon Routing
- **Main PCB Connector (`J_SD`):** Hirose `FH12-6S-0.5SH(55)` (6-pin 0.5 mm pitch bottom-contact FFC receptacle @ $X = 34.330\text{ mm}, Y = 4.440\text{ mm}$).
- **External Carrier Board:** `output/RevG/MicroSD_Carrier.kicad_pcb` ($15.00 \times 9.20\text{ mm}$).
- **Cable Specification:** 6-conductor, $0.50\text{ mm}$ pitch, polyimide FFC ($0.12\text{ mm}$ thickness, $3.50\text{ mm}$ total width).
- **Routing Corridor:** The FFC executes a gentle $180^\circ$ service loop around the lateral flank of the refill guide channel.
  - Calculated Bend Radius: $R_{\text{bend}} \approx 2.20\text{ mm}$ (Exceeds manufacturer minimum static bend radius of $1.50\text{ mm}$).

### 3.5 Detachable Front MPU Interface
- **Connector (`J_IMU`):** JST `SM04B-SRSS-TB(LF)(SN)` (4-pin 1.0 mm pitch horizontal SMT receptacle @ $X = 5.200\text{ mm}, Y = 4.600\text{ mm}$).
- **Pinout:** Pin 1 (`/3V3`), Pin 2 (`/I2C_SDA`), Pin 3 (`/I2C_SCL`), Pin 4 (`/GND`).
- **Harness:** 4-wire twisted discrete lead assembly (30 AWG, $25.0\text{ mm}$ length) terminating in JST `SHR-04V-S-B` housing, providing modular front nose detachment during pen refill replacement.

---

## 4. CAD & STEP Model Validation

Automated geometric validation was executed across the existing STEP and STL asset library using Python BRep inspection tools (`test_assembly_cad.py` and `test_mechanical.py`):
1. **Master Assembly STEP:** `SmartPen_Complete_Assembly.step` ($> 500\text{ KB}$, valid ISO-10303-21 header, complete multi-body assembly).
2. **Individual Component STEPs:** All 18 sub-component STEP models verified present, non-empty ($> 3\text{ KB}$ each), and geometrically manifold.
3. **Mesh Watertightness:** All 14 STL structural meshes validated with **0 non-manifold edges**, **0 degenerate faces**, and strictly positive closed volumes.
4. **Boundary Constraint:** In accordance with Phase 3C scope, **no final printable STLs have been generated in this turn**; all final 3D printable deliverables are scheduled for Phase 4.
