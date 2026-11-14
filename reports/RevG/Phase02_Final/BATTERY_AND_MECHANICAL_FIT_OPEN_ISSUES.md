# BATTERY MECHANICAL TOLERANCE STACK-UP, SWELLING HAZARD & CRADLE FIT AUDIT

**Document ID:** RPT-REVG-P02-FINAL-BATTERY-FIT  
**Author:** Senior Mechanical CAD & Battery Safety Engineer  
**Baseline Model:** 401035 Lithium-Ion Polymer Pouch Cell (Nominal $130\text{ mAh}$, $3.7\text{ V}$)  
**Enclosure Baseline:** Smart Pen Revision G Removable Electronics Rail & Battery Cradle  
**Status:** **FORMAL HOLD / PRODUCTION BLOCKER**  

---

## 1. Context and Problem Statement

Requirement **R3** of the Master Engineering Instructions mandates:
> *"The battery must physically rest below the removable electronics rail. Provide a separate battery cradle and insulation from the Main PCB. Verify battery size, protection, swelling allowance, and keyed detachable connector."*

During Phase 2 audits and Phase 2.2 tolerance verification, a critical dimensional interference risk was identified between the internal battery cradle geometry and the nominal pouch cell specification.

---

## 2. Dimensional Stack-Up & Tolerance Analysis

### 2.1 Component Specifications

| Dimension | Battery Cradle Pocket (CAD Rev F) | 401035 Pouch Cell (Nominal) | Cell Mfg Tolerance | Cell State-of-Charge / Cycle Swelling | Worst-Case Cell Dimension | Clearance Margin |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Length (X)** | $38.0\text{ mm}$ | $35.0\text{ mm}$ | $\pm 0.5\text{ mm}$ | $+0.5\text{ mm}$ | $36.0\text{ mm}$ | **$+2.0\text{ mm}$ (Adequate)** |
| **Thickness (Z)**| $4.8\text{ mm}$ | $4.0\text{ mm}$ | $\pm 0.2\text{ mm}$ | $+0.4\text{ mm}$ ($+10\%$) | $4.6\text{ mm}$ | **$+0.2\text{ mm}$ (Marginal)** |
| **Width (Y)** | **$10.0\text{ mm}$** | **$10.0\text{ mm}$** | **$\pm 0.3 - 0.5\text{ mm}$**| **$+0.5\text{ mm}$ ($+5\%$)** | **$10.8 - 11.0\text{ mm}$** | **$-0.8\text{ mm}$ to $-1.0\text{ mm}$ (INTERFERENCE)** |

### 2.2 Failure Mechanism & Hazard Assessment
1. **Initial Assembly Interference:** With nominal pouch cell width at $10.0\text{ mm}$ and standard vendor cut tolerances ranging up to $+0.5\text{ mm}$, cells measuring $10.3 - 10.5\text{ mm}$ cannot be inserted into a $10.0\text{ mm}$ pocket without forceful mechanical compression.
2. **Cyclic Swelling Hazard:** During standard LiPo operation (especially fast charging or elevated ambient temperatures), pouch cells experience $5\%$ to $10\%$ volumetric expansion. Constraining a pouch cell in a rigid, undersized polymer cradle generates lateral compressive stress on the aluminum foil pouch seams.
3. **Catastrophic Failure Modes:**
   - Rupture of the hermetic polymer-aluminum seal, leading to electrolyte outgassing and toxic solvent emission inside the sealed pen barrel.
   - Mechanical pinch against the sharp plastic cradle ribs, risking internal cathode-anode separator puncture, thermal runaway ($> 500^\circ\text{C}$), and battery fire.

---

## 3. Engineering Remediation Pathways

To eliminate the interference hazard, two distinct engineering solutions are proposed for client review:

```
Pathway 1: Mechanical Pocket Widening (Recommended)
┌──────────────────────────────────────────────┐
│ Rail Width: 12.0 mm                          │
│ ┌──────────────────────────────────────────┐ │
│ │ Cradle Pocket Width: 10.8 mm             │ │  <-- Thinned cradle walls (0.6mm)
│ │   [ 401035 Cell: 10.0mm (+0.5mm max) ]   │ │  <-- Guaranteed 0.3mm air gap
│ └──────────────────────────────────────────┘ │
└──────────────────────────────────────────────┘

Pathway 2: Sourcing Narrower Cell (Alternative)
┌──────────────────────────────────────────────┐
│ Rail Width: 12.0 mm                          │
│ ┌──────────────────────────────────────────┐ │
│ │ Cradle Pocket Width: 10.0 mm (Unchanged) │ │
│ │   [ 350935 Cell: 9.0mm (+0.3mm max) ]    │ │  <-- Guaranteed 0.7mm air gap
│ └──────────────────────────────────────────┘ │  <-- Capacity penalty: ~105mAh vs 130mAh
└──────────────────────────────────────────────┘
```

### Pathway 1: Mechanical Cradle Pocket Modification (Recommended)
- Widen the internal battery cradle pocket from $10.0\text{ mm}$ to **$10.80\text{ mm}$**.
- Reduce the internal non-structural pocket guide rib thickness from $1.0\text{ mm}$ to $0.60\text{ mm}$.
- Retain the existing $130\text{ mAh}$ 401035 battery form factor and run-time budget ($> 4.5\text{ hours}$ active tracking).
- Requires zero schematic or PCB layout modifications.

### Pathway 2: Alternative Battery Cell Sourcing
- Procure a $9.0\text{ mm}$ wide pouch cell (e.g. Model `350935` or `400935`: $3.5\times 9.0\times 35.0\text{ mm}$, $100 - 110\text{ mAh}$).
- Maintains the current CAD cradle dimensions ($10.0\text{ mm}$ pocket width) with a comfortable $1.0\text{ mm}$ nominal clearance margin.
- Trade-off: Nominal battery capacity reduces by $\sim 15 - 20\%$ (from $130\text{ mAh}$ to $\sim 105\text{ mAh}$), reducing active runtime to $\sim 3.8\text{ hours}$.

---

## 4. Electrical Protection & Detachable Interconnect Audit

The electrical parameters of the battery subsystem meet all Phase 2 safety requirements:
1. **Integrated Protection Circuit Module (PCM):**
   - Overcharge cutoff voltage: $4.28\text{ V} \pm 0.05\text{ V}$
   - Overdischarge cutoff voltage: $2.80\text{ V} \pm 0.08\text{ V}$
   - Overcurrent / Short-circuit trip current: $1.5\text{ A} - 2.5\text{ A}$ (auto-recovering)
2. **Keyed Detachable Interconnect:**
   - Mating pair: JST-SH 2-pin $1.0\text{ mm}$ pitch or Molex PicoBlade $1.25\text{ mm}$ pitch.
   - Pin 1: `VBAT` (Red, 28 AWG silicone-jacketed wire).
   - Pin 2: `GND` (Black, 28 AWG silicone-jacketed wire).
   - Mechanical shroud prevents reverse-polarity insertion.
   - Strain-relieved wire loop ($15\text{ mm}$ service loop) prevents tensile stress on solder joints during rail insertion/removal.

---

## 5. Formal Hold Declaration

Until the mechanical cradle CAD geometry is updated or an alternative $9.0\text{ mm}$ cell is formally approved:
- **BATTERY PHYSICAL PROCUREMENT & TOOLING IS ON FORMAL HOLD.**
- While the schematic, netlist, charging controller (`MCP73831T`), and power-path routing are approved, physical tooling of the polymer cradle must not proceed until the clearance margin is expanded to $\ge 0.60\text{ mm}$ under worst-case thermal expansion.
