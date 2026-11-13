# Baseline Engineering Audit: Smart Pen Rev D

## 1. Executive Summary
- **Baseline Design Source**: `SmartPen_RevD_AutoLinked_DRAFT` (Rev D)
- **Status**: Non-functional staging draft — **BLOCKED for manufacturing**
- **Schematic Components**: 60 total
- **PCB Components**: 40 placed (20 unplaced)
- **Placeholder / Unresolved Footprints**: 19 components with `_TBD` footprints
- **Components Missing Real MPN / Orderable Parts**: 34 components
- **Pin-to-Pad Mismatches**: 1 among placed parts
- **PCB Routing**: 0 traces routed; 0 copper zones; staging board outline is provisional only (77.0 mm x 9.4 mm).

---

## 2. Component & Footprint Audit

### 2.1 Missing in PCB Staging Board (20 components)
The following 20 schematic components are completely absent from the PCB staging layout:
`D1, D2, D3, J_BAT, J_IMU, J_MOT, J_PWR, J_RF, J_SD, J_TOUCH, J_UART, J_USB, Q1, SW1, SW2, SW3, SW4, SW5, U_ESD, Y1`

### 2.2 Unresolved Footprints with TBD Placeholders (19 components)
| RefDes | Current Placeholder Footprint | Schematic Description / Part |
| :--- | :--- | :--- |
| SW1 | `TACT_2PAD_TBD` | RESET switch NO |
| SW2 | `TACT_2PAD_TBD` | BOOT switch NO |
| Y1 | `CRYSTAL_4PAD_TBD` | 40MHz +/-10ppm crystal |
| J_RF | `UFL_CONNECTOR_TBD` | U.FL RF ANTENNA |
| J_USB | `USB_C_16PIN_TBD` | USB2.0 Type-C receptacle |
| U_ESD | `USB_ESD_PART_TBD` | USB ESD array TBD |
| J_BAT | `BAT_2PIN_CONNECTOR_TBD` | 2P KEYED BATTERY |
| J_PWR | `REGULATOR_CARD_TBD` | 3V3 converter interface |
| SW3 | `SLIDE_SWITCH_TBD` | POWER on/off |
| J_IMU | `CONN_4P_TBD` | 4P KEYED FRONT IMU |
| U3 | `QFN20_4x4_P0.5_TBD` | MCP23008 QFN20 |
| SW4 | `TACT_2PAD_TBD` | ERASE button NO |
| SW5 | `TACT_2PAD_TBD` | MODE button NO |
| Q1 | `SOT23_GSD_TBD` | N-MOS logic level |
| J_MOT | `MOTOR_2PIN_TBD` | 2P vibration motor |
| D3 | `DIODE_SMD_TBD` | Flyback diode TBD |
| J_SD | `CONN_6P_TBD` | REMOTE MicroSD SPI carrier |
| J_TOUCH | `TOUCH_3PIN_TBD` | EXTERNAL touch controller |
| J_UART | `TESTPAD_4P_TBD` | UART debug pads |

### 2.3 Pin-to-Pad Count Mismatches (1 components)
| RefDes | Schematic Pins | PCB Pads | Schematic Package | PCB Package |
| :--- | :--- | :--- | :--- | :--- |
| U3 | 18 | 20 | `QFN20_4x4_P0.5_TBD` | `QFN20_4x4_P0.5_TBD` |

---

## 3. Electrical & Circuitry Deficiencies

### 3.1 Power Architecture & Regulation Blockers
1. **MCP73831 is NOT a Power-Path Regulator**:
   - The schematic uses U2 (`MCP73831T-2ACI/OT`) as a basic linear LiPo charger.
   - MCP73831 has NO power-path management (no automatic switchover between VBUS and VBAT). If the pen operates while charging, system current robs charge current from the termination sensing loop, potentially preventing charge termination or overheating the battery.
   - `CHG_STAT` (U2 pin 1) is floating (single-pin net, no MCU monitoring or LED indication).
2. **Missing 3.3 V Regulator (`J_PWR`)**:
   - The 3.3V supply is represented as a dummy header `J_PWR` (`REGULATOR_CARD_TBD`) rather than an onboard low-noise, high-PSR buck/buck-boost or high-current LDO.
   - ESP32-C3 requires >=500 mA peak transient capability for RF transmission bursts.
3. **Missing Battery Protection**:
   - The schematic lacks an onboard LiPo protection IC (e.g., DW01A + dual MOSFET FS8205A) for over-discharge (<2.8V), over-charge (>4.28V), and short-circuit protection, risking catastrophic failure if an unprotected raw pouch cell is attached.

### 3.2 ESP32-C3 Core & Strapping Verification
1. **Strapping Pins Allocation**:
   - `GPIO9` (BOOT / Strapping): Pulled high via R2 (10k) with SW2 to GND. (PASS)
   - `GPIO2` (Strapping): Pulled high via R3 (10k). (PASS)
   - `GPIO8` (Strapping): High during download boot. Currently floating in Rev D schematic.
2. **VDD_SPI & Internal Flash**:
   - U1 is `ESP32-C3FH4X` with 4MB embedded flash. Pin 18 (`VDD_SPI`) is decoupled by C5 (1uF). It is internally driven by an on-chip LDO and must NOT be connected to external 3.3V power. Rev D correctly keeps it isolated to C5.
3. **Clock / Crystal Circuit**:
   - Y1 has a placeholder footprint (`CRYSTAL_4PAD_TBD`). Needs an exact 40 MHz, 10 ppm, 10 pF/12 pF load crystal with verified load capacitors (C6, C7) and dampening inductor L1.

### 3.3 RF Design & Antenna Interface
1. **RF Matching & Transmission Line**:
   - Rev D uses a discrete pi-network (L2, C8, C9) feeding `J_RF` (`UFL_CONNECTOR_TBD`).
   - The RF trace must be designed as a 50-ohm coplanar waveguide with ground reference.
   - Ground keepout under antenna / connector is undefined on the staging board.

### 3.4 Peripheral & Sensor Deficiencies
1. **Front IMU (`J_IMU`)**:
   - Connected via `CONN_4P_TBD` to I2C bus (`I2C_SDA` on GPIO0, `I2C_SCL` on GPIO1).
   - Needs rigid mechanical retention, strain relief, and standardized keyed 1.0mm/1.25mm connector (e.g., JST SH or Molex PicoBlade).
2. **MicroSD Carrier (`J_SD`)**:
   - Connected via 6-pin remote header `CONN_6P_TBD` rather than an integrated micro-profile push-pull MicroSD socket, due to previous 9.4 mm board width constraints.
3. **Touch Controller (`J_TOUCH`)**:
   - Uses a 3-pin placeholder `TOUCH_3PIN_TBD`. Must be resolved to an actual capacitive touch controller (e.g., TTP223 / Azoteq IQS263 / Microchip CAP1203) with electrode conditioning.
4. **Haptic Motor Driver**:
   - Q1 uses placeholder `SOT23_GSD_TBD` with flyback diode D3 (`DIODE_SMD_TBD`). Drive signal is generated from U3 (MCP23008 expander). Needs verified logic-level N-MOSFET (e.g. DMG2302UK or AO3400A) and Schottky flyback (e.g. B0520W / 1N5819HW).
5. **GPIO Expander U3 (MCP23008)**:
   - Uses placeholder `QFN20_4x4_P0.5_TBD`. Needs footprint validation or pin optimization.

---

## 4. Mechanical & Enclosure Interface Deficiencies

1. **Envelope Constraints**:
   - Client specified: Max Outer Diameter 16 mm (target 15–16 mm), Total length 150–155 mm.
   - Internal clearance radius is ~6.5 to 7.0 mm (internal diameter ~13 to 14 mm depending on wall thickness >= 1.0–1.2 mm).
2. **Battery Below Rail**:
   - Battery must fit below the internal electronics rail without pinching wires or obstructing the central refill tube.
3. **Bayonet & Rail Latch**:
   - The existing CAD files have placeholder bayonet collars with no locking ramps, no detents, and no mechanical stops.
4. **Refill & Click Mechanism**:
   - Needs axial tunnel clearance through the entire assembly from tip through rear clicker.

---

## 5. Summary of Baseline Tests
- **KiCad ERC/DRC**: BLOCKED (EasyEDA format, KiCad CLI not natively installed).
- **Static Netlist Consistency**: 42 nets, 180 connections. 1 single-pin net (`CHG_STAT`).
- **PCB Parity**: 20 schematic components missing from PCB layout.
- **Manufacturing Readiness**: **FAIL** (Draft/Review stage only).
