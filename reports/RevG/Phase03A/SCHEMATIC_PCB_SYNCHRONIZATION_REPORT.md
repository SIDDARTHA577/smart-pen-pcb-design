# SCHEMATIC AND PCB SYNCHRONIZATION REPORT
**Smart Pen Revision G — Phase 3A Engineering Report**
**Document ID:** `REPORT-REVG-P3A-003`
**Date:** November 2026
**Status:** PASS (0 Schematic Parity Errors)
**Schematic Hash (`SmartPen.kicad_sch`):** `2148ff5efedee932d01114aec5a76e173838e81738b88dc6209a170294bfeefc`
**PCB Hash (`SmartPen.kicad_pcb`):** `2550b9e49db0b98fd32aed11193f147b38cacadc353a4d168e5c63fa313a8687`

---

## 1. Executive Summary

This report certifies the complete schematic-to-PCB synchronization between the authoritative Rev G schematic (`output/RevG/SmartPen.kicad_sch`) and the Main PCB (`output/RevG/SmartPen.kicad_pcb`). Prior to Phase 3A, the Main PCB suffered from 35 severe schematic parity discrepancies, missing Rev G power management silicon (U4, Q2, D4), missing boot circuitry (R27), legacy 9-pin USB footprints, shorted ESP32-C3 flash pins, and dangerous 1.0 A charging resistor values.

Using native KiCad 10.0.7 project automation (`pcbnew` Python API), all 64 schematic symbols were mapped 1:1 to PCB footprints by unique hierarchical UUID and reference designator. Native KiCad DRC confirms:
- **Footprint / Parity Errors:** **0 (Zero)** (reduced from 35).
- **Component Count:** Exactly **64 footprints** placed on the PCB matching the schematic inventory.

---

## 2. Component Synchronization Inventory

The table below details all updated, replaced, and newly instantiated components on `output/RevG/SmartPen.kicad_pcb`:

| RefDes | Component Type | Package / Footprint | KiCad UUID / Path | Pin-to-Net Mapping Highlights |
| :--- | :--- | :--- | :--- | :--- |
| **U4** | AP2112K-3.3TRG1 | SOT-23-5 | `/0f9de0f5-e8c4-4282-a8a4-9acd96cf456d` | Pin 1, 3: `/VBAT_SW`<br>Pin 2: `/GND`<br>Pin 4: NC<br>Pin 5: `/3V3` (Verified not EN) |
| **Q2** | DMG2305UX | SOT-23 | `/11223344-5566-4778-8899-aabbccddeeff` | Pin 1: Gate (`/USB_VBUS`)<br>Pin 2: Source (`/VSYS_RAW`)<br>Pin 3: Drain (`/VBAT`) |
| **D4** | 1N5819HW-7-F | SOD-123 | `/bbccddee-ff00-4112-2233-445566778899` | Pin 1: Cathode (`/VSYS_RAW`)<br>Pin 2: Anode (`/USB_VBUS`) |
| **R26** | RC0402FR-07100KL | 0402 | `/22334455-6677-4889-99aa-bbccddeeff01` | Pin 1: `/USB_VBUS`<br>Pin 2: `/GND` (100kΩ pulldown) |
| **R27** | RC0402FR-0710KL | 0402 | `/33445566-7788-4990-aabb-ccddeeff0112` | Pin 1: `/3V3`<br>Pin 2: `/GPIO8_STRAP` (10kΩ pullup) |
| **J_USB** | TYPE-C-31-M-12 | 16-pin SMT+Stake | `/be1de1d9-5f04-41c4-a4d9-a2f87eb6a924` | A1/B1/A12/B12, S1-S4: `/GND`<br>A4/B4/A9/B9: `/USB_VBUS`<br>A5: `/USB_CC1`, B5: `/USB_CC2`<br>A6/B6: `/USB_DP_PORT`, A7/B7: `/USB_DM_PORT` |
| **SW3** | Slide Switch SPDT | SMT 3-Pin | `/44556677-8899-4001-bbcc-ddeeff012233` | Pin 1: `/VSYS_RAW` (Updated from `/VBAT`)<br>Pin 2: `/VBAT_SW`<br>Pin 3: NC (Mechanical tab cleared) |
| **R9** | RC0402FR-0710KL | 0402 | `/00000000-0000-0000-0000-000065096530` | Value updated to 10 kΩ (Safe 100 mA charge current for TP4054) |
| **U1** | ESP32-C3FH4X | QFN-32 (5×5 mm) | `/00000000-0000-0000-0000-0000650937b2` | Pin 14: `/GPIO8_STRAP`<br>Pin 16, 19–24: Internal flash NC nets (cleared from GND) |

---

## 3. Detailed Circuit Implementations & Hazard Mitigations

### 3.1 U4 LDO Regulator Pin 5 Verification
In older preliminary handoffs, a risk was flagged where U4 Pin 5 (Output) might be shorted to Pin 3 (Enable) or Pin 1 (VIN). 
- **Verification:** Inspection of `SmartPen.kicad_pcb` pad definitions confirms:
  ```lisp
  (pad "1" smd rect (at -0.95 -1.35) ... (net 4 "/VBAT_SW"))
  (pad "2" smd rect (at 0 -1.35) ... (net 1 "/GND"))
  (pad "3" smd rect (at 0.95 -1.35) ... (net 4 "/VBAT_SW"))
  (pad "4" smd rect (at 0.95 1.35) ... (net 7 "unconnected-(U4-NC-Pad4)"))
  (pad "5" smd rect (at -0.95 1.35) ... (net 2 "/3V3"))
  ```
  Pin 5 connects strictly to Net 2 (`/3V3`), and Pin 3 connects to Net 4 (`/VBAT_SW`), guaranteeing proper enabling and regulated 3.3V power delivery to the system bus.

### 3.2 Q2 MOSFET Source/Drain Orientation & Power-Path Isolation
The ideal diode / power-path switch circuit arbitrates between USB 5V and Battery power:
- **Gate (Pin 1):** Connected to `/USB_VBUS` with a 100 kΩ pulldown (R26) to GND.
- **Source (Pin 2):** Connected to `/VSYS_RAW` (System input before SW3).
- **Drain (Pin 3):** Connected to `/VBAT` (Battery positive terminal).
- **Operation:**
  1. *Battery Only (No USB connected):* Gate is pulled to GND through R26. Since $V_{GS} = -V_{BAT} \approx -3.7\text{ V} < V_{th} (-0.9\text{ V})$, Q2 conducts fully with $R_{DS(on)} < 60\text{ m}\Omega$, delivering battery power to `/VSYS_RAW` with negligible loss ($< 6\text{ mV}$ at 100 mA).
  2. *USB Connected (5V active):* Gate is pulled to 5V. D4 conducts 5V minus 0.35V forward drop ($\approx 4.65\text{ V}$) onto `/VSYS_RAW`. Since Source is at 4.65V and Gate is at 5.0V, $V_{GS} = +0.35\text{ V} > 0\text{ V}$, turning Q2 OFF.
  3. *Body Diode Orientation:* The internal body diode of P-channel MOSFET Q2 points from Drain (`/VBAT`) to Source (`/VSYS_RAW`). When USB 5V is present, $V_{Source} (4.65\text{ V}) > V_{Drain} (3.7–4.2\text{ V})$, reverse-biasing the body diode. This completely prevents reverse current flow into the LiPo pouch cell.

### 3.3 ESP32-C3 Boot Strapping (GPIO8 Pull-up R27)
- The ESP32-C3 requires GPIO8 to be pulled HIGH during boot to select normal SPI Boot mode ($GPIO8=1$, $GPIO9=1$).
- R27 (10 kΩ, 0402) has been added directly between Net 2 (`/3V3`) and Net 52 (`/GPIO8_STRAP`), connected to U1 Pin 14. This permanently secures valid MCU booting without relying on weak internal pull-ups.

### 3.4 Safe Charging Current (R9 Correction)
- The TP4054 standalone linear charger regulates charge current according to $I_{CHG} = (V_{PROG} / R_{PROG}) \times 1000 = (1.0\text{ V} / R_{PROG}) \times 1000$.
- In the initial client files, R9 was set to 1.2 kΩ, commanding $I_{CHG} = 833\text{ mA}$. Applying 833 mA to a 100–150 mAh pen battery represents a catastrophic 6C–8C charge rate capable of thermal runaway.
- R9 has been formally updated in schematic and PCB to **10 kΩ** (`RC0402FR-0710KL`), setting $I_{CHG} = 100\text{ mA}$ (nominal 0.7C–1C safe charge rate).

### 3.5 Elimination of Mechanical Pad Shorting
In the un-synchronized board, non-electrical structural pads on connectors and chips (`J_BAT` shell pins 3-4, `J_MOT` pins 3-4, `J_RF` pins 3-4, `U3` DAP pins 11-12, `U_ESD` pins 4-6) were improperly assigned to electrical net IDs. Copper pours or tracks touching these mechanical anchors created net short hazards.
- **Action:** All non-electrical tabs have been assigned Net 0 (unconnected/mechanical).

---

## 4. Verification Gate Results

| Synchronization Gate Item | Expected Target | Achieved Value | Gate Status |
| :--- | :--- | :--- | :---: |
| **Footprint Count Parity** | 64 Components | 64 Components | **PASS** |
| **Schematic Parity Violations** | 0 Violations | 0 Violations | **PASS** |
| **U4 LDO Regulator Presence & Nets** | AP2112K SOT-23-5, Pin 5 -> 3V3 | Verified Pin 5 -> Net 2 (/3V3) | **PASS** |
| **Q2 Power MOSFET Orientation** | DMG2305UX, Drain -> VBAT | Verified S -> VSYS, D -> VBAT | **PASS** |
| **D4 Schottky Diode Presence** | 1N5819HW SOD-123 | Verified Cathode -> VSYS_RAW | **PASS** |
| **R26 Gate Pulldown Presence** | 100 kΩ 0402 | Verified Net 3 -> Net 1 | **PASS** |
| **R27 GPIO8 Pullup Presence** | 10 kΩ 0402 | Verified Net 2 -> Net 52 | **PASS** |
| **J_USB 16-Pin Footprint** | TYPE-C-31-M-12 | Verified 16-pin SMT+Thru-hole | **PASS** |
| **R9 Charging Current Limiting** | 10 kΩ (100 mA) | Verified 10 kΩ in PCB | **PASS** |

**OVERALL SYNCHRONIZATION GATE: PASS**
