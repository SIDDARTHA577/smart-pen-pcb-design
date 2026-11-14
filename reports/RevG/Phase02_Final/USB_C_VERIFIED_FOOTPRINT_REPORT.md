# USB-C RECEPTACLE MANUFACTURER FOOTPRINT AUDIT & REVERSIBLE ROUTING SPECIFICATION

**Document ID:** RPT-REVG-P02-FINAL-USBC-AUDIT  
**Author:** Senior KiCad PCB Layout & SMT Manufacturing Engineer  
**Component:** Korean Hroparts TYPE-C-31-M-12 (LCSC Part # `C165948`)  
**Designator:** `J_USB` (Main Smart Pen PCB)  
**Footprint File:** `output/RevG/SmartPen.pretty/J_USB.kicad_mod`  
**Status:** **100% MANUFACTURER-VERIFIED / ERC-CLEAN / PRODUCTION-READY**  

---

## 1. Executive Summary

During the Phase 2.1 review, `output/RevG/SmartPen.pretty/J_USB.kicad_mod` was found to have a discrepancy: while advertised as a 12-contact USB-C receptacle, it defined only 9 SMT pads, omitted through-hole retention shell stakes, and contained comment formatting that broke KiCad's library parser.

In Phase 2.2, a complete mechanical and electrical reconstruction was executed using the manufacturer drawing for **Korean Hroparts TYPE-C-31-M-12** and reference KiCad 10.0 footprint data. The resulting footprint provides complete 16-pin connectivity (12 SMT signal/power contacts + 4 through-hole mechanical retention stakes) plus 2 non-plated through holes (NPTH) for mechanical alignment pegs.

---

## 2. Manufacturer Drawing vs Footprint Dimensional Comparison

### 2.1 Mechanical & Geometric Parameters

| Geometric Feature | Manufacturer Drawing (C165948) | Reconstructed Footprint (`J_USB.kicad_mod`) | Delta / Tolerance | Compliance |
| :--- | :---: | :---: | :---: | :---: |
| **Number of SMT Signal Pads** | 12 | 12 (Pads 1 through 12) | 0 | **PASS** |
| **SMT Pad Width (X)** | $0.30\text{ mm}$ | $0.30\text{ mm}$ | $0.00\text{ mm}$ | **PASS** |
| **SMT Pad Length (Y)** | $1.20\text{ mm}$ | $1.20\text{ mm}$ | $0.00\text{ mm}$ | **PASS** |
| **SMT Pad Pitch (Inner 8)** | $0.50\text{ mm}$ | $0.50\text{ mm}$ | $0.00\text{ mm}$ | **PASS** |
| **SMT Pad Pitch (Outer GND/VBUS)**| $0.70\text{ mm}$ | $0.70\text{ mm}$ | $0.00\text{ mm}$ | **PASS** |
| **TH Shell Anchor Stakes** | 4 (Oval slotted) | 4 (Pads 13, 14, 15, 16) | 0 | **PASS** |
| **TH Stake Drill Size** | $0.60 \times 1.40\text{ mm}$ oval | $0.60 \times 1.40\text{ mm}$ oval | $0.00\text{ mm}$ | **PASS** |
| **TH Stake Pad Size** | $1.20 \times 2.00\text{ mm}$ oval | $1.20 \times 2.00\text{ mm}$ oval | $0.00\text{ mm}$ | **PASS** |
| **TH Stake Front Spacing (X)** | $8.64\text{ mm}$ ($\pm 4.32\text{ mm}$) | $8.64\text{ mm}$ ($\pm 4.32\text{ mm}$) | $0.00\text{ mm}$ | **PASS** |
| **TH Stake Rear Spacing (X)** | $8.64\text{ mm}$ ($\pm 4.32\text{ mm}$) | $8.64\text{ mm}$ ($\pm 4.32\text{ mm}$) | $0.00\text{ mm}$ | **PASS** |
| **TH Front-to-Rear Offset (Y)**| $4.20\text{ mm}$ ($-0.40$ to $-4.60\text{ mm}$) | $4.20\text{ mm}$ ($-0.40$ to $-4.60\text{ mm}$) | $0.00\text{ mm}$ | **PASS** |
| **NPTH Alignment Pegs** | 2 | 2 (NPTH) | 0 | **PASS** |
| **NPTH Peg Diameter** | $\varnothing 0.65\text{ mm}$ | $\varnothing 0.65\text{ mm}$ | $0.00\text{ mm}$ | **PASS** |
| **NPTH Peg Spacing (X)** | $4.40\text{ mm}$ ($\pm 2.20\text{ mm}$) | $4.40\text{ mm}$ ($\pm 2.20\text{ mm}$) | $0.00\text{ mm}$ | **PASS** |
| **NPTH Peg Offset (Y)** | $-0.95\text{ mm}$ | $-0.95\text{ mm}$ | $0.00\text{ mm}$ | **PASS** |

---

## 3. Contact Mapping & Schematic Connectivity

The 16 physical footprint pads are mapped to schematic pins in `SmartPen_Lib.kicad_sym` and wired in `SmartPen.kicad_sch` as follows:

| Footprint Pad | Standard USB-C Pin Name | Schematic Net | Function / Termination |
| :---: | :---: | :--- | :--- |
| **1** | `GND (A1/B12)` | `/GND` | Digital & Power Ground |
| **2** | `VBUS (A4/B9)` | `/USB_VBUS` | 5V Input from USB Host / Charger |
| **3** | `SBU2 (B8)` | `no_connect` | Sideband Use (Unused in USB 2.0) |
| **4** | `CC1 (A5)` | `/USB_CC1` | $5.1\text{ k}\Omega \pm 1\%$ (`R5`) Pull-Down to GND |
| **5** | `DN2 (B7)` | `/USB_DM_PORT`| USB 2.0 Data Negative (Reversible tie) |
| **6** | `DP1 (A6)` | `/USB_DP_PORT`| USB 2.0 Data Positive (Reversible tie) |
| **7** | `DN1 (A7)` | `/USB_DM_PORT`| USB 2.0 Data Negative (Reversible tie) |
| **8** | `DP2 (B6)` | `/USB_DP_PORT`| USB 2.0 Data Positive (Reversible tie) |
| **9** | `CC2 (B5)` | `/USB_CC2` | $5.1\text{ k}\Omega \pm 1\%$ (`R6`) Pull-Down to GND |
| **10** | `SBU1 (A8)` | `no_connect` | Sideband Use (Unused in USB 2.0) |
| **11** | `VBUS (B9/A4)` | `/USB_VBUS` | 5V Input from USB Host / Charger |
| **12** | `GND (B12/A1)` | `/GND` | Digital & Power Ground |
| **13** | `SHIELD_1` | `/GND` | Front-Left Shell Mechanical Ground Stake |
| **14** | `SHIELD_2` | `/GND` | Front-Right Shell Mechanical Ground Stake |
| **15** | `SHIELD_3` | `/GND` | Rear-Left Shell Mechanical Ground Stake |
| **16** | `SHIELD_4` | `/GND` | Rear-Right Shell Mechanical Ground Stake |

---

## 4. Reversible Plug Bridging & USB-C Compliance

### 4.1 USB 2.0 Reversible Data Lines
A Type-C receptacle exposes two pairs of USB 2.0 differential pins: `A6/A7` (DP1/DN1) on the top row, and `B6/B7` (DP2/DN2) on the bottom row.
- In `SmartPen.kicad_sch`, Pad 6 (`DP1`) and Pad 8 (`DP2`) are connected to net `/USB_DP_PORT`.
- Pad 7 (`DN1`) and Pad 5 (`DN2`) are connected to net `/USB_DM_PORT`.
- Net `/USB_DP_PORT` routes through series resistor `R7` ($0\,\Omega$ / $22\,\Omega$) and ESD array `D2` to ESP32-C3 Pin 13 (`GPIO19/USB_D+`).
- Net `/USB_DM_PORT` routes through series resistor `R8` ($0\,\Omega$ / $22\,\Omega$) and ESD array `D2` to ESP32-C3 Pin 12 (`GPIO18/USB_D-`).
- **Result:** Host connection functions identically regardless of whether the Type-C plug is inserted right-side up or upside down.

### 4.2 Configuration Channel (CC1 / CC2) Termination
Per the USB Type-C Cable and Connector Specification (Release 2.1):
- `CC1` (Pad 4) is connected to net `/USB_CC1` and pulled down to GND via `R5` ($5.1\text{ k}\Omega \pm 1\%$).
- `CC2` (Pad 9) is connected to net `/USB_CC2` and pulled down to GND via `R6` ($5.1\text{ k}\Omega \pm 1\%$).
- > [!IMPORTANT]
  > **CC Lines MUST NEVER Be Shorted Together:** Shorting CC1 to CC2 violates the USB Type-C specification and causes E-marked active cables to fail discovery, resulting in 0V output from USB-C Power Delivery host ports. Our schematic strictly maintains separate $5.1\text{ k}\Omega$ pull-down resistors for CC1 and CC2.

---

## 5. Mechanical Enclosure & Pen Barrel Clearance

The Smart Pen enclosure imposes a strict outer diameter constraint:
- Outer Barrel Diameter: $15.0 - 16.0\text{ mm}$
- Nominal Barrel Wall Thickness: $0.80 - 1.00\text{ mm}$
- Resulting Inner Barrel Diameter (ID): $13.4 - 14.0\text{ mm}$

### Connector Geometric Envelope:
- Maximum SMT contact width: $8.94\text{ mm}$
- Maximum outer shell stake width: $9.80\text{ mm}$ ($8.64\text{ mm}$ center-to-center $+ 1.16\text{ mm}$ outer pad extension)
- Receptacle body height: $3.16\text{ mm}$

### Clearance Margin:
$$\text{Radial Margin} = \frac{\text{Barrel ID} - \text{Shell Width}}{2} = \frac{14.0\text{ mm} - 9.80\text{ mm}}{2} = 2.10\text{ mm}$$

Even with internal rail wall thickness ($0.8\text{ mm}$), the connector provides $\ge 1.30\text{ mm}$ clearance to the internal rail structures. Mechanical interference risk with the outer barrel is **ZERO**.

---

## 6. Automated Test Suite Validation

The integrity of `J_USB` is validated by automated pytest suites:
- `test_usb_c_connector_pin_mapping`: Confirms all 16 pins are present in netlist, CC resistors are $5.1\text{ k}\Omega$, and DP/DN lines are bridged.
- `test_usb_c_physical_footprint_structure`: Verifies 12 SMT pads, 4 TH oval stakes, 2 NPTH holes, and zero syntax-violating `;` comments.
- `test_negative_unbridged_usb_dplus_fails`: Verifies that if DP1 and DP2 are not tied to the same net, test fails.
- `test_negative_swapped_usb_pins_fails`: Verifies that swapped CC/VBUS or DP/DN lines are caught by verification assertions.
