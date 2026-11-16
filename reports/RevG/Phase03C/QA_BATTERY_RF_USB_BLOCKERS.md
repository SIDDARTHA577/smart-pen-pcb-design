# Smart Pen Rev G — Battery, Power-Path, RF & USB Blockers Audit
**Document ID:** QA-REVG-P3C-005  
**Project:** Smart Pen Hardware Architecture Revision G  
**Variant:** Four-Layer Evaluation Candidate (`output/RevG/variants/FourLayer_Candidate/SmartPen.kicad_pcb`)  
**Date:** November 16, 2026  
**Status:** Power-Path Verified; Critical Hardware Blockers Preserved  

---

## 1. Executive Summary

This audit validates the electrical safety, power-path selection logic, battery charging characteristics, and regulator performance of the Smart Pen Revision G candidate. While the schematic and PCB routing of the power-path circuitry are electrically sound and defect-free, three critical procurement and integration blockers remain open and must be resolved by client decision before Phase 4 mechanical enclosure finalization.

---

## 2. Power-Path & Charging Architecture Validation

### 2.1 Battery Charging Circuitry (U2: MCP73831)
- **Controller:** Microchip `MCP73831T-2ACI/OT` (SOT-23-5)
- **Charge Voltage:** Fixed $4.20\text{V} \pm 0.75\%$
- **Charge Current Program Resistor ($R_9$):** Connected from PROG (Pin 5) to GND. Value $= 10.0\text{ k}\Omega$ ($1\%$, 0402).
- **Calculated Constant-Current Charge Rate:**
  $$I_{\text{REG}} = \frac{1000\text{ V}}{R_{\text{PROG}}} = \frac{1000\text{ V}}{10.0\text{ k}\Omega} = 100.0\text{ mA}$$
- **Thermal & Safety Assessment:** For an assumed 100–120 mAh cell, a 100 mA charge rate corresponds to $\approx 0.83\text{C}\text{–}1.0\text{C}$. In an unventilated cylindrical pen barrel, charging at 1.0C produces concentrated heat dissipation within U2 ($\Delta V \approx 5.0\text{V} - 3.7\text{V} = 1.3\text{V} \implies P_{\text{diss}} \approx 130\text{ mW}$). Enclosure thermal dissipation must be verified in Phase 4.

### 2.2 Battery Connector Polarity (`J_BAT`)
- **Connector Type:** JST `SM02B-SRSS-TB(LF)(SN)` (1.0 mm pitch, 2-pin horizontal SMT)
- **Physical Coordinates:** $X = 62.80\text{ mm}, Y = 1.72\text{ mm}$
- **Pad Mapping:**
  - **Pad 1:** Net `/VBAT` (Battery Positive, $+3.7\text{V}$ nominal)
  - **Pad 2:** Net `/GND` (Battery Negative / Ground)
  - **Pads 3 & 4:** Mechanical shield tabs (Floating / GND)
- **Safety Directive:** The external battery lead harness must follow standard wire color orientation: Pin 1 (Red, $+3.7\text{V}$) and Pin 2 (Black, GND). Reversing the harness will cause catastrophic reverse-polarity failure of U2 and Q2.

### 2.3 Battery Protection Mandate (Mandatory PCM / BMB)
- **Critical Circuit Finding:** The main PCB contains **no onboard battery protection IC** (such as a DW01A / FS312F with dual MOSFET switch).
- **Safety Mandate:** The external lithium-polymer pouch cell **MUST** incorporate a built-in Protection Circuit Module (PCM) providing:
  1. Over-charge voltage cutoff ($4.28\text{V} \pm 0.025\text{V}$)
  2. Over-discharge voltage cutoff ($2.80\text{V} \pm 0.05\text{V}$)
  3. Over-current / short-circuit protection cutoff ($\le 1.5\text{A}$)
  4. Automatic recovery upon fault clearing
- **Warning:** Connecting an unprotected bare LiPo pouch cell to `J_BAT` presents a catastrophic thermal runaway and fire hazard during operation or cell puncture.

### 2.4 Automatic Power Handover & Reverse-Current Blocking

The power-path circuit employs a P-Channel MOSFET (`Q2`, `DMG2305UX`) and a Schottky diode (`D4`, `1N5819HW-7-F`) to automatically negotiate power source selection:

```
                  +---------------- D4 (1N5819HW) ----------------+
                  |                                               |
                  |     (Anode)                       (Cathode)   v
USB 5V (VBUS) ----+----------------- Gate (Pin 1)             /VSYS_RAW ---> [SW3] ---> [U4 AP2112K] ---> 3.3V
                  |                   Q2                      ^
                  |              (DMG2305UX)                  |
                 [R26]      Drain (Pin 3)      Source (Pin 2) |
                100kΩ             |                  |        |
                  |               +---|<|------------+--------+
                 GND              |  Body Diode
                                  |
                                /VBAT (From LiPo Battery via J_BAT)
```

#### State 1: Battery Power Only (USB Disconnected)
- `/USB_VBUS` $= 0\text{ V}$.
- Gate of Q2 is pulled to GND by $R_{26}$ ($100\text{ k}\Omega$).
- Source of Q2 is initially at $V_{\text{BAT}} - V_{\text{body\_diode}}$ ($\approx 3.4\text{ V}$).
- Gate-to-Source voltage: $V_{GS} = 0\text{ V} - 3.7\text{ V} = -3.7\text{ V}$.
- Because $V_{GS} << V_{GS(\text{th})}$ ($-0.9\text{ V}$ max for DMG2305), Q2 turns fully ON ($R_{\text{DS(on)}} \approx 50\text{ m}\Omega$).
- Battery current flows smoothly through the MOSFET channel from Drain to Source into `/VSYS_RAW` with negligible voltage drop ($< 5\text{ mV}$ at typical $100\text{ mA}$ load).
- Schottky diode D4 is reverse-biased ($V_{\text{Cathode}} \approx 3.7\text{ V}, V_{\text{Anode}} = 0\text{ V}$); zero leakage current reaches the USB connector.

#### State 2: USB Connected (Battery Charging & System Operation)
- `/USB_VBUS` $= 5.0\text{ V}$.
- 5V power flows through Schottky diode D4 into `/VSYS_RAW`:
  $$V_{\text{SYS\_RAW}} = 5.0\text{ V} - V_{\text{Schottky}} \approx 5.0\text{ V} - 0.35\text{ V} = 4.65\text{ V}$$
- Gate of Q2 is driven to $5.0\text{ V}$.
- Source of Q2 is held at $V_{\text{SYS\_RAW}} \approx 4.65\text{ V}$.
- Drain of Q2 is at battery voltage $V_{\text{BAT}} \approx 3.7\text{–}4.2\text{ V}$.
- Gate-to-Source voltage: $V_{GS} = 5.0\text{ V} - 4.65\text{ V} = +0.35\text{ V} > 0\text{ V}$.
- The P-MOSFET channel is completely turned OFF (cut off).
- Q2's internal body diode is oriented with Anode at Drain (`/VBAT`) and Cathode at Source (`/VSYS_RAW`). Because $V_{\text{Source}} (4.65\text{V}) > V_{\text{Drain}} (3.7\text{–}4.2\text{V})$, the body diode is **reverse-biased**.
- **Result:** No reverse current can flow from USB into the battery through Q2. The battery is isolated from the 5V bus and charges exclusively through the regulated MCP73831 linear charger (U2).

### 2.5 Low Dropout Voltage Regulator (U4: AP2112K-3.3)
- **Part Number:** Diodes Inc `AP2112K-3.3TRG1` (SOT-23-5)
- **Input Rails:** Pin 1 (VIN) and Pin 3 (EN) connect to `/VBAT_SW` (switched power after slide switch SW3).
- **Output Rail:** Pin 5 (VOUT) outputs `/3V3`, decoupled by $10\text{ µF}$ ceramic capacitor $C_{14}$.
- **Electrical Capacity:** $600\text{ mA}$ continuous output, $250\text{ mV}$ dropout at $600\text{ mA}$.
- **Operating Margin:** When running on battery at $V_{\text{BAT}} = 3.60\text{ V}$, $V_{\text{IN}} - V_{\text{OUT}} = 300\text{ mV}$, remaining above the LDO dropout threshold for ESP32-C3 peak current bursts ($350\text{ mA}$).

---

## 3. Preserved Client-Approval & Engineering Blockers

### Blocker 1: Battery Procurement & Specification Sign-Off
- **Status:** **BLOCKED (Client Decision Required)**
- **Issue:** Prior project reports made arbitrary claims of a "120 mAh cell with 8 hours runtime." In reality, no commercial battery part number, official manufacturer datasheet, UL1642 certification, or verified physical envelope has been approved by the client.
- **Physical Requirement:** The battery pouch must fit beneath the removable PCB rail inside a cylindrical internal space of $\approx 10.0\text{ mm}$ width, $4.5\text{ mm}$ height, and $30.0\text{ mm}$ length.
- **Action Required:** Client must select and approve a specific commercial protected pouch cell (e.g. 401030 or 501030 format) with integrated PCM before Phase 4 mechanical cradle design can proceed.

### Blocker 2: 2.4 GHz RF Antenna & Pigtail Selection
- **Status:** **BLOCKED (Client / Engineering Decision Required)**
- **Issue:** The main PCB contains no on-board antenna; it terminates at U.FL receptacle `J_RF`. Wireless communication requires an external antenna.
- **Action Required:** Client and RF engineering must approve:
  1. Antenna type: Flexible PCB dipole (e.g. Molex 146153), ceramic patch, or wire monopole mounted inside the pen cap.
  2. Coaxial cable pigtail: Ultra-miniature $0.81\text{ mm}$ cable assembly, specified length ($35\text{–}50\text{ mm}$).
  3. Enclosure material impact: Pen barrel must be non-metallic (e.g. polycarbonate or ABS) in the antenna zone to prevent total RF shielding.

### Blocker 3: USB Differential Signal Routing Integrity
- **Status:** **OPEN FOR PHASE 4 PROTOTYPE TESTING**
- **Issue:** Full-Speed USB differential pair (`/USB_DP` and `/USB_DM`) routes across internal layer `In2.Cu` (the 3.3V power plane). Although passing KiCad DRC, physical return-current discontinuities must be evaluated with TDR and eye-diagram measurements on physical Revision G prototype hardware.
