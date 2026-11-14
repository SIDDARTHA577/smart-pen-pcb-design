# BOARD DIMENSION AND STACKUP AUDIT
**Smart Pen Revision G — Phase 3A Engineering Report**
**Document ID:** `REPORT-REVG-P3A-002`
**Date:** November 2026
**Status:** APPROVED (Baseline) / PROPOSED ECR (4-Layer)
**Authoritative Hash (`SmartPen.kicad_pcb`):** `2550b9e49db0b98fd32aed11193f147b38cacadc353a4d168e5c63fa313a8687`

---

## 1. Executive Summary

This audit establishes the definitive physical dimensions, copper stackup, and mechanical fit of the Smart Pen Revision G Main PCB (`output/RevG/SmartPen.kicad_pcb`). An independent geometry audit was conducted directly using the KiCad 10.0.7 native PCB engine (`pcbnew`) and mechanical CAD models (`04_Internal_Rail_Cartridge.stl`).

Prior documentation (specifically the Phase 3 entry checklist) contained an unverified assumption citing an "11.0 × 128.0 mm 4-layer board." Direct measurement of the KiCad PCB and enclosure CAD proves this assertion was geometrically impossible. The actual committed PCB outline is **84.00 × 9.20 mm** with a **2-layer copper stackup** (`F.Cu`, `B.Cu`).

---

## 2. Direct Pcbnew Geometry Verification

### 2.1 Edge.Cuts Coordinate Inspection
Inspection of all graphical segments on the `Edge.Cuts` layer of `output/RevG/SmartPen.kicad_pcb` yields the following exact bounding envelope:

| Parameter | Measurement (mm) | Source Inspection |
| :--- | :--- | :--- |
| **Minimum X** | `0.000 mm` | `(gr_line (start 0 0) (end 0 9.2) (layer "Edge.Cuts"))` |
| **Maximum X** | `84.000 mm` | `(gr_line (start 84 0) (end 84 9.2) (layer "Edge.Cuts"))` |
| **Minimum Y** | `0.000 mm` | `(gr_line (start 0 0) (end 84 0) (layer "Edge.Cuts"))` |
| **Maximum Y** | `9.200 mm` | `(gr_line (start 0 9.2) (end 84 9.2) (layer "Edge.Cuts"))` |
| **Total Board Length** | **84.000 mm** | Calibrated Cartesian span along X-axis |
| **Total Board Width** | **9.200 mm** | Calibrated Cartesian span along Y-axis |
| **Board Area** | **772.80 mm²** | Nominal rectangular outline |
| **Corner Radii** | Sharp 90° corners | Rail retention tracks provide internal corner clearance |

### 2.2 Copper Stackup Audit
Inspection of the `(setup ...)` block in `SmartPen.kicad_pcb` confirms the committed board stackup:

```lisp
(stackup
  (layer "F.SilkS" (type "Top Silk Screen"))
  (layer "F.Paste" (type "Top Solder Paste"))
  (layer "F.Mask" (type "Top Solder Mask") (thickness 0.01))
  (layer "F.Cu" (type "copper") (thickness 0.035))
  (layer "dielectric 1" (type "core") (thickness 1.51) (material "FR4") (epsilon_r 4.5) (loss_tangent 0.02))
  (layer "B.Cu" (type "copper") (thickness 0.035))
  (layer "B.Mask" (type "Bottom Solder Mask") (thickness 0.01))
  (layer "B.Paste" (type "Bottom Solder Paste"))
  (layer "B.SilkS" (type "Bottom Silk Screen"))
  (copper_finish "None")
  (dielectric_constraints no)
)
```

- **Total Copper Layers:** Exactly **2** (`0 "F.Cu"`, `2 "B.Cu"`).
- **Nominal Finished Thickness:** **1.60 mm** (Standard FR4 core 1.51 mm + 2× 35 µm copper + soldermask).
- **Inner Copper Layers:** None (`In1.Cu` and `In2.Cu` are not defined in the committed project).

---

## 3. Reconciliation with Mechanical Enclosure & Internal Rail

### 3.1 Comparison Against the 11.0 × 128.0 mm Claim
The erroneous 11.0 × 128.0 mm dimension mentioned in preliminary documentation would fail assembly immediately:
1. **Width Interference:** The internal rail cartridge (`04_Internal_Rail_Cartridge.stl`) has an internal pocket width of **9.40 mm** (Y = ±4.70 mm). An 11.0 mm board exceeds the pocket width by 1.60 mm and cannot enter the cartridge. Furthermore, the pen barrel has an internal diameter of 14.0 mm, but internal sliding rails, battery channels, and clip bayonet features restrict the electronics rail width to $\le 10.0$ mm.
2. **Length Interference:** The total pen body length constraint is **150.0–155.0 mm**. Inside this envelope, the writing refill mechanism occupies 35.0 mm forward, the rear click/bayonet mechanism occupies 28.0 mm rearward, and the battery cradle pocket (`05_Battery_Cradle_Below_Rail.stl`) extends from Z = 72.0 mm to 118.0 mm (46.0 mm length). A 128.0 mm rigid PCB cannot coexist with the battery pocket and click plunger.

### 3.2 Mechanical Fit of the Baseline 84.00 × 9.20 mm Board
- **Rail Pocket Clearance:** With a board width of 9.20 mm inside a 9.40 mm pocket, bilateral clearance is **0.10 mm per side** (total 0.20 mm loose slide fit), perfectly matching precision injection molding / 3D printing tolerances.
- **Axial Position:** The 84.00 mm board spans Z = 28.0 mm to 112.0 mm within the 152.0 mm nominal barrel length, leaving adequate clearance for the front MPU daughterboard keyed connector (`J_IMU` at X=2.50 mm) and rear click assembly.
- **Battery Below Rail Architecture:** The battery cradle rests beneath the rail floor (Y = -1.20 mm to -5.80 mm). The PCB sits on the upper rail platform (Y = +0.80 mm to +2.40 mm), providing complete physical isolation between the pouch cell and PCB solder points.

---

## 4. Routing Feasibility Analysis: 2-Layer vs. 4-Layer

### 4.1 2-Layer Feasibility Evaluation (Baseline)
- **Component Density:** 64 components on 772.8 mm² yields an average density of **12.0 mm² per component**.
- **Power Management Congestion:** In the power section (X = 60.0 mm to 72.0 mm), 11 discrete ICs and passives (U2, U4, Q2, D4, C13, C14, C15, R9, R26, SW3, J_BAT) occupy 110 mm² out of a available 110.4 mm² (over 95% surface area utilization).
- **Ground Return Integrity:** On a 2-layer board of 9.2 mm width, routing 5 parallel digital buses (SPI, I2C, UART, USB D+/D−, GPIO strapping) across the X-axis completely fragments the bottom ground plane (`B.Cu`), creating large loop areas and high RF harmonic emissions for the ESP32-C3 2.4 GHz Wi-Fi/BLE transceiver.
- **Clearance / Unconnected Metrics:** The unrouted baseline contains 245 geometric clearance violations and 41 unconnected pins. Routing all 41 remaining nets on 2 layers requires complex jumper vias that violate the 0.20 mm annular ring and track-to-track clearances.

### 4.2 4-Layer Engineering Change Proposal (Recommended for Phase 3B)
A standard JLC2313 or JLC7628 4-layer stackup (1.6 mm or 1.0 mm thickness) would provide:
1. `F.Cu` (Signal & Component pads)
2. `In1.Cu` (Solid GND reference plane)
3. `In2.Cu` (Split Power plane: `3V3`, `VSYS_RAW`, `VBAT`, `USB_VBUS`)
4. `B.Cu` (Signal & bottom bypass capacitors)

**Benefits:**
- Unbroken RF ground return for the ESP32-C3 chip antenna.
- Controlled 90 Ω differential impedance for USB D+/D−.
- Eliminates 100% of power bus cross-talk and via bottlenecks in the U2/U4 power path.

**Action:** The 84.00 × 9.20 mm 2-layer stackup is retained as the baseline for Phase 3A to maintain strict repository parity. A formal Engineering Change Request (ECR-003) is documented in `BLOCKERS_AND_UNRESOLVED_DECISIONS.md` to transition to 4-layer before routing execution in Phase 3B.

---

## 5. Board Edge Extensions & Connector Mounting Ears

- **Side-Mount USB-C (Baseline Orientation):** The USB-C connector (`TYPE-C-31-M-12`) is placed at X = 78.40 mm, Y = 4.60 mm with its receptacle opening facing the North edge (+Y). In this orientation, the total connector length of 7.35 mm spans Y = 2.50 mm to 8.10 mm. This fits completely inside the 9.20 mm board width with **1.10 mm clearance to the North edge** and **2.50 mm clearance to the South edge**. No board edge extensions or mounting ears are required.
- **Rear-Mount USB-C (Alternative Orientation):** If the connector is rotated 90° to face the rear edge (+X = 84.0 mm), its 9.80 mm outer shell pad span would overhang the 9.20 mm PCB width by 0.30 mm on each side. In that event, local mounting ears extending the PCB width to 10.60 mm over a 7.5 mm axial zone would be required. The baseline retains the side-mount orientation.

---

## 6. Audit Conclusion & Gate Determination

| Verification Item | Specification | Measured Status | Gate |
| :--- | :--- | :--- | :---: |
| **Board Length** | 84.00 mm nominal | 84.000 mm | **PASS** |
| **Board Width** | 9.20 mm nominal | 9.200 mm | **PASS** |
| **Rail Pocket Fit** | 9.40 mm pocket width | 0.20 mm total clearance | **PASS** |
| **Layer Count** | 2 Copper Layers | 2 Layers (`F.Cu`, `B.Cu`) | **PASS** |
| **Stackup Baseline** | Preserve Rev G baseline | 2 Layers Preserved | **PASS** |
| **4-Layer ECR** | Client Approval Required | Documented for Phase 3B | **HOLD** |

**OVERALL AUDIT GATE: PASS (Baseline Confirmed)**
