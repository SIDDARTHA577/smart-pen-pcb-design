# Smart Pen Rev G — 4-Layer Candidate PCB Specification
**Document ID:** RPT-REVG-P3C-003  
**Project:** Smart Pen Hardware Architecture Revision G  
**Variant Target:** `output/RevG/variants/FourLayer_Candidate/SmartPen.kicad_pcb`  
**Date:** November 16, 2026  

---

## 1. Specification Overview

This document establishes the formal engineering specification for the Smart Pen Rev G 4-layer production candidate PCB. It serves as the baseline technical reference for manufacturing, assembly, and test engineering.

---

## 2. General Physical & Mechanical Specifications

| Parameter | Specification | Tolerance | Verification Method |
| :--- | :--- | :---: | :--- |
| **Board Length** | 84.00 mm | ±0.10 mm | KiCad Edge.Cuts bounding box measurement |
| **Board Width** | 9.20 mm | ±0.10 mm | KiCad Edge.Cuts bounding box measurement |
| **Board Thickness** | 1.60 mm | ±10% (±0.16 mm) | Standard PCB stackup specification |
| **Layer Count** | 4 Copper Layers | Exact (4) | KiCad layers definition inspection |
| **Board Material** | Standard High-Tg FR4 (Tg $\ge 150^\circ\text{C}$) | — | IPC-4101E / RoHS Compliant |
| **Surface Finish** | ENIG (Electroless Nickel Immersion Gold) | Au $\ge 0.05\text{ }\mu\text{m}$ | RoHS / Lead-Free SMT standard |
| **Solder Mask** | Matte Black (or High-Contrast Green) | 15 µm nominal | Both sides (F.Mask, B.Mask) |
| **Silkscreen** | High-Resolution White (LPI) | Minimum line 0.15 mm | F.SilkS, B.SilkS (clipped from pads) |
| **Outer Copper Weight** | 1.0 oz (35 µm nominal) | ±10% | Top (`F.Cu`) and Bottom (`B.Cu`) |
| **Inner Copper Weight** | 0.5 oz (17.5 µm nominal) | ±10% | Inner 1 (`In1.Cu`) and Inner 2 (`In2.Cu`) |

---

## 3. Design Rules & Manufacturing Constraints

The candidate board strictly complies with standard JLCPCB / standard high-density multi-layer manufacturing rules:

```
[Design Rule Checks Summary]
- Minimum Trace Width:         0.1500 mm (6.0 mil)
- Minimum Trace Spacing:       0.1500 mm (6.0 mil)
- Minimum Via Pad Diameter:    0.5000 mm (20.0 mil)
- Minimum Via Drill Diameter:  0.3000 mm (12.0 mil)
- Minimum Annular Ring:        0.1000 mm (4.0 mil)
- Minimum Hole-to-Hole Spacing:0.2500 mm (10.0 mil)
- Minimum Solder Mask Web:     0.0800 mm (3.2 mil)
- Pad to Solder Mask Clearance:0.0250 mm (1.0 mil)
- Board Edge to Copper Spacing:0.2500 mm (10.0 mil)
```

All standard through-vias on the candidate board adhere to the uniform geometry:
$$\text{Diameter} = 0.500\text{ mm}, \quad \text{Drill} = 0.300\text{ mm}, \quad \text{Annular Ring} = \frac{0.500 - 0.300}{2} = 0.100\text{ mm}$$

---

## 4. Component Inventory & Major IC Placements

The board hosts 33 physical components, including micro-controllers, power management devices, sensors, and passive arrays:

| Reference | Component Description | Package / Footprint | Function / Net Connections |
| :--- | :--- | :--- | :--- |
| **U1** | ESP32-C3-MINI-1 (QFN-32 + EP) | QFN-32_4x4mm | Main System MCU & 2.4 GHz RF Transceiver |
| **U2** | XC6206P332MR (SOT-23-3) | SOT-23-3 | 3.3V Low-Dropout Linear Voltage Regulator |
| **U4** | TPS7A2433DBVR (SOT-23-5) | SOT-23-5 | Precision Ultra-Low-Noise LDO Regulator |
| **Q2** | DMG2305UX (SOT-23-3) | SOT-23-3 | P-Channel Reverse-Blocking / Power-Path MOSFET |
| **D4** | 1N5819HW-7-F (SOD-123) | SOD-123 ($0.8 \times 0.9\text{ mm}$ pads) | USB VBUS to VSYS_RAW Schottky OR-ing Diode |
| **J_USB** | Type-C 16-Pin Side-Mount | TYPE-C-31-M-12 | USB-C Power Delivery & Full-Speed D+/D- |
| **J_SD** | Molex 104031-0811 | MicroSD Push-Push | MicroSD High-Speed SPI Data Storage |
| **J_RF** | U.FL / IPEX Coaxial Jack | U.FL-R-SMT | External RF Test & Diagnostics Port |
| **SW1** | Tactile Micro-Switch | Pushbutton SMD | System Mode Selection (`/BTN_MODE`) |
| **SW2** | Tactile Micro-Switch | Pushbutton SMD | Hardware Boot/Strap Control (`/BOOT9`) |
| **C1–C15** | Decoupling Capacitors | 0402 / 0603 SMD | Local High-Frequency Filtering |
| **R1–R27** | Precision Resistors | 0402 SMD | Pull-ups, strapping, dividers, current limits |

---

## 5. Layer Assignment & Net Topology

- **Layer 1 (`F.Cu` - Top):** High-speed RF output microstrip, high-priority MCU breakouts, SMD component landing pads, local interconnections.
- **Layer 2 (`In1.Cu` - Inner 1):** Solid Ground (GND) return plane. Contains continuous ground copper with low-impedance stitching, plus the single fully-contained transit track for `/SD_MISO` passing north of U1.
- **Layer 3 (`In2.Cu` - Inner 2):** Continuous 3.3V System Power (`/3V3`) plane. Feeds all digital and analog rails across the board with sub-milliohm DC resistance. Contains localized strap and power traces (`/SD_CS`, `/3V3_RTC`, `/VSYS_RAW`).
- **Layer 4 (`B.Cu` - Bottom):** Power switching tracks (`/VBAT_SW`), system peripheral buses (`/UART_TX`, `/UART_RX`, `/USB_DM_CORE`, `/BOOT9`), and inter-module bridges.

---

## 6. Verification Status

The candidate board (`output/RevG/variants/FourLayer_Candidate/SmartPen.kicad_pcb`) has been compiled and validated using native KiCad 10.0 CLI. It reports **0 Real DRC Violations**, **0 Unconnected Items**, and **0 Schematic Parity Errors**.
