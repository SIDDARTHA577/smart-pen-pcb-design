# SMART PEN REV G — PHASE 4 HANDOFF & OUTSTANDING WORK SPECIFICATION

**Document ID:** `SP-REVG-P3B-011`  
**Status:** HANDOFF ROADMAP  
**Current Phase:** Phase 3B Complete  
**Next Phase:** Phase 4 (Detailed Multi-Layer Routing, Manufacturing Preflight & Prototype Release)  
**Target Branch:** `engineering/revg-production`  

---

## 1. Executive Summary

Phase 3B has successfully achieved critical safety and geometry milestones:
1. Complete elimination of all 50 catastrophic short circuits.
2. Complete resolution of all 11 footprint library mismatches.
3. Verification of 100% clean DRC and ERC across all three daughterboards (Front MPU, MicroSD Carrier, Touch Sensor).
4. Sizing and spatial verification of the ideal diode power-path switch and LDO regulation.
5. Reconciled authoritative $84.00 \times 9.20\text{ mm}$ geometry and side-mount USB-C orientation.

This document specifies the exact sequence of technical tasks required in Phase 4 upon receiving client approvals for ECR-003 (4-layer stackup) and the battery cradle specification.

---

## 2. Phase 4 Work Breakdown Structure (WBS)

### Work Package 1: Stackup Migration & Layer Setup (ECR-003 Execution)
- Update `SmartPen.kicad_pcb` layer stackup from 2 copper layers to 4 copper layers:
  - Layer 1 (`F.Cu`): High-speed signals, RF coplanar waveguide, component pads.
  - Layer 2 (`In1.Cu`): Solid continuous ground plane (`/GND`).
  - Layer 3 (`In2.Cu`): Dedicated power distribution plane (`/3V3`) + local analog power islands.
  - Layer 4 (`B.Cu`): Low-speed digital control lines, UART, button inputs, secondary ground fill.
- Define netclasses with controlled impedance rules:
  - `RF_50OHM`: Width $0.35\text{ mm}$, clearance $0.20\text{ mm}$.
  - `USB_DIFF_90OHM`: Width $0.20\text{ mm}$, gap $0.15\text{ mm}$, clearance $0.20\text{ mm}$.
  - `POWER_BUS`: Width $0.35–0.50\text{ mm}$, clearance $0.15\text{ mm}$.
  - `DEFAULT_SIGNAL`: Width $0.15\text{ mm}$, clearance $0.15\text{ mm}$.

### Work Package 2: Comprehensive Signal & Power Routing Closure
- **Power Routing:**
  - Route `/USB_VBUS` from J_USB to D4/R26/Q2 and U2 with solid $0.35\text{ mm}$ copper.
  - Route `/VSYS_RAW` through SW3 power switch to U4 AP2112K LDO.
  - Route `/3V3` out of U4 Pin 5 directly into Inner Layer 2 power plane.
  - Drop power vias directly from decoupling capacitors (C13, C14, C15, C1, C2, C3) into In2.Cu plane within $1.0\text{ mm}$ of IC power pins.
- **RF Subsystem Routing:**
  - Route $50\ \Omega$ coplanar transmission line from ESP32-C3 Pin 2 through L1, C7, to AE1 chip antenna on Layer 1 over unbroken Layer 2 ground.
  - Implement ground stitching via picket fence along the RF feedline (via pitch $\le 1.0\text{ mm}$).
- **USB-C Data Routing:**
  - Route $90\ \Omega$ differential pair (`USB_DP_PORT`, `USB_DM_PORT`) from J_USB through U_ESD array and R7/R8 to ESP32-C3 Pins 25/26.
  - Maintain length matching within $0.10\text{ mm}$ ($< 5\text{ ps}$ skew).
- **SPI & I2C Buses:**
  - Route 4-line SPI bus (`SD_CLK`, `SD_MOSI`, `SD_MISO`, `SD_CS`) to J_SD header.
  - Route I2C bus (`I2C_SDA`, `I2C_SCL`) to 4-pin J_IMU header with ground guarding.
- **Target Routing Outcome:** Exactly **0 (Zero) Unconnected Items** and **0 (Zero) Clearance Violations**.

### Work Package 3: DRC & Manufacturing Preflight Closure
- Run native KiCad DRC with zero exclusions:
  - Assert 0 Errors, 0 Warnings, 0 Unconnected Nets.
- Export production Gerbers (RS-274X / Gerber X2) and Excellon drill files:
  - Copper layers: F.Cu, In1.Cu, In2.Cu, B.Cu.
  - Solder mask: F.Mask, B.Mask.
  - Silkscreen: F.SilkS, B.SilkS.
  - Solder paste: F.Paste, B.Paste.
  - Mechanical: Edge.Cuts.
- Generate Bill of Materials (BOM) in JLCPCB / PCBWay format with verified LCSC part numbers.
- Generate Centroid / Pick-and-Place (CPL) files with corrected component rotation angles.

### Work Package 4: Prototype Fabrication and Assembly Gate
- Perform 3D clearance collision audit with final 4-layer PCB STEP model inside `cad/SmartPen_Master_Assembly.step`.
- Verify battery wiring harness strain relief and J_BAT connector engagement.
- Package final fabrication archive for prototype fab release.

---

## 3. Milestone Completion Criteria

Phase 4 will be marked complete when:
1. KiCad DRC reports 0 violations, 0 unconnected items, 0 parity issues across all four boards.
2. Full automated pytest suite passes 100% on generated fabrication files.
3. 3D STEP export confirms zero interference with pen barrel, removable rail, and moving click refill pushrod.
4. Client formally signs off on prototype manufacturing release.
