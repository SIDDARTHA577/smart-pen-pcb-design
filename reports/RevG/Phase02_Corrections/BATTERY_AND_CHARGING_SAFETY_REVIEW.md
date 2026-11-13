# SMART PEN REVISION G — BATTERY TRACEABILITY & CHARGING SAFETY REVIEW
## Cell Sizing, Protection Circuitry, Cradle Clearances, and Charging Dynamics

- **Project:** Smart Pen Hardware System
- **Document ID:** `REVG-DOC-BATT-002`
- **Revision:** Rev G Phase 2.1
- **Subsystem:** Power Electronics & Energy Storage
- **Compliance Constraints:** Mandatory Requirements R1 (Outer Dimensions) & R3 (Battery Below Rail)
- **Author:** Senior Power Electronics & Battery Safety Engineer

---

## 1. Mechanical Enclosure & Cradle Spatial Envelope

Per Master Engineering Hard Constraints:
- **R1:** Maximum pen outer barrel diameter: $15.0 - 16.0\text{ mm}$; total pen body length: $150.0 - 155.0\text{ mm}$.
- **R3:** The LiPo battery must physically rest **beneath the removable electronics rail** in a dedicated cradle, completely insulated from the Main PCB, with a keyed detachable connector.

### 1.1 Removable Rail Cradle Pocket Dimensions
From the authoritative 3D CAD mechanical model of the internal removable chassis:
- **Available Cradle Pocket Length ($L_{cradle}$):** $46.00\text{ mm}$
- **Available Cradle Pocket Width ($W_{cradle}$):** $10.00\text{ mm}$
- **Available Cradle Pocket Depth ($H_{cradle}$):** $4.50\text{ mm}$ (to allow for cell swelling)

```
+-------------------------------------------------------------------------+
|                    INTERNAL REMOVABLE RAIL (SIDE VIEW)                  |
|                                                                         |
|  [=== MAIN PCB (1.0 mm) ==============================================] |
|  ------------------ KAPTON DIELECTRIC INSULATOR ----------------------- |
|  +--------------------------------------------+    [ Refill Channel ]   |
|  |           BATTERY CRADLE POCKET            |                         |
|  |   Length: 46.0 mm  |  Depth: 4.5 mm        |                         |
|  |                                            |                         |
|  +--------------------------------------------+                         |
+-------------------------------------------------------------------------+
```

---

## 2. Evaluation of Traceable Battery Candidates

To establish physical feasibility and eliminate unverified sizing assumptions, two commercial LiPo cell configurations from traceable vendors (e.g., EEMB Co., Ltd., PKCELL Battery Co., Ltd., Liter Energy Battery) were evaluated:

| Parameter | Candidate A (Recommended) | Candidate B (Disqualified) | Notes / Design Impact |
| :--- | :--- | :--- | :--- |
| **Model / Form Factor** | **LP401035 / 401035** | **LP401040 / 401040** | Standard prismatic pouch cell |
| **Nominal Voltage** | $3.70\text{ V}$ | $3.70\text{ V}$ | LiCoO2 / NMC chemistry |
| **Charge Cutoff Voltage** | $4.20\text{ V} \pm 0.05\text{ V}$ | $4.20\text{ V} \pm 0.05\text{ V}$ | Constant Voltage (CV) target |
| **Discharge Cutoff Voltage**| $3.00\text{ V}$ (PCM: $2.80\text{ V}$) | $3.00\text{ V}$ (PCM: $2.80\text{ V}$) | Under-voltage threshold |
| **Nominal Capacity** | **$130 - 150\text{ mAh}$** (typ. $140\text{ mAh}$) | **$300\text{ mAh}$** | Candidate B claims double energy density |
| **Bare Cell Dimensions** | $4.0\text{ mm} \times 10.0\text{ mm} \times 35.0\text{ mm}$ | $4.0\text{ mm} \times 10.0\text{ mm} \times 40.0\text{ mm}$ | Thickness $\times$ Width $\times$ Length |
| **Length with PCM ($L_{pack}$)**| **$37.0\text{ mm} \pm 0.5\text{ mm}$** | **$43.5\text{ mm} - 44.0\text{ mm}$** | Protection PCB + tape wrap adds $\sim 2.5\text{ mm}$ |
| **Remaining Cradle Space** | **$9.00\text{ mm}$** ($46.0 - 37.0$) | **$2.00 - 2.50\text{ mm}$** | Longitudinal clearance for wire leads |
| **Wire Exit & Bend Feasibility**| **EXCELLENT:** 9.0 mm allows gentle 28 AWG wire loop to JST SH connector | **FAIL / SEVERE PINCH:** 2.0 mm forces 90° sharp kink, wire shearing risk during insertion | Candidate B is disqualified |
| **Charge Current ($I_{CHG}$)** | $100\text{ mA}$ | $100\text{ mA}$ | Set by $R_9 = 10\text{ k}\Omega$ on MCP73831 |
| **Effective Charge C-Rate** | **$0.71\text{C}$** ($100\text{ mA} / 140\text{ mAh}$) | **$0.33\text{C}$** ($100\text{ mA} / 300\text{ mAh}$) | Both well within $\le 1.0\text{C}$ safe limit |
| **10% Swelling Thickness** | $4.40\text{ mm}$ (fits $4.50\text{ mm}$ pocket) | $4.40\text{ mm}$ | Accommodated by cradle depth |
| **Operational Run Time** | **$\sim 2.5 - 3.5\text{ hours}$ continuous writing** | $\sim 5.0 - 6.0\text{ hours}$ | Candidate A meets client operational brief |

### 2.1 Conclusion on Cell Selection
**Candidate A (LP401035, $140\text{ mAh}$)** is the only mechanically viable cell that satisfies all spatial, wire routing, and DFM constraints within the strict $15.0 - 16.0\text{ mm}$ outer diameter envelope. Candidate B must remain disqualified due to severe wire pinch hazards.

---

## 3. Battery Protection Circuit Module (PCM) Requirements

All battery packs delivered for the Smart Pen must incorporate an integrated Protection Circuit Module (PCM) ultrasonic-welded directly to the cell tabs:

```
[ Cell + ] ---> [ PCM: Seiko S-8261 / DW01A ] ---> [ Red Lead: 28 AWG ] ---> Pin 1 (VBAT) [ JST SH 2-Pin ]
[ Cell - ] ---> [ Dual MOSFET: 8205A        ] ---> [ Black Lead: 28 AWG] ---> Pin 2 (GND)  [ Keyed Receptacle ]
```

### 3.1 PCM Electrical Thresholds
- **Overcharge Protection Detection Voltage ($V_{DET1}$):** $4.28\text{ V} \pm 0.025\text{ V}$
- **Overcharge Release Voltage ($V_{REL1}$):** $4.08\text{ V} \pm 0.05\text{ V}$
- **Overdischarge Protection Detection Voltage ($V_{DET2}$):** $2.80\text{ V} \pm 0.05\text{ V}$
- **Overdischarge Release Voltage ($V_{REL2}$):** $3.00\text{ V} \pm 0.05\text{ V}$
- **Overcurrent Protection Current ($I_{OCP}$):** $2.0\text{ A} - 3.0\text{ A}$ (cutoff in $< 15\text{ ms}$)
- **Short Circuit Protection:** Continuous short detection with automatic recovery upon load removal.
- **Quiescent Current ($I_{DD}$):** $\le 3.0\,\mu\text{A}$ in active standby; $\le 0.1\,\mu\text{A}$ in power-down mode (preserves cell during 12-month shelf life).

---

## 4. Charging Subsystem & Thermal Safety Analysis

The charging management circuit is powered by `/USB_VBUS` and implemented with Microchip **MCP73831T-2ACI/OT** (`U2`):

### 4.1 Programming Resistor Equation & Verification
Per the Microchip MCP73831 datasheet (Section 4.1.1):
$$I_{REG} = \frac{1000\text{ V}}{R_{PROG}}$$
In `output/RevG/SmartPen.kicad_sch`, programming resistor $R_9$ is connected between Pin 5 (`PROG`) and `/GND`:
$$R_9 = 10.0\text{ k}\Omega \pm 1\% \quad (\text{MPN: } \text{RC0402FR-0710KL})$$
$$I_{REG} = \frac{1000\text{ V}}{10,000\,\Omega} = 0.100\text{ A} = 100.0\text{ mA}$$

### 4.2 Charging Dynamics & Thermal Dissipation
- **Preconditioning Phase:** If $V_{BAT} < 2.8\text{ V}$, $I_{pre} = 0.1 \times I_{REG} = 10\text{ mA}$ until cell recovers.
- **Constant Current (CC) Phase:** $I_{REG} = 100\text{ mA}$ until $V_{BAT}$ reaches $4.20\text{ V}$.
- **Constant Voltage (CV) Phase:** Voltage held at $4.20\text{ V} \pm 0.75\%$ until current tapers to termination threshold ($I_{term} = 0.075 \times I_{REG} = 7.5\text{ mA}$).
- **Power Dissipation in SOT-23-5 Package:**
  Worst-case dissipation occurs at start of CC phase with deeply discharged cell ($V_{BAT} = 3.0\text{ V}$):
  $$P_D = (V_{BUS} - V_{BAT}) \times I_{REG} = (5.0\text{ V} - 3.0\text{ V}) \times 0.100\text{ A} = 0.200\text{ W} = 200\text{ mW}$$
  With SOT-23 thermal resistance $\theta_{JA} \approx 230^\circ\text{C/W}$:
  $$\Delta T = P_D \times \theta_{JA} = 0.200\text{ W} \times 230^\circ\text{C/W} = 46^\circ\text{C}$$
  At an ambient temperature of $25^\circ\text{C}$, junction temperature reaches $71^\circ\text{C}$, safely below the maximum allowable $T_J = 125^\circ\text{C}$.

---

## 5. Formal Hold & Next Step Obligations

In accordance with master engineering directives:
- **Decision Status:** Sizing calculations indicate Candidate A (LP401035, $140\text{ mAh}$) is optimal. However, physical procurement of production cell samples from the battery manufacturer and verification of lead exit bending in the 3D-printed chassis sample is required.
- **Formal Status:** Retained as **FORMAL HOLD / BLOCKED** pending physical sample fit signoff.
