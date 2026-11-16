# Smart Pen Rev G — External 2.4 GHz Antenna Integration
**Document ID:** RPT-REVG-P3C-ANT-INTEGRATION  
**Project:** Smart Pen Hardware Architecture Revision G  
**Variant:** Four-Layer Evaluation Candidate (`output/RevG/variants/FourLayer_Candidate/SmartPen.kicad_pcb`)  
**Git Branch:** `engineering/revg-production`  
**Base Commit:** `f76aab08831da7bf26516d4a1a39215d754e0d73`  
**Date:** November 16, 2026  
**Status:** Commercial Antenna Trade Study Complete; Phase 4 Mechanical Integration Envelope Established  

---

## 1. Executive Summary

This report establishes the external 2.4 GHz antenna architecture for the Smart Pen Revision G hardware system. Direct physical inspection of the authoritative four-layer PCB candidate confirms that microcontroller `U1` (Espressif `ESP32-C3FH4X`) feeds an onboard discrete matching network (L1, L2, C8, C9) terminating at `J_RF` (Hirose `U.FL-R-SMT-1(10)` surface-mount coaxial receptacle). **There is NO onboard printed trace antenna or ceramic chip antenna.**

To enable wireless Wi-Fi (802.11b/g/n) and Bluetooth Low Energy (BLE 5.0) operation, an external miniature cabled antenna assembly must be integrated into the mechanical assembly. This report evaluates three real, commercially available manufacturer parts with verified datasheets, specifies enclosure material requirements (metal vs plastic), and creates the definitive mechanical integration envelope for Phase 4 CAD modeling.

---

## 2. Commercial Antenna Trade Study

All evaluated candidates are commercially available off-the-shelf (COTS) parts terminating in micro-coaxial cable with an I-PEX MHF / U.FL-compatible plug that mates directly with PCB connector `J_RF`.

### 2.1 Candidate Comparison Matrix

| Parameter | Candidate 1 (Recommended) | Candidate 2 | Candidate 3 |
| :--- | :--- | :--- | :--- |
| **Manufacturer** | **Molex LLC** | **Taoglas Limited** | **TE Connectivity / Linx** |
| **Exact MPN** | **`146153-0050`** | **`FXP73.07.0100A`** | **`ANT-2.4-FPC-SAH50UF`** |
| **Antenna Type** | Balanced Flexible Dipole | Flexible PCB Monopole | Ultra-Miniature Adhesive FPC |
| **Frequency Bands** | $2.4\text{ GHz}$ & $5\text{ GHz}$ (Dual-Band) | $2.4\text{ GHz}$ (Wi-Fi / BLE) | $2.4\text{ GHz}$ (ISM / BLE) |
| **Radiator Dimensions** | **$34.90 \times 9.00 \times 0.10\text{ mm}$** | **$47.00 \times 7.00 \times 0.10\text{ mm}$** | **$12.00 \times 8.00 \times 0.10\text{ mm}$** |
| **Cable Type** | $\varnothing 1.13\text{ mm}$ micro-coaxial | $\varnothing 1.13\text{ mm}$ mini-coaxial | $\varnothing 1.13\text{ mm}$ micro-coaxial |
| **Cable Length** | $50.0\text{ mm} \pm 3.0\text{ mm}$ | $100.0\text{ mm} \pm 3.0\text{ mm}$ | $50.0\text{ mm} \pm 3.0\text{ mm}$ |
| **Connector Type** | U.FL / I-PEX MHF1 plug | I-PEX MHF1 plug | U.FL / MHF1 plug |
| **Minimum Cable Bend Radius**| $4.00\text{ mm}$ | $4.00\text{ mm}$ | $4.00\text{ mm}$ |
| **Mounting Method** | 3M 467MP peel-and-stick adhesive | 3M 467 peel-and-stick adhesive | 3M adhesive backing |
| **Ground Independence**| **Balanced (Ground-Independent)** | Ground-Dependent | Ground-Dependent |
| **Peak Gain (Free Space)**| $+2.2\text{ dBi}$ | $+2.5\text{ dBi}$ | $+1.2\text{ dBi}$ |
| **Datasheet Source** | [Molex Document 1461530050-SD](https://www.molex.com) | [Taoglas Datasheet FXP73](https://www.taoglas.com) | [TE Datasheet ANT-2.4-FPC-SAH](https://www.te.com) |

---

## 3. Recommended Antenna Selection & Rationale

### Primary Recommendation: **Molex `146153-0050`**

1. **Balanced Dipole Architecture:** Unlike conventional monopoles, the Molex 146153 is an electrically balanced dipole. It operates independently of the main PCB ground plane size, ensuring consistent resonance even in the compact, narrow confines of a pen barrel.
2. **Optimal Cable Length ($50\text{ mm}$):** Connector `J_RF` is located at $X = 54.850\text{ mm}$. A $50\text{ mm}$ cable reaches comfortably into the pen nose cone or forward barrel section without excess coiled cable cluttering the interior mechanism.
3. **Cylindrical Conformity:** The radiator substrate is an ultra-thin ($0.10\text{ mm}$) polyimide flex film. The internal barrel diameter is $13.50\text{ mm}$ (internal perimeter $C = \pi \times 13.5 \approx 42.4\text{ mm}$). The $9.0\text{ mm}$ radiator width curves naturally along the inner circumference of the barrel with zero mechanical stress.

---

## 4. Pen Enclosure Material & RF Shielding Constraints

The choice of pen barrel material completely dictates wireless functionality:

```
[SCENARIO A: ALL-PLASTIC BARREL]          [SCENARIO B: METALLIC BARREL + RF WINDOW]
+-----------------------------------+     +-------------+===============+-------------+
| Plastic Enclosure (Polycarbonate) |     | Metal Body  |   RF Window   | Metal Body  |
| (100% RF Transparent)             |     | (Faraday)   |  (Polycarb)   | (Faraday)   |
|   (( Antenna Radiates 360° ))     |     | Shielded    | (( Radiates ))| Shielded    |
+-----------------------------------+     +-------------+===============+-------------+
```

### Scenario A: Dielectric / Plastic Enclosure (Recommended)
- **Approved Materials:** Polycarbonate (PC), ABS, PEEK, Delrin / POM, Glass-filled Nylon.
- **RF Impact:** Complete $360^\circ$ RF transparency. Negligible attenuation ($< 0.5\text{ dB}$).
- **Antenna Mounting:** Radiator adhered directly to the inside cylindrical surface of the main barrel or the top face of the internal removable rail.

### Scenario B: Metallic Enclosure (Aluminum / Brass / Steel)
- **Critical RF Blocker:** A continuous metallic pen barrel forms an impenetrable **Faraday cage**. 2.4 GHz electromagnetic radiation is attenuated by $>30\text{ dB}$, resulting in complete loss of Wi-Fi and Bluetooth connectivity.
- **Mandatory Requirement for Metal Barrel:** If an aluminum alloy exterior is selected by the industrial design team, the enclosure **MUST** incorporate a non-metallic RF-transparent section:
  1. **Option 1 (RF Nose Cone / Front Grip):** Fabricate the front grip section ($X = 0\text{ to }35\text{ mm}$) from non-conductive plastic, mounting the antenna forward of the metal barrel joint.
  2. **Option 2 (Circumferential RF Window):** Machine a minimum $40.0\text{ mm}$ continuous axial slot or molded plastic dielectric ring in the pen body.

---

## 5. Phase 4 Mechanical Integration Envelope

The following physical envelope constraints must be implemented in Phase 4 3D CAD modeling:

```
          J_RF Receptacle                       Antenna Mounting Zone
           (X = 54.85 mm)                       (X = 15.0 to 45.0 mm)
                 |                                      |
PCB Top (F.Cu) --[J_RF]---------------------------------+========================+
                   |                                    | 34.9 x 9.0 mm Flex FPC |
                   \===[ 50 mm Micro-Coax Cable (Ø1.13 mm) ]=====================+
                        - Min Bend Radius: R >= 4.0 mm
                        - Routing Corridor: Lateral gap between PCB rail & barrel
                        - Clearance to Ink Refill Pushrod: >= 2.0 mm
```

1. **Connector Mating Height:**
   - `J_RF` receptacle height: $1.25\text{ mm}$.
   - Mated U.FL plug height: $2.00\text{ mm}$ max above PCB top surface.
   - Total vertical envelope above PCB: $\ge 2.50\text{ mm}$ clear clearance required.
2. **Coaxial Cable Routing Channel:**
   - Cable diameter: $\varnothing 1.13\text{ mm}$.
   - Minimum static bend radius: $4.00\text{ mm}$.
   - Cable must route along the lateral perimeter of the internal removable rail, avoiding any pinch points with the ink refill clicker spring or pushrod corridor.
3. **Antenna Clearances:**
   - Clearance to metallic components (ink refill brass body, springs, battery casing): $\ge 3.00\text{ mm}$ dielectric separation required to prevent detuning.

---

## 6. Regulatory & Testing Disclaimer

- **Deliverable Scope:** This project deliverable encompasses **DIGITAL DESIGN FILES ONLY**.
- **No Physical RF Range Guarantee:** Wireless communication range, total radiated power (TRP), and total isotropic sensitivity (TIS) depend entirely on the final enclosure tooling, dielectric constants, and antenna placement.
- **Certification Mandate:** Physical FCC Part 15 / CE RED regulatory compliance testing and antenna passive chamber characterization must be conducted on assembled physical prototypes during Phase 5.
