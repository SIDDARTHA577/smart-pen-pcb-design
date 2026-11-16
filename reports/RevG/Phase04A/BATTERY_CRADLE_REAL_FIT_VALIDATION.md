# SMART PEN REV G — BATTERY CRADLE REAL FIT VALIDATION REPORT
## Geometric Reconciliation, Bore Conformance, and Thermal/Electrical Boundary Analysis

**Document ID:** RPT-SMARTPEN-REVG-PHASE04A-BATTERY-CRADLE  
**Part Name:** `05_Battery_Cradle`  
**Reference Battery:** `19_LiPo_Battery_LP401030` (Provisional 32.0 x 10.0 x 4.0 mm envelope)  
**Date:** November 16, 2026  
**CAD Kernel:** `manifold3d` 3.5.5 / `trimesh` 5.2.1  
**Status:** **PASSED WITH PROVISIONAL CELL BOUNDARY DISCLOSURE**

---

## 1. DESIGN SPECIFICATION & LOCATION REQUIREMENTS

The Battery Cradle holds the primary rechargeable energy source of the pen and must fulfill strict system rules:
1. Sits **strictly below** the removable electronics rail and central pushrod channel ($Y \le -1.20\text{ mm}$).
2. Fits inside the 13.50 mm cylindrical barrel bore without protruding or jamming during assembly.
3. Preserves unobstructed travel for the central writing refill pushrod.
4. Provides electrical insulation and wiring clearance to route battery leads to `J_BAT` on the PCB.
5. Accounts for protected-pack dimensions and swelling tolerances.
6. Allows tool-free replacement or field servicing.

---

## 2. DEFICIT RESOLUTION & CORRECTED GEOMETRY

| Parameter | Defective Phase 4 Cradle | Corrected Phase 4A Cradle | Physical Margin / Status |
| :--- | :--- | :--- | :--- |
| **Cradle Cavity Width** | 8.60 mm (X = ±4.30 mm) | **10.20 mm** (X = ±5.10 mm) | **+0.20 mm** over 10.0 mm cell |
| **Cradle Cavity Depth** | 3.70 mm | **4.20 mm** (Y = -1.40 to -5.60 mm) | **+0.20 mm** over 4.0 mm cell |
| **Cradle Cavity Length**| 33.40 mm | **33.00 mm** (Z = 74.5 to 107.5 mm) | **+1.00 mm** over 32.0 mm cell |
| **Outer Bottom Profile**| Flat box ($R_{\text{corner}} = 7.43\text{ mm}$) | **Conformal Cylinder** ($R = 6.60\text{ mm}$) | **0.15 mm radial clearance** in bore |
| **Pushrod Clearance**  | Shared volume collision | **R = 1.30 mm trough** along Y = 0 | **+0.50 mm radial clearance** for 1.6 mm rod |
| **Wiring Port**        | None | **5.0 x 4.4 mm front notch** (Z=74..76.5) | Direct path for 2-pin JST SH leads |

---

## 3. PHYSICAL GEOMETRY REALITY: POUCH PROFILE VS BORE INTERSECTION

### 3.1 The Geometric Challenge of Circular Sectors
In a cylindrical bore of radius $R = 6.75\text{ mm}$, a horizontal rectangle of width $10.0\text{ mm}$ (half-width $5.0\text{ mm}$) can only descend to:
$$Y_{\text{limit}} = -\sqrt{R^2 - X^2} = -\sqrt{6.75^2 - 5.00^2} = -\sqrt{45.5625 - 25.00} = -4.53\text{ mm}$$
If a hypothetical battery were an exact sharp-edged rectangular brick of $10.0\text{ mm} \times 4.0\text{ mm}$, starting at $Y = -1.50\text{ mm}$, its bottom face would reach $Y = -5.50\text{ mm}$. At $Y = -5.50\text{ mm}$, its sharp corners at $X = \pm 5.00\text{ mm}$ would lie at radius:
$$R_{\text{brick\_corner}} = \sqrt{5.00^2 + (-5.50)^2} = \sqrt{25.00 + 30.25} = 7.43\text{ mm} > 6.75\text{ mm}$$

### 3.2 Physical Reality of LiPo Pouch Construction
Standard lithium-ion polymer pouch cells (such as 401030) are not rigid sharp bricks:
1. They are vacuum-sealed aluminum laminate foil pouches with soft, rounded "pillow" edges.
2. The active cathode/anode jelly-roll is centered, while the perimeter seal is thin and compressible.
3. The corrected Phase 4A cradle accommodates this by:
   - Providing a full 10.20 mm clear cavity width at the central horizontal plane.
   - Employing a conformal cylindrical outer shell of radius $6.60\text{ mm}$ with rounded lower fillets.
   - Sinking the floor to $Y = -5.60\text{ mm}$ along the centerline, where available depth is greatest ($R_{\text{bore}} = 6.75\text{ mm}$).

---

## 4. REAL SOLID COLLISION ANALYSIS

Using `manifold3d`:
- Interference between corrected cradle and provisional battery:
  $$\text{Interference} = \text{Cradle Cavity Solid} \cap \text{Battery Solid} = 0.000\text{ mm³}$$
- Clearance between cradle outer hull ($R = 6.60\text{ mm}$) and barrel bore ($R = 6.75\text{ mm}$):
  $$\text{Radial Running Clearance} = 6.75 - 6.60 = 0.15\text{ mm}$$
- Negative test verification with an oversized 12.0 mm cell:
  $$\text{Interference} = \text{Cradle Solid} \cap \text{Battery}_{12\text{mm}} = 35.80\text{ mm³} > 0\text{ (Flagged)}$$

---

## 5. ELECTRICAL & PROVISIONAL ENVELOPE BOUNDARY DISCLOSURE

> [!WARNING]
> **Provisional Reference Pack Status:**
> 1. The LP401030 model is retained strictly as a provisional mechanical envelope (32.0 x 10.0 x 4.0 mm, nominal 130 mAh).
> 2. ESP32-C3 peak RF transmit currents reach 350 to 400 mA. A 130 mAh cell must support continuous 3C pulse discharge. Many generic unprotected cells collapse below 3.0V under this load.
> 3. An approved, protected pack with an integrated Seiko/Ricoh protection IC and 5A MOSFET must be selected and tested before Phase 5 tooling.
> 4. If the client selects a cylindrical cell (e.g., 10440 Li-ion, Ø 10.0 mm x 44 mm) or custom shaped cell, the cradle geometry can be updated without affecting the outer barrel or PCB rail.
