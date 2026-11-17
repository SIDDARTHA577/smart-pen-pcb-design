# SMART PEN REV G — 4-LAYER MAIN BOARD STACKUP SPECIFICATION

**Document ID:** SRG-MFG-STK-001  
**Revision:** 1.0 (Rev G ECR-ELEC-REVG-001 Production Baseline)  
**Date:** November 17, 2026  
**Target Fabrication Vendor:** JLCPCB / PCBWay / Standard Quick-Turn High-Reliability Fab  

---

## 1. LAYER STRUCTURE & DIELECTRIC BUILD-UP

| Layer # | Layer Name | Layer Function | Material | Thickness (mm) | Copper Weight | Dielectric Constant ($E_r$) |
| :---: | :--- | :--- | :--- | :---: | :---: | :---: |
| -- | Top Solder Mask | Protective Finish | Taiyo Matte Black PSR-4000 | $0.020\text{ mm}$ | -- | 3.8 |
| **L1** | **F.Cu (Top)** | High-Speed RF & Signals | Electrodeposited Copper | **$0.035\text{ mm}$** | **$1.0\text{ oz}$** | -- |
| -- | Dielectric 1-2 | Prepreg Insulation | 7628 Prepreg ($1\times 7628$) | $0.2104\text{ mm}$ | -- | 4.50 @ 1 GHz |
| **L2** | **In1.Cu (Internal 1)** | Unbroken Ground Return Plane | Copper Foil (Power plane) | **$0.0175\text{ mm}$** | **$0.5\text{ oz}$** | -- |
| -- | Core Dielectric | Structural Core | FR-4 Standard TG150 | $1.0650\text{ mm}$ | -- | 4.60 @ 1 GHz |
| **L3** | **In2.Cu (Internal 2)** | 3.3V Power Distribution Plane | Copper Foil (Power plane) | **$0.0175\text{ mm}$** | **$0.5\text{ oz}$** | -- |
| -- | Dielectric 3-4 | Prepreg Insulation | 7628 Prepreg ($1\times 7628$) | $0.2104\text{ mm}$ | -- | 4.50 @ 1 GHz |
| **L4** | **B.Cu (Bottom)** | Peripheral & Escape Signals | Electrodeposited Copper | **$0.035\text{ mm}$** | **$1.0\text{ oz}$** | -- |
| -- | Bottom Solder Mask | Protective Finish | Taiyo Matte Black PSR-4000 | $0.020\text{ mm}$ | -- | 3.8 |

**Total Nominal Finished Board Thickness:** **$1.60\text{ mm} \pm 10\%$ ($1.591\text{ mm}$ calculated)**.

---

## 2. CONTROLLED IMPEDANCE TRANSMISSION LINE DESIGN

- **50 Ω Single-Ended Coplanar RF Trace (ANT Feed):**
  - Signal Layer: `F.Cu`
  - Reference Ground: `In1.Cu` (Solid uninterrupted copper)
  - Trace Width ($W$): $0.380\text{ mm}$ ($15.0\text{ mil}$)
  - Ground Coplanar Clearance ($S$): $0.254\text{ mm}$ ($10.0\text{ mil}$)
  - Substrate Height ($H$): $0.2104\text{ mm}$ ($8.28\text{ mil}$)
  - Effective Permittivity ($\varepsilon_r$): $4.50$
  - Resulting Characteristic Impedance: **$50.2\ \Omega \pm 5\%$ (100% compliant with Molex 146153 & ESP32-C3 RF specification)**.

---

## 3. DAUGHTERBOARD 2-LAYER STACKUPS (0.80 mm THICKNESS)

All three daughterboards (Front MPU, MicroSD Carrier, Touch Sensor) utilize a matching high-density 2-layer build:
- Finished Thickness: **$0.80\text{ mm} \pm 0.08\text{ mm}$**
- Copper Weight: **$1.0\text{ oz}$ ($0.035\text{ mm}$)** on Top and Bottom
- Core Material: FR-4 TG150 ($0.710\text{ mm}$)
- Solder Mask: Matte Black
- Surface Finish: ENIG (Electroless Nickel Immersion Gold)
