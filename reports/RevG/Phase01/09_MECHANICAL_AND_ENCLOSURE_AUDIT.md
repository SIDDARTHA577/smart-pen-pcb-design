# Smart Pen Rev G — Phase 1: Mechanical Constraints & 3D CAD Audit

**Document ID**: `reports/RevG/Phase01/09_MECHANICAL_AND_ENCLOSURE_AUDIT.md`  
**Execution Date**: November 13, 2026  
**Revision Baseline**: Revision F  
**Target Development Revision**: Revision G  
**Branch**: `engineering/revg-production`  

---

## 1. Executive Summary

The mechanical enclosure of the Smart Pen was audited against the mandatory client requirements (**R1**, **R2**, **R3**, **R4**) specified in `Smart_Pen_PCB_Handoff.docx` (Revision 0.2) and the Master Engineering Instructions.

The CAD model exists as a fully parametric Python solid generator (`output/RevF_Client_Delivery/07_3D_CAD_Source/SmartPen_Parametric_CAD_RevF.py`) and a complete 15-part STEP assembly (`output/RevF_Client_Delivery/07_3D_STEP/SmartPen_Complete_Assembly.step`, 742,970 bytes).

---

## 2. Mandatory Requirement Compliance Matrix

| Requirement | Specification | Measured CAD Geometry | Audit Status | Evidence / Notes |
| :--- | :--- | :--- | :---: | :--- |
| **R1 — Pen Body Length** | 150.00 – 155.00 mm | **153.50 mm** | **PASS** | Tip aperture at Z = 0.00 mm; rear click dome at Z = 153.50 mm |
| **R1 — Outer Barrel Diameter** | 15.00 – 16.00 mm | **15.50 mm** | **PASS** | Outer barrel OD is constant 15.50 mm (R = 7.75 mm) |
| **R1 — Clip Radial Protrusion** | Document separately | **+2.80 mm** | **PASS** | Max radial extent at pocket clip is R = 10.55 mm |
| **R1 — Refill Extension** | Document click states | **+2.50 mm** | **PASS** | Retracted tip at Z = +1.50 mm; extended tip at Z = -2.50 mm |
| **R2 — Detachable Front MPU** | Separate tip daughterboard | 7.2 x 10.0 x 0.8 mm PCB | **PASS** | Dedicated PCB located at Z = 25.00 to 35.00 mm in tip |
| **R2 — Keyed Connector** | Detachable, keyed, small | JST-SH 4-pin (1.0 mm pitch) | **PASS** | SM04B-SRSS-TB(LF)(SN) header on board |
| **R2 — Zero Structural Load** | Connector carries 0 weight | Dedicated sensor carrier | **PASS** | `06_Front_IMU_Carrier` retains PCB via mechanical rails |
| **R2 — Repeatable Orientation**| Fixed XYZ sensor alignment | Documented coordinate system | **PASS** | +X = Right, +Y = Top (writing plane), +Z = Rear (axial) |
| **R3 — Battery Below Rail** | Strictly beneath rail spine | Y = -1.20 mm to -5.80 mm | **PASS** | Electronics rail spine at Y = -1.0 mm; battery at Y < -1.2 mm |
| **R3 — Detachable Battery** | Keyed detachable connector | JST-SH 2-pin (1.0 mm pitch) | **PASS** | SM02B-SRSS-TB(LF)(SN) on Main PCB; keyed lead |
| **R3 — Battery Swelling Room** | Swelling & retention | 0.60 mm depth clearance | **NOT VERIFIED**| Nominal 4.60mm cradle depth vs 4.0mm cell; requires real cell test |
| **R4 — Full Architecture** | All 15 subsystems preserved| 15 CAD solid parts modeled | **PASS** | Rail, bayonet, clicker, refill, cradle, MPU, clip all modeled |
| **BRep Solid Clash Check** | True 3D solid interference | BRep intersection analysis | **NOT VERIFIED**| CadQuery / OpenCASCADE unavailable in Python environment |

---

## 3. Dimensional Measurement & Geometric Coordinate Verification

Measurements extracted directly from `SmartPen_Parametric_CAD_RevF.py` parametric entities:

```
Z = 0.0 mm                                                                   Z = 153.5 mm
[Front Tip]=====[Front Grip]==========[Outer Barrel]====================[Rear Clicker]
  0.0-18.0 mm    18.0-54.0 mm             54.0-142.0 mm                    140.0-153.5 mm
       |               |                        |                                |
  [MPU Carrier]   [Bayonet Collar]      [Rail & Battery]                   [Pushrod]
   24.0-36.0 mm    50.0-56.0 mm         PCB: 54.0-138.0 mm                140.0-147.0 mm
                                        Bat: 74.0-114.0 mm
```

### 1. Longitudinal Axis (Z-Coordinates)
- **Front Cap Tip (`03_Front_Cap_Tip`)**: Z = 0.00 mm to 18.00 mm. Tip cone aperture diameter: 2.35 mm (accepts standard D1 refill sleeve of 2.30 mm OD).
- **Front Grip (`02_Front_Grip`)**: Z = 18.00 mm to 54.00 mm. Contoured ergonomic profile: OD tapers from 11.20 mm at front to 15.50 mm at barrel interface.
- **Bayonet Locking Collar (`14_Bayonet_Locking_Collar`)**: Z = 50.00 mm to 56.00 mm. 3-lug bayonet system (120° spacing, 30° rotational lock) securing the internal rail to the front grip.
- **Outer Barrel (`01_Outer_Barrel`)**: Z = 54.00 mm to 142.00 mm. OD = 15.50 mm, ID = 13.00 mm (wall thickness = 1.25 mm).
- **Removable Electronics Rail (`04_Internal_Rail_Cartridge`)**: Z = 52.00 mm to 142.00 mm. Features longitudinal anti-rotation guide ribs engaging barrel keyways.
- **Rear Click Mechanism Cap (`08_Rear_Click_Mechanism_Cap`)**: Z = 140.00 mm to 153.50 mm. Push-button travel sleeve and spherical dome. Total assembled pen body length = **153.50 mm**.

### 2. Radial & Transverse Envelope (X/Y-Coordinates)
- **Outer Radius**: R = 7.75 mm (OD = 15.50 mm).
- **Internal Clearance Bore**: R = 6.50 mm (ID = 13.00 mm).
- **Main PCB Elevation**: Mounted on top of the rail spine from Y = 0.00 mm to Y = +1.00 mm. Component clearance above board: +1.00 mm to +4.50 mm (accommodates 1.45 mm ESP32-C3, 1.20 mm switches, 1.00 mm passives).
- **LiPo Battery Elevation (R3 Compliance)**:
  - Rail spine thickness: Y = -0.20 mm to Y = -1.00 mm.
  - Insulating barrier air gap: Y = -1.00 mm to Y = -1.20 mm (0.20 mm clearance).
  - Battery cradle cavity (`05_Battery_Cradle`): Y = -1.20 mm to Y = -5.80 mm (total depth = 4.60 mm).
  - LiPo cell (`11_LiPo_Battery_LP401040`): Y = -1.50 mm to Y = -5.50 mm (cell thickness = 4.00 mm).
  - Wall clearance beneath battery to barrel ID: -5.80 mm to -6.50 mm (0.70 mm clearance).
  - **Verdict**: Battery is **100% physically situated beneath the rail**, completely separated from the Main PCB.

---

## 4. Subsystem Mechanical Fit & Clearances

### R2: Front MPU Daughterboard Carrier
- **Location**: Z = 24.00 mm to 36.00 mm, inside the front grip section.
- **Daughterboard Dimensions**: 7.20 mm width x 10.00 mm length x 0.80 mm thickness.
- **Carrier Pocket**: Retained in `06_Front_IMU_Carrier` with snap-in retention tabs and positive mechanical stops.
- **Wiring & Strain Relief**: J1 connector mates facing rearwards. A dedicated 1.80 mm wiring channel routes the 4-conductor flexible harness alongside the refill sleeve back to Main PCB header `J_IMU`, providing a 4.0 mm bend radius and strain relief. Connector carries 0 structural load.
- **Sensor Orientation**: Documented as:
  - +X: Transverse Right
  - +Y: Normal to writing surface (Pen Top)
  - +Z: Longitudinal towards rear clicker

### R3: Battery Cradle & Moving Refill Clearance
- **Battery Model**: Modeled as standard pouch cell `LP401040` (4.00 mm thick x 10.50 mm wide x 40.00 mm long, 300 mAh nominal).
- **Cradle Retention**: Sits in snap-in cradle `05_Battery_Cradle` (Z = 72.00 mm to 118.00 mm).
- **Refill Movement Axis**: The D1 ink refill pushrod (`13_Click_Ratchet_and_Pushrod`) travels along the central axis (X = 0.00 mm, Y = -0.50 mm) from Z = 68.50 mm to 140.00 mm.
- **Clearance to Pushrod**: Minimum radial clearance between the pushrod and battery cradle upper lip is 0.70 mm. Click stroke of 2.50 mm does not contact the battery or wiring exit tabs.
- **Swelling Assessment**: Cradle depth is 4.60 mm for a 4.00 mm nominal cell, providing **0.60 mm (15%) vertical expansion margin**. However, because real pouch cells with integrated protection circuits (PCM) often measure 42–44 mm in length, physical fit must be verified with real vendor samples.

### Rear Click Mechanism & Pocket Clip
- **Clicker**: Two-stage ratchet mechanism (`13_Click_Ratchet_and_Pushrod`) with return spring (`make_spring_solid`, wire diameter 0.40 mm, 8 coils, compressed length 12.0 mm).
- **Pocket Clip (`09_Pocket_Clip`)**: Spring steel clip mounted to the rear cap at Z = 120.00 mm to 148.00 mm. Protrudes 2.80 mm radially beyond the barrel OD (R_max = 10.55 mm).

---

## 5. Mechanical Collision & Toolchain Limitation Analysis

### Toolchain Audit
An attempt was made to run live automated solid boundary representation (BRep) clash detection using CadQuery and OpenCASCADE:
```powershell
python -c "import cadquery; import OCP"
```
**Result**: `ModuleNotFoundError: No module named 'cadquery'` and `No module named 'OCP'`.

### Compliance with Engineering Integrity Rules 6 & 7
- **Rule 6**: *"Never claim successful mechanical collision verification using only hardcoded dimensions."*
- **Rule 7**: *"Do not treat a watertight STL as proof of mechanical fit."*

While the existing script `scripts/validate_assembly_motion_and_clash.py` verified that bounding boxes and nominal analytical cylinders do not overlap, **this does not constitute true 3D solid BRep intersection verification**. Complex geometries (such as the 30° helical bayonet lugs, internal wire routing channels, and FPC flex radii) cannot be certified as collision-free without native CAD kernel boolean operations or physical 3D print validation.

### Final Verification Status
- Overall Dimensional Envelope (R1): **PASS** (153.50 mm length, 15.50 mm OD).
- Mechanical Architecture (R2, R3, R4): **PASS** (Geometry correctly modeled).
- Solid BRep Collision Verification: **NOT VERIFIED** (Pending OpenCASCADE/CadQuery BRep environment).
- Physical Part Tolerancing & Swelling Fit: **NOT VERIFIED** (Pending 3D-printed SLA prototype).
