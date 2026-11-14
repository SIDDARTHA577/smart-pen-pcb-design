# PHASE 3B ROUTING ACTION PLAN
**Smart Pen Revision G — Phase 3A Engineering Deliverable**
**Document ID:** `REPORT-REVG-P3A-009`
**Date:** November 2026
**Status:** READY FOR PHASE 3B EXECUTION (Phase 3B Not Started)
**Target PCB:** `output/RevG/SmartPen.kicad_pcb`

---

## 1. Executive Summary & Phase Boundary

This engineering document defines the execution strategy, routing priority hierarchy, physical net rules, and design closure methodology for **Phase 3B: Detailed PCB Routing Closure**.

> [!IMPORTANT]
> **PHASE BOUNDARY ENFORCEMENT:**
> In strict accordance with the client mandate, Phase 3A is restricted to footprint verification, schematic-to-PCB synchronization, and component placement engineering. **Phase 3B routing has NOT been started.** No traces have been routed, no legacy nets have been deleted, and no fabrication Gerbers have been generated.

---

## 2. Preflight Net Priority Hierarchy

To guarantee signal integrity, RF performance, and low-noise power delivery across the 84.00 × 9.20 mm board, routing execution in Phase 3B will follow a strict five-tier priority matrix:

| Priority Tier | Net Classification | Target Nets | Trace Width / Geometry | Design Constraints |
| :---: | :--- | :--- | :--- | :--- |
| **Tier 1** | **RF & Antenna Feed** | Net from U1 Pin 2 to L1/C7/AE1 | Coplanar waveguide (50 Ω target) | Keepout envelope: 3.5 mm void on all layers. No digital crossings. |
| **Tier 2** | **Power Distribution** | `/3V3`, `/VSYS_RAW`, `/VBAT`, `/VBAT_SW`, `/USB_VBUS` | 0.35–0.50 mm (14–20 mil) | Star topology from U4 Pin 5. Minimize loop inductance to C13/C14/C15. |
| **Tier 3** | **USB Differential Pair** | `/USB_DP_CORE`, `/USB_DM_CORE`, `/USB_DP_PORT`, `/USB_DM_PORT` | 0.20 mm width / 0.20 mm gap ($90\ \Omega \pm 10\%$) | In-line flow through U_ESD. Intra-pair length match $\le 0.50\text{ mm}$. |
| **Tier 4** | **High-Speed Digital** | `/SD_CLK`, `/SD_CMD`, `/SD_DAT0`, `/I2C_SDA`, `/I2C_SCL` | 0.20 mm (8 mil) | Route away from RF section. Pullups R24/R25 near J_IMU. |
| **Tier 5** | **Low-Speed GPIO & Sensing** | `/GPIO8_STRAP`, `/VBAT_SENSE`, `/TOUCH_PULSE`, Buttons, LEDs | 0.15–0.20 mm (6–8 mil) | Filter capacitor on VBAT_SENSE near ADC pin. Solid pullup on GPIO8. |

---

## 3. Power Bus Width & Current Capacity Guidelines

Trace width calculations adhere to IPC-2152 standards for 1 oz copper ($35\ \mu\text{m}$) with a maximum allowable temperature rise $\Delta T \le 10^\circ\text{C}$:

$$\text{Width} = \frac{I}{k \times (\Delta T)^b \times t^c}$$

| Net Name | Maximum Current | Minimum Required Width | Target Routed Width | Copper Layer |
| :--- | :--- | :--- | :--- | :--- |
| **`/USB_VBUS`** | 500 mA (USB 2.0 In) | 0.25 mm (10 mil) | **0.40 mm (16 mil)** | `F.Cu` / `B.Cu` |
| **`/VSYS_RAW`** | 500 mA (Switch Input) | 0.25 mm (10 mil) | **0.40 mm (16 mil)** | `F.Cu` |
| **`/VBAT`** | 200 mA (Pouch Cell) | 0.12 mm (5 mil) | **0.30 mm (12 mil)** | `F.Cu` / `B.Cu` |
| **`/VBAT_SW`** | 400 mA (LDO Input) | 0.20 mm (8 mil) | **0.35 mm (14 mil)** | `F.Cu` |
| **`/3V3`** | 600 mA (LDO Peak Out) | 0.30 mm (12 mil) | **0.50 mm (20 mil)** | `F.Cu` / `B.Cu` (or Plane) |
| **Signal Nets** | $< 10\text{ mA}$ | 0.127 mm (5 mil) | **0.20 mm (8 mil)** | `F.Cu` / `B.Cu` |

---

## 4. USB Differential Pair & ESD Routing Strategy

```
  [J_USB Receptacle]
    Pins A6, B6 (DP) -------------\
    Pins A7, B7 (DM) --------\     \
                              v     v
                            [U_ESD Clamping Array] (USBLC6-2SC6)
                              |     |
                              v     v
    Pins 26, 25 (ESP32-C3) <-=== Differential Pair (90 Ohm)
```

1. **In-Line ESD Clamping:** USB lines must pass directly through the pads of `U_ESD` before continuing into the PCB interior. No T-junction stubs are permitted between the connector and ESD clamp.
2. **Length Matching:** Physical routing software will enforce $\Delta L \le 0.50\text{ mm}$ between `/USB_DP_PORT` and `/USB_DM_PORT`.
3. **Reference Plane Continuity:** Traces will route over an unbroken ground plane to prevent impedance discontinuities.

---

## 5. 2-Layer vs. 4-Layer Execution Strategy

### 5.1 Baseline 2-Layer Attempt
Phase 3B will initially attempt full 0-DRC routing on the committed 2-layer stackup:
- `F.Cu`: Signal routes, power buses, and component pads.
- `B.Cu`: Continuous ground plane flood with short orthogonal signal jumpers.
- **Stop Condition:** If achieving 100% routing completion requires slotting or fragmenting $> 25\%$ of the bottom ground copper directly beneath U1 or the RF section, 2-layer routing will be paused.

### 5.2 Transition to 4-Layer (ECR-003)
If 2-layer ground fragmentation threatens RF or EMC compliance:
- Transition stackup to JLC2313 4-layer:
  - Layer 1 (`F.Cu`): Signals + RF Coplanar Feed.
  - Layer 2 (`In1.Cu`): Continuous solid Ground Plane.
  - Layer 3 (`In2.Cu`): Power Plane split (`3V3`, `VSYS_RAW`, `VBAT`).
  - Layer 4 (`B.Cu`): Low-speed signal jumpers + bottom Ground Flood.
- This transition eliminates 100% of power bottlenecks and guarantees 0-DRC compliance.

---

## 6. Detailed Step-by-Step Phase 3B Execution Plan

1. **Step 1: Clean Legacy Unrouted Stubs:** Safely purge obsolete unrouted trace segments and redundant vias that conflict with newly placed footprints.
2. **Step 2: RF Subsystem Routing:** Route 50 Ω coplanar feed between U1 Pin 2, L1, C7, and AE1 with unbroken bottom ground return.
3. **Step 3: USB Front-End Routing:** Connect J_USB pins to U_ESD, route CC1/CC2 5.1 kΩ pull-downs, and route differential pair to U1 Pins 25/26.
4. **Step 4: Power-Path Routing:** Route U2 charger, Q2 P-MOSFET, D4 Schottky diode, SW3 power switch, and U4 LDO with high-current copper corridors.
5. **Step 5: High-Speed Digital Bus Routing:** Connect J_SD MicroSD lines, U3 DRV2605L haptic lines, and J_IMU I2C lines.
6. **Step 6: GPIO, Sensing & Passive Routing:** Connect R27 boot strapping to U1 Pin 14, SW1 reset, SW2 boot, LEDs, and battery sense divider.
7. **Step 7: Ground Flood & Thermal Stitching:** Perform complete zone fill on `F.Cu` and `B.Cu`. Add thermal vias beneath U1 ground paddle and U4 regulator.
8. **Step 8: Native DRC & Parity Closure:** Execute `kicad-cli pcb drc` with full flags. Verify:
   - **0 Violations**
   - **0 Unconnected Items**
   - **0 Footprint / Parity Errors**

---

## 7. Plan Sign-Off & Verification Gate

| Preflight Readiness Gate | Target Standard | Status |
| :--- | :--- | :---: |
| **Schematic Parity Baseline** | 0 Footprint Errors | **PASS** |
| **Footprint Accuracy** | 100% IPC-7351B Compliance | **PASS** |
| **Netlist Rules Defined** | Widths, Clearances, Priorities | **PASS** |
| **Phase 3B Routing Execution** | Hold until Phase 3A Delivery | **NOT STARTED** |

**OVERALL PHASE 3B READINESS: READY FOR EXECUTION**
