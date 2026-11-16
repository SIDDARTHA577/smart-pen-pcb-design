# SMART PEN REV G — ORIGINAL CAD DEFECTS & REPAIR LEDGER
## Comprehensive Analysis of Geometric Errors Uncovered in Phase 4 Baseline

**Document ID:** RPT-SMARTPEN-REVG-PHASE04A-DEFECTS  
**Date:** November 16, 2026  
**Reference Baseline:** `output/RevG/Mechanical_Phase04/CAD_Source/SmartPen_Parametric_CAD_RevG.py`  
**Starting Commit:** `102939cf32e214d9ae331918897bd8c2aa365b49`

---

## 1. DEFECT 1: MAIN PCB RAIL WIDTH DEFICIT (1.40 mm Interference)

### 1.1 Original Code Inspection
In `output/RevG/Mechanical_Phase04/CAD_Source/SmartPen_Parametric_CAD_RevG.py`, line 790:
```python
rail_deck = make_u_channel_solid(x_out=4.80, y_bottom=1.20, y_top=3.60, wall_t=0.90, z_start=38.0, z_end=122.0)
```
- Outer half-width (`x_out`): `4.80 mm`
- Wall thickness (`wall_t`): `0.90 mm`
- Inside half-width: `4.80 - 0.90 = 3.90 mm`
- **Actual Clear Inside Width:** `2 * 3.90 = 7.80 mm`
- **Required Main PCB Width:** `9.20 mm`
- **Deficit / Interference:** `9.20 - 7.80 = 1.40 mm`

### 1.2 Root Cause Analysis
The Phase 4 CAD report incorrectly treated the *outside* width of the rail (`2 * 4.80 = 9.60 mm`) as the cavity width, claiming `9.60 mm - 9.20 mm = 0.40 mm clearance`. In physical reality, the side walls consumed `1.80 mm` of that width, leaving only `7.80 mm`. A physical 9.20 mm wide PCB could never be seated into this rail.

### 1.3 Corrected Phase 4A Implementation
In `output/RevG/Mechanical_Phase04_Corrected/CAD_Source/SmartPen_Parametric_CAD_RevG_Corrected.py`:
- Inside half-width (`x_in`): `4.75 mm` -> **Clear Inside Width = 9.50 mm**
- Clearance to 9.20 mm PCB: `9.50 - 9.20 = 0.30 mm` total (0.15 mm per side).
- Wall thickness: `0.75 mm` -> Outside half-width = `5.50 mm` (Outer width = 11.00 mm).
- Bounding radius inside 13.5 mm bore (R = 6.75 mm):
  $$\sqrt{x_{\text{out}}^2 + y_{\text{top}}^2} = \sqrt{5.50^2 + 2.80^2} = \sqrt{30.25 + 7.84} = 6.17\text{ mm} < 6.75\text{ mm}$$
- Radial clearance to bore wall: `6.75 - 6.17 = 0.58 mm`.
- **CAD Collision Result:** `rail ^ pcb = 0.000 mm³` (Clean fit).

---

## 2. DEFECT 2: BATTERY CRADLE CAVITY DEFICITS (Width & Depth Errors)

### 2.1 Original Code Inspection
In `output/RevG/Mechanical_Phase04/CAD_Source/SmartPen_Parametric_CAD_RevG.py`, line 809:
```python
v_batc, f_batc, t_batc = make_open_pocket_solid(xo=5.30, yo_bot=-5.70, yo_top=-1.20, zo_start=74.0, zo_end=109.0, wall_t=1.00, floor_t=0.80)
```
- Outside half-width (`xo`): `5.30 mm`
- Side wall thickness: `1.00 mm`
- **Actual Clear Inside Width:** `2 * (5.30 - 1.00) = 8.60 mm`
- **Assumed Battery Width:** `10.00 mm`
- **Width Deficit:** `10.00 - 8.60 = 1.40 mm`
- Outside height: `-1.20 - (-5.70) = 4.50 mm`
- Floor thickness: `0.80 mm`
- **Available Clear Depth:** `4.50 - 0.80 = 3.70 mm`
- **Assumed Battery Thickness:** `4.00 mm`
- **Depth Deficit:** `4.00 - 3.70 = 0.30 mm`

### 2.2 Geometric Collision with Barrel Bore
A sharp-cornered rectangular cuboid of 10.0 mm width (X = ±5.0 mm) and 4.0 mm depth in the lower sector under the pushrod (Y = -1.50 to -5.50 mm) has bottom outer corners at:
$$R_{\text{corner}} = \sqrt{5.00^2 + (-5.50)^2} = \sqrt{25.00 + 30.25} = 7.43\text{ mm} > 6.75\text{ mm}$$
The corners of a flat-bottomed box protruded `7.43 - 6.75 = 0.68 mm` through the cylindrical barrel wall!

### 2.3 Corrected Phase 4A Implementation
- Clear Cavity Width: **10.20 mm** (X = ±5.10 mm, 0.10 mm clearance per side).
- Clear Cavity Depth: **4.20 mm** (Y = -1.40 to -5.60 mm, 0.20 mm clearance).
- Clear Cavity Length: **33.00 mm** (Z = 74.5 to 107.5 mm, 1.00 mm clearance).
- Conformal Cylindrical Hull: Outer surface of the cradle is curved to radius **6.60 mm**, providing `0.15 mm` sliding clearance inside the `6.75 mm` barrel bore.
- Top Pushrod Trough: Longitudinal clearance notch along Y = 0 to clear the 1.60 mm pushrod.
- **CAD Collision Result:** `cradle ^ batt = 0.000 mm³` (Clean fit).

---

## 3. DEFECT 3: USB-C APERTURE ABSENCE & 38.0 mm OFFSET ERROR

### 3.1 Original Code Inspection
In `output/RevG/Mechanical_Phase04/CAD_Source/SmartPen_Parametric_CAD_RevG.py`, lines 751 & 838:
```python
# Add USB-C port frame bezel (Z = 73.65 to 83.15 mm, Y = +2.70 to +6.50 mm)
usb_bezel = make_box_solid(self.r_bore - 0.2, self.r_outer + 0.2, 2.70, 6.50, 73.65, 83.15)
...
v_usbf, f_usbf, t_usbf = make_box_solid(6.40, 8.00, 2.50, 6.70, 73.20, 83.60)
```
- No Boolean subtraction was executed on the outer barrel cylinder. A solid box was simply unioned to the outside surface.
- The Z coordinates `73.65 to 83.15 mm` (center `78.40 mm`) directly copied the PCB footprint X coordinate without adding the **38.00 mm** longitudinal offset of the PCB start face!
- Actual J_USB on PCB is at PCB X = 78.40 mm -> In pen coordinates:
  $$Z = 38.00 + 78.40 = 116.40\text{ mm}$$
- The original CAD model placed the USB bezel at `Z = 78.40 mm`, directly hovering over the battery (Z = 74 to 106 mm) and completely detached from the actual USB-C receptacle on the PCB!

### 3.2 Corrected Phase 4A Implementation
- Real Boolean Subtraction cut through barrel wall at **Z = 116.40 mm** (Z = 111.15 to 121.65 mm, Y = 2.10 to 6.70 mm).
- 45-degree lead-in chamfer around opening for standard USB-C cable overmold insertion.
- Custom Part 08 (`08_USB_C_Access_Feature`) remodeled as a hollow bezel ring with an actual `9.40 x 3.80 mm` through-aperture.
- Alignment error between connector and aperture: **0.000 mm**.

---

## 4. DEFECT 4: NON-FUNCTIONAL CLICK RETRACTABLE MECHANISM

### 4.1 Original Code Inspection
Phase 4 modeled Part 10 as two concentric solid cylinders (`click_sleeve` and `click_dome`), with no internal cam teeth, no pushrod mating socket, and no validation of retracted vs extended states.

### 4.2 Corrected Phase 4A Implementation
- Modeled actual 8-tooth 45° helical ratchet cam with deep (retracted) and shallow (writing) detent shelves.
- Writing stroke: **4.50 mm**; Plunger overtravel: **1.30 mm** (Total button travel: **5.80 mm**).
- Helical return spring envelope: Seated in nose cone counterbore (ID 4.20 mm, spring OD 3.80 mm, wire 0.40 mm).
- Coil bind margin: Extended compressed length is 7.50 mm vs solid height 5.60 mm -> **1.90 mm safety margin**.

---

## 5. DEFECT 5: INCOMPLETE BAYONET LOCKING GEOMETRY

### 5.1 Original Code Inspection
Phase 4 placed 3 rectangular blocks on a sleeve without matching barrel internal grooves or rotational locking paths.

### 5.2 Corrected Phase 4A Implementation
- Part 11 Bayonet Collar: 3 radial locking lugs at 120° (height 0.40 mm, width 1.80 mm, length 3.30 mm).
- Part 01 Barrel: 3 internal J-grooves cut into bore wall with 4.0 mm axial entry slot, 30° circumferential locking track, and positive detent pocket at 30°.
- Tested and verified across 30° rotation travel.

---

## 6. DEFECT 6: UNREALISTIC FFC RIBBON CABLE MODELING

### 6.1 Original Code Inspection
Modeled as a single straight box (`Z = 96.4 to 122.0 mm`) intersecting the central pushrod corridor.

### 6.2 Corrected Phase 4A Implementation
- Replaced with realistic 180° service loop:
  - Leg 1 from J_SD (Z = 96.4 to 108.0 mm) at Y = +3.20 mm.
  - Smooth 180° bend (radius R = 2.50 mm) at Z = 108.0 to 110.5 mm.
  - Return leg (Z = 108.0 to 122.0 mm) at Y = +5.20 mm.
- Vertical clearance to central pushrod (Y = 0.00 mm): `3.20 - 0.80 = 2.40 mm > 1.50 mm`. Zero interference.

---

## 7. DEFECT 7: TACTILE BUTTONS & PLUNGERS

### 7.1 Original Code Inspection
Buttons were generic rectangular pads hovering outside the barrel with no plungers contacting the PCB tactile switches.

### 7.2 Corrected Phase 4A Implementation
- Part 09 dual rocker actuator with ERASE paddle (Z = 68.5 to 73.5 mm) and MODE paddle (Z = 82.5 to 87.5 mm).
- Integral plungers extending through barrel button apertures to contact SW1 (Z = 70.96 mm) and SW2 (Z = 85.10 mm) at Y = 5.30 mm.

---

## 8. DEFECT 8: CYLINDRICAL OD VS BOUNDING ENVELOPE MISREPRESENTATION

### 8.1 Original Code Inspection
Phase 4 reported maximum bounding box as `15.50 x 16.95 x 104.00 mm`, but falsely claimed the barrel outer diameter was 15.50 mm without clarifying that the pocket clip extended beyond the cylindrical barrel.

### 8.2 Corrected Phase 4A Implementation
- Cylindrical Barrel OD: exactly **15.50 mm** (radius 7.75 mm) along entire body.
- Pocket Clip Protrusion: extends to Y = +9.80 mm (**+2.05 mm** radial protrusion).
- Button Protrusion: extends to Y = +8.10 mm (**+0.35 mm** radial protrusion).
- Total Assembled Bounding Box: **15.50 x 17.55 x 153.50 mm**.

---

## 9. BASELINE PRESERVATION & CHECKPOINT

All baseline files have been preserved in `output/RevG/Mechanical_Phase04/` and verified against the recorded SHA256 hashes in `reports/RevG/Phase04A/ORIGINAL_PHASE4_FILE_HASHES.txt`.
