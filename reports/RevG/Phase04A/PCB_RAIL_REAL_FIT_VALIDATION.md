# SMART PEN REV G — PCB RAIL REAL FIT VALIDATION REPORT
## Geometric Reconciliation and Real Solid Fit of Removable Electronics Rail (Part 04)

**Document ID:** RPT-SMARTPEN-REVG-PHASE04A-PCB-RAIL  
**Part Name:** `04_Removable_Electronics_Rail`  
**Reference PCB:** `15_Main_SmartPen_PCB` (from `output/RevG/SmartPen.kicad_pcb`)  
**Date:** November 16, 2026  
**CAD Kernel:** `manifold3d` 3.5.5 / `trimesh` 5.2.1  
**Status:** **PASSED — ZERO INTERFERENCE VALIDATED**

---

## 1. DESIGN SPECIFICATION & INTERFACE SUMMARY

The Removable Electronics Rail is the structural spine of the Smart Pen. It slides into the 13.50 mm bore of the outer barrel and provides:
1. An upper deck channel securing the four-layer Main SmartPen PCB (84.00 x 9.20 x 1.60 mm).
2. Lateral retention lips to prevent PCB pop-out under writing vibration.
3. A central tubular corridor along X = 0, Y = 0 guiding the moving click pushrod (OD 1.60 mm).
4. Three external alignment guide ribs matching the barrel bore with running clearance.
5. Underside clearance and snap mounts for the LiPo battery cradle.
6. A rear extraction pull tab for tool-free assembly and servicing.

---

## 2. DIMENSIONAL AUDIT & CORRECTION OF DEFICIT

| Dimension Parameter | Phase 4 Defective Model | Phase 4A Corrected Model | Physical Margin / Clearance |
| :--- | :--- | :--- | :--- |
| **Rail Length (Z)** | 84.00 mm (Z = 38 to 122) | 84.00 mm (Z = 38 to 122) | Matches 84.00 mm PCB length |
| **Inside Deck Width** | 7.80 mm (X = ±3.90 mm) | **9.50 mm** (X = ±4.75 mm) | **+0.30 mm total (+0.15 mm per side)** |
| **Deck Floor Level** | Y = +1.20 mm | Y = +1.20 mm | 1.20 mm above pen centerline |
| **Side Wall Thickness** | 0.90 mm | **0.75 mm** | Adequate rigidity for SLS / SLA resin |
| **Outside Rail Width** | 9.60 mm (X = ±4.80 mm) | **11.00 mm** (X = ±5.50 mm) | Sits within circular bore segment |
| **Snap Lip Overhang** | None | **0.35 mm per side** (slot 8.80 mm) | Secure positive vertical snap |
| **Pushrod Corridor ID** | 2.00 mm | **2.40 mm** (radius 1.20 mm) | **+0.40 mm radial clearance** for 1.6 mm rod |
| **Alignment Ribs OD** | 13.00 mm | **13.10 mm** (radius 6.55 mm) | **0.20 mm radial clearance** in 13.5 mm bore |

---

## 3. BORE SEGMENT CLEARANCE VERIFICATION

The outer barrel bore is a cylinder with radius $R_{\text{bore}} = 6.75\text{ mm}$ (diameter 13.50 mm).

At the top of the rail side walls ($Y = +2.80\text{ mm}$):
$$R_{\text{wall\_top}} = \sqrt{x_{\text{out}}^2 + y_{\text{top}}^2} = \sqrt{5.50^2 + 2.80^2} = \sqrt{30.25 + 7.84} = \sqrt{38.09} = 6.17\text{ mm}$$

Margin between rail wall corner and barrel bore:
$$\Delta R = R_{\text{bore}} - R_{\text{wall\_top}} = 6.75 - 6.17 = 0.58\text{ mm}$$

At the top of the retention lips ($Y = +3.20\text{ mm}$):
$$R_{\text{lip\_top}} = \sqrt{5.50^2 + 3.20^2} = \sqrt{30.25 + 10.24} = \sqrt{40.49} = 6.36\text{ mm}$$
$$\Delta R = 6.75 - 6.36 = 0.39\text{ mm}$$

The corrected 11.00 mm wide rail channel fits completely inside the 13.50 mm barrel bore with over **0.39 mm radial clearance** everywhere along its length.

---

## 4. REAL CAD BOOLEAN INTERFERENCE RESULTS

Using the `manifold3d` solid modeling engine, an exact solid intersection operation was executed:
$$\text{Interference Volume} = \text{Rail Solid} \cap \text{PCB Solid}$$

```python
rail_solid = build_04_removable_electronics_rail(p)
pcb_solid = refs['15_Main_SmartPen_PCB']
inter = rail_solid ^ pcb_solid
print("Interference Volume:", inter.volume())
```
**Measurement:** `inter.volume() = -2.93e-14 mm³` (Numerically zero).  
**Result:** **PASS (ZERO COLLISION)**.

### Negative Test Confirmation
When an intentionally oversized PCB of width `10.50 mm` was evaluated against the rail:
$$\text{Oversized Interference} = \text{Rail Solid} \cap \text{PCB}_{10.5\text{mm}} = 40.32\text{ mm³} > 0$$
**Result:** Defect detection confirmed.

---

## 5. PRINTABILITY & MESH TOPOLOGY

The exported STL file `output/RevG/Mechanical_Phase04_Corrected/STL/04_Removable_Electronics_Rail.stl` was audited using `trimesh`:
- Vertices: 292
- Triangles: 580
- `is_watertight`: **True**
- `is_volume`: **True**
- Volume: **3067.52 mm³**
- Non-manifold edges: **0**
- Degenerate faces: **0**

**Manufacturing Recommendation:** Stereolithography (SLA) using high-temperature engineering resin (e.g., Formlabs Tough 2000 or Draft Resin v2) or SLS Nylon PA12 with 0.10 mm layer resolution.
