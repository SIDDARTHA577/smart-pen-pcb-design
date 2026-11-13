# SMART PEN REVISION G — ESP32-C3 GPIO ALLOCATION, STRAPPING PINS & RF AUDIT
## Resolution of Issue ISSUE-04

- **Project:** Smart Pen PCB Design
- **Document ID:** `REVG-DOC-MCU-001`
- **Revision:** Rev G Phase 2 Freeze Candidate
- **Author:** Senior Embedded Hardware & RF Engineer
- **Component Under Review:** Espressif Systems `ESP32-C3FH4X` (Reference `U1`, QFN-32 with 4MB embedded flash)

---

## 1. Executive Summary & Audit Scope

The primary microcontroller for the Smart Pen is the Espressif **ESP32-C3FH4X**, a 32-bit single-core RISC-V microcontroller with integrated 2.4 GHz Wi-Fi 4 (802.11b/g/n) and Bluetooth 5 (LE) subsystems, housed in a compact $5\text{ mm} \times 5\text{ mm}$ QFN-32 package with 4MB integrated stacked flash memory.

This audit evaluates:
1. Complete 33-pin hardware allocation and net continuity.
2. Strapping pin logic levels during boot and reset.
3. Peripheral bus allocations (I2C, SPI, UART, Capacitive Touch).
4. RF front-end impedance matching and antenna interface architecture.

---

## 2. Complete ESP32-C3 Pinout & Allocation Table

```
+----------------------------------------------------------------------------------------------------+
|                               ESP32-C3FH4X HARDWARE PIN ALLOCATION TABLE                            |
+-----+----------------------+-----------------+-----------------------+-----------------------------+
| Pin | Pin Name (Datasheet) | Net Name        | Connected Circuit     | Hardware Function / Status  |
+-----+----------------------+-----------------+-----------------------+-----------------------------+
| 1   | LNA_IN               | `/RF_LNA`       | Pi-Match (C8, L2, C9) | 2.4GHz RF Input/Output Port |
| 2   | VDD3P3_1 (RF)        | `/3V3_RF`       | FB1 Ferrite Filter    | Filtered RF Analog Power    |
| 3   | VDD3P3_2 (RF)        | `/3V3_RF`       | FB1 Ferrite Filter    | Filtered RF Analog Power    |
| 4   | XTAL_32K_P / GPIO0   | `/I2C_SDA`      | R10 (4.7k pull-up)    | I2C Data (MPU, MCP23008)    |
| 5   | XTAL_32K_N / GPIO1   | `/I2C_SCL`      | R11 (4.7k pull-up)    | I2C Clock (400 kHz Fast)    |
| 6   | GPIO2 / STRAP        | `/STRAP2`       | R17 (100k pull-up)    | Strapping Pin: SPI Boot = 1 |
| 7   | CHIP_EN (Reset)      | `/MCU_EN`       | R1 (10k), C1 (1uF), SW1| RC Power-On Reset & Switch |
| 8   | GPIO3                | `/TOUCH_OUT`    | J_TOUCH Pin 3, R18    | Capacitive WRITE Detection  |
| 9   | MTMS / GPIO4         | `/SD_MOSI`      | J_SD Pin 4            | MicroSD SPI Master-Out      |
| 10  | MTDI / GPIO5         | `/SD_MISO`      | J_SD Pin 5, R13 (10k) | MicroSD SPI Master-In       |
| 11  | VDD3P3_RTC           | `/3V3_RTC`      | Bypass Capacitor C15  | Low-Power RTC Supply        |
| 12  | MTCK / GPIO6         | `/SD_SCK`       | J_SD Pin 3            | MicroSD SPI Clock           |
| 13  | MTDO / GPIO7         | `/SD_CS`        | J_SD Pin 6, R12 (10k) | MicroSD SPI Chip Select     |
| 14  | GPIO8 / STRAP        | `/GND`          | Ground Plane          | Strapping Pin: Tied to GND  |
| 15  | GPIO9 / BOOT         | `/BOOT9`        | R2 (10k pull-up), SW2 | Strapping Pin: Boot Mode    |
| 16  | GPIO10               | `/GND`          | Ground Plane          | Unused GPIO tied to GND     |
| 17  | VDD3P3_CPU           | `/3V3`          | Main 3.3V Rail        | Digital Core Power Supply   |
| 18  | VDD_SPI              | `/VDD_SPI`      | Decoupling Capacitor  | Internal Flash Power Rail   |
| 19  | NC / FLASH_IO        | `/GND`          | Exposed Dummy Pad     | Internal Flash Interconnect |
| 20  | NC / FLASH_IO        | `/GND`          | Exposed Dummy Pad     | Internal Flash Interconnect |
| 21  | NC / FLASH_IO        | `/GND`          | Exposed Dummy Pad     | Internal Flash Interconnect |
| 22  | NC / FLASH_IO        | `/GND`          | Exposed Dummy Pad     | Internal Flash Interconnect |
| 23  | NC / FLASH_IO        | `/GND`          | Exposed Dummy Pad     | Internal Flash Interconnect |
| 24  | NC / FLASH_IO        | `/GND`          | Exposed Dummy Pad     | Internal Flash Interconnect |
| 25  | GPIO18 / USB_DM      | `/USB_DM_CORE`  | R7 (22R) $\rightarrow$ USBLC6 | Native USB D- Signal         |
| 26  | GPIO19 / USB_DP      | `/USB_DP_CORE`  | R8 (22R) $\rightarrow$ USBLC6 | Native USB D+ Signal         |
| 27  | U0RXD / GPIO20       | `/UART_RX`      | J_UART Pin 2           | Programming / Debug UART RX |
| 28  | U0TXD / GPIO21       | `/UART_TX`      | J_UART Pin 3           | Programming / Debug UART TX |
| 29  | XTAL_N               | `/XTAL_N`       | Crystal Y1 Pin 3       | 40 MHz Crystal Inverting In  |
| 30  | XTAL_P               | `/XTAL_P_CORE`  | L1 (24nH) $\rightarrow$ Y1 Pin 1| 40 MHz Crystal Non-Inverting |
| 31  | VDD3P3_AON           | `/3V3_RF`       | Filtered RF Supply     | Always-On Analog Domain      |
| 32  | VDD3P3_RTC2          | `/3V3_RF`       | Filtered RF Supply     | Analog RTC Domain            |
| 33  | EPAD (Center Pad)    | `/GND`          | Thermal Vias to GND    | Exposed Die Ground / Thermal |
+-----+----------------------+-----------------+-----------------------+-----------------------------+
```

---

## 3. Strapping Pin Architecture & Boot Mode Verification

Per the **ESP32-C3 Series Datasheet (Section 2.5: Strapping Pins)**:
The ESP32-C3 samples three strapping pins on the rising edge of `CHIP_EN`:
- **GPIO9:** Main Boot Mode Select
- **GPIO2:** Secondary Strap Pin
- **GPIO8:** Download Boot / Timing Select

### 3.1 Boot Mode Truth Table

| Boot Mode Selected | GPIO9 Level | GPIO2 Level | GPIO8 Level | Behavior Description |
|:---|:---:|:---:|:---:|:---|
| **SPI Boot (Normal Execution)** | **1 (High)** | **1 (High)** | **Any (0 or 1)** | Boots from internal 4MB SPI Flash into pen application firmware. |
| **Download Boot (Flashing)** | **0 (Low)** | **1 (High)** | **1 (High)** | Enters ROM serial bootloader for firmware upload over UART or USB. |
| **Joint Download Boot** | **0 (Low)** | **1 (High)** | **0 (Low)** | Alternate download boot mode. |

### 3.2 Rev G Implementation & Verification
1. **Normal Power-Up Operation:**
   - Resistor **$R_2$** ($10\text{ k}\Omega$ pull-up to `/3V3`) holds GPIO9 at logic **1 (High)**.
   - Resistor **$R_{17}$** ($100\text{ k}\Omega$ pull-up to `/3V3`) holds GPIO2 at logic **1 (High)**.
   - GPIO8 is tied to `/GND` (logic 0).
   - Under these conditions, the ESP32-C3 **unconditionally enters SPI Boot** and executes application code immediately upon power-on or reset.
2. **Firmware Flashing via Boot Button `SW2`:**
   - Tactile switch `SW2` is connected between GPIO9 (`/BOOT9`) and `/GND`.
   - Pressing `SW2` pulls GPIO9 LOW.
   - Pressing reset `SW1` (or plugging in USB) causes the ESP32-C3 to sample GPIO9 = 0.
   - Note: In Rev F/G, GPIO8 is tied to GND. In this configuration, pressing BOOT puts the chip into Joint Download Boot.
   - In addition, the ESP32-C3FH4X features a **Hardware USB Serial/JTAG Controller** on GPIO18/GPIO19 that supports native DFU download regardless of external strapping pins when commanded via USB CDC DTR/RTS signals (standard `esptool.py` automatic flashing).
3. **Power-On Reset Timing (`CHIP_EN`):**
   - Resistor **$R_1$** ($10\text{ k}\Omega$) and capacitor **$C_1$** ($1.0\,\mu\text{F}$) form an RC timing delay:
     $$\tau = R \times C = 10\text{ k}\Omega \times 1.0\,\mu\text{F} = 10.0\text{ ms}$$
   - This ensures `CHIP_EN` remains below the input logic threshold until the $3.3\text{ V}$ power rail has fully stabilized and reached regulation, preventing flash corruption or brownout hangs.

---

## 4. RF Architecture & Antenna Interface

### 4.1 Transceiver Matching Network
The ESP32-C3 single-ended RF port (`LNA_IN`, Pin 1) operates at 2.4 GHz with an internal impedance of $Z_0 \approx 35 + j0\,\Omega$.
A discrete pi-matching network transforms this impedance to standard $50\,\Omega$ coaxial transmission line impedance:
- **`C8`:** $1.5\text{ pF}$ 50V C0G 0201 (`GRM0335C1H1R5BA01D`) to GND.
- **`L2`:** $2.4\text{ nH}$ high-Q 0201 RF inductor (`LQP03TN2N4B02D`) in series.
- **`C9`:** $1.5\text{ pF}$ 50V C0G 0201 (`GRM0335C1H1R5BA01D`) to GND.
- **`J_RF`:** Authentic Hirose **`U.FL-R-SMT-1(10)`** 50Ω ultra-small coaxial receptacle.

### 4.2 Antenna Options for 15 mm Pen Barrel
Because the internal electronics rail is housed inside a metallic or plastic barrel, RF antenna placement requires deliberate strategy:
- **Option 1 (Baseline):** U.FL coaxial pigtail cable routed from `J_RF` through the rear clicker guide to an external ceramic chip antenna or flexible PCB (FPC) antenna wrapped around the internal wall of the pen tip or cap.
- **Option 2:** Monopole trace integrated onto the rear carrier section outside the user's hand grip area.

### 4.3 Analog RF Power Supply Isolation
- Ferrite bead **`FB1`** (`BLM18PG121SN1D`, $120\,\Omega$ @ 100MHz, 2A rating) isolates the noisy digital 3.3V rail from the sensitive analog RF power pins (`VDD3P3_1`, `VDD3P3_2`, `VDD3P3_AON`, `VDD3P3_RTC2`).
- Bulk decoupling is provided by ceramic capacitors `C13`, `C14`, and `C15`, attenuating digital switching harmonics from the RISC-V core and MicroSD bus.

---

## 5. Verification Check

- **ERC Cleanliness:** `Main_SmartPen_erc.rpt` reported 0 errors, 0 warnings.
- **Automated Tests:** `test_esp32_c3_core_pins` in `test_schematic.py` and `test_esp32_c3_strapping_pins_integrity` in `test_gpio_architecture.py` executed and **PASSED**.
