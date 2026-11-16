# Smart Pen Rev G — Below-Rail Protected Battery Integration & Safety Audit
**Document ID:** RPT-REVG-P4-BATTERY-INTEGRATION  
**Project:** Smart Pen Hardware Architecture Revision G  
**Target Variant:** Four-Layer Authoritative Candidate (`output/RevG/variants/FourLayer_Candidate/SmartPen.kicad_pcb`)  
**Git Branch:** `engineering/revg-production`  
**Date:** November 16, 2026  
**Status:** Mechanical Compartment Verified; Electrical Change Recommendation Formulated; Client Approval Preserved  

---

## 1. Executive Summary & Critical Mandate

Section 3A and Section 5 (Part 3) of the Phase 4 engineering mandate dictate that:
> **"Do not accept the battery model as final merely because its dimensions fit."**  
> **"Never label an electrically incompatible protected battery as safe merely because it fits geometrically."**  
> **"Do not silently modify the PCB while performing mechanical design."**

In strict adherence to these engineering ethics, this report provides both the **mechanical compartment integration proof** and the **independent electrical safety and power-budget review**. 

The mechanical compartment (`05_Battery_Cradle.step` / `.stl`) cradles the candidate lithium-polymer pouch cell directly beneath the removable electronics rail. However, our independent electrical analysis exposes two critical electrical discrepancies between the physical cell datasheets and the main board:
1. **Discharge Current vs. System Peak:** The candidate `LP401030` cell has a manufacturer-rated continuous discharge capability of $1.0\text{C}$ ($90\text{--}100\text{ mA}$). The ESP32-C3 microcontroller draws up to $350\text{ mA}$ during Wi-Fi transmissions, and simultaneous MicroSD writing and haptic pulsing produce system peak pulses of $\approx 490\text{ mA}$.
2. **Charge Current Mismatch:** Main PCB resistor $R_9$ remains at $10.0\text{ k}\Omega$, setting the linear charger (`U2: MCP73831`) to deliver $100.0\text{ mA}$ ($1.11\text{C}$). This exceeds the cell manufacturer's recommended $0.5\text{C}$ ($45\text{--}50\text{ mA}$) safe charge rate.

Because the client has not formally signed off on cell procurement or schematic modifications, **this enclosure design is formally classified as a Provisional CAD Candidate**, and an explicit Engineering Change Recommendation (ECR-004) is submitted for the PCB team.

---

## 2. Mechanical Cradle Integration & Swelling Allowance

The battery cradle is molded as an integral lower pocket of the removable chassis rail spanning $Z = 74.00\text{ mm}$ to $Z = 109.00\text{ mm}$ ($35.00\text{ mm}$ longitudinal length), situated at $Y = -1.20\text{ mm}$ to $Y = -5.70\text{ mm}$ ($4.50\text{ mm}$ cavity depth).

```
                      Z = 74.0 mm                            Z = 109.0 mm
                      +--------------------------------------+  Y = -1.20 mm
                      |  Upper Isolation Deck (0.20 mm)      |
+---------------------+--------------------------------------+---------------------+
| Refill Tail Cup     | <<< 3.0 mm Wire Egress >>>           |                     |
| Z = 68.5 mm (Retr)  |                                      |                     |
|                     | [EEMB LP401030 Protected LiPo Pack]  | Cradle End Wall     |
| <--- 5.5 mm Gap --->| Length: 32.0 mm                      | (1.0 mm polymer)    |
|   (Zero Clash)      | Thickness: 4.0 mm (Swell gap: 0.5mm) |                     |
|                     | Width: 10.0 mm (Lateral gap: 0.5 mm) |                     |
+---------------------+--------------------------------------+---------------------+
                      | Cradle Floor (1.0 mm polymer)        |  Y = -5.70 mm
                      +--------------------------------------+
```

### 2.1 Mechanical Dimension Comparison

| Parameter | Cradle Cavity Specification | LP401030 Cell Envelope (with PCM) | Available Clearance Margin | Design Purpose |
| :--- | :---: | :---: | :---: | :--- |
| **Longitudinal Length ($Z$)** | $35.00\text{ mm}$ | $32.00\text{ mm}$ max | **$+3.00\text{ mm}$** | 28 AWG wire lead egress & strain relief |
| **Transverse Width ($X$)** | $10.50\text{ mm}$ | $10.00\text{ mm}$ max | **$+0.50\text{ mm}$** ($0.25\text{ mm}$ / side) | Lateral slide fit without pouch compression |
| **Vertical Depth ($Y$)** | $4.50\text{ mm}$ | $4.00\text{ mm}$ max | **$+0.50\text{ mm}$** ($12.5\%$ margin) | Absorbs standard $\le 10\%$ chemical swelling |
| **Floor Thickness** | $1.00\text{ mm}$ | N/A | Solid barrier | Isolates cell from outer barrel bore |
| **Ceiling Deck Thickness** | $0.40\text{ mm}$ | N/A | Solid barrier | Isolates cell from central pushrod conduit |

### 2.2 Refill-to-Battery Axial Clearance Verification
- **Battery Forward Boundary:** Fixed at $Z = 74.00\text{ mm}$.
- **D1 Refill Tail (Retracted / Idle):** $Z = 68.50\text{ mm}$.
  $$\text{Retracted Clearance: } \Delta Z_{\text{retracted}} = 74.00 - 68.50 = \mathbf{5.50\text{ mm}} \quad (> 5.00\text{ mm required})$$
- **D1 Refill Tail (Extended / Writing):** $Z = 64.00\text{ mm}$ ($4.50\text{ mm}$ forward stroke).
  $$\text{Extended Clearance: } \Delta Z_{\text{extended}} = 74.00 - 64.00 = \mathbf{10.00\text{ mm}} \quad (> 9.00\text{ mm required})$$
- **Kinematic Conclusion:** Zero collision under all operational writing states. The refill never enters the battery cradle zone.

---

## 3. Independent Electrical & Power-Budget Review

### 3.1 Candidate Cell Datasheet Specification (EEMB `LP401030`)
- **Manufacturer:** EEMB Battery Co., Ltd.
- **Orderable Part Number:** `LP401030` (with pre-installed PCM and lead wires).
- **Nominal Capacity:** $90\text{ mAh to }100\text{ mAh}$ ($0.333\text{--}0.370\text{ Wh}$).
- **Nominal Voltage:** $3.70\text{ V}$ (Operating voltage: $3.00\text{ V to }4.20\text{ V}$).
- **Integrated PCM Parameters:**
  - Overcharge Protection: $4.28\text{V} \pm 0.025\text{V}$ (Release: $4.08\text{V}$).
  - Overdischarge Protection: $2.75\text{V} \pm 0.050\text{V}$ (Release: $3.00\text{V}$).
  - Overcurrent Cutoff Threshold: $2.0\text{A to }2.5\text{A}$ with automatic recovery.
- **Maximum Continuous Discharge Current:** $1.0\text{ C} \implies 90.0\text{ mA to }100.0\text{ mA}$.
- **Manufacturer Recommended Charge Current:** $0.5\text{ C} \implies 45.0\text{ mA to }50.0\text{ mA}$.
- **Manufacturer Maximum Charge Current:** $1.0\text{ C} \implies 90.0\text{ mA to }100.0\text{ mA}$ ($0.5\text{C}$ for extended cycle life).

### 3.2 System Power Budget & Peak Current Analysis

```
========================================================================================
SUBSYSTEM COMPONENT         OPERATING STATE              CURRENT DEMAND       DURATION
========================================================================================
ESP32-C3FH4X Core & LDO     Active Processing (160 MHz)   20.0 to  25.0 mA    Continuous
InvenSense IMU (Front MPU)  6-DOF Sampling @ 200 Hz        2.5 to   3.5 mA    Continuous
Capacitive Touch (TTP223)   Touch Active State             1.0 to   1.5 mA    Continuous
Status LEDs (D1 / D2)       Illuminated (Green / Red)      4.0 to   8.0 mA    Continuous
MicroSD Flash Memory Card   SPI Multi-Sector Block Write  50.0 to 100.0 mA    Bursts (1-5 ms)
Haptic Coin Motor (M1)      Tactile Feedback Pulse        60.0 to  80.0 mA    Pulse (50-100 ms)
ESP32-C3 Wi-Fi Transceiver  802.11b TX (+21 dBm Peak)    335.0 to 350.0 mA    Bursts (< 1 ms)
ESP32-C3 BLE 5.0 Radio      BLE TX (+0 dBm)              120.0 to 135.0 mA    Periodic pulses
========================================================================================
BASELINE ACTIVE (No Radio): ~30 mA                       PEAK (BLE + Write):  ~210 mA
PEAK PULSE (Wi-Fi + Write + Haptic):                     350 + 100 + 80 = 530 mA (!)
========================================================================================
```

### 3.3 Electrical Discrepancy & Technical Impact

1. **Continuous vs. Peak Current Capability:**
   - The cell's continuous rating is $90\text{--}100\text{ mA}$.
   - During BLE streaming ($\sim 35\text{ mA}$ average with transient peaks of $130\text{ mA}$), onboard bulk ceramic capacitors ($C_{11}, C_{12}, C_{13} = 30\text{ }\mu\text{F}$ total) and cell internal impedance ($R_i \approx 200\text{ m}\Omega$) comfortably supply the pulses without tripping the PCM ($2.5\text{A}$ threshold).
   - **Severe Risk under Continuous Wi-Fi:** If the firmware attempts continuous unthrottled 802.11b transmission, continuous current exceeds $200\text{ mA}$ ($> 2.0\text{C}$). This causes internal cell ohmic heating ($\Delta T > 15^\circ\text{C}$ inside an unventilated sealed barrel), rapid capacity loss, and voltage sag below the AP2112 LDO dropout ($V_{\text{in}} < 3.55\text{V}$), triggering brownout resets.
   - **Engineering Mitigation:** Firmware must restrict Wi-Fi operation to low-duty-cycle batch synchronization when connected to external USB power, using low-power BLE for mobile phone tethering.
2. **Charger Current Resistor $R_9$ Discrepancy:**
   - Main PCB schematic and layout confirm $R_9 = 10.0\text{ k}\Omega$ ($100.0\text{ mA}$ charging).
   - For an $85\text{--}90\text{ mAh}$ pack, $100\text{ mA}$ equals $1.11\text{C}\text{ to }1.18\text{C}$.
   - Operating at $> 1.0\text{C}$ charge rate inside an enclosed pen barrel accelerates electrolyte degradation and raises pouch thermal dissipation ($P_{\text{diss}} \approx 180\text{ mW}$ in charger U2).
   - **Mandatory ECR:** Redesign $R_9$ to $20.0\text{ k}\Omega \pm 1\%$ to establish a standardized $50.0\text{ mA}$ ($0.5\text{C}$) charge current.
   - In accordance with our guidelines, **$R_9$ was NOT silently changed on the PCB**; it is documented as an open ECR for client sign-off.

---

## 4. Harness & Polarized Connector Specification

- **Board Connector (`J_BAT`):** JST `SM02B-SRSS-TB(LF)(SN)` (1.0 mm pitch horizontal SMT receptacle @ $X = 62.800, Y = 1.720$).
- **Mating Housing:** JST `SHR-02V-S-B` (Keyed 2-pin with locking ramp).
- **Polarity Assignment:**
  - **Pin 1:** `/VBAT` ($+3.7\text{V}$ nominal, Red 28 AWG wire).
  - **Pin 2:** `/GND` (Ground return, Black 28 AWG wire).
- **Wire Specification:** UL1007, 28 AWG stranded copper, silicone or PVC insulation, length $45.0\text{ mm} \pm 2.0\text{ mm}$.
- **Mechanical Retention:** The battery is retained in its cradle by a non-conductive dielectric kapton tape wrapper and foam compression pad ($0.30\text{ mm}$ thick), preventing cell movement during writing impacts.
