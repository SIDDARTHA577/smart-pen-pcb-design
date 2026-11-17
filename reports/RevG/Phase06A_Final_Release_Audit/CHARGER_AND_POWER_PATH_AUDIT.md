# CHARGER AND POWER-PATH ELECTRICAL AUDIT

**Document ID:** SRG-P6A-PWR-005  
**Revision:** 1.0  
**Date:** November 17, 2026  
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

## 2. MCP73831 THERMAL DISSIPATION & JUNCTION TEMPERATURE

### 2.1 Worst-Case Power Dissipation
The maximum thermal stress on $U_2$ occurs at the start of constant-current (CC) charging when the battery is deeply discharged ($V_{\text{BAT}} = 3.00\text{ V}$):
- USB input voltage: $V_{\text{BUS}} = 5.00\text{ V}$
- Diode $D_3$ forward voltage drop at $50\text{ mA}$: $V_{F(D3)} \approx 0.35\text{ V}$
- Voltage at MCP73831 $V_{\text{DD}}$ pin: $V_{\text{IN}} = 5.00\text{ V} - 0.35\text{ V} = 4.65\text{ V}$
- Maximum IC Voltage Drop: $\Delta V = V_{\text{IN}} - V_{\text{BAT}} = 4.65\text{ V} - 3.00\text{ V} = \mathbf{1.65\text{ V}}$
- Worst-Case Dissipation:
  $$P_D = \Delta V \times I_{\text{charge}} = 1.65\text{ V} \times 0.050\text{ A} = \mathbf{0.0825\text{ W} \quad (82.5\text{ mW})}$$

### 2.2 Thermal Rise and Junction Temperature
The MCP73831 is packaged in a SOT-23-5 package mounted on a 4-layer FR4 board with continuous internal copper planes (In1.Cu GND and In2.Cu Power).
- Conservative junction-to-ambient thermal resistance: $\theta_{JA} = 230^\circ\text{C/W}$
- Thermal Rise above Ambient:
  $$\Delta T = P_D \times \theta_{JA} = 0.0825\text{ W} \times 230^\circ\text{C/W} = \mathbf{18.98^\circ\text{C} \quad (\approx 19.0^\circ\text{C})}$$
- At an ambient operating temperature of $T_A = 25^\circ\text{C}$:
  $$T_J = 25.0^\circ\text{C} + 19.0^\circ\text{C} = \mathbf{44.0^\circ\text{C}}$$
- At maximum elevated ambient inside the plastic enclosure ($T_A = 45^\circ\text{C}$):
  $$T_{J,\text{max}} = 45.0^\circ\text{C} + 19.0^\circ\text{C} = \mathbf{64.0^\circ\text{C}}$$

**Conclusion:** The junction temperature remains well below the maximum continuous silicon limit of $125^\circ\text{C}$ and the internal thermal regulation threshold of $150^\circ\text{C}$.

---

## 3. POWER-PATH LOAD SWITCHING & BODY DIODE ANALYSIS

The circuit employs an automatic power-path switch consisting of P-channel MOSFET $Q_2$ (`DMG2305UX`), pull-down resistor $R_8$ ($100\text{ k}\Omega$), and Schottky diode $D_3$ (`1N5819HW-7-F`).

```
                    POWER-PATH TOPOLOGY & TRUTH TABLE
                       VBUS (5V USB)
                             │
                  ┌──────────┴──────────┐
                  │                     │
                  ▼ D3 (Schottky)       ▼ MCP73831 Charger
             (VF = 0.35V)          (I_chg = 50 mA)
                  │                     │
                  ├─────────┐           ▼
                  │         │      VBAT (Battery)
                  │         │           │
                  │         ▼ Source    ▼ Drain
               VSYS_RAW ───[ Q2 P-FET ]───
                            ▲ Gate (Driven by VBUS)
```

### 3.1 State 1: Battery-Only Operation (USB Unplugged, $V_{\text{BUS}} = 0\text{ V}$)
- Gate of $Q_2$ is tied to GND via $R_8$ ($100\text{ k}\Omega$): $V_G = 0\text{ V}$.
- Source of $Q_2$ is connected to $V_{\text{SYS\_RAW}}$: $V_S \approx V_{\text{BAT}} = 3.7\text{ V}$.
- Gate-to-Source Voltage: $V_{GS} = 0\text{ V} - 3.7\text{ V} = -3.7\text{ V}$.
- Since threshold voltage $V_{GS(\text{th})} \in [-0.5, -1.0]\text{ V}$, $Q_2$ is fully turned ON with $R_{DS(\text{on})} \approx 40\text{ m}\Omega$.
- At typical active writing load ($22.5\text{ mA}$), voltage drop is only:
  $$\Delta V = 0.0225\text{ A} \times 0.040\ \Omega = \mathbf{0.9\text{ mV}}$$
- Diode $D_3$ is reverse-biased, isolating the disconnected USB connector.

### 3.2 State 2: USB Attached & Charging ($V_{\text{BUS}} = 5.0\text{ V}$)
- Gate of $Q_2$ is driven directly by $V_{\text{BUS}}$: $V_G = 5.00\text{ V}$.
- Diode $D_3$ conducts, powering $V_{\text{SYS\_RAW}}$: $V_S = 5.00\text{ V} - 0.35\text{ V} = 4.65\text{ V}$.
- Gate-to-Source Voltage: $V_{GS} = 5.00\text{ V} - 4.65\text{ V} = \mathbf{+0.35\text{ V} > 0\text{ V}}$.
- $Q_2$ is turned completely OFF.
- **Body Diode Orientation:** The internal parasitic body diode of $Q_2$ points from Drain ($V_{\text{BAT}} \le 4.20\text{ V}$) to Source ($V_S = 4.65\text{ V}$). Because $V_S > V_{\text{BAT}}$, the body diode is **reverse-biased by at least $0.45\text{ V}$**.
- Zero current flows from USB into the battery via $Q_2$. The system runs entirely from USB power, and MCP73831 independently recharges the battery safely.
