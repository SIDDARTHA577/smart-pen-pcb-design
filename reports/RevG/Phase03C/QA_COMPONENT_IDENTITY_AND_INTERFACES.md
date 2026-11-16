# Smart Pen Rev G — Component Identity & Inter-Board Interface Audit
**Document ID:** QA-REVG-P3C-004  
**Project:** Smart Pen Hardware Architecture Revision G  
**Variant:** Four-Layer Evaluation Candidate (`output/RevG/variants/FourLayer_Candidate/SmartPen.kicad_pcb`)  
**Date:** November 16, 2026  
**Status:** Component Identifications Formally Reconciled  

---

## 1. Executive Summary & Statement of Fact

Previous Phase 3C reports contained critical inaccuracies regarding the microcontroller package, the MicroSD interface topology, and the wireless antenna configuration. This report establishes the authoritative truth extracted directly from the native KiCad 10 schematic (`SmartPen.kicad_sch`), PCB layout (`SmartPen.kicad_pcb`), and project libraries.

### Key Corrections Summary
1. **Microcontroller U1 is an `ESP32-C3FH4X` SoC:** It is a discrete $5.0 \times 5.0\text{ mm}$ QFN-32 chip with embedded 4MB flash, external 40 MHz crystal ($Y_1$), and discrete passive matching. It is **NOT** a pre-certified `ESP32-C3-MINI-1` module with integrated shield and PCB antenna.
2. **MicroSD Connector `J_SD` is an FFC/FPC Connector:** It is a Hirose `FH12-6S-0.5SH(55)` 6-pin, 0.5 mm pitch flat flexible cable connector. It is **NOT** a directly soldered Molex MicroSD card socket. It routes signals via an external flexible cable to a separate daughterboard (`MicroSD_Carrier`).
3. **No On-Board RF Antenna Exists:** The RF output path from U1 terminates directly into a surface-mount Hirose U.FL coaxial receptacle (`J_RF`). There is no printed PCB trace antenna or ceramic chip antenna on the main PCB.

---

## 2. Authoritative Component Identity Ledger

The following table documents the verified hardware components on the Smart Pen Rev G board:

| RefDes | Part Number | Manufacturer | Package / Footprint | Description / Verified Role | Previous Misidentification |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **U1** | `ESP32-C3FH4X` | Espressif Systems | QFN-32 ($5.0 \times 5.0\text{ mm}$) / `SmartPen:U1` | 32-bit RISC-V SoC, 4MB embedded flash, 2.4 GHz Wi-Fi 4 + BLE 5.0 | Inaccurately described as `ESP32-C3-MINI-1` module |
| **U2** | `MCP73831T-2ACI/OT` | Microchip Technology | SOT-23-5 / `SmartPen:U2` | Miniature Single-Cell, Fully Integrated Li-Ion/Li-Polymer Charge Management Controller ($100\text{ mA}$) | Confirmed correct |
| **U3** | `MCP23008T-E/ML` | Microchip Technology | QFN-20 ($4.0 \times 4.0\text{ mm}$) / `SmartPen:U3` | 8-bit I2C Bus I/O Expander with open-drain interrupt | Confirmed correct |
| **U4** | `AP2112K-3.3TRG1` | Diodes Incorporated | SOT-23-5 / `SmartPen:J_PWR` | 600 mA Low Dropout (LDO) Linear Regulator with Enable ($3.3\text{V}$) | Confirmed correct |
| **J_SD** | `FH12-6S-0.5SH(55)` | Hirose Electric | 6-pin SMT 0.5mm pitch / `SmartPen:J_SD` | Bottom-contact FFC/FPC connector linking to separate MicroSD carrier PCB | Inaccurately described as a mounted Molex MicroSD socket |
| **J_IMU** | `SM04B-SRSS-TB(LF)(SN)` | JST | 4-pin SMT 1.0mm pitch / `SmartPen:J_IMU` | Right-angle SH header connecting to detachable front MPU sensor board | Confirmed correct |
| **J_RF** | `U.FL-R-SMT-1(10)` | Hirose Electric | Ultra-miniature SMT / `SmartPen:J_RF` | 50 Ω coaxial RF receptacle for external antenna connection | Inaccurately implied on-board antenna existed |
| **J_USB** | `TYPE-C-31-M-12` | Hroparts / Korean | 16-pin / 12-pin SMT / `SmartPen:J_USB` | Mid-mount USB Type-C receptacle with side-entry access | Confirmed correct |
| **Q1** | `AO3400A` | Alpha & Omega Semi | SOT-23-3 / `SmartPen:Q1` | 30V N-Channel MOSFET for haptic motor PWM low-side drive | Confirmed correct |
| **Q2** | `DMG2305UX` | Diodes Incorporated | SOT-23-3 / `SmartPen:Q1` | 20V P-Channel MOSFET for automatic battery/USB power-path selection | Confirmed correct |
| **D3** | `1N5819HW-7-F` | Diodes Incorporated | SOD-123 / `SmartPen:D3` | Flyback freewheeling clamp diode across haptic motor | Confirmed correct |
| **D4** | `1N5819HW-7-F` | Diodes Incorporated | SOD-123 / `SmartPen:D4` | Reverse-current blocking Schottky diode from USB VBUS to VSYS_RAW | Footprint reconciled (was `SmartPen:D3`) |

---

## 3. MicroSD Architecture & Inter-Board Cabling Verification

### 3.1 Separate Daughterboard Architecture
The Smart Pen architecture divides the MicroSD subsystem across two distinct physical PCBs:
1. **Main PCB (`output/RevG/variants/FourLayer_Candidate/SmartPen.kicad_pcb`):** Hosts the MCU, power management, RF, and the 6-pin FFC connector `J_SD`.
2. **MicroSD Carrier PCB (`output/RevG/MicroSD_Carrier/` and `output/RevF_Client_Delivery/02_KiCad_Source/MicroSD_Carrier/`):** A dedicated miniature carrier board that holds the physical Molex push-push MicroSD socket (`104031-0811`).

### 3.2 Cable Pinout & Net Alignment
The pinout across the Hirose `FH12-6S-0.5SH(55)` interface is identical and verified 1-to-1 between the main board and the carrier board:

| Pin Number | J_SD Pad (Main PCB) | FFC Conductor | MicroSD Carrier Header | SPI Net Function |
| :---: | :---: | :---: | :---: | :--- |
| **1** | `/3V3` | Conductor 1 | `VCC` | 3.3V Power Supply |
| **2** | `/GND` | Conductor 2 | `GND` | Ground Reference |
| **3** | `/SD_SCK` | Conductor 3 | `SCK` | SPI Serial Clock |
| **4** | `/SD_MOSI` | Conductor 4 | `MOSI` | Master Out Slave In |
| **5** | `/SD_MISO` | Conductor 5 | `MISO` | Master In Slave Out |
| **6** | `/SD_CS` | Conductor 6 | `CS` | Active-Low Chip Select |

### 3.3 Mechanical Routing & Cable Orientation
- **FFC Specification:** 6-conductor, $0.5\text{ mm}$ pitch, bottom-contact, polyester insulation with polyimide stiffener.
- **Orientation:** Because both `J_SD` on the main board and the carrier connector use bottom-contact receptacles, the cable must have contacts on the bottom at both ends (same-side contacts, Type A) or reverse-side (Type B) depending on whether the carrier PCB is flipped over the battery.
- **Refill Click Clearance:** The flexible cable must route around the pen refill cartridge clicker tube (diameter $3.0\text{–}4.0\text{ mm}$). Minimum dynamic bend radius of the FFC ($R \ge 2.0\text{ mm}$) must be preserved in Phase 4 CAD.

---

## 4. RF Architecture & Missing Antenna Analysis

### 4.1 Circuit Topology
- The ESP32-C3FH4X RF port (Pin 1) connects to a discrete matching network:
  - $L_2 = 2.4\text{ nH}$ (`LQP03TN2N4B02D`)
  - $C_8 = 1.5\text{ pF}$ (`GRM0335C1H1R5BA01D`)
  - $C_9 = 1.5\text{ pF}$ (`GRM0335C1H1R5BA01D`)
- The matching network terminates at `J_RF` (Hirose `U.FL-R-SMT-1(10)`).

### 4.2 Missing Component & Integration Gap
- **No Internal Antenna:** There is no trace antenna or chip antenna anywhere on the PCB.
- **Physical Dependency:** Wireless communication is impossible without an external 2.4 GHz antenna connected to `J_RF`.
- **Identified Gap:** The bill of materials (BOM), CAD assembly, and mechanical specifications currently lack:
  1. An approved manufacturer part number for the external 2.4 GHz antenna (e.g. Molex 146153 flexible dipole or custom chassis-mounted flex).
  2. The coaxial pigtail cable assembly (U.FL to antenna, diameter $0.81\text{ mm}$ or $1.13\text{ mm}$, length $35\text{–}50\text{ mm}$).
  3. Designated mounting surface and RF keep-out within the pen enclosure.
- **Regulatory Impact:** Because the system uses a discrete SoC (`ESP32-C3FH4X`) rather than a pre-certified modular transceiver, any external antenna choice directly impacts full FCC / CE intentional radiator certification.

---

## 5. Front MPU Sensor Interface (`J_IMU`)

- **Connector:** JST `SM04B-SRSS-TB(LF)(SN)` (1.0 mm pitch, 4-pin, horizontal SMT).
- **Location:** Front tip of main PCB ($X = 3.20\text{ mm}, Y = 4.60\text{ mm}$).
- **Pinout:**
  - Pin 1: `/3V3` (Power)
  - Pin 2: `/GND` (Ground)
  - Pin 3: `/I2C_SDA` (Data)
  - Pin 4: `/I2C_SCL` (Clock)
- **Destination:** Connects via a 4-conductor micro-harness to the detachable `Front_MPU` daughterboard located in the pen nose cone.
