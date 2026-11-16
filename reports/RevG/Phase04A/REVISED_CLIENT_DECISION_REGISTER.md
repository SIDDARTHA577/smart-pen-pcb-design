# SMART PEN REV G — REVISED CLIENT DECISION REGISTER
## Formal Ledger of Open Electrical, Mechanical, and Component Trade-Offs

**Document ID:** RPT-SMARTPEN-REVG-PHASE04A-DECISION-REGISTER  
**Date:** November 16, 2026  
**Status:** **ACTIVE — ACTION REQUIRED BEFORE PHASE 5 ENTRY**

---

## 1. PURPOSE

In strict adherence to **Section 14 (Electrical and Client Approval Boundaries)**, mechanical CAD geometry has been coordinated using explicitly documented provisional envelopes. This register lists the critical unresolved items that require formal client sign-off before manufacturing release or tooling fabrication can proceed.

---

## 2. DECISION MATRIX & OPEN ITEMS

### Item 1: Protected Battery Pack Selection & Peak Current Capability
- **Current Assumption:** LP401030 lithium-ion pouch cell ($32.0\text{ mm} \times 10.0\text{ mm} \times 4.0\text{ mm}$, nominal $130\text{ mAh}$).
- **The Issue:**
  1. The ESP32-C3 microcontroller draws peak pulse currents of $350\text{ to }400\text{ mA}$ during Wi-Fi 802.11b/g/n transmission bursts.
  2. For a $130\text{ mAh}$ cell, $400\text{ mA}$ corresponds to a $\approx 3.1\text{C}$ discharge rate.
  3. Generic unprotected cells often experience severe voltage sag below the $3.0\text{V}$ LDO brownout threshold under this load.
  4. An integrated Protection Circuit Module (PCM) with a low-resistance dual-MOSFET (e.g., $R_{\text{DS(on)}} \le 35\text{ m}\Omega$) is mandatory.
- **Client Action Required:** Select and approve a qualified commercial protected pack vendor (e.g., EEMB, JHY, or Grepow) with certified pulse discharge rating $\ge 3\text{C}$ and maximum swollen thickness $\le 4.20\text{ mm}$.
- **Tooling Impact:** Cradle cavity floor and length can be adjusted if an alternate cylindrical (10440) or custom-profile cell is selected.

### Item 2: Battery Charge Current & Resistor R9 Modification
- **Current Assumption:** On-board linear Li-ion charger (TP4054 / MCP73831) programmed with current-setting resistor R9.
- **The Issue:**
  1. Standard charging convention recommends $0.5\text{C}$ charge rate ($65\text{ mA}$ for $130\text{ mAh}$) to ensure cycle life and prevent thermal accumulation inside the sealed barrel.
  2. If R9 is set for $200\text{ mA}$ or $500\text{ mA}$, charging will exceed $1.5\text{C}$ to $3.8\text{C}$, posing thermal runaway hazards.
- **Client Action Required:** Formally approve the target charging current ($65\text{ mA}$ to $100\text{ mA}$) and confirm the required value for R9.

### Item 3: Outer Barrel Enclosure Material & RF Transparency
- **Current Assumption:** Non-conductive engineering plastic or SLA/SLS resin ($\epsilon_r \approx 3.0$).
- **The Issue:**
  1. If the client desires a premium anodized aluminum (6061-T6) barrel, the internal Molex 146153 antenna ($Z = 49.0$ to $83.9\text{ mm}$) will be completely Faraday-shielded, resulting in zero Wi-Fi/BLE range.
  2. A metal barrel requires either an external dielectric RF window (polycarbonate insert) or switching to an external antenna.
- **Client Action Required:** Select final barrel material:
  - *Option A (Recommended for simplicity):* Full high-grade polymer barrel (polycarbonate or ABS/PC blend).
  - *Option B:* Anodized aluminum barrel with co-molded or bonded polycarbonate RF window ring.

### Item 4: MicroSD Card Servicing Arrangement
- **Current Architecture:** Rear bayonet quick-release cap provides direct push-push access to the MicroSD socket without removing the main electronics rail.
- **Alternative:** Fully sealed barrel requiring full rail extraction for SD card access.
- **Client Action Required:** Confirm whether rear bayonet access meets user experience requirements.

### Item 5: Tactile Button Travel & Force Preference
- **Current Architecture:** Dual rocker actuator with $0.80\text{ mm}$ plunger travel to activate $1.6\text{ N}$ tactile switches SW1 (ERASE) and SW2 (MODE).
- **Client Action Required:** Approve the $0.80\text{ mm}$ travel distance and button paddle ergonomics.
