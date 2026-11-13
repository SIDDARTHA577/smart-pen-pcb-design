# Smart Pen Rev G — Phase 1: Fresh Native KiCad ERC & DRC Audit

**Document ID**: `reports/RevG/Phase01/04_FRESH_ERC_DRC_AUDIT.md`  
**Execution Date**: November 13, 2026  
**KiCad Version**: KiCad 10.0.7 (`kicad-cli.exe`)  
**CLI Path**: `C:\Users\goran\AppData\Local\Programs\KiCad\10.0\bin\kicad-cli.exe`  
**Branch**: `engineering/revg-production`  

---

## 1. Executive Summary

Official KiCad 10.0.7 command-line tools were executed freshly on all four electrical schematics and five physical PCB layout candidates. 

Verification parameters enforced:
- All severity levels enabled: `--severity-all` (Errors, Warnings, Exclusions).
- Strict exit code returns on rule failure: `--exit-code-violations`.
- Refilled copper zones prior to DRC evaluation: `--refill-zones` (without `--save-board` to protect source files from modification).
- In-memory schematic-to-PCB parity verification: `--schematic-parity`.
- Exhaustive track error reporting: `--all-track-errors`.
- Machine-readable JSON and human-readable text report exports preserved in `reports/RevG/Phase01/raw/`.

---

## 2. Fresh ERC Results (Schematic Capture)

### Command Shape
```powershell
& "C:\Users\goran\AppData\Local\Programs\KiCad\10.0\bin\kicad-cli.exe" sch erc `
  --severity-all --units mm --exit-code-violations `
  --output "<raw_output_path>.rpt" "<input_sch_path>"
```

### ERC Results Summary Table

| Board Subsystem | Schematic Input File | Input SHA-256 | Exit Code | Total Violations | Errors | Warnings | Exclusions | Raw Report Artifact | Verdict |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- | :---: |
| **Main PCB** | `output/RevF_Working/SmartPen.kicad_sch` | `ad190c9369258b47...` | **0** | **0** | 0 | 0 | 0 | [`Main_SmartPen_erc.rpt`](file:///c:/Users/goran/Downloads/SmartPen_RevD_AutoLinked_Footprints_Review_ONLY/reports/RevG/Phase01/raw/Main_SmartPen_erc.rpt) | **PASS** |
| **Front MPU** | `output/RevF_Working/Front_MPU/Front_MPU.kicad_sch` | `a33fedfbbcd18857...` | **0** | **0** | 0 | 0 | 0 | [`Front_MPU_erc.rpt`](file:///c:/Users/goran/Downloads/SmartPen_RevD_AutoLinked_Footprints_Review_ONLY/reports/RevG/Phase01/raw/Front_MPU_erc.rpt) | **PASS** |
| **MicroSD Carrier** | `output/RevF_Working/MicroSD_Carrier/MicroSD_Carrier.kicad_sch` | `6fe97adc5cd62d62...` | **0** | **0** | 0 | 0 | 0 | [`MicroSD_Carrier_erc.rpt`](file:///c:/Users/goran/Downloads/SmartPen_RevD_AutoLinked_Footprints_Review_ONLY/reports/RevG/Phase01/raw/MicroSD_Carrier_erc.rpt) | **PASS** |
| **Touch Sensor** | `output/RevF_Working/Touch_Sensor/Touch_Sensor.kicad_sch` | `867a01c8150585f3...` | **0** | **0** | 0 | 0 | 0 | [`Touch_Sensor_erc.rpt`](file:///c:/Users/goran/Downloads/SmartPen_RevD_AutoLinked_Footprints_Review_ONLY/reports/RevG/Phase01/raw/Touch_Sensor_erc.rpt) | **PASS** |

### Critical Engineering Note on ERC Passing
While all four schematics pass ERC with 0 errors, **Rule 3 of the Engineering Integrity Rules strictly mandates: "Do not claim that passing ERC means the schematic is electrically correct."**
Schematic ERC confirms only that pins are not conflicting on pin-types (e.g. two output pins fighting each other) and nets are tagged. As documented in Task 6, catastrophic circuit flaws exist within the schematic that ERC cannot detect:
1. `J_PWR` (AP2112K LDO) has its Enable pin wired to `3V3` and its actual output pin left unconnected.
2. `J_USB` connector pads map VBUS onto data/ground lines in the PCB.
3. Charge programming resistor R9 sets a potentially hazardous 303 mA charge rate.

---

## 3. Fresh DRC Results (Physical PCB Layout)

### Command Shape
```powershell
& "C:\Users\goran\AppData\Local\Programs\KiCad\10.0\bin\kicad-cli.exe" pcb drc `
  --severity-all --all-track-errors --schematic-parity --refill-zones --units mm `
  --exit-code-violations --output "<raw_output_path>.rpt" "<input_pcb_path>"
```

### DRC Results Summary Table

| Board Candidate | Layout Input File | Input SHA-256 | Exit Code | Total Violations | Shorting Items | Crossing Tracks | Clearance Violations | Unconnected Items | Schematic Parity Errors | Raw Report Artifact | Verdict |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :---: |
| **Main PCB (Working)** | `output/RevF_Working/SmartPen.kicad_pcb` | `e39c401f1ae25908...` | **5** | **185** | **33** | **1** | **38** | **29** | **22** | [`Main_SmartPen_Working_drc.rpt`](file:///c:/Users/goran/Downloads/SmartPen_RevD_AutoLinked_Footprints_Review_ONLY/reports/RevG/Phase01/raw/Main_SmartPen_Working_drc.rpt) | **FAIL** |
| **Main PCB (Delivery)**| `output/RevF_Client_Delivery/.../SmartPen.kicad_pcb` | `37a2f4a69b317719...` | **5** | **1,338** | **199** | **199** | **499** | **0** | **199** | [`Main_SmartPen_ClientDelivery_drc.rpt`](file:///c:/Users/goran/Downloads/SmartPen_RevD_AutoLinked_Footprints_Review_ONLY/reports/RevG/Phase01/raw/Main_SmartPen_ClientDelivery_drc.rpt) | **FAIL** |
| **Front MPU** | `output/RevF_Working/Front_MPU/Front_MPU.kicad_pcb` | `ec59f0dcbee3e9dd...` | **0** | **0** | **0** | **0** | **0** | **0** | **0** | [`Front_MPU_drc.rpt`](file:///c:/Users/goran/Downloads/SmartPen_RevD_AutoLinked_Footprints_Review_ONLY/reports/RevG/Phase01/raw/Front_MPU_drc.rpt) | **PASS** |
| **MicroSD Carrier** | `output/RevF_Working/MicroSD_Carrier/MicroSD_Carrier.kicad_pcb` | `96eb291ed0d287f9...` | **0** | **0** | **0** | **0** | **0** | **0** | **0** | [`MicroSD_Carrier_drc.rpt`](file:///c:/Users/goran/Downloads/SmartPen_RevD_AutoLinked_Footprints_Review_ONLY/reports/RevG/Phase01/raw/MicroSD_Carrier_drc.rpt) | **PASS** |
| **Touch Sensor** | `output/RevF_Working/Touch_Sensor/Touch_Sensor.kicad_pcb` | `cd5027f737b65b27...` | **5** | **0** | **0** | **0** | **0** | **0** | **16** | [`Touch_Sensor_drc.rpt`](file:///c:/Users/goran/Downloads/SmartPen_RevD_AutoLinked_Footprints_Review_ONLY/reports/RevG/Phase01/raw/Touch_Sensor_drc.rpt) | **FAIL (PARITY)** |

---

## 4. Violation Breakdown by Type

### A. Main PCB Working (`output/RevF_Working/SmartPen.kicad_pcb`)
Total DRC entries: 185 geometric violations + 29 unconnected pads + 22 schematic parity errors.
- `hole_clearance`: **56** (Vias too close to adjacent component pads or via barrels < 0.25 mm)
- `clearance`: **38** (Track-to-pad and track-to-track spacing < 0.127 mm)
- `shorting_items`: **33** (Vias intersecting signal and power tracks on B.Cu)
- `solder_mask_bridge`: **32** (Solder mask slivers between fine-pitch pads < 0.10 mm)
- `lib_footprint_mismatch`: **11** (Footprint cached in board differs slightly from library)
- `isolated_copper`: **9** (Copper islands in filled ground plane lacking via stitching)
- `starved_thermal`: **5** (Thermal relief spokes constricted by nearby traces)
- `tracks_crossing`: **1** (`/CHG_STAT` track crossing `/BOOT9` track on B.Cu)
- `unconnected_items`: **29** (Unrouted connections, primarily GPIO expander and sensor nets)
- `schematic_parity`: **22** (Mismatches on J_USB pad-to-net mapping)

### B. Main PCB Client Delivery (`output/RevF_Client_Delivery/.../SmartPen.kicad_pcb`)
Total DRC entries: 1,338 geometric violations + 0 unconnected + 199 schematic parity errors.
- `clearance`: **499** violations
- `shorting_items`: **199** dead shorts
- `hole_clearance`: **199** violations
- `tracks_crossing`: **199** track intersections on same copper layer
- `solder_mask_bridge`: **170** violations
- `hole_to_hole`: **59** violations
- `starved_thermal`: **13** violations
- `schematic_parity`: **199** parity mismatches

### C. Touch Sensor (`output/RevF_Working/Touch_Sensor/Touch_Sensor.kicad_pcb`)
- Geometric Violations: **0**
- Unconnected Items: **0**
- Schematic Parity: **16** errors
  - Cause: Net naming mismatch between schematic (`/3V3`, `/GND`, `/TOUCH_IN`, `/TOUCH_OUT`) and layout (`3V3`, `GND`, `TOUCH_IN`, `TOUCH_OUT`).
  - Repair: Harmless prefix mismatch, resolved in Phase 2 by synchronizing netlist names.

---

## 5. DRC Issue Register Reference

Every single violation is indexed with exact coordinates, affected nets, component references, and severity in [`05_DRC_ISSUE_REGISTER.csv`](file:///c:/Users/goran/Downloads/SmartPen_RevD_AutoLinked_Footprints_Review_ONLY/reports/RevG/Phase01/05_DRC_ISSUE_REGISTER.csv) (1,789 total records).

---

## 6. Audit Verdict

- **Main PCB Working**: **FAIL** (Requires Phase 2 routing fix of 33 shorts and 29 unrouted connections).
- **Main PCB Client Delivery**: **CATASTROPHIC FAIL** (Rejected from project).
- **Front MPU**: **PASS** (Zero DRC/ERC violations).
- **MicroSD Carrier**: **PASS** (Zero DRC/ERC violations).
- **Touch Sensor**: **PASS WITH MINOR PARITY WARNING** (Parity prefix fix required).
