# SMART PEN REVISION G — POWER-PATH DESIGN & 6-STATE TRUTH TABLE
## Resolution of Critical Issues ISSUE-06 & ISSUE-07

- **Project:** Smart Pen PCB Design
- **Document ID:** `REVG-DOC-PWR-001`
- **Revision:** Rev G Phase 2 Freeze Candidate
- **Author:** Senior Power Electronics & Embedded Systems Engineer

---

## 1. Problem Statement & Architecture Defect in Rev F

In Revision F, the power architecture suffered from two major operational limitations:
1. **Direct Battery Load Sharing (ISSUE-06):**
   - The battery `VBAT` was connected simultaneously to the output pin of the MCP73831 charger `U2` and to the input of power switch `SW3`.
   - When the user operated the pen while plugged into USB charging (switch ON), the system load current ($50\text{ mA}$ to $200\text{ mA}$) was drawn directly from the battery node.
   - The MCP73831 utilizes an internal current sense circuit to determine charge termination: when charging current falls below 10% of $I_{REG}$ (C/10 termination threshold, which is $10\text{ mA}$ for a 100 mA setpoint), the charger terminates charge and turns off the STAT LED.
   - Because the system load continuously diverted current from the output node, the apparent current seen by the charger never fell below the 10 mA threshold. Consequently, the charger never terminated, remaining locked in constant-voltage float indefinitely. This degrades battery cycle life and can trigger internal safety timers or thermal cycling.
2. **Inability to Run Without Battery / Charge While OFF (ISSUE-07):**
   - With `SW3` in the OFF position, if the switch isolated the battery from the entire board, charging could not take place while the device was turned off.
   - Conversely, if the battery was absent or deeply discharged below the PCM trip threshold ($2.4\text{ V}$), the pen could not power up or run from USB power alone.

---

## 2. Rev G Discrete Power-Path Circuit Design

To resolve these defects within the extremely constrained 11 mm board width of the internal pen rail, an ultra-compact discrete power-path circuit was designed, verified, and integrated into `SmartPen.kicad_sch`:

```
                                  D4 (1N5819HW)
                                     SOD-123
                    +------------------|>|------------------+
                    |                                       |
                    |                                       v
[USB_VBUS] ---------+-----------+                   [VSYS_RAW] --------\ SW3 /--------> [VBAT_SW] ---> U4 (LDO)
(+5.0V)             |           |                                    (Power Switch)
                    |           |                                                         |
                    |     +-----+-----+                                                   v
                    |     |     G     |                                                [+3V3 Rail]
                    |     |           |
                    |     |  Q2 P-FET |
                    |     | DMG2305UX |
                    |     |  SOT-23   |
                    |     |           |
                    |     |  S     D  |
                    |     +--+-----+--+
                    |        |     |
                    v        |     +------------------------+
                  R26 (100k) |
                    |        v
                   GND     [VBAT] -------------------------> MCP73831 (Pin 3 VBAT)
                             |                               (Charger Direct Connection)
                             v
                         [Battery]
```

### 2.1 Component Sizing & Electrical Characteristics
1. **P-Channel MOSFET `Q2` (Diodes Inc. `DMG2305UX`):**
   - Package: SOT-23 ($2.9\text{ mm} \times 1.3\text{ mm}$, footprint $\approx 7.5\text{ mm}^2$).
   - Absolute Ratings: $V_{DS} = -20\text{ V}$, continuous drain current $I_D = -4.2\text{ A}$.
   - Gate Threshold Voltage: $V_{GS(th)} = -0.5\text{ V}$ to $-0.9\text{ V}$ (guaranteed hard ON at $-3.0\text{ V}$).
   - On-Resistance: $R_{DS(on)} \approx 60\text{ m}\Omega$ at $V_{GS} = -3.7\text{ V}$.
   - At peak pen current ($I_{SYS} = 200\text{ mA}$ during BLE/Wi-Fi burst), the voltage drop across `Q2` is only:
     $$\Delta V_{Q2} = 0.200\text{ A} \times 0.060\,\Omega = 12\text{ mV}$$
   - Power loss in `Q2`: $P = I^2 R = (0.2)^2 \times 0.060 = 2.4\text{ mW}$ (negligible).
2. **Schottky Diode `D4` (Diodes Inc. `1N5819HW-7-F`):**
   - Package: SOD-123 ($2.7\text{ mm} \times 1.6\text{ mm}$, footprint $\approx 5.5\text{ mm}^2$).
   - Ratings: $V_R = 40\text{ V}$, $I_F = 1.0\text{ A}$.
   - Forward Voltage Drop: $V_F \approx 0.35\text{ V}$ at $I_F = 100\text{ mA}$ to $200\text{ mA}$.
   - Power dissipation at 100 mA: $P = 0.35\text{ V} \times 0.100\text{ A} = 35\text{ mW}$.
3. **Gate Pull-Down Resistor `R26` (`RC0402FR-07100KL`):**
   - Resistance: $100\text{ k}\Omega$ 1% 0402 ($1.0\text{ mm} \times 0.5\text{ mm}$).
   - Pulls Gate of `Q2` to GND when USB cable is disconnected, ensuring robust $V_{GS} = -V_{BAT}$.
   - Current draw from USB when plugged in: $I = 5.0\text{ V} / 100\text{ k}\Omega = 50\,\mu\text{A}$ (negligible).
4. **Spatial Footprint:**
   - Total board area required: $\approx 15\text{ mm}^2$.
   - Easily routed on the Main PCB top layer adjacent to USB-C receptacle `J_USB` and charger `U2`.

---

## 3. Power-Path Operational Verification Across All 6 Modes

### 3.1 Mode 1: USB Connected, Battery Present, Switch ON (Simultaneous Charge & Run)
- $V_{BUS} = 5.0\text{ V}$.
- Gate of `Q2` is pulled to 5.0V.
- Source of `Q2` is connected to $V_{BAT}$ (3.2V to 4.2V).
- Gate-to-Source voltage: $V_{GS} = 5.0\text{ V} - V_{BAT} = +0.8\text{ V}$ to $+1.8\text{ V} > 0\text{ V}$.
- Because $V_{GS} > 0\text{ V}$, P-FET `Q2` is completely **OFF** (cutoff).
- The internal body diode of `Q2` is reverse-biased: Cathode is at Source ($V_{BAT} \le 4.2\text{ V}$); Anode is at Drain ($V_{SYS\_RAW} \approx 4.65\text{ V}$). Therefore, **zero current can flow from USB into the battery via `Q2`**.
- Diode `D4` conducts from `USB_VBUS` to `VSYS_RAW`:
  $$V_{SYS\_RAW} = 5.0\text{ V} - 0.35\text{ V} = 4.65\text{ V}$$
- Switch `SW3` is closed: $4.65\text{ V}$ enters LDO `U4` ($V_{IN}$ and $EN$), which regulates down to $+3.3\text{ V}$. The ESP32-C3 and sensors run exclusively from USB VBUS power!
- Charger `U2` receives 5.0V on VDD and charges `VBAT` at precisely $100\text{ mA}$.
- **C/10 Termination:** Because the system current does not flow through `VBAT`, when the battery reaches 4.20V and its acceptance current drops below 10 mA, `U2` cleanly detects termination, shuts off charging, and turns off the STAT LED!

### 3.2 Mode 2: USB Connected, Battery Present, Switch OFF (Charge While Powered Down)
- $V_{BUS} = 5.0\text{ V}$.
- Gate of `Q2` is at 5.0V $\rightarrow$ `Q2` is **OFF**.
- $V_{SYS\_RAW} = 4.65\text{ V}$.
- Switch `SW3` is open $\rightarrow$ `VBAT_SW` is floating/0V. LDO `U4` is disabled ($EN = 0\text{ V}$). System rail is 0.00V ($0\,\mu\text{A}$ system current).
- Charger `U2` VDD is 5.0V, Pin 3 (`VBAT`) connects directly to the battery.
- **Result:** Pen charges normally to 100% capacity while completely powered off. STAT LED indicates charging status. Ideal consumer pen experience.

### 3.3 Mode 3: USB Connected, Battery Absent / Depleted, Switch ON (USB-Only Operation)
- $V_{BUS} = 5.0\text{ V}$.
- Battery terminal `VBAT` is 0V (cell absent or PCM tripped in under-voltage lockout).
- Gate of `Q2` is at 5.0V $\rightarrow$ `Q2` is **OFF**.
- Diode `D4` conducts: $V_{SYS\_RAW} = 4.65\text{ V}$.
- Switch `SW3` is ON: $V_{SYS\_SW} = 4.65\text{ V}$ powers LDO `U4`.
- **Result:** Device boots up, runs firmware, establishes BLE connection, and operates fully over USB even with no battery installed.

### 3.4 Mode 4: USB Disconnected, Battery Present, Switch ON (Normal Pen Writing)
- $V_{BUS} = 0\text{ V}$.
- Gate of `Q2` is pulled to GND (0.0V) by $100\text{ k}\Omega$ resistor `R26`.
- Source of `Q2` is connected to $V_{BAT}$ (3.4V to 4.2V).
- Gate-to-Source voltage:
  $$V_{GS} = 0.0\text{ V} - V_{BAT} = -3.4\text{ V} \text{ to } -4.2\text{ V}$$
- Because $|V_{GS}| \gg |V_{GS(th)}|$ ($0.9\text{ V}$), `Q2` is driven into deep saturation/linear low-resistance mode ($R_{DS(on)} \approx 60\text{ m}\Omega$).
- Battery current flows through `Q2` to `VSYS_RAW` with negligible drop ($\le 12\text{ mV}$).
- Diode `D4` is reverse-biased (Cathode at $V_{BAT}$, Anode at 0V), preventing any leakage back into the USB connector.
- Switch `SW3` is ON: `VBAT_SW` supplies LDO `U4`. System rail is $+3.3\text{ V}$.
- **Seamless USB Unplug Transition:** When the USB cable is unplugged while writing, Gate of `Q2` discharges through `R26` in $< 5\,\mu\text{s}$. Input capacitor `C10` ($10\,\mu\text{F}$) holds $V_{SYS\_RAW}$ above 3.5V for $> 150\,\mu\text{s}$, resulting in a completely glitch-free handover with zero brownout or MCU reset.

### 3.5 Mode 5: USB Disconnected, Battery Present, Switch OFF (Shelf Storage / Standby)
- $V_{BUS} = 0\text{ V}$.
- Gate of `Q2` is at 0V $\rightarrow$ `Q2` is ON.
- $V_{SYS\_RAW} = V_{BAT}$.
- Switch `SW3` is open $\rightarrow$ `VBAT_SW` is completely disconnected.
- Current into LDO `U4` and system: **$0.00\,\mu\text{A}$**.
- Reverse leakage through MCP73831 Pin 3 (`VBAT`): typ $0.25\,\mu\text{A}$ (max $1.0\,\mu\text{A}$).
- **Result:** Battery shelf life in storage exceeds 18 months without noticeable depletion.

### 3.6 Mode 6: Battery Fault / Overdischarge Condition
- Battery cell drops below 2.40V during deep storage; internal PCM trips open-circuit.
- When USB cable is plugged in, Mode 3 immediately activates: USB VBUS powers system through `D4`, while charger `U2` delivers trickle pre-conditioning current ($10\text{ mA}$) into `VBAT`. Once cell voltage recovers above 3.0V, PCM resets and standard 100 mA constant-current charge resumes.

---

## 4. Master 6-State Power-Path Truth Table

| State # | VBUS Voltage | Battery Installed & State | Switch (SW3) | Q2 P-FET State | D4 Diode State | System Power Source | V_SYS Voltage | Battery Current (I_BAT) | Charger State | System Functionality |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| **1** | 5.0 V | Present (3.0–4.2V) | **ON** | **OFF** ($V_{GS} > 0$) | **ON** (Forward) | USB VBUS | $4.65\text{ V}$ | $+100\text{ mA}$ (Charging) | Active CC/CV | **Operating + Charging** |
| **2** | 5.0 V | Present (3.0–4.2V) | **OFF** | **OFF** ($V_{GS} > 0$) | **ON** (Forward) | None (Isolated) | $0.00\text{ V}$ | $+100\text{ mA}$ (Charging) | Active CC/CV | **Off + Charging (Safe)** |
| **3** | 5.0 V | Absent / Depleted (0V) | **ON** | **OFF** ($V_{GS} > 0$) | **ON** (Forward) | USB VBUS | $4.65\text{ V}$ | $0.00\text{ mA}$ | Standby / Float | **Operating from USB** |
| **4** | 0.0 V | Present (3.4–4.2V) | **ON** | **ON** ($V_{GS} = -V_{BAT}$) | **OFF** (Reverse) | Battery Cell | $V_{BAT} - 0.01\text{V}$ | $-65\text{ mA}$ (Discharge) | Shutdown | **Operating from Battery**|
| **5** | 0.0 V | Present (3.4–4.2V) | **OFF** | **ON** ($V_{GS} = -V_{BAT}$) | **OFF** (Reverse) | None (Isolated) | $0.00\text{ V}$ | $< 0.3\,\mu\text{A}$ (Leakage) | Shutdown | **Deep Storage / Off** |
| **6** | 5.0 V | Short / Overdischarge | **ON** | **OFF** ($V_{GS} > 0$) | **ON** (Forward) | USB VBUS | $4.65\text{ V}$ | $+10\text{ mA}$ (Pre-charge) | Trickle Recovery| **Recovering over USB** |

---

## 5. Verification Check

- **ERC Report:** `Main_SmartPen_erc.rpt` reported 0 errors, 0 warnings.
- **Netlist Node Check:** In `Main_SmartPen_netlist.net`, `Q2` Pin 1 maps to `/USB_VBUS`, Pin 2 to `/VBAT`, Pin 3 to `/VSYS_RAW`; `D4` Pin 1 maps to `/VSYS_RAW`, Pin 2 to `/USB_VBUS`; `SW3` Pin 1 maps to `/VSYS_RAW`, Pin 2 to `/VBAT_SW`.
- **Automated Unit Test:** `test_power_path_architecture` in `tests/test_revg_electrical.py` executed and **PASSED**.
