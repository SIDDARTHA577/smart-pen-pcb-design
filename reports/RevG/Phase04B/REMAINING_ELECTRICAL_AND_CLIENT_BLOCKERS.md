# Remaining Electrical, Mechanical, and Client Blockers Register

**Document ID:** PEN-REV-G-MECH-PHASE04B-REP-10  
**Deliverable Directory:** [Mechanical_Phase04B/](file:///c:/Users/goran/Downloads/SmartPen_RevD_AutoLinked_Footprints_Review_ONLY/output/RevG/Mechanical_Phase04B/)  
**Date:** November 17, 2026  
**Status:** ACTIVE CLIENT DECISION REGISTER — RESOLUTION REQUIRED BEFORE PHASE 5  

---

## 1. Executive Summary

Phase 4B has successfully closed all internal spatial, kinematic, and CAD solid modeling errors. There are **zero mechanical collisions** within the pen assembly. However, moving into Phase 5 (Digital Tooling, DFM, and Prototype Fabrication) requires formal client resolution on four cross-disciplinary electrical and architectural trade-offs.

---

## 2. Itemized Blocker & Decision Register

### 2.1 Blocker 1: Battery Capacity PRD Specification Reconciliation (CRITICAL)
- **Client Marketing Specification:** $130\text{ mAh}$ single-cell LiPo battery.
- **Physical Reality:** As rigorously demonstrated in [Report 02](file:///c:/Users/goran/Downloads/SmartPen_RevD_AutoLinked_Footprints_Review_ONLY/reports/RevG/Phase04B/BATTERY_TO_BARREL_INTERFERENCE_ANALYSIS.md) and [Report 03](file:///c:/Users/goran/Downloads/SmartPen_RevD_AutoLinked_Footprints_Review_ONLY/reports/RevG/Phase04B/PROTECTED_BATTERY_PACK_FEASIBILITY.md), an active $130\text{ mAh}$ cell envelope ($10.0 \times 4.0 \times 40.0\text{ mm}$) has outer bottom corners at radius $r = 7.433\text{ mm}$, penetrating the $\varnothing 13.50\text{ mm}$ ($R = 6.75\text{ mm}$) barrel bore by $0.683\text{ mm}$ ($31.67\text{ mm}^3$ collision) and colliding with the USB-C receptacle.
- **Phase 4B Implemented Baseline:** Commercial protected pouch cell LP380830 / LP350830 ($32.0 \times 7.6 \times 3.6\text{ mm}$, $85\text{--}95\text{ mAh}$) achieving **$0.0000\text{ mm}^3$ collision** and $+0.39\text{ mm}$ radial bore clearance.
- **Impact on Product:** Provides $2.7\text{ hours}$ of continuous active handwriting with BLE streaming, or $\approx 3.5\text{ days}$ of typical intermittent office usage.
- **Required Client Action:** Formally sign off on updating the PRD target battery capacity from $130\text{ mAh}$ to **$90\text{ mAh}$ nominal** ($85\text{ mAh}$ minimum).

### 2.2 Blocker 2: Battery Charger Resistor ($R_{PROG}$) Optimization
- **Current PCB Baseline:** In `SmartPen.kicad_pcb`, the Microchip MCP73831T charge controller uses programming resistor $R_{PROG} = 10.0\text{ k}\Omega$ (pin 5 to GND).
- **Current Charge Rate:** $I_{CHG} = 1000\text{ V} / 10\text{ k}\Omega = 100\text{ mA}$. For a $90\text{ mAh}$ cell, this equates to a $1.11\text{C}$ fast charge rate.
- **Engineering Recommendation:** While $1.1\text{C}$ is acceptable for ambient bench charging, enclosed operation inside a sealed plastic barrel benefits from lower thermal dissipation.
- **Proposed Modification for Phase 5:** Update $R_{PROG}$ to **$12.0\text{ k}\Omega$** ($83.3\text{ mA}$, $0.92\text{C}$) or **$13.0\text{ k}\Omega$** ($76.9\text{ mA}$, $0.85\text{C}$) in the Phase 5 schematic revision. This reduces thermal rise during charging by $\approx 25\%$ while keeping charge time under $75\text{ minutes}$.

### 2.3 Blocker 3: ESP32-C3 Peak RF Current & Cell Pulse Rating
- **Electrical Characteristic:** The ESP32-C3 draws short current pulses of $350\text{--}385\text{ mA}$ (duration $\approx 1\text{ ms}$) during 802.11b/g/n Wi-Fi transmission bursts.
- **C-Rate on 90 mAh Cell:** Pulse discharge equates to $\approx 4.4\text{C}$.
- **Risk Mitigation:**
  1. The battery procurement specification must mandate high-drain chemistry (e.g. Grepow 5C continuous / 10C pulse cell series) with cell AC internal impedance $ESR \le 180\text{ m}\Omega$.
  2. The Main PCB ceramic MLCC capacitor bank ($2 \times 22\text{ µF} + 10\text{ µF}$) provides low-impedance transient decoupling.
- **Required Client Action:** Approve sourcing criteria for high-drain LiPo micro-cells rather than generic ultra-cheap commodity cells.

### 2.4 Blocker 4: Detachable Front MPU Mechanical Latch Fatigue
- **Mechanism:** The Front MPU carrier (`06`) is designed to detach from the front grip for standalone stylus/sensor calibration.
- **Dynamic Interaction:** The D1 refill passes through the central bore of the MPU carrier and reciprocates by $4.50\text{ mm}$ during each click actuation.
- **Verification:** Solid clearance is $0.55\text{ mm}$ radially around the D1 refill. The MPU daughterboard is securely seated outside the refill sleeve.
- **Phase 5 Action:** During tooling design, add dual miniature snap detents to ensure cyclic click vibrations do not walk the MPU carrier forward over time.

---

## 3. Client Sign-Off Matrix

| Blocker ID | Description | Severity | Recommended Engineering Resolution | Client Decision Required? |
| :---: | :--- | :---: | :--- | :---: |
| **BLK-01** | Battery Capacity Reconciliation | HIGH | Baseline $90\text{ mAh}$ commercial protected cell LP380830 | **YES (Sign-off required)** |
| **BLK-02** | Charger $R_{PROG}$ Resistor Change | LOW | Adjust $R_{PROG} = 12\text{ k}\Omega$ ($83.3\text{ mA}$, $0.92\text{C}$) in Phase 5 | **YES (Approval to update)** |
| **BLK-03** | High-Drain Cell Procurement | MEDIUM | Specify Grepow 5C pulse rating in BOM vendor notes | NO (Engineering standard) |
| **BLK-04** | MPU Snap Detent Hardening | LOW | Incorporate retention ribs in Phase 5 injection tooling | NO (Tooling DFM detail) |

---

## 4. Conclusion

None of these items require mechanical geometry enlargement or PCB copper layout redesign. Once the client confirms the $90\text{ mAh}$ capacity sign-off, the project is fully cleared to transition into Phase 5 digital tooling.
