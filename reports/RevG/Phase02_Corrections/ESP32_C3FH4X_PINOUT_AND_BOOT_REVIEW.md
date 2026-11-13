# SMART PEN REVISION G — ESP32-C3FH4X PINOUT, BOOT STRAPPING & INTERNAL FLASH AUDIT
## Resolution of Strapping Pin Faults and Internal Flash Grounding Hazards

- **Project:** Smart Pen Hardware System
- **Document ID:** `REVG-DOC-MCU-002`
- **Revision:** Rev G Phase 2.1
- **Component Under Review:** Espressif Systems `ESP32-C3FH4X` QFN-32 (`U1`)
- **Author:** Senior Embedded Electronics & Firmware Integration Engineer

---

## 1. Component Identification & Architecture

The central controller of the Smart Pen is the Espressif **ESP32-C3FH4X**, a 32-bit RISC-V single-core microcontroller with integrated $2.4\text{ GHz}$ Wi-Fi and Bluetooth 5 (LE) subsystems.

### 1.1 The Embedded Flash Subsystem (FH4X Architecture)
Unlike standard ESP32-C3 chips (such as the ESP32-C3FN4 or base ESP32-C3), the **ESP32-C3FH4X** incorporates a $4\text{ MB}$ ($32\text{ Mbit}$) high-temperature Quad SPI flash die stacked directly inside the $5 \times 5\text{ mm}$ QFN-32 package.
- In standard ESP32-C3 chips, package pins 19 through 24 break out the SPI flash bus (GPIO12/SPIHD, GPIO13/SPIWP, GPIO14/SPICS0, GPIO15/SPICLK, GPIO16/SPID, GPIO17/SPIQ) to connect an external SPI flash memory IC.
- In the **ESP32-C3FH4X**, these signals are wire-bonded **internally** between the MCU die and the flash die.
- **Espressif Datasheet Directive (Section 2.1 Pin Description, Table 2-1):**
  > *"For ESP32-C3FH4X, pins 19–24 are not connected to the package pins and should be left unconnected/floating (do not connect to GND or any other net)."*

---

## 2. Root Cause Analysis of the Rev F / Phase 2 Grounding Defect

In the inherited Revision F schematic and uncorrected Rev G Phase 2 files:
- **Pins 19, 20, 21, 22, 23, and 24** were tied directly to `/GND`!
- **Pin 14 (GPIO8)** was tied directly to `/GND`!
- **Pin 16 (GPIO10)** was tied directly to `/GND`!

### 2.1 Hazards of Grounding Pins 19–24
1. **Internal Flash Contention:** Although the package pins are marked NC externally, any internal parasitic leakage, package substrate metallization, or wire bond misregistration could bridge the high-speed Quad SPI flash lines (operating at up to $80\text{ MHz}$) to ground, causing flash read corruption or chip bricking.
2. **Signal Integrity Degradation:** Grounding unused flash leadframe fingers creates parasitic capacitive stubs adjacent to high-speed RF and USB traces.

### 2.2 Hazards of Grounding Pin 14 (GPIO8)
Per the **ESP32-C3 Series Datasheet (Section 2.5 Strapping Pins)**:
- Pin 15 (`GPIO9`) and Pin 14 (`GPIO8`) are strapping pins that determine the chip's boot mode upon reset:

| Strapping Pin State | Boot Mode | Function / Behavior |
| :--- | :--- | :--- |
| **`GPIO9 = 1`** | **SPI Flash Boot** | Default normal operational boot from embedded 4MB flash. `GPIO8` state is ignored. |
| **`GPIO9 = 0`, `GPIO8 = 1`** | **ROM Download Boot** | Standard bootloader mode for flashing firmware via UART0 (`TXD0`/`RXD0`) or USB Serial/JTAG. |
| **`GPIO9 = 0`, `GPIO8 = 0`** | **Joint Download Boot** | Non-standard / reserved test mode. Breaks standard esptool / ESP-IDF serial programming! |

**The Fatal Flaw:** When Pin 14 (GPIO8) was tied to `/GND`:
- Whenever a developer pressed `SW2` (`BOOT9` button) to ground GPIO9 for flashing, the hardware forced `GPIO9 = 0` AND `GPIO8 = 0`.
- The MCU entered **Joint Download Boot** instead of standard **ROM Download Boot**, causing serial programming tools to fail to synchronize with the chip!

---

## 3. Revision G Phase 2.1 Corrections

In `output/RevG/SmartPen.kicad_sch`, all grounding ties on Pins 14, 16, and 19–24 have been completely removed and replaced with explicit KiCad `(no_connect)` flags.

```
       ESP32-C3FH4X (U1)
       +-----------------------+
       |                       |
 14 ---| GPIO8/STRAP      [NC] | <--- Explicit No-Connect (Internal weak pull-up active)
 15 ---| GPIO9/BOOT  --/BOOT9  | <--- Pulled up by R2 (10k) to 3V3, grounded by SW2
 16 ---| GPIO10           [NC] | <--- Explicit No-Connect (Floating)
 17 ---| VDD3P3_CPU   --/3V3   |
 18 ---| VDD_SPI      --C13    | <--- 0.1uF Decoupling Capacitor to GND
 19 ---| NC/FLASH         [NC] | <--- Explicit No-Connect
 20 ---| NC/FLASH         [NC] | <--- Explicit No-Connect
 21 ---| NC/FLASH         [NC] | <--- Explicit No-Connect
 22 ---| NC/FLASH         [NC] | <--- Explicit No-Connect
 23 ---| NC/FLASH         [NC] | <--- Explicit No-Connect
 24 ---| NC/FLASH         [NC] | <--- Explicit No-Connect
       +-----------------------+
```

### 3.1 Verification of Boot Modes Post-Correction
1. **Normal SPI Boot:**
   - At power-on reset, resistor $R_2$ ($10\text{ k}\Omega$ 0402) pulls `/BOOT9` to `/3V3` ($\text{Logic } 1$).
   - The chip boots from internal SPI flash immediately.
2. **Firmware Flashing / Download Boot:**
   - User holds `SW2` while powering on or resetting the pen, pulling `/BOOT9` to `/GND` ($\text{Logic } 0$).
   - Pin 14 (`GPIO8`) is floating externally; its internal weak pull-up pulls the pin to $\text{Logic } 1$.
   - Strapping condition met: $\text{GPIO9} = 0, \text{GPIO8} = 1 \implies$ **ROM Download Boot**.
   - Standard firmware flashing via USB Serial/JTAG or UART is guaranteed to function reliably.

---

## 4. Complete MCU Pinout Verification Matrix

| Pin | Symbol Name | Rev G Net Name | External Termination | Subsystem Connected |
| :--- | :--- | :--- | :--- | :--- |
| **1** | LNA_IN | `/RF_LNA` | $\pi$-matching network ($C_7, L_1, L_2$) | 2.4 GHz Ceramic Chip Antenna |
| **2** | VDD3P3_1 | `/3V3_RF` | $10\,\mu\text{F} + 0.1\,\mu\text{F}$ bypass | Internal RF Analog Supply |
| **3** | VDD3P3_2 | `/3V3_RF` | $10\,\mu\text{F} + 0.1\,\mu\text{F}$ bypass | Internal RF Analog Supply |
| **4** | XTAL_32K_P / GPIO0 | `/I2C_SDA` | $2.2\text{ k}\Omega$ pull-up ($R_{10}$) | MPU-6050 Tip Sensor I2C Bus |
| **5** | XTAL_32K_N / GPIO1 | `/I2C_SCL` | $2.2\text{ k}\Omega$ pull-up ($R_{11}$) | MPU-6050 Tip Sensor I2C Bus |
| **6** | GPIO2 / STRAP | `/STRAP2` | $10\text{ k}\Omega$ pull-up ($R_3$) to 3V3 | Strapping Pin (Must be HIGH at boot) |
| **7** | CHIP_EN | `/MCU_EN` | $10\text{ k}\Omega$ pull-up ($R_1$) + $1\,\mu\text{F}$ ($C_8$) | RC Reset Timing ($10\text{ ms}$) |
| **8** | GPIO3 | `/TOUCH_OUT`| Direct connection to Touch Board | Capacitive Nib Grip Sensor |
| **9** | MTMS / GPIO4 | `/SD_MOSI` | SPI Master-Out Slave-In | MicroSD Card Carrier |
| **10**| MTDI / GPIO5 | `/SD_MISO` | SPI Master-In Slave-Out | MicroSD Card Carrier |
| **11**| VDD3P3_RTC | `/3V3_RTC` | $0.1\,\mu\text{F}$ bypass ($C_9$) | RTC / Low-Power Domain |
| **12**| MTCK / GPIO6 | `/SD_SCK` | SPI Clock | MicroSD Card Carrier |
| **13**| MTDO / GPIO7 | `/SD_CS` | $10\text{ k}\Omega$ pull-up ($R_4$) | MicroSD Chip Select |
| **14**| GPIO8 / STRAP | `unconnected` | **Explicit No-Connect (Internal Pull-Up)**| Boot Mode Strapping (Must be HIGH) |
| **15**| GPIO9 / BOOT | `/BOOT9` | $10\text{ k}\Omega$ pull-up ($R_2$) + Switch SW2 | Boot Strapping & Flash Button |
| **16**| GPIO10 | `unconnected` | **Explicit No-Connect** | Spare GPIO |
| **17**| VDD3P3_CPU | `/3V3` | $10\,\mu\text{F} + 0.1\,\mu\text{F}$ bypass | Main Digital Core Supply |
| **18**| VDD_SPI | `/VDD_SPI` | $0.1\,\mu\text{F}$ bypass ($C_{13}$) to GND | Internal Flash Power Supply |
| **19**| NC / FLASH | `unconnected` | **Explicit No-Connect** | Embedded Flash Internal Line |
| **20**| NC / FLASH | `unconnected` | **Explicit No-Connect** | Embedded Flash Internal Line |
| **21**| NC / FLASH | `unconnected` | **Explicit No-Connect** | Embedded Flash Internal Line |
| **22**| NC / FLASH | `unconnected` | **Explicit No-Connect** | Embedded Flash Internal Line |
| **23**| NC / FLASH | `unconnected` | **Explicit No-Connect** | Embedded Flash Internal Line |
| **24**| NC / FLASH | `unconnected` | **Explicit No-Connect** | Embedded Flash Internal Line |
| **25**| GPIO18 / USB_DM | `/USB_DM_CORE`| $22\,\Omega$ series ($R_7$) + USBLC6-2SC6 | USB Full-Speed D- |
| **26**| GPIO19 / USB_DP | `/USB_DP_CORE`| $22\,\Omega$ series ($R_8$) + USBLC6-2SC6 | USB Full-Speed D+ |
| **27**| U0RXD / GPIO20 | `/UART_RX` | Test Point / UART Header | Serial Debug Receive |
| **28**| U0TXD / GPIO21 | `/UART_TX` | Test Point / UART Header | Serial Debug Transmit |
| **29**| XTAL_N | `/XTAL_N` | $40\text{ MHz}$ Crystal Pin 1 + $12\text{ pF}$ ($C_{17}$) | Main High-Speed Oscillator |
| **30**| XTAL_P | `/XTAL_P_CORE`| $40\text{ MHz}$ Crystal Pin 3 + $12\text{ pF}$ ($C_{18}$) | Main High-Speed Oscillator |
| **31**| VDDA_1 | `/3V3_RF` | Dedicated analog decoupling | Analog RF Receiver Core |
| **32**| VDDA_2 | `/3V3_RF` | Dedicated analog decoupling | Analog RF Transmitter Core |
| **33**| EPAD / GND | `/GND` | Ground Plane Thermal Via Array | Central Power & Thermal Ground |

---

## 5. Automated Netlist Verification

- **KiCad Netlist Export:** `reports/RevG/Phase02_Corrections/raw/Main_SmartPen_netlist.net` confirms that pins 14, 16, 19, 20, 21, 22, 23, and 24 are listed with unique `unconnected-(U1-...)` net designators and have 0 connections to `/GND`.
- **Pytest Automated Test:** `test_esp32_c3fh4x_pinout_and_boot` in `tests/test_revg_electrical.py` executed and **PASSED**.
- **Negative Fixture:** `test_negative_grounded_internal_flash_fails` and `test_negative_grounded_gpio8_boot_fails` verified test harness sensitivity.
