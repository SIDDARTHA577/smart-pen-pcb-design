# Smart Pen Revision F — Enclosure Mechanical Drawings, Tolerancing & Kinematic Datums

**Project**: Smart Pen PCB and 3D Enclosure — RadixView Technologies  
**Date**: November 2, 2026  
**Revision**: Rev F Engineering Release  
**Authoritative Reference**: `Smart_Pen_PCB_Handoff(1).docx` (Revision 0.2, September 2026)  
**Drawing Package**: `SmartPen_Mechanical_Drawings.svg`  

---

## 1. Outer Envelope & Critical Datums

| Dimension Parameter | Nominal Specification | Design Value | Tolerance / Fits | Status | Reference Datum |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Total Assembly Length** | 150.0 to 155.0 mm | **153.50 mm** | $\pm 0.25\text{ mm}$ | **PASS** | Tip aperture (Z=0) to Click Dome |
| **Maximum Outer Diameter** | $\le 16.00\text{ mm}$ | **15.50 mm** | $+0.00 / -0.10\text{ mm}$ | **PASS** | Outer cylindrical barrel |
| **Main Outer Barrel Length**| N/A | **88.00 mm** | $\pm 0.10\text{ mm}$ | **PASS** | $Z = 54.0$ to $142.0\text{ mm}$ |
| **Front Grip Length** | Ergonomic grip zone | **36.00 mm** | $\pm 0.10\text{ mm}$ | **PASS** | $Z = 18.0$ to $54.0\text{ mm}$ (OD 11.2 to 15.5 mm) |
| **Front Cap Tip Length** | Nib guard | **18.00 mm** | $\pm 0.10\text{ mm}$ | **PASS** | $Z = 0.0$ to $18.0\text{ mm}$ |
| **Rear Click Cap Length** | Push-button sleeve | **13.50 mm** | $\pm 0.10\text{ mm}$ | **PASS** | $Z = 140.0$ to $153.5\text{ mm}$ |
| **Barrel Wall Thickness** | Structural rigidity | **1.25 mm** | $\pm 0.05\text{ mm}$ | **PASS** | ID: $13.00\text{ mm}$, OD: $15.50\text{ mm}$ |

---

## 2. Removable Internal Rail Cartridge & Sub-Assembly Interfaces

- **Total Rail Length**: **86.00 mm** ($Z = 52.0$ to $138.0\text{ mm}$).
- **Outer Guide Rib Diameter**: **12.40 mm**, providing **$0.30\text{ mm}$ per side diametral slide fit** inside the $13.00\text{ mm}$ barrel inner bore.
- **Upper PCB Mounting Deck**:
  - Elevation: $Y = +1.20\text{ mm}$.
  - Deck Width: **9.40 mm** (providing $0.10\text{ mm}$ per side lateral guide for the $84.0 \times 9.2\text{ mm}$ PCB).
  - Headroom: Crest component elevation at $Y = +5.36\text{ mm}$ leaves **1.14 mm safety clearance** to the $Y = +6.50\text{ mm}$ barrel ceiling.
- **Central Longitudinal Tunnel Conduit**:
  - Diameter: **$\varnothing 3.20\text{ mm}$** ID, centered along the neutral pen axis ($X = 0, Y = 0$).
  - Houses the **$\varnothing 1.60\text{ mm}$** Delrin push-rod with **$0.80\text{ mm}$ radial clearance per side**, preventing buckling and mechanical snag.
- **Lower Battery Cradle Pocket**:
  - Elevation: $Y = -1.20$ to $-5.80\text{ mm}$ (depth: **4.60 mm**).
  - Accommodates verified LiPo cell `LP401040` ($4.0\text{ mm thick} \times 10.5\text{ mm wide} \times 40.0\text{ mm long}$) with **+0.60 mm chemical swelling margin**.
  - Cradle floor at $Y = -5.80\text{ mm}$ provides **0.70 mm safety clearance** to the barrel floor at $Y = -6.50\text{ mm}$.
- **Solid Composite Bulkhead**:
  - Thickness: **2.40 mm** solid structural deck separating PCB bottom copper from the battery pouch top, meeting Section 1.15 rigid isolation rules.

---

## 3. Kinematic Mechanism Tolerancing & Travel

### 3.1 Refill & Click Mechanism
- **Standard D1 Refill**: Outer diameter $\varnothing 2.35\text{ mm}$, reservoir length $67.0\text{ mm}$.
- **Axial Gap to Battery**:
  - Retracted State: Refill tail cup is at $Z = 68.50\text{ mm}$. Battery starts at $Z = 74.00\text{ mm}$. **Axial gap = 5.50 mm**.
  - Extended State: Refill moves forward by $4.50\text{ mm}$ to $Z = 64.00\text{ mm}$. **Axial gap = 10.00 mm**.
  - **Zero physical clash** between refill and battery under all operating conditions.
- **Clicker Stroke**: **4.50 mm** forward travel to engage writing detent.
- **Return Spring**: Seated around refill neck ($Z = 4.0$ to $14.0\text{ mm}$).
  - Free length: $12.00\text{ mm}$.
  - Compressed length during write: $7.50\text{ mm}$.
  - Over-travel click length: $6.20\text{ mm}$ (Solid height limit: $5.50\text{ mm} \implies \mathbf{0.70\text{ mm}}$ anti-binding safety margin).

### 3.2 Bayonet Twist-Lock Mechanism
- **Configuration**: 3 radial locking lugs spaced at $120.0^\circ$ on radius $R = 6.40\text{ mm}$.
- **Engagement Stroke**: **$30.0^\circ$ clockwise rotation** into positive locking detents.
- **Disengagement**: $30.0^\circ$ counter-clockwise twist allows the entire internal rail cartridge to slide out rearward as a single serviceable assembly.

---

## 4. Shell Apertures & User Interface Fits

- **USB-C Port Bezel**: $9.00 \times 3.50\text{ mm}$ rounded rectangular slot at $Z = 131.0$ to $137.5\text{ mm}$, aligned with PCB receptacle `J1`.
- **Dual Button Slot**: $4.50 \times 10.00\text{ mm}$ axial slot at $Z = 63.0$ to $73.0\text{ mm}$, accepting rocker actuator `07_Dual_Button_Actuator.stl`.
- **Dual Status LED Light Guides**: Two $\varnothing 1.20\text{ mm}$ apertures at $Z = 76.0\text{ mm}$ (Green `D1`) and $Z = 79.0\text{ mm}$ (Red `D2`).
- **Capacitive Touch Pad Recess**: Flushed surface pocket on upper front grip ($Z = 20.0$ to $35.0\text{ mm}$) for index finger ergonomic contact.
- **Pocket Clip Retention**: Mechanical interference dovetail on rear barrel ($Z = 120.0$ to $142.0\text{ mm}$).
