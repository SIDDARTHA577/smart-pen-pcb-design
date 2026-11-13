# Critical Circuits and Electrical Risk Review — Smart Pen Rev E
**Author**: Senior Embedded Hardware & Validation Lead  
**Client**: RadixView Technologies  
**Date**: November 2, 2026  

---

## 1. ESP32-C3 Core, Clock and RF Circuitry
- **Microcontroller**: ESP32-C3FH4X with 4MB in-package flash. Pin 18 (`VDD_SPI`) is decoupled with 1.0 uF (`C5`) and strictly isolated from the 3.3V power rail.
- **Clock**: 40.000 MHz +/- 10 ppm crystal (`FA-20H`), loaded by two 15 pF precision C0G capacitors (`C6`, `C7`) and 24 nH clock harmonic filter inductor (`L1`).
- **RF Matching**: Pin 1 (`LNA_IN`) feeds a pi-matching network (`L2` 2.4 nH, `C8` 1.5 pF, `C9` 1.5 pF) connecting to Hirose `U.FL-R-SMT-1(10)` receptacle.
- **Strapping & Reset**: `CHIP_EN` has 10k pullup (`R1`) and 1 uF delay (`C1`) with reset switch `SW1`. `GPIO9` has 10k pullup (`R2`) with boot switch `SW2`. `GPIO2` has 10k pullup (`R3`).

---

## 2. USB-C Charging and Wired Data Transfer
- **Receptacle**: 16-Pin USB Type-C (`TYPE-C-31-M-12`).
- **Configuration Channel**: Two 5.1k 1% resistors (`R5`, `R6`) pull CC1 and CC2 to GND, configuring the pen as a standard UFP (device) compliant with USB Type-C Specification 2.0.
- **Data Protection**: STMicroelectronics `USBLC6-2SC6` dual TVS array protects `D+` and `D-` lines with <0.6 pF parasitic capacitance. Series 22 ohm damping resistors (`R7`, `R8`) match high-speed USB 2.0 impedance.
- **MCU Connection**: Connected directly to ESP32-C3 native USB Serial/JTAG on `GPIO18` (D-) and `GPIO19` (D+).

---

## 3. Power Architecture, Battery and Regulation
- **LDO Regulator**: Diodes Inc. `AP2112K-3.3TRG1` in SOT-23-5:
  * 600 mA continuous / 800 mA peak rating.
  * Ultra-low dropout: 250 mV at 600 mA.
  * Operates stably down to battery voltage $V_{BAT} \approx 3.45\text{ V}$. Below 3.45V, output tracks battery voltage ($V_{BAT} - V_{drop}$), remaining well within the ESP32-C3 minimum operating voltage limit ($3.0\text{ V}$).
- **LiPo Charger**: Microchip `MCP73831T-2ACI/OT` in SOT-23-5:
  * Regulates battery voltage to 4.20V.
  * Charge current programmed to 500 mA via $R_{prog} = 2.0\text{ k}\Omega$ (`R9`).
  * *Charge Current vs. Cell Life Note*: For standard 300 mAh pouch cells ($1.0\text{ C}$ rating), $R_{prog}$ should be adjusted to $3.3\text{ k}\Omega$ (300 mA) during pilot production to avoid cell stress in the sealed enclosure.
- **Power-Path Behavior**:
  * The `MCP73831` does not contain autonomous power-path management.
  * When charging while operating, system current is drawn in parallel with the battery charging current.
  * *Future Recommendation*: Add a P-MOSFET / Schottky power-path circuit for high-volume consumer release.
- **Battery Protection**: Relies on cell-integrated Protection Circuit Module (PCM: DW01A + FS8205A) preventing over-charge, over-discharge (<2.8V), and short-circuit.

---

## 4. Peripheral Interfaces & Sensor Routing
- **Front Tip IMU**: Detachable 4-Pin keyed JST SH 1.0mm connector (`J_IMU`): 3.3V, GND, SDA (`GPIO0`), SCL (`GPIO1`) with 4.7k bus pullups (`R10`, `R11`) and 0.1 uF filter (`C15`).
- **WRITE Touch**: Detachable 3-Pin keyed JST SH 1.0mm connector (`J_TOUCH`): 3.3V, GND, `TOUCH_OUT` (`GPIO3`) with 100k pull-down (`R19`).
- **MicroSD Storage**: 6-Pin 0.5mm pitch FPC carrier connector (`J_SD`): 3.3V, GND, SCK (`GPIO6`), MOSI (`GPIO4`), MISO (`GPIO5`), CS (`GPIO7`) with 10k pullup (`R18`).
- **Haptic Driver**: `AO3400A` N-MOSFET (`Q1`) driven by expander `U3.14` via 100R gate resistor (`R16`) and 100k pull-down (`R17`), protected by `1N5819HW` Schottky flyback diode (`D3`).

