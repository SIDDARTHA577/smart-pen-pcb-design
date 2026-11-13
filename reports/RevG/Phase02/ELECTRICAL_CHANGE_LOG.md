# SMART PEN REVISION G — ELECTRICAL CHANGE LOG
## Comprehensive Record of Modifications from Revision F to Revision G

- **Project:** Smart Pen PCB Design
- **Document ID:** `REVG-ECL-001`
- **Revision:** Rev G Phase 2 Freeze Candidate
- **Source Baseline:** Revision F (`output/RevF_Working/`)
- **Authoritative Files Modified:**
  - `output/RevG/SmartPen_Lib.kicad_sym`
  - `output/RevG/SmartPen.kicad_sch`
  - `output/RevG/SmartPen.pretty/J_BAT.kicad_mod`
  - `output/RevG/Touch_Sensor/Touch_Sensor.kicad_pcb`
  - `reports/RevG/Phase02/BOM_REV_G.csv`
  - `tests/test_revg_electrical.py`

---

## 1. Itemized Electrical Architecture Modifications

| Change ID | Subsystem | Component(s) | Rev F Baseline Implementation | Rev G Phase 2 Corrected Implementation | Engineering Justification & Impact |
|:---|:---|:---|:---|:---|:---|
| **ECL-01** | Voltage Regulation | `U4` (formerly `J_PWR`) | 3-pin symbol `J_PWR`; Pin 1=VIN, Pin 2=GND, Pin 3=VOUT (symbol text), Pin 4 & 5 omitted. SOT-23-5 footprint Pad 3 is EN; Pad 5 is VOUT. Net `/3V3` wired to Pin 3 (EN). VOUT floating. | 5-pin symbol `U4` (`AP2112K-3.3TRG1`). Pin 1 (VIN) $\rightarrow$ `/VBAT_SW`, Pin 2 (GND) $\rightarrow$ `/GND`, Pin 3 (EN) $\rightarrow$ `/VBAT_SW`, Pin 4 (NC) $\rightarrow$ No-Connect, Pin 5 (VOUT) $\rightarrow$ `/3V3`. | **Critical bug fix (ISSUE-01).** Hardware dead on arrival in Rev F due to floating regulator output. Output now properly delivers 3.3V @ up to 600mA to system rail. |
| **ECL-02** | Battery Charger | `R9` | $3.3\text{ k}\Omega$ 1% 0402 (`RC0402FR-073K3L`). MCP73831 programmed for $I_{REG} = 1000 / 3300 = 303\text{ mA}$. | $10.0\text{ k}\Omega$ 1% 0402 (`RC0402FR-0710KL`). MCP73831 programmed for $I_{REG} = 1000 / 10000 = 100\text{ mA}$. | **Severe safety hazard elimination (ISSUE-03).** 303 mA charged a 140 mAh cell at 2.16C with 545 mW dissipation in sealed barrel ($\Delta T \approx 125^\circ\text{C}$). 100 mA yields safe 0.71C charge rate and 180 mW dissipation ($\Delta T \approx 41^\circ\text{C}$). |
| **ECL-03** | Power Architecture | `Q2`, `D4`, `R26`, `SW3` | Battery `VBAT` connected directly to `SW3` input and charger `U2` output. System load shared charger output node during charging. | Discrete power-path circuit added: P-FET `Q2` (`DMG2305UX`, SOT-23), Schottky `D4` (`1N5819HW-7-F`, SOD-123), Gate pull-down `R26` ($100\text{ k}\Omega$, 0402). `SW3` input re-routed from `VBAT` to `VSYS_RAW`. | **Power-path resolution (ISSUE-06, ISSUE-07).** Decouples system current from charger C/10 termination. Allows device to operate over USB with battery missing/depleted. Enables battery charging with switch OFF. |
| **ECL-04** | USB Receptacle | `J_USB` | 11-pin generic symbol. Pin 1 labeled VBUS_A, Pin 2 labeled VBUS_B, Pin 3 GND_A, Pin 4 GND_B, Pin 10 D-_B. Contradicted `TYPE-C-31-M-12` footprint pads. | 16-pin 1:1 symbol matching Korean Hroparts `TYPE-C-31-M-12`. Pads 1, 3, 12, 13–16: `/GND`; Pads 2, 10: `/USB_VBUS`; Pad 5: `/USB_CC1`; Pad 6: `/USB_CC2`; Pad 7: `/USB_DP_PORT`; Pad 9: `/USB_DM_PORT`. | **Parity & short-circuit fix (ISSUE-05).** Footprint Pad 1 is GND; symbol Pin 1 was wired to VBUS. Netlist and physical connector pin mapping now 100% matched. |
| **ECL-05** | Battery Header | `J_BAT` | SMD header `SM02B-SRSS-TB(LF)(SN)` with Pin 1=VBAT, Pin 2=GND. Footprint lacked silk screen polarity indication. | Added visible `+` text marking on `F.SilkS` adjacent to Pad 1 in `J_BAT.kicad_mod`. | **Manufacturing / assembly safety.** Prevents reverse battery connection during assembly or field maintenance. |
| **ECL-06** | Touch Daughterboard | `Touch_Sensor.kicad_pcb` | Net names in PCB declared without leading slash (`3V3`, `GND`, `TOUCH_IN`, `TOUCH_OUT`), generating 16 DRC warnings against schematic. | Updated PCB nets to `/3V3`, `/GND`, `/TOUCH_IN`, `/TOUCH_OUT`. All pads and zone fills updated to matching net IDs. | **DRC remediation (ISSUE-02).** Net conflicts dropped from 16 to 0. PCB and schematic now achieve 100% net parity. |

---

## 2. Component Reference Designator Transitions

| Rev F Reference | Rev G Reference | Part Description | Footprint | Action in Rev G |
|:---|:---|:---|:---|:---|
| `J_PWR` | `U4` | AP2112K-3.3TRG1 LDO Regulator | `SmartPen:J_PWR` (SOT-23-5) | Replaced symbol, upgraded to 5 pins, renamed reference to IC standard `U4` |
| `NEW` | `Q2` | DMG2305UX P-MOSFET | `SmartPen:Q1` (SOT-23) | Added for Power-Path automatic battery isolation |
| `NEW` | `D4` | 1N5819HW-7-F Schottky Diode | `SmartPen:D3` (SOD-123) | Added for USB VBUS system supply conduction |
| `NEW` | `R26` | 100k Ohm 1% Resistor 0402 | `SmartPen:R1` (0402) | Added for Q2 Gate pull-down to GND |
| `R9` | `R9` | Programming Resistor | `SmartPen:R9` (0402) | Value changed from $3.3\text{ k}\Omega$ to $10.0\text{ k}\Omega$ |
| `J_USB` | `J_USB` | TYPE-C-31-M-12 Receptacle | `SmartPen:J_USB` (Mid-mount) | Replaced 11-pin generic symbol with 16-pin 1:1 footprint symbol |
| `SW3` | `SW3` | MK-12C02-G025 Slide Switch | `SmartPen:SW3` (SMD) | Re-wired Pin 1 from net `/VBAT` to `/VSYS_RAW` |

---

## 3. Netlist Continuity & Node Differences

```diff
--- RevF_Working/Main_SmartPen_netlist.net
+++ RevG_Production/Main_SmartPen_netlist.net
@@ Nets Modified @@
- (net (code "1") (name "/3V3") (node (ref "J_PWR") (pin "3")))
+ (net (code "1") (name "/3V3") (node (ref "U4") (pin "5")))
+ (net (code "18") (name "/VBAT_SW") (node (ref "U4") (pin "1")) (node (ref "U4") (pin "3")))
+ (net (code "9") (name "/GND") (node (ref "U4") (pin "2")))

@@ Power Path Nodes Added @@
+ (net (code "42") (name "/VSYS_RAW")
+   (node (ref "Q2") (pin "3"))
+   (node (ref "D4") (pin "1"))
+   (node (ref "SW3") (pin "1")))
+ (net (code "36") (name "/USB_VBUS")
+   (node (ref "Q2") (pin "1"))
+   (node (ref "D4") (pin "2"))
+   (node (ref "R26") (pin "1")))
+ (net (code "9") (name "/GND")
+   (node (ref "R26") (pin "2")))

@@ Switch Connection Updated @@
- (net (code "8") (name "/VBAT") (node (ref "SW3") (pin "1")))
+ (net (code "8") (name "/VBAT") (node (ref "Q2") (pin "2")))
```

---

## 4. Verification Check

All modifications were verified with `kicad-cli sch erc` and `pytest tests/test_revg_electrical.py`:
- Schematic Electrical Rules Check: **0 Errors, 0 Warnings**
- Netlist Consistency: **100% Continuous**
- Pytest Suite: **54 Passed, 0 Failed**
