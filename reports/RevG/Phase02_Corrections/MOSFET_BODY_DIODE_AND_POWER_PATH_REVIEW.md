# SMART PEN REVISION G — POWER-PATH CIRCUIT & MOSFET BODY-DIODE CORRECTION REPORT
## Physical Device Physics, Load-Sharing Architecture, and Conduction State Analysis

- **Project:** Smart Pen Hardware System
- **Document ID:** `REVG-DOC-POWER-PATH-002`
- **Revision:** Rev G Phase 2.1
- **Component Under Review:** Diodes Inc. `DMG2305UX` SOT-23 P-Channel MOSFET (`Q2`)
- **Author:** Senior Power Electronics & Battery Safety Engineer

---

## 1. Defect Analysis of the Rejected Phase 2 Configuration

In the Phase 2 schematic freeze candidate (`commit 3e2905e`), component `Q2` was incorporated into the load-sharing power path with the following pin assignments:
- Pin 1 (Gate) $\rightarrow$ `/USB_VBUS` (pulled down by $R_{26} = 100\text{ k}\Omega$ to `/GND`)
- Pin 2 (Source) $\rightarrow$ `/VBAT`
- Pin 3 (Drain) $\rightarrow$ `/VSYS_RAW`

### 1.1 Physical Device Physics of Enhancement P-Channel MOSFETs
In an enhancement-mode discrete P-channel MOSFET (such as the Diodes Inc. `DMG2305UX` in standard SOT-23 packaging):
1. **Terminals:**
   - **Pin 1:** Gate ($G$)
   - **Pin 2:** Source ($S$)
   - **Pin 3:** Drain ($D$)
2. **Substrate / Body Connection:**
   The P-channel MOSFET is fabricated on an N-type silicon substrate (or N-well). The Source and Drain regions are heavily doped $P^+$ regions. To prevent the source-to-substrate junction from ever forward-biasing in standard operation, the internal N-substrate is internally shorted to the **Source** terminal.
3. **Intrinsic Body Diode Orientation:**
   Because the N-substrate is shorted to the Source ($S$), a parasitic P-N junction exists between the $P^+$ Drain region and the N-type substrate. Consequently:
   $$\text{Body Diode Anode} = \text{Drain } (D, \text{ Pin 3})$$
   $$\text{Body Diode Cathode} = \text{Source } (S, \text{ Pin 2})$$
   Therefore, the intrinsic body diode conducts **strictly from Drain to Source**!

```
                  +--- Drain (Pin 3, P+ Anode)
                  |
                 ---
                 \ /   Intrinsic Body Diode
                 ---
                  |
                  +--- Source (Pin 2, N-Cathode & Substrate)
```

### 1.2 The Catastrophic Failure Mechanism in Phase 2
When `Q2` had Source connected to `/VBAT` and Drain connected to `/VSYS_RAW`:
- With USB power connected ($V_{BUS} = +5.0\text{ V}$), Schottky diode `D4` (`1N5819HW-7-F`, $V_F \approx 0.35\text{ V}$) supplies the internal system rail:
  $$V_{SYS\_RAW} = V_{BUS} - V_{F(D4)} = 5.00\text{ V} - 0.35\text{ V} = 4.65\text{ V}$$
- Drain (Pin 3) was at $V_{SYS\_RAW} = 4.65\text{ V}$.
- Source (Pin 2) was at $V_{BAT} \le 4.20\text{ V}$.
- **Resulting Body Diode Voltage:**
  $$V_{diode} = V_{Drain} - V_{Source} = 4.65\text{ V} - 4.20\text{ V} = +0.45\text{ V} > 0$$
- **Hazard:** The intrinsic body diode **FORWARD-BIASED**! Uncontrolled current rushed from `/USB_VBUS` through Schottky `D4` and through the forward-biased body diode of `Q2` directly into `/VBAT`, completely bypassing the MCP73831 battery charger.
- The battery was subject to unmanaged, constant-voltage float charging at $\sim 4.4\text{ V}$ with zero CC/CV termination, zero thermal cutoff, and zero current limiting—a severe safety violation capable of causing lithium plating, swelling, and thermal runaway.

---

## 2. Corrected Revision G Phase 2.1 Load-Sharing Architecture

To eliminate this hazard, `Q2` Source and Drain terminals have been swapped to implement the standard, authoritative P-channel load-sharing architecture (Microchip AN1149 standard):

```
                                      D4 (1N5819HW)
                       +-----------------|>|-----------------+
                       |                                     |
                       |         Q2 (DMG2305UX P-MOSFET)     |
                       |               Source (Pin 2)        |
                       |                  |                  |
                       |                 ---                 |
                       |                 / \  (Body Diode)   |
                       |                 ---                 |
                       |                  |                  |
                       |               Drain (Pin 3)         |
                       |                  |                  |
/USB_VBUS -------------+                  |                  +---- /VSYS_RAW ----[ SW3 ]----> /VBAT_SW
   |                   |                  |
  [R26: 100k]          |                  |
   |                   |                  |
  GND                  +---> Gate (Pin 1) |
                                          |
/VBAT (from Battery J_BAT & MCP73831) ----+
```

### 2.1 Corrected Pin Mapping Table

| Component | Pin Number | Pin Name | Corrected Rev G Net | Connected Element | Functional Role |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`Q2`** | Pin 1 | Gate ($G$) | `/USB_VBUS` | USB VBUS + $R_{26}$ | Turn-off control when USB present |
| **`Q2`** | Pin 2 | Source ($S$) | `/VSYS_RAW` | Load Rail & `D4` Cathode | System power distribution node |
| **`Q2`** | Pin 3 | Drain ($D$) | `/VBAT` | Battery & `U2` Pin 3 (VBAT) | Battery supply entry |
| **`D4`** | Pin 1 | Cathode ($K$) | `/VSYS_RAW` | `Q2` Source & `SW3` Pin 1 | Prevents reverse battery feed to USB |
| **`D4`** | Pin 2 | Anode ($A$) | `/USB_VBUS` | USB VBUS Receptacle | USB bus power forward path |
| **`R26`** | Pin 1 / 2 | Resistor | `/USB_VBUS` $\rightarrow$ `/GND` | Gate Pull-Down | Pulls Gate to 0V when USB unplugged |
| **`SW3`** | Pin 1 / 2 | SPDT Switch | `/VSYS_RAW` $\rightarrow$ `/VBAT_SW`| Power Switch | Connects system rail to LDO & pen logic |

---

## 3. Mathematical Verification of Conduction States

### 3.1 State 1: USB Powered Mode ($V_{BUS} = 5.0\text{ V}$, Battery Present $V_{BAT} \in [3.0\text{ V}, 4.2\text{ V}]$)
1. **System Rail Voltage:**
   Current flows from `/USB_VBUS` through Schottky `D4` ($V_F \approx 0.35\text{ V}$ at typical system load of $50\text{ mA}$):
   $$V_{SYS\_RAW} = V_{BUS} - V_{F(D4)} = 5.00\text{ V} - 0.35\text{ V} = 4.65\text{ V}$$
2. **MOSFET Channel State:**
   - Gate Voltage: $V_G = V_{BUS} = 5.00\text{ V}$
   - Source Voltage: $V_S = V_{SYS\_RAW} = 4.65\text{ V}$
   - Gate-to-Source Voltage:
     $$V_{GS} = V_G - V_S = 5.00\text{ V} - 4.65\text{ V} = +0.35\text{ V}$$
   - Because $V_{GS} > 0\text{ V}$ (and far above the threshold $V_{GS(th)} \in [-0.4\text{ V}, -0.9\text{ V}]$), the P-channel inversion layer cannot form.
   - **MOSFET Channel is Hard OFF.**
3. **MOSFET Body Diode State:**
   - Diode Anode is at Drain (`/VBAT`): $V_{Anode} \le 4.20\text{ V}$
   - Diode Cathode is at Source (`/VSYS_RAW`): $V_{Cathode} = 4.65\text{ V}$
   - Diode Bias Voltage:
     $$V_{bias} = V_{Anode} - V_{Cathode} = 4.20\text{ V} - 4.65\text{ V} = -0.45\text{ V}$$
   - Because $V_{bias} < 0\text{ V}$, the body diode is **STRONGLY REVERSE-BIASED**!
4. **Current Paths:**
   - Current from USB to Battery through `Q2`: **$0.00\,\mu\text{A}$ (Blocked by reverse-biased body diode & OFF channel).**
   - Current from USB to System: Supplies all pen operating current through `D4`.
   - Current into Battery: Sourced **strictly** through MCP73831 `U2` Pin 3 under constant-current / constant-voltage regulation ($100\text{ mA}$ max).

### 3.2 State 2: Battery Powered Mode ($V_{BUS} = 0.0\text{ V}$, Battery Present $V_{BAT} \in [3.0\text{ V}, 4.2\text{ V}]$)
1. **Initial Sub-Microsecond Transient:**
   - Gate is discharged to $0.0\text{ V}$ through $R_{26}$ ($100\text{ k}\Omega$).
   - Battery voltage ($V_{BAT}$) forward-biases the body diode (Anode = Drain = $V_{BAT}$, Cathode = Source = $V_{SYS\_RAW}$).
   - The body diode conducts momentarily, pulling $V_{SYS\_RAW}$ up to:
     $$V_{SYS\_RAW(initial)} = V_{BAT} - V_{diode} \approx 3.70\text{ V} - 0.60\text{ V} = 3.10\text{ V}$$
2. **MOSFET Channel Conduction:**
   - Gate-to-Source Voltage immediately becomes:
     $$V_{GS} = V_G - V_S = 0.0\text{ V} - 3.10\text{ V} = -3.10\text{ V}$$
   - Since $V_{GS} = -3.10\text{ V} \ll V_{GS(th)} (-0.9\text{ V})$, the P-channel MOSFET turns **hard ON**.
   - With channel fully enhanced, $R_{DS(on)} \le 60\text{ m}\Omega$ (DMG2305UX specification at $V_{GS} = -2.5\text{ V}$).
   - The conductive channel shorts Drain directly to Source, collapsing the voltage drop across the transistor:
     $$V_{drop} = I_{load} \times R_{DS(on)} = 80\text{ mA} \times 0.060\,\Omega = 4.8\text{ mV}$$
   - The body diode is completely bypassed, and $V_{SYS\_RAW} \approx V_{BAT} - 4.8\text{ mV} \approx V_{BAT}$.
3. **Schottky Diode `D4` State:**
   - Anode is at `/USB_VBUS` ($0.0\text{ V}$).
   - Cathode is at `/VSYS_RAW` ($\approx 3.7\text{ V}$).
   - Reverse voltage across `D4`: $V_R = 3.7\text{ V}$.
   - Leakage current into unpowered USB port: $I_R \le 1.0\,\mu\text{A}$ (negligible).

---

## 4. Power Switch (`SW3`) Interaction & Operational Modes

Power switch `SW3` is inserted between `/VSYS_RAW` (Pin 1) and `/VBAT_SW` (Pin 2).

```
   /VSYS_RAW (Output of Load-Share) ----[ SW3: Power Switch ]----> /VBAT_SW (Input to LDO U4 & Logic)
```

| Operational Scenario | USB State | Battery State | SW3 Position | System Logic (`VBAT_SW`) | Battery State / Current |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Desk Tethered / In-Use** | Plugged (5V) | Charged (4.2V) | **ON** | Powered by USB ($4.65\text{ V}$) | Idle (Float / Standby, 0 mA) |
| **Desk Tethered / Charging**| Plugged (5V) | Depleted (3.6V)| **ON** | Powered by USB ($4.65\text{ V}$) | Charging via MCP73831 ($100\text{ mA}$) |
| **Off-State Charging** | Plugged (5V) | Depleted (3.6V)| **OFF** | **OFF (0V, completely dark)**| Charging via MCP73831 ($100\text{ mA}$) |
| **Normal Wireless Writing** | Unplugged (0V)| Normal (3.7V) | **ON** | Powered by LiPo ($3.7\text{ V}$) | Discharging ($30 - 80\text{ mA}$) |
| **Storage / Transport** | Unplugged (0V)| Any | **OFF** | **OFF (0V)** | Zero discharge ($< 1\,\mu\text{A}$ PCM leak) |

### 4.1 Off-State Charging Guarantee
A critical user-experience requirement is that the pen must recharge when connected to USB even if the physical power switch is in the OFF position.
- In the corrected Rev G schematic, charger input `/USB_VBUS` (Pin 4 of `U2`) and battery terminal `/VBAT` (Pin 3 of `U2`) connect directly to the battery node regardless of `SW3` position.
- When `SW3` is open, `/VBAT_SW` is disconnected from `/VSYS_RAW`. The LDO `U4`, ESP32-C3, and peripherals remain completely unpowered, while the MCP73831 charges the cell safely.

---

## 5. Hot-Plug, Unplug Transients & Untested Boundary Conditions

### 5.1 USB Disconnection Transient Analysis
When USB is unplugged during active writing ($I_{load} \approx 60\text{ mA}$):
1. `/USB_VBUS` falls toward $0\text{ V}$ with time constant $\tau = R_{26} \times C_{VBUS} = 100\text{ k}\Omega \times 14.7\,\mu\text{F} \approx 1.47\text{ s}$ if unloaded, but falls in $< 50\,\mu\text{s}$ due to charger and host discharge.
2. As `/VSYS_RAW` drops below $V_{BAT}$, `Q2` body diode begins conducting within nanoseconds.
3. Decoupling capacitors $C_{16}$ ($10\,\mu\text{F}$) and $C_{14}$ ($10\,\mu\text{F}$) hold `/VBAT_SW` and `/3V3` stable during the $< 100\,\mu\text{s}$ gate turn-on transition.
4. LDO `AP2112K` operates with dropout voltage $V_{DO} \le 250\text{ mV}$ at $300\text{ mA}$, providing continuous $3.3\text{ V}$ regulation as long as $V_{BAT} \ge 3.55\text{ V}$.

### 5.2 Verification Limitations & Formal Status
In accordance with master engineering guidelines:
- **Simulation Status:** Circuit SPICE switching transients and instantaneous glitch depth during hot-unplug have been calculated analytically; physical oscilloscope capture is pending hardware bench prototype.
- **Documentation Obligation:** All dynamic voltage transient switching durations ($t_{switch}$) and hot-plug ESD ringing waveforms are classified as **NOT VERIFIED ON PHYSICAL HARDWARE**. Bench validation on Rev G prototype is a mandatory Phase 3 gate prerequisite.
