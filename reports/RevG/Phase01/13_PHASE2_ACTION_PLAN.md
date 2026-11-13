# Smart Pen Rev G — Phase 2: Implementation & Repair Action Plan

**Document ID**: `reports/RevG/Phase01/13_PHASE2_ACTION_PLAN.md`  
**Execution Date**: November 13, 2026  
**Revision Baseline**: Revision F  
**Target Development Revision**: Revision G  
**Branch**: `engineering/revg-production`  

---

## 1. Executive Summary

Based on the baseline audit, ERC/DRC execution, electrical netlist analysis, and DFM findings in Phase 1, this document defines the prioritized engineering work packages for **Revision G Phase 2**.

**Execution Rule**: Phase 2 implementation will not begin until Phase 1 reports are reviewed, committed, pushed to GitHub, and formally approved.

---

## 2. Prioritized Engineering Work Packages

```
[ WP1: Critical Power & LDO Fixes ] ---> [ WP2: Schematic & Footprint Parity ]
                     |
                     v
[ WP3: Main PCB Rerouting & DRC Closure ] ---> [ WP4: DFM, Panel & Silkscreen ]
                     |
                     v
[ WP5: Live Test Harness Overhaul ] ---> [ WP6: Mechanical Prototype Package ]
```

---

### Work Package 1: Critical Power Architecture & Battery Safety Repairs
**Priority**: **P0 (Mandatory Electrical Prerequisite)**  
**Target Files**:
- `output/RevG/SmartPen.kicad_sch` (cloned from `output/RevF_Working/SmartPen.kicad_sch`)
- `output/RevG/SmartPen.pretty/`
- `output/RevG/SmartPen_RevG_BOM.csv`

**Action Steps**:
1. **Resolve LDO Regulator Pinout & Symbol (`ISSUE-01`)**:
   - Create dedicated KiCad symbol `U4` (`AP2112K-3.3TRG1`) with all 5 active pins:
     - Pin 1: `VIN` $\rightarrow$ Connect to Net `/VBAT_SW` (or power-path output).
     - Pin 2: `GND` $\rightarrow$ Connect to Net `/GND`.
     - Pin 3: `EN` $\rightarrow$ Connect to Net `/VBAT_SW` (enables regulator when switched on).
     - Pin 4: `NC` $\rightarrow$ No connection.
     - Pin 5: `VOUT` $\rightarrow$ Connect to Net `/3V3` (System 3.3V Logic Rail).
   - Deprecate the misnamed symbol `J_PWR`. Replace reference designator with `U4`.
   - Update footprint pad mapping to match standard SOT-23-5 pinout.
2. **Recalculate Charging Current Resistor R9 (`ISSUE-03`)**:
   - Validate true physical LiPo cell capacity:
     - For 130–150 mAh cell: Replace `R9` (3.3 kΩ) with **10.0 kΩ ±1%** ($I_{CHG} = 100\text{ mA}$, 0.67C–0.77C safe charge rate).
     - If client approves 300 mAh cell: Set `R9` to **6.8 kΩ ±1%** ($I_{CHG} = 147\text{ mA}$, 0.49C charge rate).
   - Prevents cell overheating and swelling in the enclosed pen barrel.
3. **Implement True Dynamic Power-Path Circuit (`ISSUE-06`, `ISSUE-07`)**:
   - Add P-channel MOSFET (`DMG2305UX` or equivalent low-$R_{DS(on)}$ SOT-23 P-FET) and Schottky diode (`1N5819HW` or `MBR0520L`) between `USB_VBUS`, `VBAT`, and LDO `VIN`:
     - Gate of P-FET pulled to `USB_VBUS`.
     - Source connected to `VBAT_SW`, Drain connected to LDO `VIN`.
     - Diode cathode connected to LDO `VIN`, anode to `USB_VBUS`.
   - Result:
     - When USB is disconnected: Gate is pulled low via 100 kΩ resistor, P-FET turns ON, battery powers LDO.
     - When USB is connected: Gate is pulled high to 5V, P-FET turns OFF, diode powers LDO directly from USB 5V while MCP73831 independently charges the battery.
     - Resolves the MCP73831 C/10 charge termination interference and enables USB operation on empty battery or switch OFF.
4. **Add Battery Polarity Silkscreen (`ISSUE-11`)**:
   - Add permanent `+` graphic silkscreen adjacent to Pin 1 on `J_BAT.kicad_mod` on `F.SilkS` and `F.Fab`.

---

### Work Package 2: Schematic & Footprint Parity Corrections
**Priority**: **P1 (High Priority)**  
**Target Files**:
- `output/RevG/SmartPen.kicad_sch`
- `output/RevG/SmartPen.pretty/J_USB.kicad_mod`
- `output/RevG/Touch_Sensor/Touch_Sensor.kicad_pcb`
- `output/RevG/Front_MPU/Front_MPU.kicad_sch`

**Action Steps**:
1. **Correct USB-C Receptacle Pin Mapping (`ISSUE-05`)**:
   - Map exact manufacturer pinout for `TYPE-C-31-M-12`:
     - Pins A1, B1, A12, B12 $\rightarrow$ GND
     - Pins A4, B4, A9, B9 $\rightarrow$ VBUS
     - Pin A5 $\rightarrow$ CC1, Pin B5 $\rightarrow$ CC2
     - Pins A6, B6 $\rightarrow$ DP, Pins A7, B7 $\rightarrow$ DM
   - Eliminate all pad net mismatches in KiCad schematic-parity check.
2. **Synchronize Touch Sensor Net Names (`ISSUE-14`)**:
   - Update `Touch_Sensor.kicad_pcb` net names with hierarchical `/` prefix (`/3V3`, `/GND`, `/TOUCH_IN`, `/TOUCH_OUT`) to eliminate 16 parity warnings.
3. **Front MPU Bus Pull-Up Optimization (`ISSUE-15`)**:
   - Mark `R1` and `R2` (4.7k) on `Front_MPU.kicad_sch` as **DNP (Do Not Populate)** to prevent redundant 2.35 kΩ bus loading against Main PCB pull-ups `R10`, `R11`.

---

### Work Package 3: Main PCB Interactive Routing & Zero-DRC Closure
**Priority**: **P0 (Layout Integrity)**  
**Target Files**:
- `output/RevG/SmartPen.kicad_pcb`

**Action Steps**:
1. **Quarantine Client Delivery PCB (`ISSUE-02`)**:
   - Discard `output/RevF_Client_Delivery/.../SmartPen.kicad_pcb`.
   - Branch `output/RevG/SmartPen.kicad_pcb` directly from `output/RevF_Working/SmartPen.kicad_pcb`.
2. **Route Highway Corridors on B.Cu (`ISSUE-04`)**:
   - Move colliding power trace `/VBAT_SW` away from strapping via `/STRAP2` and I2C via `/I2C_SCL`.
   - Separate MicroSD SPI tracks (`/SD_SCK`, `/SD_MOSI`, `/SD_MISO`, `/SD_CS`) into a clean 0.20 mm track / 0.15 mm space bus along North edge (Y = 1.0 to 2.8 mm).
   - Stagger vias around U1 (ESP32-C3) and U3 (MCP23008) in a 45° diamond pattern.
3. **Complete 29 Unconnected Net Escapes**:
   - Route MCP23008 GPIO lines to tactile switches SW4, SW5, LEDs D1, D2, and haptic gate.
   - Route J_IMU I2C lines to ESP32-C3 GPIO8/GPIO9.
4. **DRC Validation Gate**:
   - Run official KiCad 10 CLI DRC:
     ```powershell
     kicad-cli pcb drc --severity-all --all-track-errors --schematic-parity --refill-zones SmartPen.kicad_pcb
     ```
   - Target acceptance gate: **Exit code 0, 0 violations, 0 unconnected, 0 parity errors**.

---

### Work Package 4: DFM, Assembly & Manufacturing Preparation
**Priority**: **P1 (Manufacturing Feasibility)**  
**Target Files**:
- `output/RevG/SmartPen.kicad_pcb`
- `output/RevG/06_Fabrication_Drawing/`

**Action Steps**:
1. **Optical Fiducials**:
   - Add two diagonal SMT fiducials (1.0 mm circular copper pad, 2.0 mm mask opening) on F.Cu at (X=5.0 mm, Y=1.5 mm) and (X=80.0 mm, Y=7.7 mm).
2. **Solder Mask Web Expansion**:
   - Set global solder mask clearance to **0.025 mm (1 mil)** and min mask web to **0.08 mm** to eliminate the 32 mask bridge violations around QFN pads.
3. **Board Edge Clearances**:
   - Pull all ground fills and copper tracks back to **>= 0.50 mm** from `Edge.Cuts`.
4. **Manufacturing Panelization**:
   - Design standard 4-up production panel with 5.0 mm breakaway rails, mouse-bite perforations, and tooling holes (3.175 mm).

---

### Work Package 5: Automated Test Harness Overhaul
**Priority**: **P1 (Quality Assurance)**  
**Target Files**:
- `tests/test_*.py`

**Action Steps**:
1. Remove all hardcoded mock math assertions (deprecate current `test_power_path.py`).
2. Retarget all test fixtures to live Revision G source paths (`output/RevG/`), eliminating references to `RevE_work` and `client_delivery`.
3. Integrate official KiCad CLI execution directly into test fixtures (`test_drc_zero_violations`, `test_erc_zero_violations`, `test_schematic_parity`).
4. Validate that tests fail if a short or unconnected ratline is injected, and pass only when live design passes.

---

### Work Package 6: Mechanical Prototype Package & Tolerancing
**Priority**: **P2 (Physical Verification)**  
**Target Files**:
- `output/RevG/07_3D_STEP/`
- `output/RevG/08_3D_STL/`

**Action Steps**:
1. Verify physical vendor sample of protected LiPo cell (including PCM length and wire exits) against the 46.0 mm battery cradle.
2. Generate export package of all 15 parts for SLA / MJF 3D printing (0.05 mm layer height) to verify hand feel, grip comfort, and click mechanism travel.

---

## 3. Phase 2 Exit Acceptance Gate

Phase 2 will be declared complete only when all the following criteria are met:
1. `kicad-cli sch erc` on all 4 schematics returns **Exit Code 0** (0 errors).
2. `kicad-cli pcb drc` on all 4 PCBs returns **Exit Code 0** (0 violations, 0 unconnected, 0 parity errors).
3. `J_PWR` is replaced with `U4`, with Pin 5 routed to 3V3 and Pin 3 to Enable.
4. Battery charge resistor R9 is updated to safe current rating ($\le 1.0C$).
5. Automated test suite passes 100% against **live KiCad CLI and real board S-expressions**.
6. All changes committed to `engineering/revg-production` with full report documentation.
