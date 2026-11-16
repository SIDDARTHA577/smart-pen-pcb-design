# Smart Pen Rev G — Protected LiPo Battery Selection & Safety Specification
**Document ID:** RPT-REVG-P3C-BATTERY-SELECTION  
**Project:** Smart Pen Hardware Architecture Revision G  
**Variant:** Four-Layer Evaluation Candidate (`output/RevG/variants/FourLayer_Candidate/SmartPen.kicad_pcb`)  
**Git Branch:** `engineering/revg-production`  
**Base Commit:** `f76aab08831da7bf26516d4a1a39215d754e0d73`  
**Date:** November 16, 2026  
**Status:** Manufacturer Battery Specifications Evaluated; Charger Current Redesign Recommendation Formulated  

---

## 1. Executive Summary

This report establishes the technical and safety specification for the rechargeable battery power source of the Smart Pen Revision G hardware system. Inspection of the authoritative schematic and PCB confirms that the onboard linear charger (`U2: MCP73831T-2ACI/OT`) is programmed via resistor $R_9 = 10.0\text{ k}\Omega$ to deliver a constant-current charge rate of approximately $100.0\text{ mA}$. **Crucially, the main PCB contains NO onboard battery protection circuit.**

To ensure absolute operational safety, prevent thermal runaway in the sealed cylindrical pen barrel, and preserve battery cycle life, this report evaluates real commercially available protected lithium-polymer (LiPo) pouch cells that fit below the internal removable rail. It uncovers a critical charge-rate mismatch between the current $100\text{ mA}$ charger setting and standard sub-100 mAh pouch cells, provides an exact circuit modification recommendation, and formally maintains the client approval gate.

---

## 2. Power-Path Circuit Architecture & Charging Baseline

```
 [USB +5V] ---+---> [U2: MCP73831] ---> [J_BAT: Pin 1] ===> [Protected LiPo Pack]
              |     (Charger, 100mA)      (SM02B-SRSS)         (Integrated PCM)
              |                                                      |
              +---> [D4: Schottky] ---+---> [U4: AP2112K] ---------> [3.3V Rail]
                                      |     (LDO Regulator)
 [Battery +3.7V] ---> [Q2: P-MOSFET] -+
```

### 2.1 Charger Programming & Thermal Dissipation
- **Charger IC:** Microchip `MCP73831T-2ACI/OT` (SOT-23-5).
- **Regulated Output Voltage:** Fixed $4.20\text{V} \pm 0.75\%$.
- **Current Programming Resistor ($R_9$):** $10.0\text{ k}\Omega \pm 1\%$ (0402, connected from PROG to GND).
- **Present Charge Current ($I_{\text{REG}}$):**
  $$I_{\text{REG}} = \frac{1000\text{ V}}{R_{\text{PROG}}} = \frac{1000\text{ V}}{10.0\text{ k}\Omega} = 100.0\text{ mA}$$
- **Thermal Power Dissipation ($P_{\text{diss}}$):** During the constant-current phase with an empty cell ($V_{\text{BAT}} \approx 3.2\text{V}$) and USB bus voltage at $+5.0\text{V}$:
  $$P_{\text{diss}} = (V_{\text{IN}} - V_{\text{BAT}}) \times I_{\text{REG}} = (5.0\text{V} - 3.2\text{V}) \times 0.100\text{A} = 180.0\text{ mW}$$
  Inside an unventilated cylindrical barrel with poor convective cooling, this localized heat dissipation elevates U2's junction temperature ($\theta_{JA} \approx 230^\circ\text{C/W} \implies \Delta T \approx 41^\circ\text{C}$).

### 2.2 Battery Connector Polarity (`J_BAT`)
- **Connector Type:** JST `SM02B-SRSS-TB(LF)(SN)` (1.0 mm pitch horizontal SMT receptacle).
- **Physical Position:** $X = 62.800\text{ mm}, Y = 1.720\text{ mm}$ on `F.Cu`.
- **Pinout Verification:**
  - **Pin 1:** `/VBAT` (Battery Positive, $+3.7\text{V}$ nominal).
  - **Pin 2:** `/GND` (Battery Negative / Ground).
  - **Pins 3 & 4:** Solder retention tabs tied to `/GND`.
- **Wire Harness Standard:** The external battery pack leads must strictly terminate in a matching JST `SHR-02V-S-B` housing with Pin 1 (Red wire / Positive) and Pin 2 (Black wire / Negative).

### 2.3 Mandatory Protection Circuit Module (PCM) Requirement
Because the main board contains no onboard battery protection IC (such as a DW01A / FS312F with dual MOSFET switches):
- **Safety Directive:** Connecting an unprotected bare LiPo pouch cell to `J_BAT` presents a severe risk of fire, cell swelling, and thermal runaway under short-circuit or deep-discharge conditions.
- **Mandatory Feature:** The selected battery pack **MUST** incorporate a built-in Protection Circuit Module (PCM) providing:
  1. Overcharge protection voltage: $4.28\text{V} \pm 0.025\text{V}$.
  2. Overdischarge protection voltage: $2.75\text{V} \pm 0.05\text{V}$.
  3. Short-circuit / overcurrent cutoff threshold: $\le 2.5\text{A}$ with auto-recovery.

---

## 3. Commercial Protected Battery Candidates

### 3.1 Clarification on Speculative "08250" Cylindrical Designation
Prior project reports referenced a speculative "08250 120 mAh" cylindrical cell. Engineering audit confirms that:
- Standard lithium-ion cylindrical cells follow 5-digit diameter-by-length codes (e.g. 10440 = 10 mm diameter $\times$ 44 mm length; 14250 = 14 mm diameter $\times$ 25 mm length).
- "08250" (hypothetical 8 mm $\times$ 25 mm) does not correspond to any commercially standardized part number with verified datasheets.
- Standard micro cylindricals (10440 or 14250) exceed the available below-rail envelope inside a $13.5\text{ mm}$ ID pen barrel.
- Therefore, the **only commercially viable format that fits beneath the removable rail is an ultra-slim Lithium-Polymer (LiPo) pouch cell**.

### 3.2 Manufacturer Candidate Matrix (Below-Rail Envelope)
Maximum permissible below-rail cradle envelope:
$$\text{Length } L \le 35.0\text{ mm}, \quad \text{Width } W \le 10.5\text{ mm}, \quad \text{Thickness } T \le 4.5\text{ mm}$$

| Parameter | Candidate 1 (Recommended) | Candidate 2 (Ultra-Slim) | Candidate 3 (Compact) |
| :--- | :--- | :--- | :--- |
| **Manufacturer** | **EEMB Battery** | **EEMB Battery** | **Renata SA (Swatch Group)** |
| **Exact Model** | **`LP401030` (with PCM)** | **`LP301030` (with PCM)** | **`ICP401130` (with PCM)** |
| **Chemistry** | LiCoO2 / Graphite | LiCoO2 / Graphite | Lithium Polymer |
| **Nominal Voltage** | $3.70\text{ V}$ | $3.70\text{ V}$ | $3.70\text{ V}$ |
| **Nominal Capacity** | **$90\text{ mAh to } 100\text{ mAh}$** | **$60\text{ mAh to } 70\text{ mAh}$** | **$85\text{ mAh}$** |
| **Max Dimensions (w/ PCM)**| **$4.0\text{ mm (T)} \times 10.0\text{ mm (W)} \times 32.0\text{ mm (L)}$** | **$3.0\text{ mm (T)} \times 10.0\text{ mm (W)} \times 32.0\text{ mm (L)}$** | **$4.2\text{ mm (T)} \times 11.0\text{ mm (W)} \times 31.5\text{ mm (L)}$** |
| **Integrated PCM** | Built-in (4.28V / 2.75V / 2.5A) | Built-in (4.28V / 2.75V / 2.5A) | Built-in (4.28V / 2.75V / 2.0A) |
| **Max Continuous Discharge** | $1.0\text{ C}$ ($90\text{--}100\text{ mA}$) | $1.0\text{ C}$ ($60\text{--}70\text{ mA}$) | $1.0\text{ C}$ ($85\text{ mA}$) |
| **Recommended Charge Rate** | **$0.5\text{ C}$ ($45\text{--}50\text{ mA}$)** | **$0.5\text{ C}$ ($30\text{--}35\text{ mA}$)** | **$0.5\text{ C}$ ($42.5\text{ mA}$)** |
| **Absolute Max Charge Rate** | $1.0\text{ C}$ ($90\text{--}100\text{ mA}$) | $0.5\text{ C}$ ($35\text{ mA}$ max!) | $1.0\text{ C}$ ($85\text{ mA}$) |
| **Wire Leads** | 28 AWG, UL1007, $50\text{ mm}$ length | 28 AWG, UL1007, $50\text{ mm}$ length | Pre-attached wire leads |
| **Connector Termination** | JST SHR-02V-S-B | JST SHR-02V-S-B | JST SHR-02V-S-B |
| **Datasheet Source** | [EEMB LP401030 Datasheet](https://www.eemb.com) | [EEMB LP301030 Datasheet](https://www.eemb.com) | [Renata Batteries Industrial](https://www.renata.com) |

---

## 4. Critical Charge-Current Mismatch & Engineering Redesign

### 4.1 Safety Hazard of 100 mA Charge Setting on Small Cells
- The present hardware setting ($R_9 = 10.0\text{ k}\Omega \implies 100.0\text{ mA}$) was selected assuming a larger 120–150 mAh pack.
- If Candidate 2 (`LP301030`, 60–70 mAh) is installed, a $100\text{ mA}$ charge current produces an effective charge rate of **$1.4\text{C}\text{ to }1.67\text{C}$**.
- This severely violates the manufacturer's maximum specified charge current ($0.5\text{C} = 35\text{ mA}$), causing electrolyte gassing, pouch swelling, rapid cycle capacity loss, and severe fire risk inside a sealed pen barrel.
- Even for Candidate 1 (`LP401030`, 90–100 mAh), $100\text{ mA}$ operates at the absolute $1.0\text{C}$ maximum boundary.

### 4.2 Circuit Modification Recommendation
To achieve safe, cool-running operation and maximize battery longevity, **resistor $R_9$ should be redesigned in Phase 4**:

| Target Charge Current | Recommended $R_9$ Value | Effective Charge Rate (for 90 mAh LP401030) | Full Charge Time | Thermal Dissipation in U2 |
| :---: | :---: | :---: | :---: | :---: |
| **$50.0\text{ mA}$ (Recommended)** | **$20.0\text{ k}\Omega$ ($1\%$, 0402)** | **$0.55\text{ C}$ (Optimal)** | $\approx 2.2\text{ hours}$ | **$90\text{ mW}$** ($\Delta T \approx 20^\circ\text{C}$) |
| $66.7\text{ mA}$ | $15.0\text{ k}\Omega$ ($1\%$, 0402) | $0.74\text{ C}$ (Fast) | $\approx 1.7\text{ hours}$ | $120\text{ mW}$ ($\Delta T \approx 27^\circ\text{C}$) |
| $100.0\text{ mA}$ (Present) | $10.0\text{ k}\Omega$ ($1\%$, 0402) | $1.11\text{ C}$ (Aggressive / High Heat) | $\approx 1.2\text{ hours}$ | $180\text{ mW}$ ($\Delta T \approx 41^\circ\text{C}$) |

**Engineering Recommendation:** Update $R_9$ to $20.0\text{ k}\Omega$ to establish a standardized $50.0\text{ mA}$ charge current ($0.5\text{C}$ on 90–100 mAh cell).

---

## 5. Client Approval Gate Status

```
================================================================================
                    BATTERY SELECTION CLIENT APPROVAL GATE
================================================================================

 [ ] CLIENT APPROVAL PENDING: Formally select battery model and charging spec.

     Recommended Selection:
     - Pack Model: EEMB LP401030 with integrated PCM (90–100 mAh, 4.0x10.0x32.0 mm)
     - Termination: JST SHR-02V-S-B (Pin 1: VBAT Red, Pin 2: GND Black)
     - Charger Setting: Redesign R9 to 20.0 kΩ for 50.0 mA nominal charging

     STATUS: PRESERVED CLIENT BLOCKER — Formal client sign-off required.
================================================================================
```
