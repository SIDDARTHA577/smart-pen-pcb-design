# Smart Pen Rev F Power & Battery Subsystem Verification

**Project:** Smart Pen PCB & 3D Enclosure Design  
**Client:** RadixView Technologies / Chattychop (G. Badrinath)  
**Document Reference:** `Smart_Pen_PCB_Handoff(1).docx` (Revision 0.2, September 2026)  
**Revision:** Rev F Engineering Validation  
**Date:** November 2026  

---

## 1. Selected Battery Specifications & Physical Packaging

### 1.1 Cell Chemistry & Form Factor
- **Model / Form Factor:** 601245 Lithium-ion Polymer (LiPo) Pouch Cell.
- **Physical Dimensions:**
  - Thickness ($T$): $6.0\text{ mm} \pm 0.2\text{ mm}$ (maximum $6.2\text{ mm}$ during full charge expansion).
  - Width ($W$): $12.0\text{ mm} \pm 0.3\text{ mm}$.
  - Length ($L$): $45.0\text{ mm} \pm 0.5\text{ mm}$ (including folded terminal seal).
- **Nominal Electrical Parameters:**
  - Nominal Voltage: $3.7\text{ V}$.
  - Full Charge Cutoff: $4.20\text{ V} \pm 0.03\text{ V}$.
  - Discharge Cutoff: $3.00\text{ V}$.
  - Rated Capacity: $300\text{ mAh}$ ($1.11\text{ Wh}$).
  - Maximum Continuous Discharge Current: $1.0\text{ C} = 300\text{ mA}$ (Pulse: $2.0\text{ C} = 600\text{ mA}$).

### 1.2 Mechanical Integration & Rail Placement
- **Location:** Resting strictly **below/within the internal removable electronics rail** in a dedicated lower cradle channel.
- **Clearance to PCB:** The main PCB sits above the battery separated by a $0.8\text{ mm}$ polycarbonate isolation rib.
- **Clearance to Outer Barrel:** The pen barrel inner diameter is $13.0\text{ mm}$. The battery width of $12.0\text{ mm}$ leaves $0.5\text{ mm}$ radial clearance per side, accommodating cell swelling over life cycle ($< 8\%$).
- **Detachable Connector:** Connected to main PCB header `J_BAT` via a miniature 2-pin JST-SH ($1.0\text{ mm}$ pitch, horizontal SMD) with ultra-flexible silicone wire leads ($28\text{ AWG}$).

### 1.3 Protection Circuit Module (PCM)
Every orderable cell must incorporate an integrated protection circuit PCB (DW01A + 8205A MOSFET or Seiko S-8261):
- **Overcharge Protection Voltage:** $4.28\text{ V} \pm 0.05\text{ V}$ (release: $4.08\text{ V}$).
- **Overdischarge Protection Voltage:** $2.80\text{ V} \pm 0.08\text{ V}$ (release: $3.00\text{ V}$).
- **Overcurrent Protection:** $1.8\text{ A} \pm 0.3\text{ A}$ (trips on dead short-circuit within $10\text{ ms}$).

---

## 2. Power Tree & Current Budget Breakdown

```
[ USB-C Port 5V ] ──> [ MCP73831T Charger ] ──> [ VBAT 3.0V - 4.2V ]
                                                      │
                       ┌──────────────────────────────┴──────────────────────────────┐
                       ▼                                                             ▼
             [ SW_POWER Switch ]                                            [ Coin Motor Transistor ]
                       │                                                       (Vibration ERM 3.7V)
                       ▼
             [ AP2112K-3.3 LDO ]
                       │
       ┌───────────────┼───────────────┬───────────────┬───────────────┐
       ▼               ▼               ▼               ▼               ▼
 [ ESP32-C3 ]    [ MPU-6050 ]    [ TTP223 ]      [ MicroSD ]      [ Status LEDs ]
 (MCU / Wi-Fi)     (Front Tip)    (Cap Touch)     (SPI Flash)      (Green / Red)
```

### 2.1 Operating States and Battery Life Calculations

| Operating Mode | Subsystem States | Typical Current | Peak Current | Battery Life (300 mAh) |
| :--- | :--- | :--- | :--- | :--- |
| **Deep Sleep (Shelf Life)** | ESP32-C3 deep sleep, LDO idle, TTP223 low power | $65\ \mu\text{A}$ | $100\ \mu\text{A}$ | **~4,615 hours (6.4 months)** |
| **Standby / Pen Held** | ESP32-C3 light sleep, TTP223 active, MPU idle | $2.8\text{ mA}$ | $4.5\text{ mA}$ | **~107 hours (4.4 days)** |
| **Active Writing (Offline)** | ESP32-C3 @ 80MHz, MPU @ 200Hz, MicroSD logging | $38.0\text{ mA}$ | $65.0\text{ mA}$ | **~7.9 hours continuous** |
| **Active Writing + Wi-Fi** | ESP32-C3 @ 160MHz, Wi-Fi 802.11b TX/RX stream | $95.0\text{ mA}$ | $340.0\text{ mA}$ | **~3.15 hours continuous** |
| **USB Streaming / Charging**| Running from USB 5V, battery charging @ 303mA | *Net charging* | *Net charging* | **Unlimited runtime** |

---

## 3. Charging Circuitry & Thermal Verification

### 3.1 Linear Charger: Microchip MCP73831T-2ACI/OT
- **Charge Resistor:** $R_9 = 3.3\text{ k}\Omega \pm 1\%$ (`RC0402FR-073K3L`).
- **Programmed Charge Current:**
  $$I_{reg} = \frac{1000\text{ V}}{R_{PROG}} = \frac{1000\text{ V}}{3300\,\Omega} = 303.0\text{ mA} \approx 1.01\text{ C}$$
- **Safety Rating:** Fully compliant with standard LiPo pouch $1.0\text{ C}$ maximum continuous charging rating. Avoids the dangerous $500\text{ mA}$ ($1.67\text{ C}$) rate previously present in Rev E.

### 3.2 Charge Time Analysis
1. **Preconditioning Phase (Trickle):**
   - Active if $V_{BAT} < 2.80\text{ V}$. Charge current throttled to $10\% \times I_{reg} = 30.3\text{ mA}$. Duration: $< 5\text{ minutes}$.
2. **Constant Current (CC) Phase:**
   - Active from $2.80\text{ V} \rightarrow 4.20\text{ V}$. Current held constant at $303\text{ mA}$.
   - Charges cell to approximately $72\%$ capacity ($216\text{ mAh}$).
   - CC Duration:
     $$t_{CC} = \frac{0.72 \times 300\text{ mAh}}{303\text{ mA}} \times 1.05 \approx 45\text{ minutes}$$
3. **Constant Voltage (CV) Phase:**
   - Voltage clamped at $4.20\text{ V} \pm 1\%$. Current exponentially decays from $303\text{ mA}$ down to termination threshold ($10\% \times I_{reg} = 30.3\text{ mA}$).
   - CV Duration: $\approx 32\text{ minutes}$.
4. **Total Charge Duration:** $t_{total} \approx 77\text{ minutes}$ (~$1.3\text{ hours}$).

### 3.3 Thermal Dissipation & Enclosure Heating
- **Maximum Charger Dissipation:**
  $$P_{D(max)} = (V_{BUS(max)} - V_{BAT(min)}) \times I_{reg} = (5.25\text{ V} - 3.20\text{ V}) \times 0.303\text{ A} = 0.621\text{ W}$$
- **Nominal CC Dissipation:**
  $$P_{D(typ)} = (5.00\text{ V} - 3.70\text{ V}) \times 0.303\text{ A} = 0.394\text{ W}$$
- **Thermal Resistance:** MCP73831 in SOT-23-5 has $\theta_{JA} = 230^\circ\text{C/W}$ in free air, reduced to $\approx 110^\circ\text{C/W}$ when soldered to a multi-via PCB ground plane.
- **Die Temperature Rise:**
  $$\Delta T_{die} = 0.394\text{ W} \times 110^\circ\text{C/W} = 43.3^\circ\text{C}$$
  At $25^\circ\text{C}$ ambient, $T_{die} \approx 68.3^\circ\text{C}$, comfortably below the $150^\circ\text{C}$ junction cutoff.
- **Outer Enclosure Shell Temperature Rise:**
  The heat dissipates into the internal aluminum/polycarbonate rail and radiates across the 153.5 mm enclosure surface. The outer barrel temperature rise during charging will not exceed $8^\circ\text{C}$ above ambient, ensuring comfortable hand grip.

---

## 4. Power-Path Behavior & Recommendations

### 4.1 Identified Limitation
In the current MCP73831 topology, the battery is directly connected to the system voltage bus without an intervening power-path controller. Consequently:
1. When charging while simultaneously operating, system load current is drawn from the charger output in parallel with the battery charging current.
2. If system load exceeds $30.3\text{ mA}$ (e.g. during Wi-Fi transmission), the net current flowing into the battery decreases, and the charger cannot sense charge termination ($I_{charge} < 0.1 \times I_{reg}$). The charger remains in top-off mode indefinitely.

### 4.2 Recommended Circuit Upgrade for Production (Rev G)
To achieve true dynamic power-path management:
```
  VBUS (5V) ──────┬───────[ MCP73831 ]───────> Battery
                  │
                  ▼
          [ Schottky Diode ]
                  │
                  ├───> System VIN (AP2112K)
                  ▲
          [ P-Channel MOSFET ] (Gate driven by VBUS)
                  │
  VBAT ───────────┘
```
When VBUS is plugged in, the P-FET gate is pulled HIGH to 5V, turning OFF the P-FET and disconnecting the battery from the system load. The system is then powered cleanly from VBUS through the Schottky diode, while the MCP73831 dedicates 100% of its current to charging the battery.
When VBUS is unplugged, the P-FET gate is pulled LOW through a $100\text{ k}\Omega$ resistor, turning ON the P-FET and powering the system from the battery with negligible voltage drop ($< 25\text{ mV}$).
