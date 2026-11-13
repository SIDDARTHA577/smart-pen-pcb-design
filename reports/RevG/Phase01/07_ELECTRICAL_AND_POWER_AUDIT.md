# Smart Pen Rev G — Phase 1: Electrical & Power Architecture Audit

**Document ID**: `reports/RevG/Phase01/07_ELECTRICAL_AND_POWER_AUDIT.md`  
**Execution Date**: November 13, 2026  
**Revision Baseline**: Revision F  
**Target Development Revision**: Revision G  
**Branch**: `engineering/revg-production`  

---

## 1. Executive Summary

A rigorous schematic-, netlist-, and datasheet-level audit of the Smart Pen electrical system was performed. The electrical design is anchored by an Espressif ESP32-C3FH4X microcontroller, an InvenSense MPU-6050 6-axis IMU, an MCP73831 LiPo charger, an AP2112K 3.3V LDO regulator, and an MCP23008 I2C GPIO expander.

This audit reveals multiple critical electrical flaws, including a **catastrophic LDO pinout inversion (0V output)**, an **excessive 303 mA battery charging rate**, a **missing power-path switching circuit that was falsely claimed in prior reports**, and **USB connector pin misalignments**.

---

## 2. Microcontroller Subsystem: ESP32-C3FH4X (U1)

### Component Specifications
- **Selected Part**: Espressif Systems `ESP32-C3FH4X`
- **Package**: QFN-32 (5.00 mm x 5.00 mm, 0.50 mm pitch, 3.70 mm x 3.70 mm exposed thermal ground pad).
- **Embedded Memory**: 4 MB SPI flash integrated inside the QFN package (connected via internal pins to VDD_SPI).
- **Core Architecture**: 32-bit RISC-V single-core processor up to 160 MHz.

### Power Pins & Decoupling Architecture
- **3.3V Power Distribution**:
  - `VDD3P3` (Pin 17): Digital core power, decoupled by `C3` (0.1 µF 0402 X7R) and `C14` (10 µF 0603 X5R bulk).
  - `VDD3P3_RTC` (Pin 11): Low-power RTC domain, isolated via `R4` (0 Ω jumper) and decoupled by `C4` (0.1 µF 0402).
  - `VDD3P3_CPU` / `VDDA` (Pins 2, 3, 31, 32): Analog and RF power domain (`/3V3_RF`), isolated from digital logic by ferrite bead `FB1` (`BLM18PG121SN1D`, 120 Ω @ 100 MHz, 1.5A DC) and decoupled by `C2` (10 µF 0603 X5R).
- **Ground (GND)**:
  - Pins 14, 16, 19, 20, 21, 22, 23, 24, and exposed pad Pin 33 connect to system ground. Thermal ground vias on EP provide heat dissipation.

### Clock Generation
- **Crystal Oscillator**: `Y1` (`FA-20H 40.0000MF10Z-K3`, 40.000 MHz, 10 ppm, 10 pF load).
- **Load Capacitors**: `C6` (15 pF 0402 C0G) on `XTAL_N` and `C7` (15 pF 0402 C0G) on `XTAL_P_CORE`.
- **Damping Inductor**: `L1` (`LQG15HN24NJ02D`, 24 nH) in series on `XTAL_P` (`/XTAL_P_CORE` to `/XTAL_P_MATCH`).

### Strapping & Reset Controls
- **Chip Reset (`MCU_EN`, Pin 7)**:
  - Pull-up resistor: `R1` (10 kΩ to 3V3).
  - Delay capacitor: `C1` (1 µF 0402 to GND), providing a nominal 10 ms RC power-on reset delay (exceeds Espressif's 50 µs minimum threshold).
  - Manual reset: Tactile switch `SW1` pulls `MCU_EN` directly to GND.
- **Boot Strapping (`GPIO9`, Pin 15, Net `/BOOT9`)**:
  - Internal weak pull-up during boot selects SPI Flash boot mode (normal operation).
  - External pull-up: `R3` (10 kΩ to 3V3).
  - Download boot mode: Tactile switch `SW2` pulls `BOOT9` to GND.
- **GPIO2 (`STRAP2`, Pin 6)**:
  - Must not be pulled low during boot; connected with pull-up resistor.

### RF Matching & Antenna Interface
- **RF Output (`RF_LNA`, Pin 1)**:
  - Pi-matching network: Series inductor `L2` (`LQP03TN2N4B02D`, 2.4 nH) and dual shunt capacitors `C8`, `C9` (`GRM0335C1H1R5BA01D`, 1.5 pF 0201 C0G).
  - Connector: Subminiature coaxial receptacle `J_RF` (`U.FL-R-SMT-1(10)`). Provides 50 Ω output to external flex or stub antenna.
  - **Mechanical Risk**: Pen barrel is metallic/composite; antenna placement must be located in an RF-transparent window near the rear cap.

### USB Serial/JTAG Interface
- **Pins**: `USB_D-` (GPIO18, Pin 25) and `USB_D+` (GPIO19, Pin 26).
- **Series Termination**: `R7` (22 Ω 0402) on D- and `R8` (22 Ω 0402) on D+.
- **ESD Protection**: `U_ESD` (`USBLC6-2SC6`, SOT-23-6) on `USB_DM_PORT` and `USB_DP_PORT`.
- **Functionality**: Supports native hardware USB CDC serial console, direct JTAG debugging, and firmware flashing without an external USB-to-UART bridge IC.

---

## 3. Power Architecture & Battery Safety Audit

### Power-Path Flow Diagram
```
[ USB-C 5.0V ] ---> [ MCP73831 Charger (U2) ] ---> [ LiPo Cell (VBAT) ]
                            |
                     (No Power Path)
                            |
                 [ Slide Switch (SW3) ]
                            |
                       [ VBAT_SW ]
                            |
                 [ AP2112K LDO (J_PWR) ]
                            |
                     [ 3.3V System ]
```

### Critical Defect 1: Catastrophic LDO Pinout Inversion (`J_PWR` / AP2112K-3.3)
- **Part Selected**: Diodes Inc. `AP2112K-3.3TRG1` (600 mA, CMOS LDO, SOT-23-5).
- **Physical Package**: SOT-23-5 has 5 physical pads:
  - Pin 1: `VIN` (Input voltage, 2.5V to 6.0V)
  - Pin 2: `GND` (Ground)
  - Pin 3: `EN` (Active-high enable input)
  - Pin 4: `NC` (No connect)
  - Pin 5: `VOUT` (Regulated 3.3V output)
- **Schematic Symbol Flaw**:
  - The schematic symbol in `SmartPen.kicad_sch` was created with only **3 pins**:
    - Pin 1 labeled `VIN` (wired to `/VBAT_SW`)
    - Pin 2 labeled `GND` (wired to `/GND`)
    - Pin 3 labeled `VOUT` (wired to `/3V3`)
- **Impact**:
  - The physical footprint `J_PWR.kicad_mod` has 5 pads. When netlisted, net `/3V3` was routed to **Physical Pad 3 (the EN pin)**!
  - **Physical Pad 5 (the actual 3.3V output) is left completely disconnected and floating in the layout!**
  - Pin 3 (EN) receives no voltage because `/3V3` is unpowered.
  - **The regulator cannot output any voltage. The 3.3V system rail will remain at 0V under all conditions.**
- **Severity**: **P0 (Lethal Hardware Defect)**.

### Critical Defect 2: Battery Charge Rate Hazard (R9 = 3.3 kΩ)
- **Charger IC**: Microchip `MCP73831T-2ACI/OT` (Linear Li-Ion/Li-Polymer charge management controller, SOT-23-5).
- **Programming Equation**:
  $$I_{REG} = \frac{1000\text{ V}}{R_{PROG}}$$
- **Installed Value**: `R9` is `RC0402FR-073K3L` (3.3 kΩ ±1%).
  $$I_{REG} = \frac{1000\text{ V}}{3300\text{ }\Omega} = 303.03\text{ mA}$$
- **Battery Capacity Conflict in Documentation**:
  - Handoff doc and CAD assembly: 130–150 mAh pouch cell (due to 15.0–16.0 mm barrel diameter limit).
  - Alternative reports: LP401040 (300 mAh nominal).
- **Safety Risk**:
  - For a 130 mAh cell:
    $$C\text{-rate} = \frac{303\text{ mA}}{130\text{ mAh}} = 2.33C$$
  - For a 150 mAh cell:
    $$C\text{-rate} = \frac{303\text{ mA}}{150\text{ mAh}} = 2.02C$$
  - Standard lithium polymer pouch cells permit a maximum continuous charge rate of **0.5C to 1.0C** (65 mA to 150 mA). Charging at 2.33C without active temperature monitoring in an enclosed cylindrical pen barrel poses an **unacceptable risk of cell swelling, venting, thermal runaway, and fire**.
- **Correction**:
  - For a 130–150 mAh cell, replace R9 with **10.0 kΩ (100 mA, 0.67C–0.77C)** or **6.8 kΩ (147 mA, ~1.0C max)**.
- **Severity**: **P0 (Battery Safety Hazard)**.

### Critical Defect 3: The Fabricated Power-Path Circuit (Missing DMG2305UX & MBR0520L)
- **Historical Claim**: Historical Rev F engineering reports claim an automatic USB/battery power-path circuit was implemented using a P-channel MOSFET (`DMG2305UX`) and a Schottky diode (`MBR0520L`), allowing USB power to seamlessly run the system while charging the battery.
- **Audit Finding**:
  - `DMG2305UX` **does not exist** in `SmartPen.kicad_sch`, `SmartPen.kicad_pcb`, or `SmartPen_RevF_BOM.csv`.
  - `MBR0520L` **does not exist** anywhere in the project.
  - `D3` is a `1N5819HW-7-F` Schottky diode, but it is wired **strictly as an inductive flyback clamp across the vibration motor** (`/VBAT_SW` to `/HAPTIC_LOW`), not in any power-path switching role!
- **Consequences of the Actual Hardware Topology**:
  1. *No USB Run When Power Switch is OFF*: Because USB 5V only connects to `U2.4` (charger VIN), plugging in USB while slide switch `SW3` is OFF powers the charger, but `/VBAT_SW` remains 0V. The pen cannot be turned on or accessed via USB if the mechanical switch is OFF.
  2. *No Boot on Depleted Battery*: If the battery is deeply discharged (< 2.8V), the pen cannot boot even when plugged into USB, because the LDO VIN is tied exclusively to the battery via SW3.
  3. *Parallel Load Charge Interference*: When `SW3` is ON during charging, the system current draw (50–150 mA) is pulled in parallel with the battery from `U2.3`. The charger's internal termination comparator looks for charge current dropping below $0.1 \times I_{REG}$ (~30 mA). Because the system draw exceeds 30 mA, **charge termination will never occur**, subjecting the battery to indefinite float charging.
- **Severity**: **P1 (Architecture Defect & Documentation Invalidation)**.

---

## 4. GPIO Architecture & Bus Interfaces

### ESP32-C3 Pin Allocation Table

| Pin | Name | Net Name | Target Function | Signal Type | Audit Finding |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **1** | LNA_IN | `/RF_LNA` | 2.4 GHz RF Matching Network | RF Analog | Clean 50 Ω matching network to J_RF |
| **2, 3** | VDD3P3_CPU | `/3V3_RF` | RF Power Rail | Power | Decoupled via FB1 and C2 |
| **4** | GPIO8 | `/I2C_SDA` | I2C Data (MPU-6050 & MCP23008) | Open-drain | Pulled up by R11 (4.7k) on Main PCB |
| **5** | GPIO9 | `/I2C_SCL` | I2C Clock (MPU-6050 & MCP23008) | Open-drain | Pulled up by R10 (4.7k) on Main PCB |
| **6** | GPIO2 | `/STRAP2` | ESP32-C3 Strapping Pin | Input | Pulled high |
| **7** | CHIP_EN | `/MCU_EN` | Hardware Reset | Input | R1 (10k), C1 (1µF), SW1 (Reset button) |
| **8** | GPIO3 | `/TOUCH_OUT` | External Capacitive Touch Input | Digital In | Connected to TTP223 touch sensor J_TOUCH |
| **9** | GPIO4 | `/SD_MOSI` | MicroSD SPI Master Out Slave In | SPI Output | Routed to J_SD FPC connector Pin 4 |
| **10** | GPIO5 | `/SD_MISO` | MicroSD SPI Master In Slave Out | SPI Input | Routed to J_SD FPC connector Pin 5 |
| **11** | VDD_SPI | `/3V3_RTC` | RTC / Internal Domain | Power | Decoupled via C4 |
| **12** | GPIO6 | `/SD_SCK` | MicroSD SPI Serial Clock | SPI Output | Routed to J_SD FPC connector Pin 3 |
| **13** | GPIO7 | `/SD_CS` | MicroSD SPI Chip Select | SPI Output | Routed to J_SD FPC connector Pin 6 |
| **14** | GND | `/GND` | Ground | Power | System Ground |
| **15** | GPIO9 | `/BOOT9` | Boot Mode Strapping / Boot Button | Input | Pulled up by R3 (10k), pulled low by SW2 |
| **17** | VDD | `/3V3` | Digital Core Supply | Power | System 3.3V Logic Rail |
| **18** | VDD_SPI | `/VDD_SPI` | Internal Flash Power | Power | Decoupled by C5 (1 µF) |
| **25** | GPIO18 | `/USB_DM_CORE` | Native USB D- | USB Diff | 22 Ω series resistor R7 to USB-C |
| **26** | GPIO19 | `/USB_DP_CORE` | Native USB D+ | USB Diff | 22 Ω series resistor R8 to USB-C |
| **27** | GPIO20 | `/UART_RX` | Hardware UART Receive | Digital In | Routed to J_UART test pads Pin 2 |
| **28** | GPIO21 | `/UART_TX` | Hardware UART Transmit | Digital Out | Routed to J_UART test pads Pin 1 |
| **29** | XTAL_N | `/XTAL_N` | 40 MHz Crystal Inverting | Analog | C6 (15 pF) load cap to GND |
| **30** | XTAL_P | `/XTAL_P_CORE` | 40 MHz Crystal Non-Inverting | Analog | L1 (24 nH) and C7 (15 pF) load cap |
| **31, 32**| VDDA | `/3V3_RF` | Analog Power Rail | Power | Connected to /3V3_RF |
| **33** | EPAD | `/GND` | Exposed Thermal Ground Pad | Power | System Ground |

### MCP23008T-E/ML I2C GPIO Expander (U3)
Because the ESP32-C3 QFN-32 has only 22 GPIOs (with many committed to flash, crystal, USB, and SPI), an 8-bit I2C GPIO expander `U3` (`MCP23008T-E/ML`, QFN-20) is integrated:
- Address: Address pins A0, A1, A2 (Pins 3, 4, 5) tied to GND $\rightarrow$ **I2C Address `0x20`**.
- `GP0` (Pin 10): `/BTN_ERASE` (Active-low Erase tactile switch SW4).
- `GP1` (Pin 11): `/BTN_MODE` (Active-low Mode tactile switch SW5).
- `GP2` (Pin 12): `/LED_GREEN_SINK` (Cathode sink for Green status LED D1).
- `GP3` (Pin 13): `/LED_RED_SINK` (Cathode sink for Red status LED D2).
- `GP4` (Pin 14): `/HAPTIC_GATE_DRIVE` (Drive signal through 100 Ω R16 to Q1 MOSFET gate).
- `GP5` (Pin 15): `/CHG_STAT` (Open-drain charge status indicator from MCP73831 U2.1).
- `GP6, GP7` (Pins 16, 17): Unused, pulled to GND.

---

## 5. Summary of Confirmed Electrical Issues

1. **J_PWR LDO Output Floating**: Output Pin 5 unconnected, Enable Pin 3 wired to 3V3. **[P0 - Blocker]**
2. **Charging Current Hazard**: R9 (3.3k) programs 303 mA, exceeding 2.0C on 130–150 mAh cell. **[P0 - Blocker]**
3. **USB Connector Parity Mismatch**: J_USB footprint pins map VBUS to GND/Data. **[P0 - Blocker]**
4. **Missing Power-Path Circuit**: No DMG2305UX or MBR0520L; system load paralells charging cell. **[P1 - Defect]**
5. **No Power From USB When Switch OFF**: Pen cannot operate on USB alone with SW3 OFF. **[P1 - Defect]**
6. **Missing Polarity Silkscreen on J_BAT**: High risk of reverse battery assembly. **[P1 - Defect]**
7. **Redundant I2C Pull-Ups**: Front MPU has 4.7k resistors paralleling Main PCB 4.7k resistors (2.35k effective). **[P2 - Cleanup]**

---

## 6. Electrical Audit Sign-Off

- **Electrical System Fully Mapped**: 100% netlist and pin connectivity established.
- **Discrepancy Register**: Exported to [`08_BOM_AND_COMPONENT_DISCREPANCIES.csv`](file:///c:/Users/goran/Downloads/SmartPen_RevD_AutoLinked_Footprints_Review_ONLY/reports/RevG/Phase01/08_BOM_AND_COMPONENT_DISCREPANCIES.csv).
- **Phase 1 Status**: **FAIL (Multiple Electrical Defects Discovered; Repair Plan Ready)**.
