# Smart Pen Rev G — Final Mechanical Preflight & Spatial Integration Audit
**Document ID:** QA-REVG-P3C-006  
**Project:** Smart Pen Hardware Architecture Revision G  
**Variant:** Four-Layer Evaluation Candidate (`output/RevG/variants/FourLayer_Candidate/SmartPen.kicad_pcb`)  
**Date:** November 16, 2026  
**Status:** Preflight Audit Completed — Dimensional Limits Established  

---

## 1. Executive Summary & Authoritative Enclosure Constraints

This mechanical preflight review audits the physical integration of the Smart Pen Revision G electronics within the client-specified cylindrical enclosure parameters:
- **Total Pen Length:** $150.0\text{–}155.0\text{ mm}$
- **Pen Outer Diameter (OD):** $15.0\text{–}16.0\text{ mm}$
- **Pen Wall Thickness:** $1.0\text{ mm}$ nominal (yielding an internal diameter $\text{ID} \approx 13.0\text{–}14.0\text{ mm}$)
- **Main PCB Dimensions:** Exactly $84.00 \times 9.20\text{ mm}$ (thickness $1.60\text{ mm}$)
- **Internal Subsystems:** Retractable pen refill cartridge (click mechanism), removable PCB chassis rail, lower battery cradle, detachable front nose MPU sensor, and separate MicroSD carrier.

---

## 2. Component Z-Height Envelope & Clearance Analysis

The main PCB ($84.00 \times 9.20\text{ mm}$) is populated with components on both sides or top-side only (SMD components on `F.Cu`, with select connectors and vias on `B.Cu`). Within a cylindrical cross-section of $\text{ID} = 13.50\text{ mm}$, the chord height available for a $9.20\text{ mm}$ wide board is:
$$h_{\text{sagitta}} = \frac{\text{ID}}{2} - \sqrt{\left(\frac{\text{ID}}{2}\right)^2 - \left(\frac{W_{\text{PCB}}}{2}\right)^2} = 6.75 - \sqrt{6.75^2 - 4.60^2} = 6.75 - 4.93 = 1.82\text{ mm}$$

This defines the curvature clearance boundary above and below the PCB edges:

| Component RefDes | Component Type | Package / Part Number | Component Height ($Z_{\text{max}}$) | Clearance Evaluation within 13.5 mm Barrel |
| :--- | :--- | :--- | :---: | :--- |
| **J_USB** | USB Type-C Receptacle | `TYPE-C-31-M-12` (Mid-Mount) | $3.16\text{ mm}$ | **CRITICAL:** Tallest top-side component; requires dedicated slot cut-out in pen barrel wall. |
| **SW1–SW5** | Side Tactile Switches | Panasonic `EVQ-P2B02B` | $2.50\text{ mm}$ | Protrudes through enclosure button apertures; requires silicone seal / actuator caps. |
| **SW3** | Power Slide Switch | Sub-miniature Slide | $1.50\text{ mm}$ | Side-accessible switch actuator. |
| **J_RF** | U.FL RF Coaxial Receptacle | Hirose `U.FL-R-SMT-1(10)` | $1.25\text{ mm}$ | Low profile ($1.25\text{ mm}$ mated with $0.81\text{ mm}$ cable); fits comfortably. |
| **J_SD** | 6-pin FFC Receptacle | Hirose `FH12-6S-0.5SH(55)` | $2.00\text{ mm}$ | Flip-lock actuator requires $2.5\text{ mm}$ vertical clearance during FFC insertion. |
| **J_IMU** | 4-pin JST SH Header | `SM04B-SRSS-TB(LF)(SN)` | $2.90\text{ mm}$ | Located at front tip ($X=3.2\text{ mm}$); cable exits horizontally toward nose cone. |
| **J_BAT** | 2-pin JST SH Header | `SM02B-SRSS-TB(LF)(SN)` | $2.90\text{ mm}$ | Located at $X=62.8\text{ mm}$; battery harness routes downward to lower cradle. |
| **U1** | ESP32-C3FH4X SoC | QFN-32 ($5 \times 5\text{ mm}$) | $0.90\text{ mm}$ | Low profile; excellent clearance. |
| **U2, U4** | Charger & LDO Regulators | SOT-23-5 | $1.15\text{ mm}$ | Standard clearance. |
| **C10, C11, C14** | Bulk Ceramic Capacitors | 0805 Package | $1.25\text{ mm}$ | Fits within standard clearance envelope. |

---

## 3. Subsystem Spatial & Mechanical Integration Audit

### 3.1 Side-Port USB-C Access
- **Connector Placement:** The `TYPE-C-31-M-12` receptacle is mounted at $X = 78.40\text{ mm}$ on `F.Cu`.
- **Enclosure Penetration:** The connector is oriented perpendicular to the pen length to provide side-access charging.
- **Aperture Requirements:**
  - Cut-out width: $\ge 9.4\text{ mm}$ (to clear the $8.94\text{ mm}$ plug metal collar).
  - Cut-out height: $\ge 3.8\text{ mm}$ (to clear the $3.26\text{ mm}$ plug profile).
  - Overmold clearance: Standard USB-C cable overmolds have widths of $11.0\text{–}12.5\text{ mm}$. The enclosure surface around the USB port must be flat or countersunk; otherwise, cylindrical barrel curvature will prevent full plug insertion depth ($6.5\text{ mm}$).

### 3.2 FFC Cable Routing to MicroSD Carrier
- **Carrier Location:** The MicroSD carrier PCB is located either beneath the main board or behind the clicker mechanism.
- **Path Length & Bend Radius:** The FFC links `J_SD` ($X = 58.40\text{ mm}$) to the carrier board over a span of $25\text{–}35\text{ mm}$.
- **Clicker Clearance:** A standard ballpoint refill cartridge has an outer diameter of $3.0\text{–}4.0\text{ mm}$ and moves longitudinally by $\approx 4.0\text{ mm}$ during click actuation. The FFC must be routed along a dedicated lateral channel in the internal chassis rail to prevent mechanical rubbing, wear, or pinching against the reciprocating refill cartridge.

### 3.3 Battery Cradle Space Below Removable Rail
- **Cradle Geometry:** The battery sits in a semi-cylindrical cavity beneath the main PCB rail.
- **Available Envelope:**
  - Length: $\le 35.0\text{ mm}$
  - Width: $\le 10.5\text{ mm}$
  - Thickness (Height): $\le 4.5\text{ mm}$
- **Compatible Cell Form Factor:** Matches commercial protected pouch cell formats such as `401030` ($4.0\text{ mm}$ thick, $10.0\text{ mm}$ wide, $30.0\text{ mm}$ long, $\approx 90\text{–}110\text{ mAh}$) or `501030` ($5.0\text{ mm}$ thick, requires tight fit).
- **Thermal & Swell Margin:** Lithium-polymer cells expand by up to $10\%$ in thickness over their cycle life. The cradle cavity must accommodate up to $4.8\text{ mm}$ maximum swollen thickness.

### 3.4 Front Detachable MPU Sensor (`Front_MPU`)
- **Location:** Integrated inside the detachable pen nose cone assembly.
- **Interconnect:** 4-pin micro-harness from `J_IMU` ($X = 3.20\text{ mm}$) to the front daughterboard.
- **Nose Cone Detachability:** The front nose cone must thread or snap into the main barrel. The wiring harness must provide adequate service loop ($10\text{–}15\text{ mm}$) to allow nose cone removal without straining solder joints.

### 3.5 Refill Click Mechanism, Bayonet & Clip
- **Longitudinal Centerline:** The ink refill cartridge passes along the central longitudinal axis of the pen from the tip to the rear clicker button.
- **Chassis Architecture:** The internal chassis must use a split "horseshoe" or "C-channel" rail architecture where the central bore guides the refill cartridge, the upper flat shelf supports the $9.20\text{ mm}$ PCB, and the lower shelf holds the battery.
- **Bayonet Retention:** A twist-lock bayonet mechanism joins the front barrel to the rear click section, requiring keyways that do not interfere with the PCB edge cuts.

### 3.6 Enclosure Material & RF Antenna Integration Constraints
- **Material Selection:**
  - **Option A (Full Aluminum / Metallic Chassis):** Provides premium tactile feel and structural rigidity, but acts as a complete **Faraday cage**. A metallic chassis will attenuate 2.4 GHz Wi-Fi/BLE signals by $> 40\text{ dB}$, rendering wireless communication inoperable unless an external plastic "RF window" or non-metallic cap is incorporated.
  - **Option B (Polycarbonate / ABS / Composite):** Transparent to RF signals. Allows an internal flexible PCB antenna (connected to `J_RF`) to radiate omnidirectionally.
- **Engineering Directive:** If an aluminum or metallic barrel is selected, the antenna must be housed in a non-metallic (plastic) end-cap, or a dedicated RF dielectric window must be designed into the pen barrel.

---

## 4. Dimensional Estimates vs. Verified 3D Collision Checks

| Integration Feature | Verification Method | Status | Phase 4 Action Required |
| :--- | :--- | :---: | :--- |
| **PCB Outline ($84.00 \times 9.20\text{ mm}$)** | KiCad 10 Native Geometry (`Edge.Cuts`) | **VERIFIED** | Enclosure rail CAD must match exact profile. |
| **PCB Thickness ($1.60\text{ mm}$)** | Stackup Definition & Title Block | **VERIFIED** | Guide rail slot width set to $1.80\text{ mm}$ ($+0.2\text{ mm}$ clearance). |
| **Component Height Envelope ($Z_{\text{max}} = 3.16\text{ mm}$)**| Part Datasheet Specifications | **CALCULATED** | Full 3D STEP collision check in SolidWorks/Inventor. |
| **Battery Cradle Volume ($35 \times 10.5 \times 4.5\text{ mm}$)** | Geometric Chord Calculation | **ESTIMATED** | Requires client battery selection and 3D CAD modeling. |
| **USB-C Plug Insertion Depth** | 2D Layout & Wall Thickness Estimate | **ESTIMATED** | Molded barrel countersink must be validated in 3D CAD. |
| **FFC Refill Click Clearance** | Schematic & Pinout Analysis | **ESTIMATED** | Dynamic travel collision simulation of clicker stroke. |
| **RF Antenna Radiation Envelope** | Electromagnetic Cavity Review | **ESTIMATED** | 3D EM simulation and chamber characterization. |
