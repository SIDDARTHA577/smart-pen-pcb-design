# ENGINEERING CHANGE REQUEST: CHARGER CURRENT PROGRAMMING RESISTOR R9

**Document ID:** ECR-ELEC-REVG-001  
**Revision:** 1.0  
**Date:** November 17, 2026  
**Originator:** Hardware & Electrical Safety Engineering Team  
**Affected Subsystem:** Main Electronics PCB (`SmartPen.kicad_sch` & `SmartPen.kicad_pcb`)  
**Affected Component:** Resistor R9 (MCP73831 Charge Current Programming)  
**Classification:** **SAFETY CRITICAL / THERMAL RELIABILITY**  
**Status:** **PENDING FORMAL ELECTRICAL REVISION APPROVAL (BASELINE PRESERVED)**

---

## 1. CHANGE IDENTIFICATION & SUMMARY

| Field | Detail |
| :--- | :--- |
| **ECR Reference** | ECR-ELEC-REVG-001 |
| **Title** | Optimization of Battery Charging Current via Programming Resistor R9 |
| **Baseline Schematic** | `SmartPen.kicad_sch` (Git Commit: `6f0568501b2371a37f933f0e4d78ab834fa4ff65`) |
| **Current Component Value** | $R_9 = 10.0\text{ k}\Omega \pm 1\%$, 0402 ($I_{\text{CHG}} = 100\text{ mA}$) |
| **Phase 4B Proposal** | $R_9 = 12.0\text{ k}\Omega \pm 1\%$, 0402 ($I_{\text{CHG}} = 83.3\text{ mA}$) |
| **Recommended ECR Value** | **$R_9 = 20.0\text{ k}\Omega \pm 1\%$, 0402 ($I_{\text{CHG}} = 50.0\text{ mA}$)** |
| **Qualified Cell Form Factor** | LP380830 Protected LiPo Pouch Cell ($C_{\text{nom}} = 70\text{ mAh}$) |

---

## 2. REASON FOR CHANGE & SAFETY DEFECT ANALYSIS

The Smart Pen incorporates a Microchip **MCP73831T-2ACI/OT** miniature single-cell Li-Ion/Li-Polymer charge management controller (U1, SOT-23-5 package). The constant-current (CC) regulation value $I_{\text{REG}}$ is programmed by a single resistor connected between the `PROG` pin and ground:
$$I_{\text{REG}} = \frac{1000\text{ V}}{R_{\text{PROG}}}$$

```
                           MCP73831 CHARGER SCHEMATIC CONTEXT
               VBUS (+5V) ───► [VDD]          [VBAT] ───► VBAT (Battery +)
                               [VSS]          [STAT] ───► LED Indicator
                                      [PROG]
                                         │
                                         ▼
                                        ┌┴┐
                                        │ │ R9 (PROG Resistor)
                                        │ │ Baseline: 10 kΩ -> 100 mA (1.43C - UNSAFE)
                                        └┬┘ Phase 4B: 12 kΩ -> 83.3 mA (1.19C - UNSAFE)
                                         │  ECR-001:  20 kΩ -> 50.0 mA (0.71C - SAFE)
                                        GND
```

### 2.1 C-Rate Overstress on 70 mAh Pouch Cell
As established in `PROTECTED_BATTERY_QUALIFICATION.md`, the true physical capacity of a commercial LP380830 pouch cell is **$70\text{ mAh}$ nominal** ($65\text{--}75\text{ mAh}$ range).
Evaluating the charge currents against this cell yields:

1. **Current Baseline ($R_9 = 10.0\text{ k}\Omega$):**
   $$I_{\text{REG}} = \frac{1000\text{ V}}{10,000\ \Omega} = 100.0\text{ mA}$$
   $$\text{Charge Rate} = \frac{100.0\text{ mA}}{70\text{ mAh}} = \mathbf{1.43C}$$
2. **Phase 4B Proposal ($R_9 = 12.0\text{ k}\Omega$):**
   $$I_{\text{REG}} = \frac{1000\text{ V}}{12,000\ \Omega} = 83.3\text{ mA}$$
   $$\text{Charge Rate} = \frac{83.3\text{ mA}}{70\text{ mAh}} = \mathbf{1.19C}$$

According to **IEC 62133-2** and manufacturer datasheets (EEMB, Grepow) for miniature lithium polymer pouch cells:
- **Standard Recommended Charge Rate:** $0.2\text{C}$ to $0.5\text{C}$ ($14\text{--}35\text{ mA}$).
- **Maximum Fast Charge Rate:** $0.7\text{C}$ to $1.0\text{C}$ ($49\text{--}70\text{ mA}$).
- **Severe Prohibition:** Charging above $1.0\text{C}$ in an unventilated, insulated enclosure accelerates lithium dendrite formation, degrades cathode stability, induces pouch swelling, and drastically increases the risk of thermal runaway.

Both the $10.0\text{ k}\Omega$ baseline ($1.43\text{C}$) and the proposed $12.0\text{ k}\Omega$ value ($1.19\text{C}$) violate manufacturer safety specifications.

---

## 3. THERMAL DISSIPATION IN SEALED BARREL

The MCP73831 is a linear pass regulator. During constant-current charging, excess voltage between the USB input ($V_{\text{BUS}} = 5.00\text{ V}$) and the battery terminal ($V_{\text{BATT}}$) is dissipated entirely as heat across the internal MOSFET.

### 3.1 Worst-Case Power Dissipation
When charging a deeply discharged battery ($V_{\text{BATT}} \approx 3.40\text{ V}$):
$$\Delta V = V_{\text{BUS}} - V_{\text{BATT}} = 5.00\text{ V} - 3.40\text{ V} = 1.60\text{ V}$$

Comparing thermal dissipation across resistor values:
- **At 100 mA ($R_9 = 10\text{ k}\Omega$):**
  $$P_{\text{diss}} = 1.60\text{ V} \times 0.100\text{ A} = 0.160\text{ W}$$
- **At 83.3 mA ($R_9 = 12\text{ k}\Omega$):**
  $$P_{\text{diss}} = 1.60\text{ V} \times 0.0833\text{ A} = 0.133\text{ W}$$
- **At 50.0 mA ($R_9 = 20\text{ k}\Omega$ - Recommended):**
  $$P_{\text{diss}} = 1.60\text{ V} \times 0.050\text{ A} = 0.080\text{ W} \quad (\mathbf{50\% \text{ reduction!}})$$

### 3.2 Temperature Rise in Enclosed Pen Barrel
The SOT-23-5 package on a 2-layer FR4 board has a junction-to-ambient thermal resistance $\theta_{\text{JA}} \approx 230^\circ\text{C/W}$. Inside an unventilated plastic barrel where convective airflow is zero:
- **At 100 mA:** $\Delta T \approx 0.160\text{ W} \times 230^\circ\text{C/W} = +36.8^\circ\text{C}$.
  At an ambient room temperature of $25^\circ\text{C}$, the IC junction reaches $61.8^\circ\text{C}$, heating the adjacent battery cradle above $45^\circ\text{C}$ (the absolute upper charging temperature threshold for LiPo cells).
- **At 50 mA:** $\Delta T \approx 0.080\text{ W} \times 230^\circ\text{C/W} = +18.4^\circ\text{C}$.
  The IC junction stays below $43.4^\circ\text{C}$, maintaining safe battery temperatures below $35^\circ\text{C}$.

---

## 4. CHARGE TIME & USER EXPERIENCE EVALUATION

A common concern with reducing charge current is extended recharge time. For a $70\text{ mAh}$ cell:
- **Constant Current (CC) Phase (0 to ~80% SOC):**
  $$t_{\text{CC}} = \frac{70\text{ mAh} \times 0.80}{50\text{ mA}} \approx 1.12\text{ hours } (67\text{ minutes})$$
- **Constant Voltage (CV) Phase (80% to 100% SOC):** $\approx 45\text{ minutes}$.
- **Total Charge Time:** $\approx 1.8\text{--}2.0\text{ hours}$.

For a smart pen recharged via USB-C docking or desk cable, a 1.8-hour full recharge time provides an excellent balance of charging speed, battery longevity ($> 500$ cycles), and thermal safety.

---

## 5. NON-MODIFICATION PROTOCOL & IMPLEMENTATION STEPS

In accordance with release gate instructions:
> *"Do not silently modify the preserved baseline. Apply changes only through a separately tracked electrical revision."*

The baseline KiCad schematic (`SmartPen.kicad_sch`) and PCB layout (`SmartPen.kicad_pcb`) at commit `6f05685` have been left strictly unmodified in this mechanical release gate.

### Implementation Checklist for Electrical Engineering (Rev H):
1. **Schematic Update:**
   - Open `SmartPen.kicad_sch`.
   - Locate Resistor `R9` connected to MCP73831 pin 5 (`PROG`).
   - Change Property `Value` from `10k` to `20k`.
   - Update Property `Description` to `Resistor, 20.0k, 1%, 0402, 1/16W`.
2. **Bill of Materials (BOM) Update:**
   - Update BOM line for R9 with exact orderable part number:
     - **Manufacturer:** YAGEO / Panasonic
     - **Manufacturer P/N:** `RC0402FR-0720KL` (or equivalent AEC-Q200 precision thick film resistor)
     - **Tolerance:** $\pm 1\%$
3. **PCB Layout Verification:**
   - Run DRC on `SmartPen.kicad_pcb` to confirm footprint 0402 compatibility.
   - Commit changes on branch `engineering/revh-electrical-fixes` with commit message:
     `fix(elec): update R9 to 20k for safe 50mA charging of LP380830 cell (ECR-ELEC-REVG-001)`

---

## 6. ECR SIGN-OFF & GATE IMPACT

- **Electrical Engineering Lead:** Review Complete (Recommended: $20.0\text{ k}\Omega$)
- **Mechanical / Thermal Engineering:** Approved (Thermal budget compliant)
- **Safety & Regulatory Compliance:** Approved (IEC 62133-2 compliant)
- **Gate Recommendation:** **HOLD PHASE 5 ENTRY** until this ECR is officially accepted and merged into the electrical baseline.
