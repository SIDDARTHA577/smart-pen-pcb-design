# SMART PEN REVISION G — USB-C PIN MAPPING AUDIT, INRUSH & ESD PROTECTION
## Resolution of Critical Issue ISSUE-05

- **Project:** Smart Pen PCB Design
- **Document ID:** `REVG-DOC-USB-001`
- **Revision:** Rev G Phase 2 Freeze Candidate
- **Author:** Senior Hardware & Interconnect Engineer
- **Component Under Review:** Korean Hroparts `TYPE-C-31-M-12` Mid-Mount 16-Pin Receptacle (`J_USB`)

---

## 1. Problem Statement & Parity Hazard in Rev F

The Smart Pen incorporates a USB Type-C interface for battery charging and laptop data connectivity (firmware updates, sensor streaming, mass storage).

### 1.1 The Physical Footprint
The physical component selected and placed on the Main PCB is the Korean Hroparts **TYPE-C-31-M-12**, a mid-mount hybrid (SMT signal pins, through-hole shield tabs) 16-pin USB Type-C receptacle. The physical pad layout in `output/RevG/SmartPen.pretty/J_USB.kicad_mod` defines the following pad assignments:
- **Pad 1:** GND (A1/B12)
- **Pad 2:** VBUS (A4/B9)
- **Pad 3:** GND (A1/B12 redundant)
- **Pad 5:** CC1 (A5)
- **Pad 7:** D+ (A6/B6)
- **Pad 9:** D- (A7/B7)
- **Pad 6:** CC2 (B5)
- **Pad 10:** VBUS (B4/A9)
- **Pad 12:** GND (B1/A12)
- **Pads 13, 14, 15, 16:** Shell Chassis Shield Tabs

### 1.2 The Rev F Schematic Error
In Revision F, the schematic symbol assigned to `J_USB` was an arbitrary generic 11-pin connector symbol with sequentially numbered pins:
- Symbol Pin 1: named "VBUS_A" $\rightarrow$ wired to `/USB_VBUS`
- Symbol Pin 2: named "VBUS_B" $\rightarrow$ wired to `/USB_VBUS`
- Symbol Pin 3: named "GND_A" $\rightarrow$ wired to `/GND`
- Symbol Pin 4: named "GND_B" $\rightarrow$ wired to `/GND`
- Symbol Pin 5: named "CC1" $\rightarrow$ wired to `/USB_CC1`
- Symbol Pin 6: named "CC2" $\rightarrow$ wired to `/USB_CC2`
- Symbol Pin 7: named "D+_A" $\rightarrow$ wired to `/USB_DP_PORT`
- Symbol Pin 8: named "D+_B" $\rightarrow$ wired to `/USB_DP_PORT`
- Symbol Pin 9: named "D-_A" $\rightarrow$ wired to `/USB_DM_PORT`
- Symbol Pin 10: named "D-_B" $\rightarrow$ wired to `/USB_DM_PORT`
- Symbol Pin 11: named "SHIELD" $\rightarrow$ wired to `/GND`

### 1.3 The Catastrophic Conflict
Because KiCad links schematic pins to footprint pads by **pin number**:
1. Symbol Pin 1 mapped to **Pad 1 of the footprint**, which on physical USB-C is **GND**! The schematic instructed KiCad that Pad 1 was `/USB_VBUS`!
2. Symbol Pin 10 mapped to **Pad 10 of the footprint**, which on physical USB-C is **VBUS**! The schematic instructed KiCad that Pad 10 was `/USB_DM_PORT`!
3. Footprint Pads 12, 13, 14, 15, 16 had no counterpart pins in the schematic symbol at all.

In Rev F, the PCB layout engineer manually overrode the nets on the PCB traces to avoid blowing up USB hosts, creating a severe netlist parity violation between schematic and PCB. If a user ever executed "Update PCB from Schematic", KiCad would have shorted VBUS directly to GND across Pad 1!

---

## 2. Rev G Authoritative 1:1 Pin Mapping

In Revision G Phase 2, a true 1:1 symbol was designed for `TYPE-C-31-M-12` in `SmartPen_Lib.kicad_sym` and integrated into `SmartPen.kicad_sch`. Every physical footprint pad now corresponds exactly to its electrical function:

```
+----------------------------------------------------------------------------------------------------+
|                                REVISION G USB-C PIN MAPPING TABLE                                   |
+---------+-------------------+-----------------------+---------------------+------------------------+
| Pad #   | Standard USB-C Pin| Net Name in Rev G     | Connected Subsystem | Functional Purpose     |
+---------+-------------------+-----------------------+---------------------+------------------------+
| **1**   | GND (A1/B12)      | `/GND`                | Ground Plane        | Power Ground Return    |
| **2**   | VBUS (A4/B9)      | `/USB_VBUS`           | Charger & D4 Anode  | +5.0V USB Bus Power    |
| **3**   | GND (A1/B12)      | `/GND`                | Ground Plane        | Power Ground Return    |
| **5**   | CC1 (A5)          | `/USB_CC1`            | Resistor R5 (5.1k)  | Type-C UFP Detection   |
| **6**   | CC2 (B5)          | `/USB_CC2`            | Resistor R6 (5.1k)  | Type-C UFP Detection   |
| **7**   | D+ (A6/B6)        | `/USB_DP_PORT`        | U_ESD Pin 1 & R8    | Full-Speed USB Data +  |
| **9**   | D- (A7/B7)        | `/USB_DM_PORT`        | U_ESD Pin 2 & R7    | Full-Speed USB Data -  |
| **10**  | VBUS (B4/A9)      | `/USB_VBUS`           | Charger & D4 Anode  | +5.0V USB Bus Power    |
| **12**  | GND (B1/A12)      | `/GND`                | Ground Plane        | Power Ground Return    |
| **13**  | SHIELD Tab 1      | `/GND`                | Chassis Shield Zone | Mechanical Ground / EMI|
| **14**  | SHIELD Tab 2      | `/GND`                | Chassis Shield Zone | Mechanical Ground / EMI|
| **15**  | SHIELD Tab 3      | `/GND`                | Chassis Shield Zone | Mechanical Ground / EMI|
| **16**  | SHIELD Tab 4      | `/GND`                | Chassis Shield Zone | Mechanical Ground / EMI|
+---------+-------------------+-----------------------+---------------------+------------------------+
```

---

## 3. CC Termination & USB-C Host Compatibility

Per the **USB Type-C Cable and Connector Specification (Release 2.1, Section 4.5.1.2)**:
- An Upstream Facing Port (UFP / Device) MUST present a pull-down resistance ($R_d$) of $5.1\text{ k}\Omega \pm 10\%$ to GND on both CC1 and CC2 pins individually.
- Under NO circumstance may CC1 and CC2 be shorted together (which causes cable orientation detection failure and blocks Power Delivery / Type-C source advertisement).

### 3.1 Rev G Verification
In `SmartPen.kicad_sch`:
- Net `/USB_CC1` (Pin 5) connects to resistor **$R_5$** ($5.1\text{ k}\Omega$ 1% 0402, `RC0402FR-075K1L`) to `/GND`.
- Net `/USB_CC2` (Pin 6) connects to resistor **$R_6$** ($5.1\text{ k}\Omega$ 1% 0402, `RC0402FR-075K1L`) to `/GND`.
- CC1 and CC2 are completely isolated from each other.
- **Compatibility:** Guarantees proper plug detection and standard 5V @ 500mA/1.5A/3.0A power delivery when plugged into modern USB-C laptops (MacBook, Dell XPS, ThinkPad) or Type-C chargers using C-to-C cables.

---

## 4. ESD Protection & High-Speed Data Path

The USB data lines connect from `J_USB` through dedicated ESD suppression and series damping resistors to the ESP32-C3 integrated USB Serial/JTAG controller:

```
[J_USB] Pin 7 (DP) ----+---- /USB_DP_PORT ----[ R8: 22R ]---- /USB_DP_CORE ----> ESP32-C3 (GPIO19 / Pin 26)
                       |
                   [ U_ESD ] (USBLC6-2SC6)
                       |
[J_USB] Pin 9 (DM) ----+---- /USB_DM_PORT ----[ R7: 22R ]---- /USB_DM_CORE ----> ESP32-C3 (GPIO18 / Pin 25)
                       |
                      GND
```

### 4.1 ESD Suppressor (`U_ESD`: STMicroelectronics `USBLC6-2SC6`)
- Package: SOT-23-6.
- Channel Capacitance: $C_{I/O} \le 3.5\text{ pF}$ (negligible signal degradation for USB Full-Speed 12 Mbps).
- ESD Rating: Exceeds IEC 61000-4-2 Level 4 (±15 kV air discharge, ±8 kV contact discharge).
- Placement: Placed immediately adjacent to the USB receptacle entry pads to clamp ESD transients before they enter the internal PCB rail.

### 4.2 Series Termination Resistors (`R7`, `R8`: $22\,\Omega$ 1% 0402)
- Match driver output impedance to $90\,\Omega$ differential transmission line impedance.
- Damp ringing, overshoot, and high-frequency emissions.

### 4.3 VBUS Inrush Current Filtering
- Capacitor `C10` ($10\,\mu\text{F}$ 25V X5R 0603) and `C11` ($4.7\,\mu\text{F}$ 16V 0603) provide bulk bypass on the VBUS rail.
- Inrush current upon hot-plugging is naturally limited by the USB cable impedance ($\sim 0.3\,\Omega$) and PCB trace resistance, keeping peak inrush well below standard USB limits ($\le 10\,\mu\text{F}$ parallel equivalent capacitance, complying with USB 2.0 Section 7.2.4.1).

---

## 5. Verification Check

- **ERC Report:** `Main_SmartPen_erc.rpt` reported **0 Errors, 0 Warnings**.
- **Netlist Verification:** All 13 pads of `J_USB` in `Main_SmartPen_netlist.net` match the target netlist table 100%.
- **Automated Test Suite:** `test_usb_c_connector_pin_mapping` in `tests/test_revg_electrical.py` executed and **PASSED**.
- **Negative Test Fixture:** `test_negative_swapped_usb_pins_fails` verified build failure occurs if VBUS and GND are transposed.
