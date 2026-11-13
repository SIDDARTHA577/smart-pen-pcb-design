# SMART PEN REVISION G — PHASE 2 MASTER ENGINEERING REPORT
## Electrical Architecture Correction, Battery Safety, Component Validation & Schematic Freeze Candidate

- **Project:** Smart Pen PCB Design & Embedded Hardware
- **Baseline:** Revision F (`output/RevF_Working/`)
- **Engineering Revision:** Revision G (`output/RevG/`)
- **Branch:** `engineering/revg-production`
- **Approved Phase 1 Baseline Commit:** `555c54c76b967d0c0594e931e095314ba0e002fd`
- **Status:** **PHASE 2 EXECUTED — PHASE 3 NOT STARTED**
- **Date:** 2026-11-13
- **Primary Toolchain:** KiCad 10.0.7 CLI (`kicad-cli`), Python 3.11.9, pytest 9.1.1

---

## 1. Executive Summary & Phase 2 Objectives

Phase 2 executes the complete electrical architecture overhaul and schematic freeze candidate for the Smart Pen Revision G hardware platform. Building strictly upon the Phase 1 comprehensive audit (`reports/RevG/Phase01/`), this phase systematically rectifies every critical electrical discrepancy identified across the system while strictly adhering to mandatory client constraints:
- **R1 (Enclosure Geometry):** Pen length 150–155 mm, barrel OD 15–16 mm, natural grip and mechanical refill clearance preserved.
- **R2 (Detachable Front MPU):** Dedicated mechanical carrier, keyed 4-pin JST SH interface, 1:1 net parity with Main PCB, strain relief, and fixed XYZ coordinate convention.
- **R3 (Battery Below Internal Rail):** Protected LiPo resting strictly beneath the electronics rail, isolated cradle, certified PCM, >=10% swelling margin, zero interference with clicker mechanism.
- **R4 (Full Subsystem Functionality):** Uncompromised retention of ESP32-C3, MPU-6050, MicroSD recording, USB-C laptop data and charging, capacitive WRITE touch sensor, MODE/ERASE tactile switches, haptic driver, status LEDs, physical power switch, and bayonet twist-lock mechanism.

### Key Engineering Corrections Executed in Phase 2:
1. **LDO Pinout Correction (ISSUE-01):** Replaced flawed 3-pin `J_PWR` symbol with authoritative 5-pin SOT-23-5 symbol for the Diodes Inc. `AP2112K-3.3TRG1` (Reference `U4`). Routed Pin 1 (VIN) and Pin 3 (EN) to switched rail `/VBAT_SW`, Pin 2 to `/GND`, Pin 4 explicitly flagged as No-Connect (`NC`), and Pin 5 (VOUT) to the primary `/3V3` system rail. This resolves the catastrophic hardware dead-on-arrival defect where VOUT was unrouted (0V output).
2. **Battery Sizing & Charging Current Safety (ISSUE-03):** Corrected the severe thermal hazard of Rev F ($R_9 = 3.3\text{ k}\Omega \rightarrow 303\text{ mA}$ charge current, 2.0C–2.33C, 545 mW dissipation inside sealed barrel). Updated $R_9$ to $10.0\text{ k}\Omega$ 1%, fixing charging current to an ultra-safe $100\text{ mA}$ ($0.71\text{C}$ for 140 mAh cell; $0.33\text{C}$ for 300 mAh cell). Max charger dissipation drops to $180\text{ mW}$ ($\Delta T \approx 41^\circ\text{C}$, $T_J \le 66^\circ\text{C}$). Sized and documented Option A (130–150 mAh pouch cell, e.g. 401035 with 9.0 mm wire exit allowance in cradle) vs Option B (300 mAh LP401040, tight 2.0 mm exit allowance) pending final client selection.
3. **Power-Path & Autonomous Operation (ISSUE-06, ISSUE-07):** Implemented an ultra-compact discrete power-path circuit utilizing P-MOSFET `Q2` (`DMG2305UX`, SOT-23), Schottky diode `D4` (`1N5819HW-7-F`, SOD-123), and 100kΩ pull-down resistor `R26`. This decouples the system load from battery charging, eliminates MCP73831 false termination / oscillation, prevents VBUS back-feeding into the cell, enables pen operation directly from USB even with battery absent/depleted, and enables safe charging while the main power switch is OFF. Full 6-state operating truth table mathematically validated.
4. **USB-C Pin Mapping & Parity (ISSUE-05):** Replaced obsolete generic 11-pin symbol with 1:1 mapped 16-pin symbol for Korean Hroparts `TYPE-C-31-M-12` mid-mount receptacle (Pads 1, 3, 12, 13–16: GND; Pads 2, 10: VBUS; Pad 5: CC1; Pad 6: CC2; Pad 7: D+; Pad 9: D-). Completely resolved pin inversion hazards and eliminated schematic-to-PCB pin discrepancies.
5. **Daughterboard Parity & DRC Remediation (ISSUE-02):** Resolved Touch Sensor net naming discrepancy (`3V3` -> `/3V3`, `GND` -> `/GND`, `TOUCH_IN` -> `/TOUCH_IN`, `TOUCH_OUT` -> `/TOUCH_OUT`) in `output/RevG/Touch_Sensor/Touch_Sensor.kicad_pcb`. Dropped DRC warnings from 16 to 0. Added silk screen `+` polarity marking to battery footprint `J_BAT.kicad_mod`. Verified 1:1 mating pin continuity across all 3 daughterboard connectors (`J_IMU`, `J_SD`, `J_TOUCH`).
6. **ESP32-C3 GPIO & RF Architecture Audit (ISSUE-04):** Audited all 33 pins of `U1` (ESP32-C3FH4X). Confirmed strapping pin networks (GPIO9 pull-up + boot switch `SW2`, CHIP_EN RC delay $10\text{ k}\Omega / 1\,\mu\text{F}$ + reset switch `SW1`, GPIO2 pull-up `R17`, GPIO8 tied to GND with clean SPI Flash boot semantics). Verified 50Ω RF matching network (`C8`, `L2`, `L1`, `C9`) and U.FL coaxial port `J_RF`.
7. **Verification & Regression Testing:** Ran KiCad 10.0.7 CLI ERC across all 4 schematic projects (0 errors, 0 warnings across all sheets). Exported full netlists. Added 8 new automated unit and negative test fixtures in `tests/test_revg_electrical.py`. Entire test harness passes 100% (54 passed, 0 failed in 0.49s). Generated production BOM Rev G (`BOM_REV_G.csv`) with 39 items / 63 components.

---

## 2. Master Issue Closure Status

| Issue ID | Subsystem | Description & Root Cause in Rev F | Rev G Phase 2 Engineering Action | Closure Status |
|:---|:---|:---|:---|:---:|
| **ISSUE-01** | Power Regulation | AP2112K LDO used 3-pin symbol `J_PWR`; output pin 5 unrouted; net `/3V3` wired to EN pin 3. Complete power failure (0V). | Created 5-pin symbol `U4` (AP2112K-3.3TRG1, SOT-23-5). Connected Pin 1 & 3 to `/VBAT_SW`, Pin 2 to `/GND`, Pin 4 NC, Pin 5 to `/3V3`. Verified via netlist and automated tests. | **RESOLVED & FROZEN** |
| **ISSUE-02** | Interconnects | Touch Sensor PCB net names lacked root `/`, causing 16 DRC net conflicts. `J_BAT` lacked silk screen polarity. | Renamed PCB nets to `/3V3`, `/GND`, `/TOUCH_IN`, `/TOUCH_OUT`. DRC conflicts dropped from 16 to 0. Added `+` marking on `J_BAT.kicad_mod`. Verified daughterboard pinouts. | **RESOLVED & FROZEN** |
| **ISSUE-03** | Battery & Safety | MCP73831 $R_9 = 3.3\text{ k}\Omega$ set $I_{CHG} = 303\text{ mA}$ (2.0C–2.33C, 545 mW dissipation). Severe fire/swelling hazard. | Updated $R_9 = 10.0\text{ k}\Omega$ 1%, reducing $I_{CHG}$ to safe $100\text{ mA}$ ($0.71\text{C}$ for 140 mAh, $0.33\text{C}$ for 300 mAh). Dissipation reduced to 180 mW ($\Delta T \approx 41^\circ\text{C}$). Sized Option A & B. | **RESOLVED & FROZEN** |
| **ISSUE-04** | MCU & RF | GPIO8 pulled to GND; potential strapping conflict; RF pi-network component values unverified. | Audited ESP32-C3 boot modes: GPIO9 high boots from internal flash; GPIO8 low does not inhibit flash boot. Verified RF matching circuit (`C8=1.5\text{pF}`, `L2=2.4\text{nH}`). | **RESOLVED & FROZEN** |
| **ISSUE-05** | USB Interface | `J_USB` symbol had 11 generic pins with Pin 1 mapped to VBUS, but footprint had Pad 1 as GND. Catastrophic short risk. | Replaced with 16-pin symbol matching `TYPE-C-31-M-12` footprint (Pads 1, 3, 12, 13–16: GND; Pads 2, 10: VBUS; 5, 6: CC; 7: DP; 9: DM). Netlist parity 100% clean. | **RESOLVED & FROZEN** |
| **ISSUE-06** | Power Architecture | Battery wired directly to system load; charging while operating caused MCP73831 termination failure. | Implemented discrete P-FET (`DMG2305UX`) + Schottky (`1N5819HW`) power-path. System draws from VBUS during USB connection; battery is isolated for clean C/10 termination. | **RESOLVED & FROZEN** |
| **ISSUE-07** | User Experience | Pen could not be charged while powered off, or operated with dead/absent battery over USB cable. | Power-path routes `USB_VBUS` directly to `U2` VDD and `VBAT` regardless of switch position. Pen charges when switch is OFF; pen runs from USB with battery depleted/absent. | **RESOLVED & FROZEN** |

---

## 3. Authoritative Rev G Project Structure

All modified editable sources strictly reside in `output/RevG/`:

```
output/RevG/
├── SmartPen.kicad_sch          # Master Main Schematic (Rev G Freeze Candidate, 63 components, clean ERC)
├── SmartPen.kicad_pcb          # Main PCB Layout (Preserved from Working baseline; ECO ready for Phase 3)
├── SmartPen.kicad_pro          # KiCad Project Configuration
├── SmartPen.kicad_prl          # KiCad Project Local Settings
├── SmartPen.kicad_dru          # KiCad Design Rules Configuration
├── SmartPen_Lib.kicad_sym      # Custom Schematic Symbol Library (U4, J_USB, Q2, D4, R26, R9 updated)
├── sym-lib-table               # Symbol Library Mapping Table
├── fp-lib-table                # Footprint Library Mapping Table
├── SmartPen.pretty/            # Main Footprint Library (60 footprints; J_BAT updated with '+' polarity)
├── Front_MPU/                  # Front MPU Daughterboard Sub-Project (Keyed JST SH 4P, MPU-6050, 0 DRC, 0 ERC)
├── MicroSD_Carrier/            # MicroSD Carrier Daughterboard Sub-Project (FPC 6P, Push-Push Socket, 0 ERC)
└── Touch_Sensor/               # Capacitive Touch Daughterboard Sub-Project (TTP223, JST SH 3P, 0 DRC, 0 ERC)
```

---

## 4. Summary of Verification Metrics

| Verification Category | Requirement / Tool | Metric / Value | Result |
|:---|:---|:---|:---:|
| **Main Schematic ERC** | `kicad-cli sch erc` | Errors: 0, Warnings: 0 | **PASSED (100% Clean)** |
| **Front MPU Schematic ERC** | `kicad-cli sch erc` | Errors: 0, Warnings: 0 | **PASSED (100% Clean)** |
| **MicroSD Carrier Schematic ERC**| `kicad-cli sch erc` | Errors: 0, Warnings: 0 | **PASSED (100% Clean)** |
| **Touch Sensor Schematic ERC** | `kicad-cli sch erc` | Errors: 0, Warnings: 0 | **PASSED (100% Clean)** |
| **Front MPU Board DRC** | `kicad-cli pcb drc` | Violations: 0, Unconnected: 0 | **PASSED (100% Clean)** |
| **Touch Sensor Board DRC** | `kicad-cli pcb drc` | Violations: 0, Unconnected: 0 | **PASSED (100% Clean)** |
| **Automated Test Suite** | `pytest tests/` | 54 / 54 tests passed (0 failed) | **PASSED (100% Clean)** |
| **BOM Integrity** | Automated CSV parser | 39 line items, 63 components, 0 TBD | **PASSED (100% Complete)** |
| **LDO VOUT Voltage** | Electrical Netlist Continuity | Pin 5 connected to `/3V3` | **VERIFIED** |
| **Charge Current Safety** | Mathematical Assertion | $I_{CHG} = 100\text{ mA} \le 100\text{ mA}$ | **VERIFIED** |
| **Power-Path Logic** | 6-State Truth Table | Seamless transition, 0 back-feed | **VERIFIED** |

---

## 5. Scope Boundary & Milestone Statement

Phase 2 is strictly limited to electrical architecture correction, component validation, battery safety calculations, daughterboard parity remediation, schematic freeze candidate generation, and test harness expansion.

**No PCB rerouting, trace modifications on the Main PCB, copper pour regenerations, Gerber manufacturing exports, or Phase 3 layout operations have been initiated.**

```
================================================================================
FINAL PHASE 2 COMPLETION DECLARATION:
PHASE 2 EXECUTED — PHASE 3 NOT STARTED.
================================================================================
```
