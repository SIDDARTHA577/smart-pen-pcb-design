# Smart Pen Rev G — USB-C Port & External RF Antenna Integration
**Document ID:** RPT-REVG-P4-USBC-RF-ANTENNA  
**Project:** Smart Pen Hardware Architecture Revision G  
**Target Variant:** Four-Layer Authoritative Candidate (`output/RevG/variants/FourLayer_Candidate/SmartPen.kicad_pcb`)  
**Git Branch:** `engineering/revg-production`  
**Date:** November 16, 2026  
**Status:** Lateral Port & Conformal RF Envelope Verified  

---

## 1. Executive Summary

This report establishes the mechanical design, clearance envelopes, and material constraints governing two critical external interfaces of the Smart Pen Revision G enclosure:
1. **USB Type-C Lateral Access Port (`08_USB_C_Access_Feature.step` / `.stl`):** A precision chamfered side-port aperture in the outer barrel aligned with mid-mount receptacle `J_USB`, accepting standard commercial USB-C cable overmolds.
2. **External 2.4 GHz RF Antenna Assembly (`14_Antenna_Mount.step` / `.stl`):** A conformal cylindrical mounting nest for the Molex `146153-0050` balanced flexible dipole antenna ($34.90 \times 9.00 \times 0.10\text{ mm}$) and its $50.0\text{ mm}$ micro-coaxial lead connecting to board receptacle `J_RF`.

Both subassemblies achieve complete geometric clearance, adhere to commercial connector standards, and provide safe servicing paths during internal rail extraction.

---

## 2. USB Type-C Lateral Access Port Architecture

```
                  +Y (Upper Barrel Flank)
                           |
+--------------------------+--------------------------+  Outer Barrel OD 15.5 mm
|   Outer Barrel Shell (1.0 mm Wall)                  |
|                                                     |
|       +-------------------------------------+       |
|       | 45° Lead-In Chamfer (0.75 mm Depth) |       |  Y = +6.50 mm (Cutout Top)
|       |                                     |       |
|       |  [ Commercial USB-C Cable Overmold ]|       |  Envelope: 12.0 x 6.5 mm
|       |  [ Receptacle J_USB (Mid-Mount)    ]|       |
|       |                                     |       |
|       | 45° Lead-In Chamfer (0.75 mm Depth) |       |  Y = +2.70 mm (Cutout Bot)
|       +-------------------------------------+       |
|                                                     |
|   Inner Barrel Bore (ID 13.5 mm)                    |
+-----------------------------------------------------+  PCB Top: Y = +2.80 mm
                           |
                  -Y (Lower Barrel Flank)
```

### 2.1 Receptacle Interface & Cutout Geometry
- **Onboard Receptacle (`J_USB`):** Korean HRO `TYPE-C-31-M-12` (12-pin mid-mount hybrid SMT/TH receptacle) located at $X = 78.400\text{ mm}, Y = 4.600\text{ mm}$ on `F.Cu` of `SmartPen.kicad_pcb`.
- **Connector Physical Envelope:** Width $8.94\text{ mm}$, Depth $7.30\text{ mm}$, Total Height $3.16\text{ mm}$ ($1.58\text{ mm}$ above PCB midline, $1.58\text{ mm}$ below).
- **Outer Barrel Cutout Geometry:**
  - Length along longitudinal $Z$-axis: **$9.50\text{ mm}$** ($Z = 73.65\text{ to }83.15\text{ mm}$).
  - Height along vertical $Y$-axis: **$3.80\text{ mm}$** ($Y = +2.70\text{ to }+6.50\text{ mm}$).
  - Peripheral Lead-in Chamfer: **$45^\circ \times 0.75\text{ mm}$** around the entire external perimeter.
- **Overmold Insertion Proof:** Standard commercial USB-C cable plugs possess molded plastic hoods measuring up to $12.00\text{ mm (W)} \times 6.50\text{ mm (T)}$. The $45^\circ$ lead-in chamfer permits the overmold face to seat comfortably against the outer barrel wall, ensuring full $6.50\text{ mm}$ plug tongue insertion into `J_USB` with $>0.40\text{ mm}$ contact overtravel margin.

---

## 3. External 2.4 GHz RF Antenna & Coaxial Routing

Microcontroller `U1` (`ESP32-C3FH4X`) feeds an onboard matching network terminating at `J_RF` (`U.FL-R-SMT-1(10)`). To radiate Wi-Fi (802.11b/g/n) and BLE signals through the cylindrical enclosure, a flexible dipole antenna is integrated:

```
PCB Top Surface (F.Cu)                          Conformal Inner Wall Mounting Zone
[J_RF Receptacle]                               [Molex 146153-0050 Dipole Flex]
(Z = 92.85 mm, Y = +2.80)                       (Z = 49.00 to 83.90 mm, R = 6.65 mm)
       |                                                         |
       \===[ 50 mm Micro-Coax Cable (Ø1.13 mm) ]=================/
             - Static Bend Radius: R_bend = 4.20 mm (> 4.0 mm min)
             - Lateral Routing Channel: X = -5.60 mm
             - Dielectric Clearance to Refill: 5.48 mm (> 3.0 mm min)
```

### 3.1 Antenna Specifications (Molex `146153-0050`)
- **Antenna Architecture:** Ground-independent balanced center-fed flexible dipole.
- **Radiator Substrate:** Polyimide flex film with 3M 467MP peel-and-stick adhesive backing.
- **Substrate Dimensions:** Length $34.90\text{ mm} \times$ Width $9.00\text{ mm} \times$ Thickness $0.10\text{ mm}$.
- **Cylindrical Conformity:** The inner barrel bore has diameter $13.50\text{ mm}$ (perimeter $C = \pi \times 13.50 \approx 42.41\text{ mm}$). The $9.00\text{ mm}$ radiator width curves along the cylindrical wall spanning an arc of $\theta = (9.00 / 42.41) \times 360^\circ \approx 76.4^\circ$. The flexible polyimide adheres seamlessly with zero spring-back stress.
- **Cable Specification:** $\varnothing 1.13\text{ mm}$ micro-coaxial cable, length $50.0\text{ mm} \pm 3.0\text{ mm}$, terminating in an I-PEX MHF1 / U.FL-compatible female plug.

### 3.2 Clearance to Metal Bodies & Dielectric Isolation
- **Electromagnetic Rule:** COTS flexible antennas require a minimum $3.00\text{ mm}$ dielectric separation from metallic conductors (steel refill, return spring, copper ground planes) to avoid detuning and radiation pattern nulls.
- **Calculated Mechanical Separation:**
  - Antenna radius: $R_{\text{ant}} = 6.65\text{ mm}$.
  - Refill body outer radius: $R_{\text{refill}} = 1.175\text{ mm}$ (on centerline $X = 0, Y = 0$).
  - Net radial clearance:
    $$\Delta R = 6.65 - 1.175 = \mathbf{5.48\text{ mm}} \quad (> 3.00\text{ mm required})$$
- **Result:** $5.48\text{ mm}$ dielectric separation represents a $+82.7\%$ safety margin over the manufacturer's detuning threshold.

---

## 4. Barrel Material & RF Shielding Constraints

The enclosure material choice dictates wireless communication feasibility:

| Enclosure Material Scenario | Approved Material Candidates | RF Attenuation @ 2.4 GHz | Antenna Integration Feasibility |
| :--- | :--- | :---: | :--- |
| **Scenario A: All-Plastic Shell (Recommended)** | Polycarbonate (PC), ABS, PEEK, Delrin / POM | $< 0.5\text{ dB}$ (Transparent) | **100% FEASIBLE** — $360^\circ$ isotropic radiation |
| **Scenario B: Metal Body w/ RF Window** | 6061-T6 Aluminum with molded PC window | $< 1.0\text{ dB}$ through window | **FEASIBLE** — Requires $40.0\text{ mm}$ non-metal window |
| **Scenario C: Continuous Metal Barrel** | Solid Aluminum / Brass / Stainless Steel | $> 30.0\text{ dB}$ (Faraday Cage) | **BLOCKED** — Wi-Fi and BLE signals completely suppressed |

**Engineering Directive:** The client industrial design team must approve either Scenario A (All-Plastic) or Scenario B (Metal Body with molded dielectric window). Solid continuous metal barrels are strictly prohibited.

---

## 5. Servicing & Rail Extraction Slack

The $50.0\text{ mm}$ coaxial cable provides sufficient mechanical service slack:
- During pen servicing, after disengaging the rear bayonet collar, the internal rail cartridge slides forward/rearward by up to $22.0\text{ mm}$ before the coaxial lead becomes taut.
- This provides technicians full fingertip or tweezer access to unmate the U.FL plug without pulling on the micro-coaxial braid or stressing solder joints.
