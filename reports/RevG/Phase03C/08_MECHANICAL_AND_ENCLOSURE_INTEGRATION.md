# Smart Pen Rev G — Mechanical & Enclosure Integration Audit
**Document ID:** RPT-REVG-P3C-008  
**Project:** Smart Pen Hardware Architecture Revision G  
**Target Board:** `output/RevG/variants/FourLayer_Candidate/SmartPen.kicad_pcb`  
**Date:** November 16, 2026  

---

## 1. Executive Summary

This report validates the physical integration of the Smart Pen Rev G 4-layer candidate PCB into the injection-molded cylindrical pen barrel. Mechanical envelope constraints require strict adherence to the $84.00 \times 9.20\text{ mm}$ outline, side-mount USB-C receptacle orientation, and vertical keepout volumes to prevent interference with the pen cartridge and click pushrod mechanism.

---

## 2. Enclosure Dimensions & Mechanical Fit

| Enclosure Feature | Enclosure Dimension | PCB Dimension | Clearance / Margin | Verification |
| :--- | :---: | :---: | :---: | :--- |
| **Internal Barrel Bore Diameter** | $\varnothing 10.50\text{ mm}$ | PCB Width $9.20\text{ mm}$ | $0.65\text{ mm}$ per side | Diagonal fit $\sqrt{9.2^2 + 1.6^2} = 9.34\text{ mm} < 10.50\text{ mm}$ |
| **PCB Internal Axial Slot Length** | $85.50\text{ mm}$ | PCB Length $84.00\text{ mm}$ | $1.50\text{ mm}$ end clearance | Axial floating allowance for thermal expansion |
| **Board Thickness** | $1.60\text{ mm}$ Guide Rail | $1.60\text{ mm} \pm 0.16\text{ mm}$ | Snap-in interference fit | Zero rattle; compliant retention ribs |
| **Top Component Height Limit** | $2.40\text{ mm}$ max | J_SD ($1.45\text{ mm}$), J_USB ($2.10\text{ mm}$) | $\ge 0.30\text{ mm}$ top clearance | Non-interfering with upper shell arc |
| **Bottom Component Height Limit** | $1.20\text{ mm}$ max | 0402 Passives ($0.45\text{ mm}$) | $\ge 0.75\text{ mm}$ bottom clearance | Ample clearance above battery cradle |

```
        Enclosure Barrel Cross-Section (Ø 10.50 mm)
                   , - ~ ~ ~ - ,
               , '       ▲       ' ,
             ,     Top Clearance     ,
            ,            │            ,
           ,    ┌────────────────┐     ,  ◄─ PCB Surface (F.Cu)
           ├────│  SmartPen PCB  │─────┤  ◄─ Guide Rails (1.60 mm)
           ,    └────────────────┘     ,  ◄─ PCB Bottom (B.Cu)
            ,            │            ,
             ,    Battery Cradle     ,
               , '       ▼       ' ,
                   ' - , _ _ , - '
```

---

## 3. Side-Mount USB-C Placement vs. Rear-Axial Clash Analysis

A fundamental requirement of the Smart Pen architecture is the side-mount orientation of the USB-C connector (`J_USB`).

### 3.1 The Rear-Axial Pushrod Clash
In traditional stylus or dongle designs, USB connectors are often placed axially at the rear end ($X > 84.0\text{ mm}$). In the Smart Pen, however, the rear cylindrical volume houses:
1. The mechanical ratcheting click cam.
2. The spring-loaded ink cartridge pushrod ($3.50\text{ mm}$ actuation stroke).
3. The pocket clip spring retention block.

If `J_USB` were oriented axially ($90^\circ$ rotation at the rear), the connector shell and cable insertion receptacle would occupy the exact cylindrical volume traversed by the pushrod, completely disabling the click-to-extend mechanism.

### 3.2 Side-Mount Integration
In the candidate layout (`output/RevG/variants/FourLayer_Candidate/SmartPen.kicad_pcb`):
- `J_USB` is positioned at $(78.400, 4.600)$ with **$0.0^\circ$ rotation**.
- The receptacle opening faces through a precision cutout in the lateral side of the pen barrel.
- The rear $5.60\text{ mm}$ of the PCB ($X \in [78.40, 84.00]\text{ mm}$) maintains clear keepout areas, allowing the pushrod to travel freely past the board without mechanical obstruction.

---

## 4. Retractable Ink Cartridge Corridor

The pen refill cartridge extends from the rear click mechanism to the front nib. 
- **Refill Body Diameter:** $\varnothing 3.00\text{ mm}$ standard D1 or Parker-style mini refill.
- **Radial Clearance:** The PCB is positioned $1.20\text{ mm}$ offset from the central axis of the barrel, establishing a dedicated clearance corridor for the refill tube.
- **Front Nib Assembly:** The western edge of the PCB ($X = 0.00\text{ mm}$) features chamfered $45^\circ$ corners that contour smoothly into the tapered front nose-cone.

---

## 5. MicroSD Socket (`J_SD`) Push-Push Operation

- **Socket Selection:** Molex `104031-0811` push-push top-mount MicroSD card connector.
- **Card Insertion Direction:** The card inserts from the side aperture of the barrel.
- **Card Ejection Clearance:** The push-push latch mechanism requires a $1.20\text{ mm}$ over-travel stroke to lock and unlock. The enclosure side slot provides $2.00\text{ mm}$ of external finger clearance, allowing card insertion and removal without disassembling the pen.

---

## 6. Conclusion

The 4-layer candidate PCB satisfies all mechanical and enclosure constraints. The $84.00 \times 9.20\text{ mm}$ outline, $1.60\text{ mm}$ thickness, and side-mount USB-C orientation preserve complete drop-in compatibility with the Revision G injection-molded pen barrel tooling.
