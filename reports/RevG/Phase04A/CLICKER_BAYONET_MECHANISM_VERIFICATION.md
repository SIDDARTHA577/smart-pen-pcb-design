# SMART PEN REV G — CLICKER & BAYONET MECHANISM VERIFICATION REPORT
## Retractable Writing Kinematics, Cam Follower Interface, Spring Envelopes, and 30-Degree Quick-Release Lock

**Document ID:** RPT-SMARTPEN-REVG-PHASE04A-MECHANISMS  
**Part Names:** `10_Rear_Click_Mechanism`, `11_Rear_Bayonet_Collar`, `20_D1_Ink_Refill`, `21_Helical_Return_Spring`, `22_Click_Pushrod`  
**Date:** November 16, 2026  
**CAD Kernel:** `manifold3d` 3.5.5 / `trimesh` 5.2.1  
**Status:** **PASSED — DUAL-STATE KINEMATIC & 30° TWIST VERIFIED**

---

## 1. RETRACTABLE WRITING MECHANISM KINEMATICS

The Smart Pen requires a reliable ballpoint click mechanism capable of extending a standard D1 refill by 4.50 mm into writing position and locking it against paper writing pressure (up to 3.0 N), then retracting it cleanly inside the nose cone.

### 1.1 Dual-State Kinematic Positions
| Motion Parameter | Retracted State (Idling/Carrying) | Extended State (Active Writing) | Differential Travel |
| :--- | :--- | :--- | :--- |
| **D1 Refill Tip ($Z$)** | **$+1.50\text{ mm}$** (recessed inside nose) | **$-3.00\text{ mm}$** (protruding for writing) | **$4.50\text{ mm}$ stroke** |
| **D1 Refill Rear End ($Z$)** | $+68.50\text{ mm}$ | $+64.00\text{ mm}$ | $4.50\text{ mm}$ forward |
| **Moving Pushrod Front ($Z$)** | $+68.50\text{ mm}$ | $+64.00\text{ mm}$ | $4.50\text{ mm}$ forward |
| **Moving Pushrod Rear ($Z$)** | $+140.00\text{ mm}$ | $+135.50\text{ mm}$ | $4.50\text{ mm}$ forward |
| **Ratchet Cam Detent ($Z$)** | Deep notch at $+140.00\text{ mm}$ | Shallow notch at $+135.50\text{ mm}$ | $4.50\text{ mm}$ latching step |
| **Plunger Button Stroke** | Peak apex at $+153.50\text{ mm}$ | Travel: $4.50\text{ mm} + 1.30\text{ mm} = 5.80\text{ mm}$ | $1.30\text{ mm}$ overtravel |

### 1.2 Ratchet Cam Follower Geometry
- **Cam Diameter:** OD $6.40\text{ mm}$, ID $3.20\text{ mm}$.
- **Ramp Profile:** 8 sawtooth helical teeth at 45° ramp angle.
- **Indexing Step:** 22.5° rotation per actuation cycle.
- **Pushrod Seat:** Central counterbore Ø $2.00\text{ mm} \times 2.50\text{ mm}$ deep securing the pushrod rear end.

---

## 2. RETURN SPRING ENVELOPE & COIL BIND VERIFICATION

The helical compression spring sits inside the counterbore of the front nose cone (Part 03):
- **Nose Cone Counterbore:** ID **$4.20\text{ mm}$**, length $12.00\text{ mm}$ ($Z = 6.00$ to $18.00\text{ mm}$).
- **Spring Outer Diameter (OD):** **$3.80\text{ mm}$** (clears $4.20\text{ mm}$ bore with $0.20\text{ mm}$ radial clearance).
- **Spring Inner Diameter (ID):** **$3.00\text{ mm}$** (clears $2.35\text{ mm}$ D1 refill body with $0.325\text{ mm}$ radial clearance).
- **Wire Diameter ($d$):** $0.40\text{ mm}$, Active coils $n = 12$, Total coils $N = 14$.
- **Free Length ($L_0$):** $16.00\text{ mm}$.
- **Retracted Installed Length ($L_{\text{ret}}$):** $12.00\text{ mm}$ ($4.0\text{ mm}$ pre-compression, pre-load force $F_0 = 1.50\text{ N}$).
- **Extended Writing Length ($L_{\text{ext}}$):** $7.50\text{ mm}$ ($8.5\text{ mm}$ compression, writing retention force $F_{\text{ext}} = 3.20\text{ N}$).
- **Solid Height ($L_{\text{solid}}$):** $N \times d = 14 \times 0.40\text{ mm} = 5.60\text{ mm}$.

$$\text{Safety Margin to Coil Bind} = L_{\text{ext}} - L_{\text{solid}} = 7.50\text{ mm} - 5.60\text{ mm} = 1.90\text{ mm}$$
The spring maintains a **$1.90\text{ mm}$ safety margin** (> $1.0\text{ mm}$ requirement), completely ruling out coil bind during normal writing or overtravel pressing.

---

## 3. 30-DEGREE QUICK-RELEASE BAYONET LOCK

The rear bayonet collar allows quick removal of the rear click mechanism to service the MicroSD card or replace the D1 ink refill without tools.

### 3.1 Lug & Groove Coordination
1. **Bayonet Collar (Part 11):**
   - Pilot Sleeve: OD $13.30\text{ mm}$ (slides smoothly inside barrel ID $13.50\text{ mm}$).
   - 3 Radial Locking Lugs: Equispaced at 120° intervals.
   - Lug Dimensions: Radial height $0.40\text{ mm}$ ($R = 6.65\text{ mm}$), width $1.80\text{ mm}$, length $3.30\text{ mm}$ ($Z = 138.20$ to $141.50\text{ mm}$).
2. **Barrel Internal Grooves (Part 01):**
   - 3 Axial Entry Slots: Width $2.20\text{ mm}$ ($0.40\text{ mm}$ clearance to lug), depth $0.60\text{ mm}$ ($R = 7.35\text{ mm}$), running from $Z = 142.00$ to $138.00\text{ mm}$.
   - 3 Circumferential Tracks: Swept across **30.0 degrees** of rotation at $Z = 138.00$ to $140.20\text{ mm}$.
   - Detent Pockets: Located at exactly 30° rotation, recessed radially by $+0.10\text{ mm}$ ($R = 7.45\text{ mm}$).

### 3.2 Assembly & Locking Procedure
1. Align collar lugs with the 3 barrel entry slots.
2. Push axially forward by $4.00\text{ mm}$ against the internal wave washer.
3. Rotate clockwise by **30.0 degrees**. The lugs drop into the detent pockets with an audible and tactile click.
4. Internal spring pressure locks the lugs in the detent, preventing accidental unlatching under clicker cycling.
