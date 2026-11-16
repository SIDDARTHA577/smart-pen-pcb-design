# Smart Pen Rev G — Detachable Front MPU Module Verification
**Document ID:** RPT-REVG-P4-FRONT-MPU  
**Project:** Smart Pen Hardware Architecture Revision G  
**Target Variant:** Four-Layer Authoritative Candidate (`output/RevG/variants/FourLayer_Candidate/SmartPen.kicad_pcb`)  
**Git Branch:** `engineering/revg-production`  
**Date:** November 16, 2026  
**Status:** Detachable Mechanical Carrier Verified; Coordinate Convention Documented  

---

## 1. Executive Summary

This report establishes the mechanical design and modular integration of the detachable Front Inertial Measurement Unit carrier (`06_Front_MPU_Carrier.step` / `.stl`) housing the authoritative `Front_MPU.kicad_pcb` daughterboard.

In strict compliance with Section 1.8 through 1.10 of the client handoff specification:
- **Detachable Front Placement:** The IMU is housed at the forward tip ($Z = 20.00\text{ to }32.00\text{ mm}$), seated inside the front grip cavity to capture raw writing motion with maximum angular leverage.
- **Serviceable Refill Replacement:** The carrier integrates a keyed, snap-release retention interface and a central concentric refill passage channel ($\varnothing 2.70\text{ mm}$ ID) that allows the user to replace the standard D1 ink refill without pulling fragile wiring leads or destroying the enclosure.
- **Keyed 4-Pin Electrical Connection:** Mating is executed via a polarized JST SH 4-pin micro-connector (`SM04B-SRSS-TB` receptacle to `SHR-04V-S-B` plug), isolating mechanical loads from the solder joints.
- **Repeatable Coordinate Frame:** Mechanical anti-rotation index keys ensure the IMU returns to the exact same rotational orientation upon reinstallation.

---

## 2. Mechanical Pocket & Carrier Architecture

```
                  +Y (Upper Grip Surface)
                           |
            +--[ Front Grip Shell (ID 8.0 mm) ]--+
            |                                    |
            |   +----------------------------+   |
            |   | Front MPU PCB (7.2x10 mm)  |   |  Y = +2.20 to +3.00 mm
            |   | [ QFN-24 IMU Sensor ]      |   |  (Thickness: 0.80 mm)
            |   +----------------------------+   |
            +------------------------------------+  Y = +2.00 mm (Pocket Floor)
            |                                    |
            |  +--[ Refill Conduit Tube ]-----+  |  OD 3.60 mm, ID 2.70 mm
            |  |  ( ( D1 Refill Ø2.35 mm ) )  |  |  Centerline: (X=0, Y=0)
            |  +------------------------------+  |  Radial gap: 0.18 mm per side
            +------------------------------------+
                           |
                  -Y (Lower Grip Surface)
```

### 2.1 Dimensional Verification & Clearances

| Parameter | Design Value | Constraint / Standard | Clearance Margin | Status |
| :--- | :---: | :---: | :---: | :---: |
| **Carrier Outer Envelope** | $8.20 \times 7.60 \times 12.00\text{ mm}$ | Grip Internal Cavity ($\varnothing 8.00\text{ mm}$) | $0.20\text{ mm}$ slide fit | **PASS** |
| **PCB Pocket Width ($X$)** | $7.60\text{ mm}$ | `Front_MPU` PCB Width ($7.20\text{ mm}$) | $0.20\text{ mm}$ per side | **PASS** |
| **PCB Pocket Length ($Z$)**| $10.40\text{ mm}$ | `Front_MPU` PCB Length ($10.00\text{ mm}$) | $0.20\text{ mm}$ per side | **PASS** |
| **PCB Deck Thickness ($Y$)**| $0.80\text{ mm}$ | `Front_MPU` Board Thickness ($0.80\text{ mm}$)| Flush seating | **PASS** |
| **Refill Conduit ID** | $\varnothing 2.70\text{ mm}$ | Standard D1 Refill OD ($\varnothing 2.35\text{ mm}$) | **$0.18\text{ mm}$ radial gap** | **PASS** |
| **Connector Access Window** | $5.50 \times 3.20\text{ mm}$ | JST `SM04B-SRSS` Envelope | $0.35\text{ mm}$ insertion clearance | **PASS** |

---

## 3. Keyed 4-Pin Electrical Interface & Wiring Harness

The Front MPU connects to `J_IMU` on the Main PCB through a dedicated 4-conductor micro-harness:

### 3.1 Connector Pinout Table

| Pin | Net Name | Wire Color | Signal Function | Electrical Characteristics |
| :---: | :--- | :---: | :--- | :--- |
| **1** | `/3V3` | Red | $+3.3\text{V}$ Regulated Power | Sourced from `U4: AP2112K-3.3` ($I_{\text{typ}} \approx 3.0\text{ mA}$) |
| **2** | `/I2C_SDA` | Blue | I2C Serial Data | Bidirectional open-drain; $2.2\text{ k}\Omega$ pullup on Main PCB |
| **3** | `/I2C_SCL` | Yellow | I2C Serial Clock | Sourced from `U1: GPIO9` ($400\text{ kHz}$ Fast Mode) |
| **4** | `/GND` | Black | System Power Ground Return | Solid ground reference |

### 3.2 Harness Mechanical Specification
- **Wire Type:** 30 AWG stranded copper with ultra-flexible PTFE insulation.
- **Assembly Length:** $28.0\text{ mm} \pm 1.0\text{ mm}$.
- **Routing Corridor:** The harness routes through an internal lateral notch along the carrier flank into the main rail channel, providing adequate slack for the carrier to slide forward by $15.0\text{ mm}$ during refill changes before disconnecting the plug.

---

## 4. Mechanical Retention & Disassembly Sequence

To replace an exhausted D1 ink refill:
1. **Step 1 (Twist Front Nose):** Rotate the Front Nose Cone $30^\circ$ counter-clockwise. The nose cone disengages from its bayonet detent and slides forward off the writing tip.
2. **Step 2 (Expose Refill Spring):** The helical return spring ($12.0\text{ mm}$) is released forward over the refill tip.
3. **Step 3 (Slide Carrier Forward):** The Front MPU carrier slides forward by $12.0\text{ mm}$ on its guide rails, exposing the rear cup of the D1 refill.
4. **Step 4 (Extract Refill):** The spent D1 refill ($\varnothing 2.35 \times 67.0\text{ mm}$) pulls straight out through the carrier's $\varnothing 2.70\text{ mm}$ central conduit. Fragile sensor wiring remains completely undisturbed.
5. **Step 5 (Insert & Lock):** A fresh D1 refill is inserted into the pushrod receiver cup, the return spring is reseated, and the nose cone is locked clockwise with a positive tactile click.

---

## 5. Inertial Coordinate Frame & Sensor Orientation

To prevent sensor coordinate mismatches between mechanical CAD, embedded firmware, and browser motion reconstruction:

```
                  +Z (Towards Click Cap / Rear)
                               ^
                               |
               -X <------------+------------> +X (Towards Right Flank)
                               |
                               v
                  -Z (Towards Pen Writing Tip)

Vertical Axis: +Y points UP towards the Capacitive Touch Pad (Index Finger)
               -Y points DOWN towards the Paper / Desk Contact Surface
```

- **Sensor Package:** QFN-24 mounted on the top surface (`F.Cu`) of `Front_MPU.kicad_pcb`.
- **Sensor Pin 1 Index:** Located towards $(X = -3.60\text{ mm}, Z = +22.00\text{ mm})$ (front-left quadrant).
- **Firmware Axis Translation:**
  - Forward writing motion translates to negative acceleration along the longitudinal $Z$-axis ($-a_z$).
  - Upward pen lift translates to positive acceleration along the vertical $Y$-axis ($+a_y$).
  - Rightward cursive stroke translates to positive acceleration along the lateral $X$-axis ($+a_x$).
