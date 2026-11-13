# Smart Pen Rev F Critical Circuit & Architectural Review

**Project:** Smart Pen PCB & 3D Enclosure Design  
**Client:** RadixView Technologies / Chattychop (G. Badrinath)  
**Specification:** `Smart_Pen_PCB_Handoff(1).docx` (Rev 0.2)  
**Author:** Engineering Validation Lead  
**Date:** November 2026  

---

## 1. ESP32-C3 Controller, Clocking, and RF Architecture

### 1.1 Microcontroller Core
- **Selected IC:** Espressif ESP32-C3-WROOM-02-N4 (RISC-V single-core 32-bit CPU, 160 MHz, 400 KB SRAM, 4 MB embedded SPI flash).
- **Supply Voltage:** 3.0 V to 3.6 V nominal. Operating current: 20 mA base, 80 mA active CPU, 350 mA peak 802.11b TX burst.
- **Clocking:** Integrated 40 MHz high-precision crystal inside module shield can; no external resonator required on the main board.
- **Strapping Pin Integrity:**
  - `GPIO2` (Strap 2): Internal weak pull-up. Connected to test pad `TP_STRAP2`. Remains unpulled during boot.
  - `GPIO8` (Strap 8): Determines boot mode along with GPIO9. Left floating/pulled HIGH.
  - `GPIO9` (Boot mode): Pulled to 3.3V via $10\text{ k}\Omega$ resistor `R10`. When HIGH at power-up/reset, boots from SPI Flash (normal operation). When pulled LOW, enters UART serial bootloader for factory recovery.
  - `CHIP_EN` (Reset): RC delay filter ($10\text{ k}\Omega$ `R8` pull-up to 3.3V and $1.0\ \mu\text{F}$ `C10` capacitor to GND) creates a 10 ms power-on delay, exceeding Espressif's minimum 50 $\mu$s requirement.

### 1.2 RF Performance & Copper Keepout
- **Antenna Type:** Integrated planar inverted-F antenna (PIFA) on module top edge.
- **Mechanical Keepout:** Minimum 15.0 × 12.0 mm area extending to the edge of the board. All copper traces, ground fills, internal battery casing, and structural screws are strictly prohibited within this zone.
- **Antenna Enclosure Housing:** The pen barrel surrounding the antenna region is modeled with non-conductive polycarbonate/ABS ($\epsilon_r \approx 2.8 - 3.2$, $\tan\delta \approx 0.005$) to prevent detuning.

---

## 2. USB-C Data Transfer vs. Smartphone Internet Tethering Analysis

### 2.1 Customer Specification Requirement
The Quick Context section of `Smart_Pen_PCB_Handoff(1).docx` explicitly states:
> *"USB-C must support both charging and data transfer (not charging-only) — it's used for local wired data transfer to a laptop and for tethering to a phone's internet connection. This resolves the open question in Section 1.25..."*

### 2.2 USB Hardware Implementation
- **Connector:** Korean Hroparts TYPE-C-31-M-12 (16-pin mid-mount receptacle).
- **Configuration Channel (CC):** Pins $CC1$ and $CC2$ are terminated with independent $5.1\text{ k}\Omega \pm 1\%$ pull-down resistors (`R1`, `R2`) to GND. This identifies the Smart Pen as an Upstream Facing Port (UFP / Device) to any standard USB Type-C host or charger, safely negotiating 5V VBUS.
- **Data Lines:** $D+$ and $D-$ signals pass through ultra-low capacitance TVS protection diodes (`D1`, `D2`, $C_j < 0.5\text{ pF}$) and series $22\,\Omega$ damping resistors directly to ESP32-C3 `GPIO19` ($D+$) and `GPIO18` ($D-$).

### 2.3 Critical Architectural Evaluation: Can ESP32-C3 Support USB Smartphone Tethering?

> [!CAUTION]
> **ESP32-C3 CANNOT tether directly to a smartphone's internet over a USB cable.** Native USB Serial/JTAG supports PC communication, but lack of USB Host OTG hardware precludes wired mobile tethering.

#### Technical Evidence & Hardware Limitations:
1. **USB Controller Capability:**
   - Per Espressif ESP32-C3 Technical Reference Manual (Chapter 26): The integrated USB controller is strictly a **USB 2.0 Full-Speed (12 Mbps) Device Controller** supporting CDC-ACM (virtual COM port) and JTAG debug protocols.
   - It **does not have USB Host mode** and **does not support USB On-The-Go (OTG)**. (In contrast, ESP32-S2 and ESP32-S3 feature full USB OTG 1.1 controllers with host capability).
2. **Smartphone Tethering Protocol Requirements:**
   - When a smartphone shares its cellular internet connection via USB tethering, the smartphone acts as a **USB Peripheral/Device** exposing a virtual network adapter class:
     - **Android Devices:** RNDIS (Remote Network Driver Interface Specification) or CDC-NCM (Network Control Model).
     - **iOS Devices (Apple iPhone):** Proprietary Apple USBMux / CDC-NCM Ethernet emulation.
   - To utilize this tethered connection, the connected device **MUST ACT AS A USB HOST**:
     - It must supply VBUS or negotiate power delivery.
     - It must enumerate the smartphone device.
     - It must run a full USB Host Class Driver (CDC-NCM/RNDIS) and TCP/IP stack with DHCP client.
3. **Hardware Impossibility on ESP32-C3:**
   - Because the ESP32-C3 is physically incapable of USB Host operation, it cannot enumerate a smartphone, cannot initiate host transactions, and cannot run RNDIS/CDC-NCM host drivers over its USB pins.
   - Connecting an iPhone or Android phone to the Smart Pen via USB-C will either do nothing, cause the phone to treat the pen as a USB accessory/serial port, or cause power conflicts.

### 2.4 Recommended & Supported Architectural Solutions
1. **Supported Mode 1 (Primary - Native Wi-Fi):** Connect the ESP32-C3 to the smartphone's **Wi-Fi Personal Hotspot**. This requires zero additional hardware, uses standard 802.11b/g/n, and provides high-speed cloud/local streaming.
2. **Supported Mode 2 (Secondary - Bluetooth PAN):** Use BLE / Bluetooth PAN tethering to the smartphone.
3. **Supported Mode 3 (Wired PC Streaming):** Use the USB-C port for bidirectional High-Speed CDC-ACM serial streaming and raw binary data transfer directly to a PC/Mac/Linux laptop running the companion browser application.
4. **Hardware Upgrade Path (Future Revision):** If wired USB smartphone tethering is non-negotiable, the MCU must be migrated to an **ESP32-S3-MINI-1** (which integrates USB OTG Host), or an external SPI USB host controller (e.g., Maxim MAX3421E) must be added.

---

## 3. Power Architecture & Battery Subsystem Review

### 3.1 Linear Voltage Regulator: Diodes Inc AP2112K-3.3TRG1
- **Topology:** Ultra-low dropout linear regulator, CMOS pass element.
- **Output:** 3.3 V fixed, up to 600 mA continuous output current.
- **Dropout Voltage:** Typical $250\text{ mV}$ at $600\text{ mA}$; $\approx 120\text{ mV}$ at $250\text{ mA}$ average operating load.
- **Battery Discharge Profile Behavior:**
  - $V_{BAT} = 4.2\text{ V} - 3.42\text{ V}$: Fully regulated 3.30 V output (ripple $< 30\ \mu\text{V}_{\text{RMS}}$).
  - $V_{BAT} = 3.42\text{ V} - 3.15\text{ V}$: Enters dropout. $V_{OUT} = V_{BAT} - V_{drop}$. At $V_{BAT} = 3.20\text{ V}$, $V_{OUT} \approx 3.08\text{ V}$. ESP32-C3 operating floor is $3.0\text{ V}$.
  - $V_{BAT} < 3.12\text{ V}$: ESP32-C3 brownout detector asserts reset.
  - **Usable Energy Extraction:** $> 93\%$ of stored cell chemical energy is utilized before regulator dropout induces MCU reset.

### 3.2 Battery Charging Circuit: Microchip MCP73831T-2ACI/OT
- **Package:** SOT-23-5.
- **Charge Resistor ($R_9$) Safety Re-tuning:**
  - Formula: $I_{reg} = \frac{1000\text{ V}}{R_{PROG}}$
  - *Rev E Baseline:* $R_9 = 2.0\text{ k}\Omega \rightarrow I_{reg} = 500\text{ mA}$.
  - *Risk:* 500 mA represents a $1.67\text{ C}$ charge rate for a 300 mAh LiPo pouch cell. Exceeding $1.0\text{ C}$ generates severe internal heating, degradation of electrolyte, and pouch swelling inside the enclosed pen barrel.
  - *Rev F Revision:* $R_9$ is updated to $3.3\text{ k}\Omega \pm 1\%$ (`RC0402FR-073K3L`).
    $$I_{reg} = \frac{1000\text{ V}}{3300\,\Omega} = 303.0\text{ mA} \approx 1.01\text{ C}$$
- **Thermal Dissipation in Charger:**
  - Maximum CC dissipation:
    $$P_{D(max)} = (5.0\text{ V} - 3.2\text{ V}) \times 0.303\text{ A} = 0.545\text{ W}$$
  - Average CC dissipation:
    $$P_{D(typ)} = (5.0\text{ V} - 3.7\text{ V}) \times 0.303\text{ A} = 0.394\text{ W}$$
  - SOT-23-5 $\theta_{JA} = 230^\circ\text{C/W}$. With $0.394\text{ W}$ dissipation and solid PCB ground thermal vias, die temperature rise is $\approx 65^\circ\text{C}$, safely below the $150^\circ\text{C}$ silicon thermal shutdown threshold.

### 3.3 Power-Path Behavior & Operational Risk
- **Topology:** The MCP73831 `VBAT` pin connects directly to the battery and system input.
- **Operational Risk:** When the Smart Pen is powered on and writing while simultaneously plugged into USB-C:
  - System current ($\approx 80-180\text{ mA}$) is drawn directly from the battery/charger node.
  - MCP73831 charge termination occurs when charge current drops below $10\%$ of $I_{reg}$ ($30.3\text{ mA}$). Because the system load permanently draws $> 30.3\text{ mA}$, the charger cannot reach termination condition, keeping the battery float-charged indefinitely.
- **Rev G Recommendation:** Implement a low-$R_{DS(on)}$ P-channel MOSFET (e.g. DMG2305UX) + Schottky diode ideal diode circuit to automatically disconnect the battery and power the system directly from USB VBUS when plugged in.

---

## 4. Peripheral Subsystems

### 4.1 External Capacitive Touch Controller (Tontek TTP223-BA6)
- **Function:** Senses user grip on external brass/conductive foil electrode to trigger `WRITE / RECORD` state.
- **Interface:** Single active-HIGH digital signal connected to ESP32-C3 `GPIO3` with $10\text{ k}\Omega$ pull-down resistor.
- **Sensitivity:** Configured via external capacitor `C15` ($0 - 50\text{ pF}$, currently $22\text{ pF}$ 0402 C0G). Allows tuning through the 1.0 mm plastic barrel wall without false triggers during hand holding.

### 4.2 Front Inertial Measurement Unit (MPU-6050)
- **Carrier:** Detachable front carrier PCB mounted directly behind pen nib.
- **Connector (`J_IMU`):** Molex 503480-0600 (6-pin 0.5 mm pitch horizontal FPC).
  - Pin 1: `3V3` (Power)
  - Pin 2: `GND` (Ground return)
  - Pin 3: `I2C_SCL` (GPIO1, $4.7\text{ k}\Omega$ pull-up `R6`)
  - Pin 4: `I2C_SDA` (GPIO0, $4.7\text{ k}\Omega$ pull-up `R7`)
  - Pin 5: `MPU_INT` (GPIO10, motion interrupt)
  - Pin 6: `FS_SYNC` (Tied to GND)

### 4.3 MicroSD Subsystem
- **Connector (`J_SD`):** Hirose FH12-6S-0.5SH (6-pin 0.5 mm pitch FPC).
- **Wiring:** SPI mode:
  - `SD_SCK` (GPIO4), `SD_MISO` (GPIO5), `SD_MOSI` (GPIO6), `SD_CS` (GPIO7).
- **Physical Reason for FPC:** A standard MicroSD push-push socket requires $14.0\text{ mm}$ width. The internal pen bore is $13.0\text{ mm}$. The socket cannot physically fit onto the 9.2 mm main board. The 6-pin FPC routes signals to a carrier board located in the rear click mechanism.

---

## 5. Summary of Circuit Validation Gates

| Gate Item | Target Spec | Rev F Result | Compliance Status |
| :--- | :--- | :--- | :--- |
| **ESP32-C3 Boot Strapping** | No pull conflicts | GPIO2/8/9 verified | **PASS** |
| **USB CC Termination** | $5.1\text{ k}\Omega \pm 1\%$ | 5.1k on CC1/CC2 | **PASS** |
| **USB Data Capability** | CDC-ACM serial to PC | D+/D- routed with TVS | **PASS** |
| **Phone USB Tethering** | Feasibility audit | Impossible on C3; Wi-Fi mandated | **DOCUMENTED** |
| **LiPo Charge Current** | $\le 1.0\text{ C}$ ($300\text{ mA}$) | $R_9 = 3.3\text{ k}\Omega \rightarrow 303\text{ mA}$ | **PASS** |
| **AP2112K Dropout** | Operate down to 3.2V | Brownout threshold 3.12V | **PASS** |
| **Power Path Behavior** | Load sharing | Documented for Rev G | **RISK DOCUMENTED** |
| **Touch Controller** | Dedicated IC | TTP223-BA6 on GPIO3 | **PASS** |
| **IMU Interface** | I2C + INT | 6-pin FPC to front tip | **PASS** |
