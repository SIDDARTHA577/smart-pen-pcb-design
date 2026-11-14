# BLOCKERS AND UNRESOLVED DECISIONS
**Smart Pen Revision G — Phase 3A Engineering Deliverable**
**Document ID:** `REPORT-REVG-P3A-010`
**Date:** November 2026
**Status:** ACTIVE AUDIT & FORMAL TRACKING
**Target Milestone:** Transition from Phase 3A to Phase 3B

---

## 1. Executive Summary

This log establishes the authoritative status of all technical blockers, unresolved design decisions, and engineering change requests (ECRs) for the Smart Pen Revision G hardware project. Phase 3A has successfully resolved all schematic discrepancies, footprint inaccuracies, and pin mapping contradictions. Four primary architectural items are formally tracked below.

---

## 2. Active Technical Blockers

### Blocker 1: Battery Cradle Physical Tooling & Procurement Hold
- **Status:** **FORMAL HOLD / BLOCKED**
- **Affected Subsystems:** `05_Battery_Cradle_Below_Rail.stl`, Battery Sourcing (120–150 mAh LiPo pouch cell), Battery Solder Terminals.
- **Root Cause & Technical Analysis:**
  - The authoritative CAD model (`scripts/build_full_parametric_assembly.py`) provides an internal cradle cavity of:
    $$\text{Length} = 46.00\text{ mm}, \quad \text{Width} = 10.00\text{ mm}, \quad \text{Depth} = 4.60\text{ mm}$$
  - Standard pouch cells in this form factor (e.g., 401042 or 501040) have a nominal uncharged thickness of $4.00\text{ mm}$.
  - During standard operation and repeated cycling (300 cycles), lithium-ion polymer cells exhibit $8–10\%$ volumetric swelling:
    $$T_{\text{swelled}} = 4.00\text{ mm} \times 1.10 = 4.40\text{ mm}$$
  - Inside a 4.60 mm cavity, the remaining radial clearance is:
    $$\text{Margin} = 4.60\text{ mm} - 4.40\text{ mm} = \mathbf{0.20\text{ mm}}$$
  - Commercial consumer safety guidelines (UL 1642 / IEC 62133) require a minimum expansion allowance of $\ge 0.60\text{ mm}$ to prevent pouch rupture, rail binding, or localized stress on the PCB substrate.
- **Corrective Action Required:**
  1. Procure physical production samples of target 401042 cells from approved vendors (e.g., Grepow, EVE).
  2. Perform accelerated charge-discharge cycling in temperature chambers to record true dimensional delta.
  3. If swelling exceeds 0.20 mm, execute CAD modification to relieve cradle floor by 0.40–0.50 mm.
- **Milestone Impact:** Physical injection tooling and procurement must remain on **FORMAL HOLD** until laboratory test data confirms safety margins. Main PCB routing (Phase 3B) may proceed using the provisional envelope.

---

## 3. Unresolved Engineering Decisions

### Decision 1: 2-Layer Baseline vs. 4-Layer Copper Stackup (ECR-003)
- **Status:** **HOLD / PENDING CLIENT DECISION**
- **Affected Subsystems:** `output/RevG/SmartPen.kicad_pcb`, RF performance, EMC compliance, routing density.
- **Technical Context:**
  - The baseline design committed in the repository is a **2-layer PCB** (84.00 × 9.20 mm).
  - Zone 4 (Power management) contains 14 components on 184 mm² (>70% surface density).
  - Routing 41 remaining connections across an 84 mm length on 2 layers requires horizontal signal stubs on `B.Cu` that segment the ground plane into isolated copper islands.
  - Slicing the ground plane directly degrades the ESP32-C3 2.4 GHz RF return path and increases radiated EMI on the USB differential pair.
  - Transitioning to a standard 4-layer stackup (JLC2313: `F.Cu`, `In1.Cu` [GND], `In2.Cu` [PWR], `B.Cu`) provides an unbroken RF reference plane and reduces routing congestion to near zero.
- **Client Decision Required:** Approve ECR-003 for 4-layer board fabrication (+~15% bare board cost delta) or accept 2-layer routing with compromised ground return.

---

### Decision 2: USB-C Physical Orientation & Mounting Ears (ECR-004)
- **Status:** **APPROVED FOR BASELINE (SIDE-MOUNT) / HOLD ON REAR-MOUNT**
- **Affected Subsystems:** `J_USB`, `01_Pen_Barrel.stl`, `04_Internal_Rail_Cartridge.stl`.
- **Technical Context:**
  - **Baseline Placement:** Side-mount orientation ($0^\circ$ rotation, opening facing North edge $+Y$). Fits 100% within the 9.20 mm board width with 1.10 mm solid FR4 edge clearance and requires no PCB modifications.
  - **Rear-Mount Option:** $90^\circ$ rotation facing pen tail ($+X$). Outer shell stake pads span 9.80 mm, overhanging the 9.20 mm board by 0.30 mm per side. Implementing this requires adding 10.60 mm wide PCB mounting ears and milling relief slots into the rear internal rail cartridge.
- **Client Decision Required:** Reconfirm preference for pen cap side-charging aperture vs. tail axial plugging.

---

## 4. Fully Resolved Engineering Decisions (Phase 3A Closure)

The following historical contradictions and hazards were fully investigated and definitively resolved during Phase 3A:

| Decision / Issue | Prior Confusion | Authoritative Resolution | Status |
| :--- | :--- | :--- | :---: |
| **MPU Connector Interface** | 5-pin claim vs 4-pin netlist | **Confirmed 4-pin interface** (`3V3`, `GND`, `SDA`, `SCL`). Firmware uses 100–200 Hz I2C polling; INT pin is unconnected; 0 free ESP32 GPIOs available. | **RESOLVED (PASS)** |
| **ESP32-C3 USB Pin Mapping** | Pins 12/13 vs Pins 25/26 | **Physical Pins 25 (`USB_DM`) & 26 (`USB_DP`)**. Verified against ESP32-C3FH4X datasheet and KiCad schematic symbol. | **RESOLVED (PASS)** |
| **TP4054 Charge Resistor R9** | 1.2 kΩ (1.0 A fire hazard) | **10 kΩ (`RC0402FR-0710KL`) installed**, commanding safe 100 mA charge rate for small pen pouch cells. | **RESOLVED (PASS)** |
| **ESP32-C3 Boot Strapping** | Floating GPIO8 / NC flash pins | **R27 (10 kΩ pullup) installed** to 3V3 on GPIO8 (U1 Pin 14). Flash pins cleared from GND to NC nets. | **RESOLVED (PASS)** |
| **U4 LDO Regulator Output** | Pin 5 shorted to EN / VIN | **Pin 5 routed strictly to Net 2 (`/3V3`)**. Enable (Pin 3) tied to `/VBAT_SW`. | **RESOLVED (PASS)** |
| **Q2 P-MOSFET Orientation** | Body diode backfeeding | **Drain tied to `/VBAT`, Source tied to `/VSYS_RAW`**. Reverse-biases body diode during USB 5V operation. | **RESOLVED (PASS)** |
| **True PCB Dimensions** | 11.0 × 128.0 mm (Impossible) | **84.00 × 9.20 mm baseline validated** directly in Pcbnew and matched to 9.40 mm rail cartridge pocket. | **RESOLVED (PASS)** |
| **Schematic Parity Violations** | 35 parity mismatches | **0 Footprint / Parity Errors achieved** on Main PCB via native KiCad 10.0.7 synchronization. | **RESOLVED (PASS)** |

---

## 5. Decision & Blocker Summary Matrix

```
+-----------------------------------------------------------------------------------------+
| Item ID  | Title                               | Severity | Owner       | Target Gate   |
+-----------------------------------------------------------------------------------------+
| BLK-001  | Battery Pouch Expansion Hold        | HIGH     | Mech / Sourcing | TOOLING FREEZE|
| ECR-003  | 4-Layer Copper Stackup Transition   | MEDIUM   | EE / Client | PHASE 3B ENTRY|
| ECR-004  | USB-C Rear Orientation Mounting Ears| LOW      | ID / Mech   | ENCLOSURE FREEZE|
| RES-001  | 4-Pin MPU Connector Parity          | RESOLVED | EE Systems  | CLOSED (PASS) |
| RES-002  | ESP32-C3 USB Pins 25/26             | RESOLVED | EE Systems  | CLOSED (PASS) |
| RES-003  | TP4054 Safe 100 mA Charging (R9)    | RESOLVED | EE Systems  | CLOSED (PASS) |
| RES-004  | GPIO8 Boot Strapping (R27)          | RESOLVED | EE Systems  | CLOSED (PASS) |
| RES-005  | 84.0 × 9.2 mm Board Dimensions      | RESOLVED | EE / Mech   | CLOSED (PASS) |
+-----------------------------------------------------------------------------------------+
```
