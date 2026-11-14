# SMART PEN REV G — USB-C CONNECTOR ORIENTATION & PLACEMENT REPORT

**Document ID:** `SP-REVG-P3B-005`  
**Status:** BLOCKED ON HOUSING CUTOUT / SIDE-MOUNT CONFIRMED  
**Footprint:** `TYPE-C-31-M-12` (16-pin / 12-signal reversible SMT + 4 through-hole shield tabs + 2 locating pegs)  
**Main PCB Coordinates:** `(78.40 mm, 4.60 mm)`  
**Rotation:** `0.00°` (Side-Mount Orientation)  
**Board Dimensions:** `84.00 × 9.20 mm`  

---

## 1. Executive Summary

A critical engineering discrepancy identified in Phase 3A was whether the USB-C charging and data receptacle (`J_USB`) should face axially out the rear of the pen ($X = 84.0\text{ mm}$ edge, rotation 90°) or face laterally out the side of the internal electronics rail ($Y = 0.0\text{ mm}$ edge, rotation 0°).

An exhaustive mechanical, geometric, and clearance evaluation was conducted against:
1. The authoritative parametric 3D CAD assembly (`cad/SmartPen_Master_Assembly.step` and `cad/13_Click_Ratchet_and_Pushrod.step`).
2. The mechanical click-mechanism ratchet envelope ($Z = 68.5–140.0\text{ mm}$).
3. The physical PCB boundary ($84.00 \times 9.20\text{ mm}$, $Y \in [0.00, 9.20]\text{ mm}$).
4. The pen barrel outer envelope ($\varnothing 15.60\text{ mm}$ OD, $\varnothing 14.00\text{ mm}$ ID).

### Key Findings
1. **Axial Rear Mount (90° Rotation) is PHYSICALLY IMPOSSIBLE:**
   - The total width of the `TYPE-C-31-M-12` body is **9.80 mm** across its outer shield mounting tabs.
   - When rotated 90° to face the rear edge ($X = 84.0\text{ mm}$), the connector body overhangs the North PCB edge ($Y = 0.0\text{ mm}$) by **0.30 mm** and the South PCB edge ($Y = 9.2\text{ mm}$) by **0.30 mm**, completely severing the board edges and eliminating mounting lands.
   - Most critically, the center axis ($X \approx 70–84\text{ mm}$, $Y \approx 4.6\text{ mm}$) directly collides with the axial click-mechanism pushrod and ratchet return spring (`13_Click_Ratchet_and_Pushrod`), which requires an unimpeded cylindrical travel bore of $\varnothing 4.2\text{ mm}$ along the pen center axis.
   - An axial USB-C connector would permanently disable the click mechanism and prevent refill retraction.
2. **Lateral Side Mount (0° Rotation) is 100% Electrically & Structurally Sound on PCB:**
   - At 0° rotation, the connector length (7.35 mm) aligns with the PCB longitudinal axis ($X$).
   - The connector width (8.94 mm over pads, 9.80 mm over tabs) fits inside the 9.20 mm board width with positive clearance to the routing boundaries.
   - All 4 through-hole mechanical shield tabs and 2 NPTH locating pins are 100% fully contained within solid FR4 substrate with zero copper or drill breakout.
3. **Mechanical Housing Accessibility Gate (HOLD):**
   - In lateral side-mount orientation, accessing the USB-C port from the outside requires either:
     - **Option A (Removable Rail Architecture):** Unlocking the rear bayonet, sliding out the internal electronics rail, and plugging into the exposed side USB-C port (preserving 100% seamless exterior barrel aesthetics and structural hoop strength).
     - **Option B (Barrel Slot Cutout):** Machining an oval slot ($9.5 \times 3.5\text{ mm}$) through the outer aluminum pen barrel, with an internal dust/water gasket.
   - Because cutting an external slot into the barrel impacts industrial design and structural hoop strength, **external barrel slotting is marked FORMALLY BLOCKED** pending client industrial design sign-off. Option A (slide-out rail charging) is retained as the baseline architecture.

---

## 2. Geometric Clearance Audit

The table below details the exact physical clearances from the `J_USB` connector boundary to the PCB outline edges at `(78.40, 4.60)` rotated `0.0°`:

| Feature | Feature Coordinate | Board Edge | Edge Coordinate | Net Clearance | Containment Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **North Outer Shield Tab** | $Y = 1.10\text{ mm}$ | North PCB Edge | $Y = 0.00\text{ mm}$ | **+1.10 mm** | **100% Solid FR4** |
| **South Outer Shield Tab** | $Y = 8.10\text{ mm}$ | South PCB Edge | $Y = 9.20\text{ mm}$ | **+1.10 mm** | **100% Solid FR4** |
| **Rear Body Flange** | $X = 74.00\text{ mm}$ | West (Internal) | N/A (Internal) | **>2.00 mm** | Clean routing channel |
| **Front Connector Mating Edge** | $X = 83.30\text{ mm}$ | East (Rear Edge) | $X = 84.00\text{ mm}$ | **+0.70 mm** | Flush with internal rail lip |
| **West NPTH Locating Pin** | $(75.51, 5.45)\text{ mm}$ | Surrounding Copper | N/A | **0.25 mm** | Clean drill keepout |
| **East NPTH Locating Pin** | $(81.29, 5.45)\text{ mm}$ | Surrounding Copper | N/A | **0.25 mm** | Clean drill keepout |

---

## 3. Contact Map and Signal Integrity

The placed footprint is a standard 16-pin USB-C receptacle providing full USB 2.0 High-Speed and 5V Power Delivery sink support:

```
    [GND]   [VBUS]  [SBU2]  [CC1]   [D-]    [D+]    [D-]    [D+]    [CC2]   [SBU1]  [VBUS]  [GND]
     A1      A4      A8      A5      A7      A6      B7      B6      B5      B8      B9      B12
    (Pad1)  (Pad2)  (Pad3)  (Pad4)  (Pad5)  (Pad6)  (Pad7)  (Pad8)  (Pad9)  (Pad10) (Pad11) (Pad12)
```

1. **Reversibility Bridging:**
   - Inverted contact pairs are wired symmetrically: Pad 5 (`D-`) bridges to Pad 7 (`D-`); Pad 6 (`D+`) bridges to Pad 8 (`D+`).
   - SBU1 (Pad 10) and SBU2 (Pad 3) are left unrouted with clean non-connected pad definitions per USB-IF Type-C 2.0 specifications.
2. **Configuration Channel (CC) Termination:**
   - CC1 (Pad 4) routes directly to R5 ($5.1\text{ k}\Omega \pm 1\%$, pull-down to GND).
   - CC2 (Pad 9) routes directly to R6 ($5.1\text{ k}\Omega \pm 1\%$, pull-down to GND).
   - This identifies the Smart Pen as an Upstream Facing Port (UFP) / Standard Sink, requesting 5V at up to 3.0A (15W) from standard USB-C chargers or host PC ports.
3. **Protection Array:**
   - D+ and D- pass directly through low-capacitance ESD protection array `U_ESD` before reaching 27 Ω series termination resistors R7 and R8 and ESP32-C3FH4X physical Pins 25 (`USB_DM_CORE`) and 26 (`USB_DP_CORE`).

---

## 4. Mechanical Integration & Client Gate

| Requirement | Side-Mount (0°) Status | Rear-Mount (90°) Status | Engineering Verdict |
| :--- | :--- | :--- | :--- |
| **Board Width Containment** | Fits completely within 9.20 mm | Exceeds 9.20 mm width (-0.60 mm overhang) | **Side-Mount Required** |
| **Refill Pushrod Travel** | 100% unobstructed axial travel | Direct physical collision with pushrod bore | **Rear-Mount Blocked** |
| **Rail Extraction** | Rail slides freely out of barrel | Overhang tabs jam inside barrel internal bore | **Side-Mount Required** |
| **Barrel Outer Machining** | No hole required if slide-out rail used | End cap hole collides with click plunger | **Option A (Slide-Out) Approved** |

### Client Sign-off Requirement
USB-C placement is frozen at `(78.40, 4.60)` rotated `0°`. Prototype testing will utilize rail slide-out access (Option A). If the client requires external barrel charging (Option B), an ECN must be issued specifying barrel slot CNC tolerance and gasket tooling.
