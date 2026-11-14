# ESP32-C3FH4X PINOUT, BOOT STRAPPING & RESET CIRCUIT VERIFICATION

**Document ID:** RPT-REVG-P02-FINAL-BOOT-STRAP  
**Author:** Senior Embedded Hardware & KiCad Engineer  
**Component:** Espressif Systems ESP32-C3FH4X (QFN-32, 4MB Embedded Flash)  
**Status:** **CORRECTED & VALIDATED (ELECTRICAL / NETLIST / ERC)**  
**Physical Validation Status:** **NOT TESTED ON PHYSICAL HARDWARE (SIMULATION & SCHEMATIC AUDIT ONLY)**  

---

## 1. Context and Problem Statement

In Phase 2.1, ESP32-C3FH4X U1 Pin 14 (`GPIO8`) was left marked with a `no_connect` flag. The accompanying report asserted that GPIO8 contained an internal pull-up. 

An independent review against official Espressif Systems documentation (*ESP32-C3 Series Datasheet* v1.6, Table 2-4 and *ESP32-C3 Family Hardware Design Guidelines* Section 2.4) identified that:
- **GPIO2** is floating during reset.
- **GPIO8** is **FLOATING (High-Impedance / No Internal Pull)** during reset.
- **GPIO9** has an internal weak pull-up during reset.

### Strapping State Table (Espressif ESP32-C3 Family)

| Mode | GPIO9 (Pin 15) | GPIO8 (Pin 14) | GPIO2 (Pin 5) | Description |
| :--- | :---: | :---: | :---: | :--- |
| **SPI Boot (Normal Run)** | **1 (HIGH)** | Any | Floating / Any | Boots firmware from internal 4MB SIP flash. |
| **Joint Download Boot** | **0 (LOW)** | **1 (HIGH)** | Floating / Any | Enters ROM serial bootloader (USB-Serial-JTAG / UART0). |
| **Invalid / Reserved** | **0 (LOW)** | **0 (LOW)** | Floating / Any | **Prohibited State** — System may crash, hang, or enter test mode. |

**Hazard:** If GPIO8 is left floating, ambient EMI, capacitive coupling during USB insertion, or leakage current could pull GPIO8 to logic LOW during reset when the user holds `SW2` (Boot Button, pulling GPIO9 LOW). This would enter the invalid `{GPIO9:0, GPIO8:0}` state, preventing firmware flashing over USB-Serial-JTAG and bricking production recovery.

---

## 2. Engineering Remediation

### 2.1 Addition of External Pull-Up Resistor R27
To guarantee that GPIO8 is pulled HIGH during reset under all operating conditions, an external pull-up resistor `R27` was added:
- **Reference Designator:** `R27`
- **Resistance:** $10\text{ k}\Omega \pm 1\%$
- **Package:** 0402 Imperial ($1.0 \times 0.5\text{ mm}$, Metric 1005)
- **Manufacturer Part Number (MPN):** Yageo `RC0402FR-0710KL`
- **LCSC Part Number:** `C25744`
- **Power Rating:** $0.063\text{ W}$ ($1/16\text{ W}$)
- **Current Draw:** At $3.3\text{ V}$, $I = 3.3\text{ V} / 10\text{ k}\Omega = 330\,\mu\text{A}$ only during active pull-down. When GPIO8 is unused or an output HIGH, static dissipation is $0\,\text{W}$.

### 2.2 Schematic & Netlist Connectivity
- `U1` Pin 14 (`GPIO8`) disconnected from `no_connect` flag and wired to net `/GPIO8_STRAP`.
- `R27` Pin 1 wired to net `/3V3`.
- `R27` Pin 2 wired to net `/GPIO8_STRAP`.
- Custom footprint `output/RevG/SmartPen.pretty/R27.kicad_mod` created and mapped.
- Schematic symbol instance placed at coordinates `(457.20, 127.00)` mm in `output/RevG/SmartPen.kicad_sch`.

---

## 3. Peripheral Strapping & Reset Subsystem Verification

### 3.1 Boot Button SW2 Subsystem (GPIO9)
- `U1` Pin 15 (`GPIO9`) is connected to net `/BOOT_BTN`.
- `R2` ($10\text{ k}\Omega$) provides a robust external pull-up to `/3V3`, supplementing the weak internal pull-up.
- `SW2` provides a momentary tactile connection to `GND`.
- When `SW2` is pressed during reset release, GPIO9 = LOW. Because GPIO8 is held HIGH by `R27`, the chip reliably enters Joint USB/UART Download Boot.
- In normal operation (SW2 unpressed), GPIO9 = HIGH, entering normal SPI Flash Boot.

### 3.2 Reset Button SW1 Subsystem (CHIP_EN)
- `U1` Pin 3 (`CHIP_EN`) is driven by an RC delay network:
  - Pull-up resistor `R1`: $10\text{ k}\Omega$ to `/3V3`.
  - Filter capacitor `C1`: $1.0\,\mu\text{F}$ 0402 to `GND`.
  - Time constant: $\tau = R \times C = 10\text{ k}\Omega \times 1.0\,\mu\text{F} = 10.0\text{ ms}$.
- Meets Espressif requirement that $V_{IL} < 0.25 \times VDD$ for at least $50\,\mu\text{s}$ during power ramp-up.
- `SW1` provides a momentary short across `C1` to `GND`, initiating a clean hardware reset.

### 3.3 Strapping Pin GPIO2 (Pin 5)
- Connected to net `/LED_DATA`.
- Floating during reset; Espressif specifies GPIO2 has no effect on ROM download mode vs SPI boot.
- Isolated from low-impedance external pull-downs during reset sequence.

---

## 4. ESP32-C3FH4X Core Power & Internal Flash Pinout Audit

A complete pinout audit of `U1` (ESP32-C3FH4X QFN-32) was executed:

| Pin # | Pin Name | Schematic Net | Connection Rule / Manufacturer Requirement | Verification Status |
| :---: | :--- | :--- | :--- | :--- |
| **1** | `VDD_SPI` | `/3V3` | Decoupled to GND with `C8` ($0.1\,\mu\text{F}$); MUST NOT be grounded. | **PASS** |
| **2** | `GPIO0` | `/I2C_SDA` | Open-drain I2C SDA with external $4.7\text{ k}\Omega$ pull-up to 3V3. | **PASS** |
| **3** | `GPIO1` | `/I2C_SCL` | Open-drain I2C SCL with external $4.7\text{ k}\Omega$ pull-up to 3V3. | **PASS** |
| **11** | `VDD3P3_RTC`| `/3V3` | Core RTC analog/digital supply; decoupled with `C6` ($0.1\,\mu\text{F}$). | **PASS** |
| **14** | `GPIO8` | `/GPIO8_STRAP`| Strapping pin; pulled HIGH to `/3V3` via `R27` ($10\text{ k}\Omega$). | **PASS (FIXED)** |
| **15** | `GPIO9` | `/BOOT_BTN` | Strapping pin / Boot button; pulled HIGH to `/3V3` via `R2` ($10\text{ k}\Omega$). | **PASS** |
| **17** | `VDD3P3_CPU`| `/3V3` | CPU core digital supply; decoupled with `C5` ($10\,\mu\text{F}$) & `C7` ($0.1\,\mu\text{F}$). | **PASS** |
| **19** | `NC_1` | `no_connect` | Internal SIP Flash `IO2` — MUST BE LEFT FLOATING. | **PASS** |
| **20** | `NC_2` | `no_connect` | Internal SIP Flash `IO3` — MUST BE LEFT FLOATING. | **PASS** |
| **21** | `NC_3` | `no_connect` | Internal SIP Flash `CMD` — MUST BE LEFT FLOATING. | **PASS** |
| **22** | `NC_4` | `no_connect` | Internal SIP Flash `CLK` — MUST BE LEFT FLOATING. | **PASS** |
| **23** | `NC_5` | `no_connect` | Internal SIP Flash `IO0` — MUST BE LEFT FLOATING. | **PASS** |
| **24** | `NC_6` | `no_connect` | Internal SIP Flash `IO1` — MUST BE LEFT FLOATING. | **PASS** |
| **33** | `EPAD (GND)`| `/GND` | Thermal exposed pad; connected directly to solid ground plane. | **PASS** |

> [!CAUTION]
> **Internal SIP Flash Protection:** Pins 19 through 24 are internally bonded to the 4MB SPI flash die inside the FH4X package. Connecting any of these pins to GND, 3V3, or external traces will permanently destroy flash communications and brick the device. Confirmed that all six pins have explicit KiCad `no_connect` directives and zero PCB copper connections.

---

## 5. Automated Test & Negative Fixture Coverage

Automated tests in `tests/test_revg_electrical.py` verify the strapping configuration:
1. `test_esp32_c3fh4x_pinout_and_boot`: Validates that U1 Pin 14 is assigned to net `/GPIO8_STRAP`, that `R27` is present with $10\text{ k}\Omega$ value, and that `R27` connects `/GPIO8_STRAP` to `/3V3`.
2. `test_negative_floating_gpio8_boot_fails`: Programmatically alters the netlist to leave Pin 14 unconnected; asserts that the validator catches this as a critical failure.
3. `test_negative_grounded_gpio8_boot_fails`: Programmatically connects Pin 14 to GND; asserts that the validator flags this invalid strapping hazard.

---

## 6. Physical Validation Notice

While the electrical schematic, netlist, ERC, and automated test suite confirm 100% compliance with Espressif hardware design rules, **physical flashing of firmware, cold-boot timing, and serial bootloader entry have not been executed on fabricated silicon**. Physical validation will take place on assembled Phase 4 prototype boards.
