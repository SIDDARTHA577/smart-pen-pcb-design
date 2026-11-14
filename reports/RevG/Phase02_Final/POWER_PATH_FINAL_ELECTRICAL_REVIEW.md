# POWER PATH ARCHITECTURE, LOAD-SHARING & BATTERY SAFETY REVIEW

**Document ID:** RPT-REVG-P02-FINAL-PWR-PATH  
**Author:** Senior Power Electronics & Battery Safety Engineer  
**Components:** DMG2305UX (Q2), MCP73831T-2ACI/OT (U2), B5819W (D1), AP2112K-3.3TRG1 (U3)  
**Status:** **ANALYTICALLY VERIFIED / SCHEMATIC-CONFIRMED**  
**Hardware Dynamic Verification Status:** **NOT VERIFIED ON PHYSICAL OSCILLOSCOPE (BENCH TEST REQUIRED)**  

---

## 1. Electrical Architecture Overview

The Smart Pen Revision G power distribution system manages seamless power sourcing from either an external USB-C port ($5.0\text{ V}$) or an internal single-cell Lithium-Polymer battery ($3.0 - 4.2\text{ V}$ nominal), stepping down to a clean, regulated $+3.3\text{ V}$ system rail via a high-PSRR low-dropout regulator (`U3`, AP2112K-3.3).

```
   USB_VBUS (5V) ───────┬────────► [U2 MCP73831 Charger] ───► VBAT (3.7V Pouch Cell)
                        │                                          │
                        │ (D1 Schottky)                            │ (Drain Q2)
                        ▼                                          ▼
                   [B5819W Diode] ──► VSYS_RAW ◄── [Q2 DMG2305UX P-MOSFET]
                                         │             (Source Q2)
                                         ▼
                                  [SW3 Power Switch]
                                         │
                                         ▼
                                       VSYS
                                         │
                                         ▼
                             [U3 AP2112K-3.3 LDO]
                                         │
                                         ▼
                                    +3V3 System
```

---

## 2. Load-Sharing P-MOSFET (Q2) Pin Mapping & Body-Diode Orientation

The P-channel MOSFET `Q2` (Diodes Inc. `DMG2305UX`, SOT-23, $V_{DS} = -20\text{ V}$, $I_D = -4.2\text{ A}$, $R_{DS(on)} = 40\text{ m}\Omega$) is configured as an active power-path selector.

### 2.1 Physical Pin Assignment
- **Pin 1 (Gate):** Connected to net `/USB_VBUS` with a $100\text{ k}\Omega$ pull-down resistor (`R20`) to `GND`.
- **Pin 2 (Source):** Connected to net `/VSYS_RAW` (system rail before power switch).
- **Pin 3 (Drain):** Connected to net `/VBAT` (positive battery terminal).

### 2.2 Intrinsic Body-Diode Orientation
In a discrete P-channel enhancement-mode MOSFET:
- The internal P-N body junction exists between the P-doped Drain and the N-doped substrate (internally bonded to Source).
- **Body Diode Anode:** Pin 3 (Drain / `VBAT`).
- **Body Diode Cathode:** Pin 2 (Source / `VSYS_RAW`).
- **Diode Forward Conduction Direction:** From **Drain (`VBAT`) to Source (`VSYS_RAW`)**.
- **Diode Blocking Direction:** Blocks current from **Source (`VSYS_RAW`) to Drain (`VBAT`)**.

---

## 3. Operating State Machine Analysis

### State 1: USB Connected ($V_{BUS} = 5.0\text{ V}$), Battery Present ($V_{BAT} = 3.0\text{ V} - 4.2\text{ V}$), Switch ON
1. **Gate Voltage:** $V_G = V_{BUS} = 5.0\text{ V}$.
2. **System Rail Voltage:** Current flows from `USB_VBUS` through Schottky diode `D1` (B5819W, $V_f \approx 0.35\text{ V}$ at $150\text{ mA}$):
   $$V_{SYS\_RAW} = V_{BUS} - V_f(D1) = 5.0\text{ V} - 0.35\text{ V} = 4.65\text{ V}$$
3. **Source Voltage:** $V_S = V_{SYS\_RAW} = 4.65\text{ V}$.
4. **Gate-to-Source Voltage ($V_{GS}$):**
   $$V_{GS} = V_G - V_S = 5.0\text{ V} - 4.65\text{ V} = +0.35\text{ V}$$
   Since $V_{GS} > 0\text{ V}$ (and threshold voltage $V_{th}$ is negative, between $-0.5\text{ V}$ and $-0.9\text{ V}$), **the P-MOSFET channel is completely pinched off (OFF)**.
5. **Body-Diode Bias Condition:**
   $$V_{diode} = V_{Anode} - V_{Cathode} = V_{BAT} - V_{SYS\_RAW} = 4.20\text{ V} - 4.65\text{ V} = -0.45\text{ V}$$
   Even at maximum battery state-of-charge ($4.20\text{ V}$), the body diode is **REVERSE-BIASED by at least $-0.45\text{ V}$**. (When battery is depleted to $3.0\text{ V}$, reverse bias increases to $-1.65\text{ V}$).
6. **Battery Current & Charge Isolation:**
   - Reverse leakage current through DMG2305UX body diode: $< 1.0\,\mu\text{A}$.
   - Current from USB directly into battery via Q2: **$0.00\text{ mA}$**.
   - Battery charging occurs **exclusively** through `U2` (MCP73831T-2ACI/OT) at the programmed constant current:
     $$I_{CHG} = \frac{1000\text{ V}}{R_{PROG}} = \frac{1000\text{ V}}{10\text{ k}\Omega} = 100\text{ mA}$$
   - Because the active system load ($60 - 120\text{ mA}$) is supplied directly from USB through `D1`, no load current passes through the battery sensing node. The charger enters constant voltage (CV) mode and terminates cleanly when charge current tapers below $C/10$ ($10\text{ mA}$).

---

### State 2: USB Disconnected ($V_{BUS} = 0\text{ V}$), Battery Present ($V_{BAT} = 3.0\text{ V} - 4.2\text{ V}$), Switch ON
1. **Gate Voltage:** With USB unplugged, `R20` ($100\text{ k}\Omega$) discharges Gate capacitance to ground: $V_G = 0.0\text{ V}$.
2. **Initial Turn-On:** Before the MOSFET channel opens, the body diode is forward-biased by `VBAT`, establishing an initial Source voltage:
   $$V_S \approx V_{BAT} - 0.60\text{ V} \approx 3.70\text{ V} - 0.60\text{ V} = 3.10\text{ V}$$
3. **Channel Conduction:**
   $$V_{GS} = V_G - V_S = 0.0\text{ V} - 3.10\text{ V} = -3.10\text{ V}$$
   Because $V_{GS} = -3.10\text{ V} \ll V_{th} (-0.9\text{ V})$, the P-MOSFET is driven into full saturation/enhancement.
4. **On-State Voltage Drop:**
   With $R_{DS(on)} = 40\text{ m}\Omega$ and maximum active load current $I_{LOAD} = 150\text{ mA}$:
   $$V_{drop} = I_{LOAD} \times R_{DS(on)} = 0.15\text{ A} \times 0.040\,\Omega = 6.0\text{ mV}$$
   $$V_{SYS\_RAW} = V_{BAT} - 0.006\text{ V} \approx 3.694\text{ V}$$
   The body diode is bypassed by the low-resistance MOSFET channel, eliminating thermal dissipation and maximizing battery run time.
5. **Reverse Blocking through D1:**
   Schottky diode `D1` has Anode at $0.0\text{ V}$ and Cathode at $\approx 3.7\text{ V}$. It is reverse-biased, completely preventing battery power from back-feeding into the USB port or CC pin circuitry.

---

### State 3: Power Switch SW3 OFF
1. `SW3` is an SPST mechanical slide switch placed between `/VSYS_RAW` and `/VSYS`.
2. In the OFF position, `SW3` physically opens the circuit to the input of LDO `U3`.
3. Quiescent draw from the battery in OFF state consists only of:
   - MCP73831 reverse battery leakage: $I_{REV} < 1\,\mu\text{A}$
   - Battery PCM protection circuit standby: $I_{PCM} < 3\,\mu\text{A}$
   - Total shelf-discharge: $< 4\,\mu\text{A}$, enabling $> 3\text{ years}$ shelf life on a $130\text{ mAh}$ cell.

---

## 4. Hot-Unplug Dynamic Behavior & Transients

When USB power is abruptly removed while the system is operating at full load ($150\text{ mA}$ with BLE/Wi-Fi active):
1. $V_{BUS}$ decays towards $0\text{ V}$.
2. Gate capacitance $C_{iss}$ ($700\text{ pF}$) discharges through $R_{20}$ ($100\text{ k}\Omega$), yielding a Gate discharge time constant:
   $$\tau = R_{20} \times C_{iss} = 100\text{ k}\Omega \times 700\text{ pF} = 70\,\mu\text{s}$$
3. During this $70\,\mu\text{s}$ interval, bulk decoupling capacitor `C11` ($10\,\mu\text{F}$) on `VSYS_RAW` supplies the system load.
4. The voltage droop on `VSYS_RAW` during this interval is estimated as:
   $$\Delta V = \frac{I \times \Delta t}{C} = \frac{150\text{ mA} \times 70\,\mu\text{s}}{10\,\mu\text{F}} = 1.05\text{ V}$$
   Since initial voltage is $4.65\text{ V}$, the rail droops to $\approx 3.60\text{ V}$ before the MOSFET channel is fully enhanced, at which point the body diode conducts instantly once the rail falls below $V_{BAT} - 0.6\text{ V} = 3.1\text{ V}$.
5. Low-dropout regulator `U3` requires only $250\text{ mV}$ dropout at $150\text{ mA}$. Provided battery voltage is above $3.55\text{ V}$, the $+3.3\text{ V}$ rail will not brown out.

> [!WARNING]
> **UNVERIFIED ELECTRICAL DYNAMICS:** While the mathematical model predicts that brownout will be avoided, parasitic trace inductances, ESR of `C11`, and momentary peak Wi-Fi transmit currents ($> 280\text{ mA}$) could induce voltage ringing or deeper transients. **Glitch-free, uninterrupted hot-unplug switching has NOT been validated on a physical test bench with an oscilloscope and MUST be verified on Phase 4 prototype boards.**
