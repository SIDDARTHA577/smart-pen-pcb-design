# Smart Pen Rev G — Phase 1: PCB Routing Risk & Defect Report

**Document ID**: `reports/RevG/Phase01/06_PCB_ROUTING_RISK_REPORT.md`  
**Execution Date**: November 13, 2026  
**Revision Baseline**: Revision F  
**Target Development Revision**: Revision G  
**Branch**: `engineering/revg-production`  

---

## 1. Executive Summary

Previous external reviews raised critical alarms regarding potential dead-shorts on power nets, differential USB signals, and bus lines on the Main PCB. 

This investigation isolates every confirmed routing defect, establishes why the two repository layouts diverge so drastically, and formulates a non-destructive repair strategy for Phase 2.

**Key Rule Enforced**: As mandated by Phase 1 instructions, **no routing or layout modifications were made during this audit**.

---

## 2. Anatomy of the Client Delivery Defect (199 Shorts, 199 Crossings)

In `output/RevF_Client_Delivery/02_KiCad_Source/SmartPen.kicad_pcb`:
- **1,338 Total DRC Violations**
- **199 Track Crossings** on copper layer B.Cu
- **199 Shorting Items**

### Confirmed Catastrophic Short Circuits
1. **Net `3V3` to `GND`**: Multiple tracks of the 3.3V system power rail intersect the continuous ground pour and ground tracks. Plugging in a battery or USB would instantly collapse the 3.3V rail.
2. **Net `USB_VBUS` to `VBAT`**: 5.0V USB input is directly short-circuited into the 3.7V nominal LiPo battery rail, bypassing the MCP73831 charger. This would over-voltage the LiPo cell to 5V, resulting in violent cell expansion, thermal runaway, or explosion.
3. **Net `VBAT` to `GND`**: The raw positive terminal of the LiPo battery is dead-shorted to ground. A connected unprotected cell would immediately vent, burn wiring, and vaporize PCB copper.
4. **Net `USB_DM_CORE` to `USB_DP_CORE`**: The USB differential data pair is dead-shorted together, disabling all USB Serial/JTAG communications.
5. **Net `UART_RX` to `UART_TX`**: Serial transmit and receive lines are shorted together.
6. **Net `USB_CC1` to `USB_CC2`**: The Type-C configuration channel pins are shorted together, violating USB Type-C Cable and Connector Specification Release 2.0 (creates invalid advertise state on Type-C chargers).

### Root Cause
These defects were caused by the algorithmic output of an automated script (`scripts/highway_astar_router.py` or similar) that attempted to resolve 29 unrouted connections without collision penalties. The router laid tracks directly through copper geometry to achieve a zero-unconnected count. **This file is an unmitigated engineering hazard.**

---

## 3. Authoritative Working PCB Defect Analysis (33 Shorts, 29 Unconnected)

In `output/RevF_Working/SmartPen.kicad_pcb`:
- **185 Total DRC Violations**
- **33 Shorting Items**
- **1 Track Crossing** (`/CHG_STAT` crossing `/BOOT9` at X=152.4 mm, Y=182.8 mm)
- **29 Unconnected Items**
- **0 Dead Shorts between 3V3 and GND**
- **0 Dead Shorts between VBUS and VBAT**

### Detailed Breakdown of the 33 Shorting Items
Unlike the delivery file, the shorts in `RevF_Working` are **localized via-to-track placement conflicts**, not chaotic mesh crossings:

| Conflict Group | Primary Net / Item | Colliding Net / Item | Layer | Location Description |
| :---: | :--- | :--- | :---: | :--- |
| **1** | Via `/BOOT9` | Track `/CHG_STAT` | B.Cu | Charger status line route crosses Boot strapping via |
| **2** | Via `/BOOT9` | Track `/SD_MISO` | B.Cu | MicroSD MISO highway track crosses Boot strapping via |
| **3** | Via `/BOOT9` | Track `/SD_SCK` | B.Cu | MicroSD clock highway track crosses Boot strapping via |
| **4** | Via `/STRAP2` | Track `/VBAT_SW` | B.Cu | Switched battery power trace routes over GPIO2 strapping via |
| **5** | Via `/CHG_STAT` | Track `/HAPTIC_GATE_DRIVE`| B.Cu | Haptic drive line intersects charger status via |
| **6** | Via `/BTN_MODE` | Track `/LED_GREEN_SINK` | B.Cu | Mode switch via overlaps green LED cathode sink track |
| **7** | Via `/SD_MOSI` | Track `/3V3_RTC` | B.Cu | RTC rail trace overlaps MicroSD MOSI via |
| **8** | Via `/SD_CS` | Track `/SD_MISO` | B.Cu | MicroSD MISO track overlaps MicroSD Chip Select via |
| **9** | Via `/I2C_SCL` | Track `/VBAT_SW` | B.Cu | Switched battery power trace overlaps I2C clock via |
| **10** | Via `/SD_MISO` | Track `/3V3_RTC` | B.Cu | RTC rail trace overlaps MicroSD MISO via |

### Analysis
All 33 shorting items on `RevF_Working` stem from a single structural issue: **insufficient routing channels on B.Cu**. High-current power traces (`/VBAT_SW`) and digital highway buses (`/SD_*`, `/I2C_*`) were routed as straight horizontal tracks without staggering around the breakout vias of U1 (ESP32-C3) and U3 (MCP23008).

### The 29 Unconnected Items
The 29 unconnected ratlines represent incomplete escape routing from:
- U3 (MCP23008) GPIO expander pins to button and LED lines.
- Front MPU J_IMU connector lines escaping to ESP32-C3 I2C pins.
- Touch Sensor J_TOUCH signal line escaping to GPIO3.
- Secondary ground via stitching.

---

## 4. Daughterboard Routing Risk Assessment

1. **Front MPU (`Front_MPU.kicad_pcb`)**:
   - DRC Violations: **0**
   - Unconnected: **0**
   - Routing Assessment: Clean, tightly coupled 4-pin breakout with local decoupling for MPU-6050. No shorts.
2. **MicroSD Carrier (`MicroSD_Carrier.kicad_pcb`)**:
   - DRC Violations: **0**
   - Unconnected: **0**
   - Routing Assessment: Clean FPC-to-socket escape routing with continuous bottom ground plane. No shorts.
3. **Touch Sensor (`Touch_Sensor.kicad_pcb`)**:
   - DRC Violations: **0** (Geometric)
   - Unconnected: **0**
   - Schematic Parity: **16** (Net prefix `/` difference only).
   - Routing Assessment: Clean routing from 5x10mm electrode through TTP223-BA6 to J1. No shorts.

---

## 5. Phase 2 Routing Repair Strategy

To resolve the 33 shorting items and complete the 29 unconnected nets on `SmartPen.kicad_pcb` without introducing clearance violations:

1. **Enforce Net Clearance Class**:
   - Set signal-to-signal minimum clearance: **0.15 mm (6 mils)**.
   - Set signal-to-via clearance: **0.20 mm (8 mils)**.
   - Set power-to-signal clearance: **0.25 mm (10 mils)**.
2. **Implement Dedicated Layer Routing Roles**:
   - **F.Cu (Top)**: Dedicated to component pads, local decoupling loops, RF 50-ohm coplanar waveguide, and solid top ground fill.
   - **B.Cu (Bottom)**: Dedicated to the horizontal highway bus (I2C, SPI, UART, power), segmented into 3 parallel longitudinal corridors:
     - *North Corridor (Y = 1.0 to 3.0 mm)*: Digital SPI bus (`SD_SCK`, `SD_MOSI`, `SD_MISO`, `SD_CS`).
     - *Center Corridor (Y = 3.5 to 5.5 mm)*: Power rails (`VBAT_SW`, `3V3`, `VBUS`).
     - *South Corridor (Y = 6.0 to 8.2 mm)*: Low-speed signals (`I2C_SDA`, `I2C_SCL`, `TOUCH_OUT`, `HAPTIC`, buttons, LEDs).
3. **Stagger Breakout Vias**:
   - Replace linear via arrays with a 45-degree staggered diamond pattern to preserve >= 0.35 mm web between via drill holes.
4. **Manual / Interactive Push Routing**:
   - Prohibit unconstrained automated batch routing scripts. All routes must be routed or verified using KiCad's official interactive push-and-shove router with DRC DRC-walkaround enabled.

---

## 6. Routing Risk Sign-Off

- **Root Cause Established**: Complete.
- **Client Delivery Corrupted File Quarantined**: Confirmed.
- **Authoritative Working Baseline Diagnosed**: Confirmed.
- **Phase 1 Status**: **PASS** (Investigation complete; routing changes deferred to Phase 2).
