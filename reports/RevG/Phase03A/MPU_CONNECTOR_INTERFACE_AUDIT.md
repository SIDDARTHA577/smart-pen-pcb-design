# MPU CONNECTOR INTERFACE AUDIT
**Smart Pen Revision G — Phase 3A Engineering Report**
**Document ID:** `REPORT-REVG-P3A-005`
**Date:** November 2026
**Status:** PASS (Authoritative 4-Pin Parity Confirmed)
**Schematic Hash (`Front_MPU.kicad_sch`):** `a33fedfbbcd188579f0e2b3f1e1e031dccaf3cd19d2044326b22d41b14e7f561`
**Main Schematic Hash (`SmartPen.kicad_sch`):** `2148ff5efedee932d01114aec5a76e173838e81738b88dc6209a170294bfeefc`

---

## 1. Executive Summary

This audit definitively resolves the interface discrepancy between historical engineering reports and the committed KiCad source files regarding the detachable Front MPU daughterboard connector. Certain preliminary reports asserted that the MPU interface required 5 pins to accommodate a dedicated hardware motion interrupt line (`MPU_INT`).

An exhaustive review of the Rev G Main PCB schematic (`SmartPen.kicad_sch`), Main PCB layout (`SmartPen.kicad_pcb`), Front MPU daughterboard schematic (`Front_MPU.kicad_sch`), and the client firmware architecture specifications proves that the connector is **strictly 4 pins** (`3V3`, `GND`, `SDA`, `SCL`). No hardware interrupt is required, implemented, or supported by the available ESP32-C3 pin budget.

---

## 2. Source Netlist & Schematic Audit

### 2.1 Main Board J_IMU Connector
Inspection of `output/RevG/SmartPen.kicad_sch` and `Main_SmartPen_netlist.net` confirms:
- **Component Reference:** `J_IMU`
- **Footprint:** `Connector_PinHeader_1.27mm:PinHeader_1x04_P1.27mm_Vertical`
- **Location on PCB:** $X = 2.500\text{ mm}, Y = 4.600\text{ mm}$ (Front pen tip interface)
- **Pin Mapping:**
  - Pin 1: Net 2 (`/3V3`)
  - Pin 2: Net 1 (`/GND`)
  - Pin 3: Net 39 (`/I2C_SDA`) — connects to ESP32-C3 GPIO4 (Pin 8)
  - Pin 4: Net 40 (`/I2C_SCL`) — connects to ESP32-C3 GPIO5 (Pin 9)
- **Netlist Output:**
  ```lisp
  (node (ref "J_IMU") (pin "1") (pinfunction "Pin_1") (pintype "passive") (net "2"))
  (node (ref "J_IMU") (pin "2") (pinfunction "Pin_2") (pintype "passive") (net "1"))
  (node (ref "J_IMU") (pin "3") (pinfunction "Pin_3") (pintype "passive") (net "39"))
  (node (ref "J_IMU") (pin "4") (pinfunction "Pin_4") (pintype "passive") (net "40"))
  ```

### 2.2 Front MPU Daughterboard J1 Connector
Inspection of `output/RevG/Front_MPU/Front_MPU.kicad_sch` and `Front_MPU_netlist.net` confirms:
- **Component Reference:** `J1`
- **Footprint:** `Connector_PinHeader_1.27mm:PinHeader_1x04_P1.27mm_Vertical`
- **Pin Mapping:**
  - Pin 1: `3V3`
  - Pin 2: `GND`
  - Pin 3: `SDA`
  - Pin 4: `SCL`
- **IMU Sensor Configuration:**
  - Sensor IC: `U1` (`ICM-42670-P` 6-axis IMU, LGA-14).
  - Pin 12 (`INT1`): Flagged with a native KiCad no-connect marker (`no_connect` symbol at coordinate $X=102.87, Y=88.90$).
  - Exported netlist entry: `unconnected-(U1-INT-Pad12)`.
  - Pin 4 (`INT2`): Unconnected.

---

## 3. Firmware Architecture & Pin Allocation Verification

### 3.1 Polling vs. Interrupt Architecture
The client handoff specification (Section 1.22: *Motion Tracking and Handwriting Recognition Engine*) explicitly specifies:
> *"The ICM-42670-P motion tracking sensor is sampled continuously via a timer-driven I2C polling task running at 100 Hz to 200 Hz in FreeRTOS. Handwriting trajectory reconstruction utilizes regular time-slice integration of angular velocity and linear acceleration. Hardware interrupts on motion thresholds are not used during active writing sessions."*

Because data acquisition occurs on fixed periodic intervals (every 5 ms or 10 ms), a discrete hardware interrupt line is architecturally superfluous.

### 3.2 ESP32-C3 Pin Allocation Constraint
The ESP32-C3FH4X is packaged in a compact QFN-32 envelope with only 22 GPIOs, of which several are multiplexed or restricted:
- **GPIO0, GPIO1:** Boot Strapping / Touch Sensor Pulse
- **GPIO2:** Haptic Motor PWM driver
- **GPIO3:** ADC1_CH3 (Battery Voltage Sensing via R10/R11 divider)
- **GPIO4, GPIO5:** I2C SDA / SCL (Dedicated bus)
- **GPIO6, GPIO7, GPIO10:** MicroSD Card Interface (SPI / 1-bit SD mode)
- **GPIO8:** Boot Strapping (Pulled HIGH via R27)
- **GPIO9:** Boot Mode / Mode Button (SW2)
- **GPIO18, GPIO19:** USB D− / USB D+ (Native USB Serial/JTAG)
- **GPIO20, GPIO21:** UART RX / UART TX (Debug Console)

**Conclusion:** The ESP32-C3 has **zero available unallocated GPIOs**. Introducing a 5th pin for `MPU_INT` would necessitate stripping hardware functionality from the MicroSD card, Touch sensor, or Battery monitor.

---

## 4. Mechanical & Keyed Connector Integration

1. **Detachable Keyed Header:** The physical interface utilizes a 1.27 mm pitch keyed friction-lock connector (Molex PicoBlade or JST-SUR compatible 4-pin receptacle).
2. **Keying Requirement:** The client specification mandates a keyed profile to prevent reverse insertion ($180^\circ$ inversion), which would short $3\text{V}3$ to $SCL$ and $GND$ to $SDA$.
3. **Pen Tip Modular Assembly:** The 4-pin interface allows the entire front writing cone and MPU module to detach during refill replacement or pen cone maintenance without exposing raw flying leads.

---

## 5. Audit Conclusion & Gate Determination

| Audit Item | Documented Claim | Verified Source Reality | Gate |
| :--- | :--- | :--- | :---: |
| **Main PCB J_IMU Pin Count** | 4 or 5 Pins | **4 Pins** (3V3, GND, SDA, SCL) | **PASS** |
| **Front MPU J1 Pin Count** | 4 or 5 Pins | **4 Pins** (3V3, GND, SDA, SCL) | **PASS** |
| **ICM-42670-P INT Pin** | Driven to Host | **NC** (KiCad no_connect verified) | **PASS** |
| **Firmware Requirement** | Interrupt Driven | **100–200 Hz I2C Polling** | **PASS** |
| **ESP32-C3 GPIO Availability**| Free GPIO for INT | **0 Free GPIOs** | **PASS** |

**OVERALL MPU CONNECTOR AUDIT GATE: PASS (4-Pin Validated)**
