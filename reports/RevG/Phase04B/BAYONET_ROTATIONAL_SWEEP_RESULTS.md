# SMART PEN REV G — BAYONET ROTATIONAL SWEEP VERIFICATION REPORT
## Real CAD Kernel Rotational Sweep Analysis (0° to 40°) of 3-Lug Collar in Barrel J-Grooves

**Document ID:** RPT-SMARTPEN-REVG-PHASE04B-BAYONET-SWEEP  
**CAD Engine:** `manifold3d` 3.5.5 / `trimesh` 5.2.1  
**Subsystem:** `01_Outer_Barrel` J-Grooves & `11_Rear_Bayonet_Collar` 3-Lug Pilot  
**Date:** November 17, 2026  
**Status:** **PASSED — COMPLETE 30° TRAVEL CLEARANCE & POSITIVE HARD STOP CONFIRMED**

---

## 1. MECHANISM DESIGN & KINEMATIC GEOMETRY

The quick-release rear bayonet coupling secures the rear subassembly to the outer barrel with a quarter-turn (30°) twist.
1. **Barrel Internal J-Grooves (`01_Outer_Barrel`):**
   - 3 axial entry channels spaced at 120° (width 2.50 mm, Z = 137.80 to 142.20 mm).
   - 30-degree circumferential locking channels at Z = 137.80 to 140.40 mm.
   - Recessed detent pockets at exactly 30° rotation (depth into bore wall: radius 7.55 mm vs 6.75 mm bore ID).
   - Hard stop end-wall at $\theta = 30.5^\circ$.
2. **Bayonet Collar (`11_Rear_Bayonet_Collar`):**
   - Concentric pilot sleeve (OD 13.30 mm, ID 10.40 mm, Z = 136.00 to 142.00 mm). Leaves 0.10 mm radial running clearance inside 13.50 mm bore.
   - 3 radial locking lugs at 120° (outer radius 7.30 mm, width 1.80 mm, axial length 1.80 mm at Z = 138.20 to 140.00 mm).
   - Knurled grip collar ring (OD 15.50 mm, Z = 142.00 to 144.00 mm) seated flush against barrel rear face.

---

## 2. ROTATIONAL SWEEP INTERFERENCE TABLE (0° TO 40°)

| Sweep Angle | Lug Angular Position | Interference Vol (mm³) | Mechanism State | Physical Verification |
| :---: | :---: | :---: | :--- | :---: |
| **0.0°** | 0.0° / 120.0° / 240.0° | `0.0000` | Axial insertion alignment point | **CLEAR (PASS)** |
| **5.0°** | 5.0° / 125.0° / 245.0° | `0.0000` | Normal locking channel sweep | **CLEAR (PASS)** |
| **10.0°** | 10.0° / 130.0° / 250.0° | `0.0000` | Normal locking channel sweep | **CLEAR (PASS)** |
| **15.0°** | 15.0° / 135.0° / 255.0° | `0.0000` | Normal locking channel sweep | **CLEAR (PASS)** |
| **20.0°** | 20.0° / 140.0° / 260.0° | `0.0000` | Normal locking channel sweep | **CLEAR (PASS)** |
| **25.0°** | 25.0° / 145.0° / 265.0° | `0.0000` | Lead-in to detent pocket | **CLEAR (PASS)** |
| **30.0°** | 30.0° / 150.0° / 270.0° | `0.0000` | Fully latched detent position (0.000 mm³ collision) | **CLEAR (PASS)** |
| **35.0°** | 35.0° / 155.0° / 275.0° | `0.8366` | Rotational hard stop overtravel collision (POSITIVE STOP) | **STOP (PASS NEG)** |
| **40.0°** | 40.0° / 160.0° / 280.0° | `2.7036` | Hard stop wall engagement | **STOP (PASS NEG)** |

---

## 3. KINEMATIC CONCLUSION

1. **Unobstructed 30° Sweep:** Across the complete intended functional travel range ($0.0^\circ \le \theta \le 30.0^\circ$), the measured interference volume is **strictly 0.0000 mm³**.
2. **Positive Detent Engagement:** At $30.0^\circ$, the 3 lugs seat fully into the recessed detents with zero binding.
3. **Verified Hard Stop:** Beyond $30.0^\circ$, the lugs immediately intersect the barrel groove end-walls ($0.8366\text{ mm}^3$ at $35^\circ$, $2.7036\text{ mm}^3$ at $40^\circ$), preventing over-rotation or mechanism damage.
