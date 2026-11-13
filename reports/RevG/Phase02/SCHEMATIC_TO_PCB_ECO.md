# SMART PEN REVISION G — SCHEMATIC-TO-PCB ENGINEERING CHANGE ORDER (ECO)
## Forward Annotation & Synchronization Strategy for Phase 3

- **Project:** Smart Pen PCB Design
- **Document ID:** `REVG-DOC-ECO-001`
- **Revision:** Rev G Phase 2 Freeze Candidate
- **Author:** Senior KiCad PCB Layout Engineer
- **Status:** **ECO DOCUMENTED — PCB FORWARD ANNOTATION HELD FOR PHASE 3**

---

## 1. Executive Summary & Phase 2 Constraint Boundary

Per mandatory Phase 2 instructions:
> "In Phase 2, do NOT reroute the PCB or run KiCad 'Update PCB from Schematic'. Instead, document the exact delta between the revised schematic and the current PCB."

This document establishes the authoritative, step-by-step Engineering Change Order (ECO) plan. It details every footprint addition, reference rename, net reassignment, and pad modification required to synchronize the Main PCB (`output/RevG/SmartPen.kicad_pcb`) with the frozen Rev G schematic (`output/RevG/SmartPen.kicad_sch`) during Phase 3.

---

## 2. Comprehensive ECO Action Matrix

```
+-----------------------------------------------------------------------------------------------------------------+
|                                 REVISION G SCHEMATIC-TO-PCB ECO ACTION MATRIX                                   |
+---------+--------------------+-----------------------+--------------------+-------------------------------------+
| ECO #   | Subsystem / Ref    | Action Type           | Footprint / Layer  | Detailed Technical Directive        |
+---------+--------------------+-----------------------+--------------------+-------------------------------------+
| **ECO-01** | LDO Regulator `U4` | Reference & Net Update| `SmartPen:J_PWR`   | 1. Rename PCB footprint `J_PWR` -> `U4`.
|         | (was `J_PWR`)      |                       | (SOT-23-5, F.Cu)   | 2. Re-assign Pad 1 from net `/VBAT_SW` (retain).
|         |                    |                       |                    | 3. Re-assign Pad 2 from net `/GND` (retain).
|         |                    |                       |                    | 4. Re-assign Pad 3 (EN) from `/3V3` to `/VBAT_SW`.
|         |                    |                       |                    | 5. Pad 4 (NC) remains unconnected.
|         |                    |                       |                    | 6. Route Pad 5 (VOUT) to primary `/3V3` rail!
+---------+--------------------+-----------------------+--------------------+-------------------------------------+
| **ECO-02** | Power-Path `Q2`    | Component Placement   | `SmartPen:Q1`      | 1. Place SOT-23 footprint on Top Layer (F.Cu)
|         | (DMG2305UX)        | & Routing             | (SOT-23, F.Cu)     |    adjacent to `J_USB` and `U2`.
|         |                    |                       |                    | 2. Route Pad 1 (Gate) to net `/USB_VBUS`.
|         |                    |                       |                    | 3. Route Pad 2 (Source) to net `/VBAT`.
|         |                    |                       |                    | 4. Route Pad 3 (Drain) to new net `/VSYS_RAW`.
+---------+--------------------+-----------------------+--------------------+-------------------------------------+
| **ECO-03** | Power-Path `D4`    | Component Placement   | `SmartPen:D3`      | 1. Place SOD-123 footprint on Top Layer (F.Cu)
|         | (1N5819HW-7-F)     | & Routing             | (SOD-123, F.Cu)    |    adjacent to `Q2` and `J_USB`.
|         |                    |                       |                    | 2. Route Pad 1 (Cathode) to net `/VSYS_RAW`.
|         |                    |                       |                    | 3. Route Pad 2 (Anode) to net `/USB_VBUS`.
+---------+--------------------+-----------------------+--------------------+-------------------------------------+
| **ECO-04** | Power-Path `R26`   | Component Placement   | `SmartPen:R1`      | 1. Place 0402 footprint on Top Layer (F.Cu)
|         | (100k 0402)        | & Routing             | (0402, F.Cu)       |    adjacent to Q2 Gate (Pad 1).
|         |                    |                       |                    | 2. Route Pad 1 to net `/USB_VBUS`.
|         |                    |                       |                    | 3. Route Pad 2 to ground net `/GND`.
+---------+--------------------+-----------------------+--------------------+-------------------------------------+
| **ECO-05** | Switch `SW3`       | Net Reassignment      | `SmartPen:SW3`     | 1. Disconnect trace entering Pad 1 from `/VBAT`.
|         | (Slide Switch)     | & Reroute             | (SMD, F.Cu)        | 2. Connect Pad 1 to new net `/VSYS_RAW` (from Q2/D4).
|         |                    |                       |                    | 3. Pad 2 remains connected to `/VBAT_SW`.
+---------+--------------------+-----------------------+--------------------+-------------------------------------+
| **ECO-06** | Programming `R9`   | Component Value Update| `SmartPen:R9`      | 1. Footprint and routing remain unchanged.
|         | (10k 0402)         | (BOM Synchronization) | (0402, F.Cu)       | 2. BOM value synchronized from 3.3k to 10.0k.
+---------+--------------------+-----------------------+--------------------+-------------------------------------+
| **ECO-07** | USB Receptacle     | Net Synchronization   | `SmartPen:J_USB`   | 1. Pads 1, 3, 12, 13–16: verify tied to `/GND`.
|         | (`J_USB`)          | (Clean DRC)           | (Mid-mount, F.Cu)  | 2. Pads 2, 10: verify tied to `/USB_VBUS`.
|         |                    |                       |                    | 3. Pad 5: verify `/USB_CC1`; Pad 6: `/USB_CC2`.
|         |                    |                       |                    | 4. Pad 7: verify `/USB_DP_PORT`; Pad 9: `/USB_DM_PORT`.
+---------+--------------------+-----------------------+--------------------+-------------------------------------+
| **ECO-08** | Battery Footprint  | Silk Screen Addition  | `SmartPen:J_BAT`   | 1. Update footprint definition from `SmartPen.pretty`.
|         | (`J_BAT`)          |                       | (F.SilkS)          | 2. Add visible `+` text marking adjacent to Pad 1.
+---------+--------------------+-----------------------+--------------------+-------------------------------------+
```

---

## 3. Spatial Allocation & Clearance Strategy on the Internal Rail

The Main PCB has fixed geometric dimensions of **$11.0\text{ mm} \times 88.0\text{ mm}$** (rigid section of the internal rail).
Integrating `Q2` (SOT-23), `D4` (SOD-123), and `R26` (0402) requires approximately $15\text{ mm}^2$ of surface area.

### 3.1 Recommended Component Placement Zone
- **X-Coordinate Span:** Between $72.0\text{ mm}$ and $82.0\text{ mm}$ along the board length.
- **Y-Coordinate Span:** Between $1.5\text{ mm}$ and $9.5\text{ mm}$ across the board width.
- This zone lies directly between USB-C receptacle `J_USB` and LiPo charger `U2` (`MCP73831`).
- Placing `Q2`, `D4`, and `R26` in this cluster minimizes trace lengths on `/USB_VBUS`, `/VBAT`, and `/VSYS_RAW` to under $4.0\text{ mm}$, minimizing parasitic inductance and resistive IR drops.

---

## 4. Phase 3 Execution Procedure

When Phase 3 is authorized by the client, the layout engineer will execute the following controlled sequence:

1. Open `output/RevG/SmartPen.kicad_pcb` in KiCad 10.0.7 PCB Editor.
2. Execute **Tools -> Update PCB from Schematic (F8)** with options:
   - *Re-link footprints to schematic symbols based on Reference Designators: CHECKED*
   - *Delete extra footprints: UNCHECKED*
3. Verify that KiCad imports components `Q2`, `D4`, `R26`, and renames `J_PWR` to `U4`.
4. Route trace from `U4` Pad 5 to the existing `/3V3` copper pour / filter capacitors (`C2`, `C14`).
5. Route `Q2`, `D4`, `R26` local power-path traces.
6. Re-route `SW3` Pad 1 from `/VBAT` to `/VSYS_RAW`.
7. Regenerate all copper ground zones (`B` key).
8. Execute `kicad-cli pcb drc` and achieve 0 DRC violations.
