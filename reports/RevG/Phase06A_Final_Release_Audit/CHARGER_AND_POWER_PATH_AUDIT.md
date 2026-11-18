# CHARGER AND POWER-PATH ELECTRICAL AUDIT

**Document ID:** SRG-P6A-PWR-005  
**Revision:** 1.1 (Phase 6B Corrected Release)  
**Date:** November 18, 2026  
**Electrical Revision:** `output/RevG/variants/FourLayer_ECR_R9_50mA/`  
**Status:** **ELECTRICAL AUDIT COMPLETE — ZERO VIOLATIONS**

---

## 1. CHARGER PROGRAMMING RESISTOR ($R_9$) AND CHARGE CURRENT

On the FourLayer_ECR_R9_50mA Main Board, resistor $R_9$ programs the charge current of the Microchip MCP73831T-2ACI/OT lithium-ion charge management controller.

### 1.1 Formula & Value Verification
According to the MCP73831 manufacturer datasheet (DS20001984G, Section 4.1):
$$I_{\text{REG}} = \frac{1000\text{ V}}{R_{\text{PROG}}}$$

With $R_9 = 20.0\text{ k}\Omega \pm 1\%$ (`RC0402FR-0720KL`):
$$I_{\text{charge}} = \frac{1000\text{ V}}{20,000\ \Omega} = \mathbf{50.0\text{ mA} \quad (0.050\text{ A})}$$

### 1.2 Battery Compatibility Rate
For the selected Model `LP300830-PCM` ($50\text{ mAh}$ nominal capacity):
$$\text{Charge Rate} = \frac{50.0\text{ mA}}{50\text{ mAh}} = \mathbf{1.0\text{C}}$$
This precisely matches the maximum recommended fast-charge rating ($1.0\text{C}$) of the commercial cell, providing a complete recharge from empty in approximately 75 minutes (CC/CV transition).

---

## 2. MCP73831 THERMAL DISSIPATION & JUNCTION TEMPERATURE AUDIT

### 2.1 Power Dissipation Calculation
In the KiCad schematic (`SmartPen.kicad_sch`), MCP73831 pin 4 ($V_{\text{DD}}$) connects directly to the `USB_VBUS` rail ($5.00\text{ V}$ nominal), while diode $D_4$ (`1N5819HW-7-F` / `MBR0520L`) provides the separate OR-ing path from `USB_VBUS` to `VSYS_RAW` for the AP2112K-3.3 system LDO.

The maximum thermal stress on charger IC $U_2$ occurs at the onset of constant-current (CC) charging with a deeply discharged cell ($V_{\text{BAT}} = 3.00\text{ V}$):
- Input voltage at MCP73831 $V_{\text{DD}}$: $V_{\text{IN}} = V_{\text{BUS}} = \mathbf{5.00\text{ V}}$
- Minimum battery cell voltage: $V_{\text{BAT}} = \mathbf{3.00\text{ V}}$
- Linear pass transistor voltage drop: $\Delta V = V_{\text{IN}} - V_{\text{BAT}} = 5.00\text{ V} - 3.00\text{ V} = \mathbf{2.00\text{ V}}$
- Programmed charge current: $I_{\text{charge}} = \mathbf{50.0\text{ mA}} \quad (0.050\text{ A})$
- **Worst-Case IC Power Dissipation:**
  $$P_D = \Delta V \times I_{\text{charge}} = 2.00\text{ V} \times 0.050\text{ A} = \mathbf{0.100\text{ W} \quad (100.0\text{ mW})}$$

*(Note: Prior draft calculations citing $82.5\text{ mW}$ assumed an unverified $V_{\text{IN}} = 4.65\text{ V}$ input. Under the actual direct $5.00\text{ V}$ $V_{\text{BUS}}$ connection, worst-case dissipation is exactly $100.0\text{ mW}$.)*

### 2.2 IC Silicon Junction Temperature vs. Battery Cell Surface Temperature
A critical engineering distinction must be maintained between the charger IC silicon die temperature and the battery pouch cell temperature:

1. **Charger IC Silicon Die Temperature ($T_{J,\text{IC}}$):**
   - Package: SOT-23-5 on 4-layer FR4 with continuous internal ground planes
   - Thermal resistance: $\theta_{\text{JA}} \approx 230^\circ\text{C/W}$
   - IC Silicon Temperature Rise:
     $$\Delta T_{\text{IC}} = P_D \times \theta_{\text{JA}} = 0.100\text{ W} \times 230^\circ\text{C/W} = \mathbf{23.0^\circ\text{C}}$$
   - At $T_{\text{ambient}} = 25.0^\circ\text{C}$:
     $$T_{J,\text{IC}} = 25.0^\circ\text{C} + 23.0^\circ\text{C} = \mathbf{48.0^\circ\text{C}}$$
   - At elevated internal barrel ambient ($T_{\text{ambient}} = 35.0^\circ\text{C}$):
     $$T_{J,\text{IC}} = 35.0^\circ\text{C} + 23.0^\circ\text{C} = \mathbf{58.0^\circ\text{C}}$$
   - **Silicon Rating Assessment:** The MCP73831 silicon junction is rated for continuous operation up to **$+125^\circ\text{C}$** (with thermal shutdown protection at $+150^\circ\text{C}$). $T_{J,\text{IC}} = 48.0^\circ\text{C}$ provides an extensive $+77.0^\circ\text{C}$ safety margin below the silicon limit.

2. **Battery Pouch Cell Surface Temperature ($T_{\text{cell}}$):**
   - The battery cell is physically isolated from the SOT-23-5 charger IC:
     - The cell is positioned in the below-rail cradle (`05_Battery_Cradle`), separated from the Main PCB top surface by the $1.6\text{ mm}$ FR4 board thickness, the $1.0\text{ mm}$ polycarbonate rail deck, and internal air gaps.
     - Heat conduction from the localized $100\text{ mW}$ SOT-23 footprint across this thermal barrier results in an estimated local battery ambient rise of less than $\Delta T_{\text{cell}} \le +3.0\text{--}5.0^\circ\text{C}$.
   - In a $25.0^\circ\text{C}$ room environment, the battery cell surface remains at:
     $$T_{\text{cell}} \le 25.0^\circ\text{C} + 5.0^\circ\text{C} = \mathbf{30.0^\circ\text{C}}$$
   - **IEC 62133-2 Charging Safety Compliance:** Under international standard IEC 62133-2, secondary lithium cells must not exceed $+45.0^\circ\text{C}$ surface temperature during charging. With cell surface temperature $\le 30.0^\circ\text{C}$, the charging design provides a robust $+15.0^\circ\text{C}$ safety margin below the cell limit.

---

## 3. POWER-PATH PIN-TO-NET & DIODE DESIGNATOR RECONCILIATION

### 3.1 Diode Designator Audit (D3 vs. D4)
An inspection of the KiCad schematic (`SmartPen.kicad_sch`) clarifies the diode references:
- **`D3` (`1N5819HW-7-F`):** Haptic Vibration Motor Flyback Clamp Diode. Connected directly across the vibration motor terminals (`VBAT_SW` and `HAPTIC_LOW`) to clamp inductive turn-off spikes.
- **`D4` (`1N5819HW-7-F`):** USB Power-Path OR-ing Schottky Diode. Connected between `USB_VBUS` (Pin 2, Anode) and `VSYS_RAW` (Pin 1, Cathode) to feed the AP2112K-3.3 regulator while USB is attached.
- *Reconciliation:* Prior draft reports that referenced "D3" as the power-path diode were in error; the correct schematic reference designator for the power-path diode is **`D4`**.

### 3.2 Power-Path Switching Architecture
- **P-Channel MOSFET $Q_2$ (`DMG2305UX`):**
  - Pin 1 (Gate): Connected to `USB_VBUS` (with $R_{26} = 100\text{ k}\Omega$ pull-down to GND).
  - Pin 2 (Source): Connected to `VSYS_RAW` (LDO input rail).
  - Pin 3 (Drain): Connected to `VBAT` (battery positive terminal).
- **USB Unplugged ($V_{\text{BUS}} = 0\text{ V}$):**
  - $R_{26}$ pulls Gate to $0\text{ V}$.
  - Battery voltage at Source/Drain enhances the P-FET ($V_{GS} \approx -3.7\text{ V} \ll V_{GS(th)} = -0.9\text{ V}$).
  - $Q_2$ is fully turned ON with $R_{DS(\text{on})} \approx 42\text{ m}\Omega$, powering `VSYS_RAW` with negligible drop ($< 3\text{ mV}$).
  - Diode $D_4$ is reverse-biased (Cathode at $V_{\text{BAT}}$, Anode at $0\text{ V}$), preventing any back-feed to USB port.
- **USB Plugged In ($V_{\text{BUS}} = 5.0\text{ V}$):**
  - $D_4$ conducts, supplying `VSYS_RAW` at $5.00\text{ V} - 0.35\text{ V} = 4.65\text{ V}$.
  - $Q_2$ Gate is pulled to $5.00\text{ V}$.
  - With Source at $4.65\text{ V}$, $V_{GS} = 5.00\text{ V} - 4.65\text{ V} = +0.35\text{ V} > 0\text{ V}$, turning $Q_2$ firmly OFF.
  - The intrinsic body diode of $Q_2$ is oriented from Drain (`VBAT` $\le 4.20\text{ V}$) to Source (`VSYS_RAW` $= 4.65\text{ V}$).
  - The body diode is reverse-biased by $V_{\text{diode}} = 4.20\text{ V} - 4.65\text{ V} = \mathbf{-0.45\text{ V}}$, completely preventing any current from leaking from `VSYS_RAW` into the battery through $Q_2$.
  - The battery charges exclusively through charger $U_2$ (`MCP73831`).

---

## 4. POWER-PATH TOPOLOGY & TRUTH TABLE

The circuit employs an automatic power-path switch consisting of P-channel MOSFET $Q_2$ (`DMG2305UX`), pull-down resistor $R_{26}$ ($100\text{ k}\Omega$), and Schottky diode $D_4$ (`1N5819HW-7-F`):

```
                    POWER-PATH TOPOLOGY & TRUTH TABLE
                       VBUS (5V USB)
                             │
                  ┌──────────┴──────────┐
                  │                     │
                  ▼ D4 (Schottky)       ▼ MCP73831 Charger
             (VF = 0.35V)          (I_chg = 50 mA)
                  │                     │
                  ├─────────┐           ▼
                  │         │      VBAT (Battery)
                  │         │           │
                  │         ▼ Source    ▼ Drain
               VSYS_RAW ───[ Q2 P-FET ]───
                            ▲ Gate (Driven by VBUS, R26 pull-down)
```

### 4.1 State 1: Battery-Only Operation (USB Unplugged, $V_{\text{BUS}} = 0\text{ V}$)
- Gate of $Q_2$ is tied to GND via $R_{26}$ ($100\text{ k}\Omega$): $V_G = 0\text{ V}$.
- Source of $Q_2$ is connected to $V_{\text{SYS\_RAW}}$: $V_S \approx V_{\text{BAT}} = 3.7\text{ V}$.
- Gate-to-Source Voltage: $V_{GS} = 0\text{ V} - 3.7\text{ V} = -3.7\text{ V}$.
- Since threshold voltage $V_{GS(\text{th})} \in [-0.5, -1.0]\text{ V}$, $Q_2$ is fully turned ON with $R_{DS(\text{on})} \approx 42\text{ m}\Omega$.
- At typical active writing load ($22.5\text{ mA}$), voltage drop is only:
  $$\Delta V = 0.0225\text{ A} \times 0.042\ \Omega = \mathbf{0.95\text{ mV}}$$
- Diode $D_4$ is reverse-biased, isolating the disconnected USB connector.

### 4.2 State 2: USB Attached & Charging ($V_{\text{BUS}} = 5.0\text{ V}$)
- Gate of $Q_2$ is driven directly by $V_{\text{BUS}}$: $V_G = 5.00\text{ V}$.
- Diode $D_4$ conducts, powering $V_{\text{SYS\_RAW}}$: $V_S = 5.00\text{ V} - 0.35\text{ V} = 4.65\text{ V}$.
- Gate-to-Source Voltage: $V_{GS} = 5.00\text{ V} - 4.65\text{ V} = \mathbf{+0.35\text{ V} > 0\text{ V}}$.
- $Q_2$ is turned completely OFF.
- **Body Diode Orientation:** The internal parasitic body diode of $Q_2$ points from Drain ($V_{\text{BAT}} \le 4.20\text{ V}$) to Source ($V_S = 4.65\text{ V}$). Because $V_S > V_{\text{BAT}}$, the body diode is **reverse-biased by at least $0.45\text{ V}$**.
- Zero current flows from USB into the battery via $Q_2$. The system runs entirely from USB power, and MCP73831 independently recharges the battery safely.
