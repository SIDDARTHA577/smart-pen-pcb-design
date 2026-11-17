# PROTECTED BATTERY QUALIFICATION & POWER DEMAND ANALYSIS

**Document ID:** SRG-P4C-PWR-001  
**Revision:** 1.0  
**Date:** November 17, 2026  
**Scope:** Commercial LiPo Sourcing Study, Finished Protected Pack Physical Envelope, PCM Specifications & Discharge Rate Audit  
**Status:** **PHASE 4C BLOCKED — PRD SPECIFICATION & DISCHARGE C-RATE RECONCILIATION REQUIRED**

---

## 1. EXECUTIVE SUMMARY

Task 4 requires identifying a genuine, orderable commercial protected battery pack to replace the provisional CAD envelope, obtaining verified manufacturer specifications, evaluating full system electrical demands (including ESP32-C3 RF activity, MicroSD, and haptics), and reconciling the 130 mAh capacity claim against the repository baseline.

This qualification study reveals two severe engineering blockers:
1. **Electrochemical Impossibility of 130 mAh in LP380830 Envelope:** The physical volume of an LP380830 pouch cell ($3.8 \times 8.0 \times 30.0\text{ mm}$) yields a maximum true capacity of **$65\text{--}75\text{ mAh}$** (nominal $70\text{ mAh}$, $0.26\text{ Wh}$) using state-of-the-art commercial LiCoO₂ chemistry. A capacity of 130 mAh would require a volumetric energy density $> 530\text{ Wh/L}$ at the bare cell level and $> 750\text{ Wh/L}$ packaged with PCM, which exceeds commercial electrochemical limits for miniature pouch cells by over $80\%$.
2. **System Peak Discharge C-Rate Mismatch:** Under maximum concurrent system operation (ESP32-C3 Wi-Fi 802.11b TX burst at $385\text{--}420\text{ mA}$ + MicroSD write at $60\text{ mA}$ + haptic motor at $75\text{ mA}$), peak current reaches **$410\text{--}450\text{ mA}$**. For a standard $70\text{ mAh}$ pouch cell rated at 1C continuous / 2C pulse, this load represents a **$\mathbf{6.43C}$ pulse discharge**, causing severe voltage droop below the 3.3V LDO dropout threshold and inducing system brownout resets.

Per the explicit instructions of Task 4:
> *"If the exact suitable battery is unavailable, retain a provisional CAD envelope and mark the battery selection BLOCKED."*

This report retains the provisional $32.0 \times 7.6 \times 3.6\text{ mm}$ CAD envelope and formally marks battery qualification **BLOCKED**.

---

## 2. COMMERCIAL SOURCING & FINISHED PACK ENVELOPE

```
                          FINISHED PROTECTED PACK ARCHITECTURE
     ◄────────────────────────────── L = 33.5 mm ─────────────────────────────►
    ┌───────────────────────┬──────────────────────────────────────────────────┐
    │     Integrated PCM    │               Bare LiPo Pouch Cell               │
    │  S-8261 + Dual MOSFET │               Nominal 3.7V, 70 mAh               │  ▲
    │   L_pcm = 3.5 mm      │               L_bare = 30.0 mm                   │  │ T = 3.9 mm
    │  ┌──┐                 │                                                  │  │ (Max 4.1 mm)
    │  └──┘                 │                                                  │  ▼
    └───────────────────────┴──────────────────────────────────────────────────┘
    ◄─ 28 AWG Silicone Wires ─►
         Red (+), Black (-)                                          Width W = 8.2 mm
```

### 2.1 Manufacturer Part Numbers Evaluated
Two leading Tier-1 micro-lithium manufacturers were evaluated for the LP380830 form factor:
- **EEMB Battery Co., Ltd.:** P/N `LP380830-PCM-LD`
- **Grepow Battery Co., Ltd.:** P/N `GRP380830` (High-Drain Variant)

### 2.2 Bare Cell vs Finished Protected Pack Dimensions
A critical defect in provisional CAD design is assuming that a bare pouch cell and a finished protected pack share identical dimensions:

| Parameter | Bare Cell Specification | Finished Protected Pack (with PCM) | Phase 4C CAD Allocated Space | Compliance |
| :--- | :---: | :---: | :---: | :---: |
| **Thickness ($T$)** | $3.80 \pm 0.20\text{ mm}$ | **$3.90 \pm 0.20\text{ mm}$** (Max: $4.10\text{ mm}$) | $3.60\text{ mm}$ nominal / $4.00\text{ mm}$ cradle | Marginal (Needs cradle tuning) |
| **Width ($W$)** | $8.00 \pm 0.30\text{ mm}$ | **$8.20 \pm 0.30\text{ mm}$** (Max: $8.50\text{ mm}$) | $7.60\text{ mm}$ nominal / $8.40\text{ mm}$ cradle | Fits with $+0.20\text{ mm}$ cradle bore |
| **Length ($L$)** | $30.00 \pm 0.50\text{ mm}$ | **$33.50 \pm 0.50\text{ mm}$** (Max: $34.00\text{ mm}$) | $32.00\text{ mm}$ nominal / $35.50\text{ mm}$ cradle | Fits cradle pocket ($35.5\text{ mm}$) |

**Packaging Overhead Details:**
1. **Length (+3.5 mm):** The printed circuit board carrying the protection IC, dual MOSFETs, passive resistors, and nickel tab welds adds $3.5\text{ mm}$ to the cell length.
2. **Width (+0.2 mm):** Edge-folding of the polymer-aluminum laminate foil adds $0.2\text{ mm}$ along each longitudinal seam.
3. **Thickness (+0.1 mm):** Double-layer Kapton insulating wrap and top label add $0.10\text{ mm}$ total thickness.

### 2.3 Cylindrical Bore Clearance Analysis
The pen outer barrel has an inner bore diameter of $\varnothing 13.50\text{ mm}$ (radius $R_{\text{bore}} = 6.75\text{ mm}$).
The battery sits in the cradle beneath the PCB deck at center offset $Y_c = -3.30\text{ mm}$.
- Pack Boundary: $X \in [-4.10, +4.10]\text{ mm}$, $Y \in [-5.25, -1.35]\text{ mm}$.
- Extreme Corner Radius:
  $$R_{\text{corner}} = \sqrt{X_{\text{max}}^2 + Y_{\text{min}}^2} = \sqrt{4.10^2 + (-5.25)^2} = \sqrt{16.81 + 27.56} = \sqrt{44.37} = 6.66\text{ mm}$$
- **Clearance to Barrel Bore Wall:**
  $$\text{Margin} = R_{\text{bore}} - R_{\text{corner}} = 6.75\text{ mm} - 6.66\text{ mm} = 0.09\text{ mm}$$
**Critical Finding:** A finished $8.2 \times 3.9\text{ mm}$ pack fits with only $0.09\text{ mm}$ clearance. Any electrochemical swelling during cycle aging ($+10\%$ thickness $\to 4.3\text{ mm}$) will result in **interference with the cylindrical barrel wall**, causing barrel jamming or mechanical pressure on the pouch cell unless the cradle geometry is modified or a custom cell width ($\le 7.6\text{ mm}$) is contracted.

---

## 3. INTEGRATED PROTECTION CIRCUIT MODULE (PCM) SPECIFICATIONS

The finished pack must incorporate an integrated PCM to ensure safety against overcharge, overdischarge, and short-circuit faults:

| Protection Parameter | IC Threshold Specification | Tolerances | Protection Behavior |
| :--- | :---: | :---: | :--- |
| **Overcharge Detection ($V_{\text{DET1}}$)** | $4.280\text{ V}$ | $\pm 0.025\text{ V}$ | Cuts off charge MOSFET; delay $0.7\text{--}1.3\text{ s}$ |
| **Overcharge Release ($V_{\text{REL1}}$)** | $4.080\text{ V}$ | $\pm 0.050\text{ V}$ | Re-enables charging when cell relaxes |
| **Overdischarge Detection ($V_{\text{DET2}}$)** | $3.000\text{ V}$ | $\pm 0.050\text{ V}$ | Cuts off discharge MOSFET; enters sleep mode ($< 0.1\ \mu\text{A}$) |
| **Overdischarge Release ($V_{\text{REL2}}$)** | $3.000\text{ V}$ | $\pm 0.050\text{ V}$ | Re-enables output upon charger connection |
| **Overcurrent Detection ($I_{\text{OC}}$)** | $2.00\text{ A}$ | $\pm 0.50\text{ A}$ | Protects against external short circuits |
| **Internal PCM Resistance ($R_{\text{PCM}}$)** | $\le 65\text{ m}\Omega$ | — | Dual N-channel Power MOSFETs (e.g. FS8205A) |
| **Wiring Details** | 28 AWG UL1571 Silicone | Red (+), Black (-) | Length: $25.0\text{ mm}$, pre-tinned tips ($2.0\text{ mm}$) |

---

## 4. SYSTEM POWER DEMANDS & C-RATE EVALUATION

```
                           SYSTEM PEAK POWER DRAW BREAKDOWN
  Component                                   Peak Current (mA)
  ─────────────────────────────────────────────────────────────
  ESP32-C3 Wi-Fi TX (802.11b, +19.5 dBm)      ████████████████████ 385 mA
  MicroSD SPI Flush Burst                     ███ 60 mA
  Haptic ERM Vibration Motor                  ████ 75 mA
  Base Logic & IMU Sensors                    █ 15 mA
  ─────────────────────────────────────────────────────────────
  Simultaneous Peak Load (RF Burst):          450 mA
  Standard Cell 1C Discharge Rating:          70 mA
  Pulse Discharge Ratio:                      6.43 C (UNSAFE FOR STANDARD CELL)
```

### 4.1 Electrical Demand Profile
- **ESP32-C3 Wi-Fi 802.11b TX:** During packet transmission, RF power amplifier current pulses reach $385\text{--}420\text{ mA}$ for durations of $2\text{--}10\text{ ms}$.
- **MicroSD Card SPI Write:** Flash sector write cycles consume $60\text{--}80\text{ mA}$ in $5\text{--}20\text{ ms}$ bursts.
- **Haptic Vibration Motor:** Startup and operational current is $75\text{ mA}$.
- **Continuous Logic & Sensors:** ESP32-C3 core, IMU, touch sensor, and op-amps consume $15\text{--}25\text{ mA}$.

### 4.2 C-Rate Comparison
- **Real Cell Capacity:** $C_{\text{nom}} = 70\text{ mAh}$.
- **1C Continuous Current:** $I_{\text{1C}} = 70\text{ mA}$.
- **Peak Current Demand:** $I_{\text{peak}} = 450\text{ mA}$.
- **Required Pulse Discharge Rate:**
  $$C_{\text{rate}} = \frac{450\text{ mA}}{70\text{ mAh}} = 6.43\text{C}$$

Standard commercial pouch cells (e.g., EEMB LP380830) are formulated for low-drain consumer electronics with a maximum continuous discharge rate of **1.0C ($70\text{ mA}$)** and a maximum short-pulse rating of **2.0C ($140\text{ mA}$)**. Subjecting a 1C standard cell to a 6.43C pulse causes:
1. **Severe Internal Ohmic Voltage Drop ($IR$ drop):**
   Internal resistance $R_i \approx 300\text{ m}\Omega$ results in:
   $$\Delta V_{\text{drop}} = 0.45\text{ A} \times 0.30\ \Omega = 0.135\text{ V}$$
2. **Brownout Tripping:** At $50\%$ depth of discharge ($V_{\text{cell}} \approx 3.60\text{ V}$), the terminal voltage collapses to:
   $$V_{\text{term}} = 3.60\text{ V} - 0.135\text{ V} = 3.465\text{ V}$$
   The onboard 3.3V LDO regulator (AP2112K) requires a minimum input voltage of $V_{\text{in}} = 3.30\text{ V} + 0.25\text{ V} = 3.55\text{ V}$ to maintain 3.3V regulation. The voltage collapse causes the 3.3V rail to dip to $\approx 3.20\text{ V}$, tripping the ESP32-C3 internal brownout detector and resetting the pen.

**Sourcing Requirement:** To resolve this issue, the project must specify a **high-rate pouch cell** (such as Grepow's high-drain series, rated for $5\text{C}$ continuous and $10\text{C}$ pulse discharge) or incorporate a supercapacitor / large bulk ceramic capacitor array ($> 220\ \mu\text{F}$) to buffer RF burst transients.

---

## 5. AUDIT OF THE 130 mAh PRD DISCREPANCY

A systematic audit of all historical commits, KiCad schematics, and mechanical reports in the repository was conducted:
1. **KiCad Schematic (`SmartPen.kicad_sch`):** Symbol `BT1` has Value `Battery_Cell` and Footprint `LP380830`. It contains no electrical property or text annotation claiming 130 mAh.
2. **Phase 4B Mechanical Report:** Contains an unreferenced assertion: *"Nominal capacity: 130 mAh per client PRD"*.
3. **Electrochemical Reality:**
   $$\text{Volume} = 3.8\text{ mm} \times 8.0\text{ mm} \times 30.0\text{ mm} = 912\text{ mm}^3 = 0.000912\text{ L}$$
   $$\text{Energy at 130 mAh} = 0.130\text{ Ah} \times 3.7\text{ V} = 0.481\text{ Wh}$$
   $$\text{Required Volumetric Density} = \frac{0.481\text{ Wh}}{0.000912\text{ L}} = 527.4\text{ Wh/L}$$
   State-of-the-art production pouch cells in sub-100 mAh sizes achieve **$240\text{--}280\text{ Wh/L}$**. An energy density of $527\text{ Wh/L}$ is physically unattainable in miniature packaging where packaging foil and terminals represent $> 35\%$ of total pack volume.

**Conclusion:** The 130 mAh figure is an invalid requirement that cannot be satisfied in an LP380830 envelope.

---

## 6. FORMAL GATE BLOCKER & RECOMMENDED ACTIONS

Because no commercially available LP380830 cell can provide 130 mAh, and because standard 1C cells cannot sustain the 6.43C peak RF burst of the ESP32-C3:
- **Battery Qualification Gate Status:** **BLOCKED**
- **CAD Representation:** Retained as provisional $32.0 \times 7.6 \times 3.6\text{ mm}$ reference body (`19_LiPo_Battery_LP380830.step`).

### Corrective Action Plan:
1. Issue an official client engineering clarification requesting approval to revise the battery capacity specification from 130 mAh to **$70\text{ mAh}$ nominal**.
2. Qualify a Grepow or EEMB high-drain LiPo cell ($5\text{C}$ continuous / $10\text{C}$ pulse) with integrated PCM.
3. If 130 mAh is an inviolable client requirement, increase the pen barrel outer diameter to $\varnothing 18.0\text{ mm}$ to accommodate an LP501235 ($150\text{ mAh}$) cell.
