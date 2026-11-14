# SMART PEN REV G — MANUFACTURING & MECHANICAL BLOCKERS REGISTER

**Document ID:** `SP-REVG-P3B-010`  
**Status:** FORMAL BLOCKED ITEMS IDENTIFIED  
**Target Milestone:** Phase 3B Review & Phase 4 Preparation  
**Baseline Hardware:** Smart Pen Revision G Prototype  

---

## 1. Executive Summary

In strict compliance with the client mandate:
> "If critical issues remain, clearly state: **PHASE 3B INCOMPLETE — ADDITIONAL CORRECTIONS REQUIRED.** Keep battery manufacturer approval and physical fit in a separate BLOCKED state until validated. Do not proceed to Phase 4, manufacture the PCB, or merge into main."

This register identifies the critical mechanical, electrical, and manufacturing blockers that prevent immediate fabrication release of the Smart Pen Revision G hardware.

Each item is categorized by severity (P0 = Production Blocking, P1 = High Priority Design Requirement) with an exact root-cause analysis, mechanical impact, and required client/engineering resolution.

---

## 2. Active Blocker Register

### Blocker 01 (P0 — MECHANICAL & SAFETY): Battery Cell Physical Cradle & Thermal Expansion HOLD
- **Description:** Lithium-Polymer cell geometry, protection circuit module (PCM) packaging envelope, and thermal swelling clearance remain unvalidated against the physical internal electronics rail.
- **Root Cause:**
  - Client requirements dictate that the battery must rest **BELOW** the removable internal electronics rail inside the $\varnothing 15–16\text{ mm}$ cylindrical pen barrel.
  - The parametric CAD assembly allocates a semi-cylindrical battery trough of nominal dimensions: length $45.0\text{ mm}$, diameter $\varnothing 10.0\text{ mm}$.
  - Commercial 180–250 mAh Li-Po pouch cells (e.g. 501240, 601235, or custom cylinder 09400) specify nominal cell dimensions of $5.0 \times 12.0 \times 40.0\text{ mm}$ or $\varnothing 9.0 \times 40.0\text{ mm}$ *unswelled*.
  - Standard IEC 62133 / UN 38.3 battery certification mandates an allowance of $+8\%$ to $+10\%$ volumetric expansion during continuous 1C cycling and elevated temperature storage ($45^\circ\text{C}$).
  - A fully expanded cell would exert radial hoop stress exceeding the elastic yield point of the 3D-printed internal rail, potentially pinching wire leads or jamming the moving writing refill pushrod.
- **Mechanical Status:** **FORMAL HOLD / BLOCKED**.
- **Required Action:**
  1. Client to supply certified specification sheet and drawing from approved battery cell vendor (e.g., EEMB, Grepow, or Renata) for the exact protected pack part number.
  2. Physical sample of cell with integrated PCM and wire leads must be test-fit inside the CNC/3D-printed rail prototype before releasing Main PCB J_BAT battery lead length.

---

### Blocker 02 (P0 — ELECTRICAL & FABRICATION): 2-Layer Controlled-Impedance Unviability (ECR-003 Approval)
- **Description:** Complete DRC closure and 50 Ω RF / 90 Ω USB controlled-impedance routing cannot be achieved on a 2-layer $84.0 \times 9.2\text{ mm}$ substrate.
- **Root Cause:**
  - As proven by IPC-2141 electromagnetic synthesis (`SP-REVG-P3B-006`), achieving $50\ \Omega$ RF coplanar waveguide on $1.6\text{ mm}$ 2-layer FR4 requires a trace width of **$2.80\text{ mm}$** ($3.60\text{ mm}$ total with coplanar ground gaps), which consumes 39% of the total $9.20\text{ mm}$ board width.
  - 2-layer routing forces digital tracks on `B.Cu` to cross the RF ground return corridor, breaking ground return continuity and introducing unacceptable RF reflection ($S_{11} > -6\text{ dB}$) and antenna desensitization.
  - 144 geometric clearance violations and 67 unconnected net segments remain on the 2-layer layout due to severe spatial overcrowding.
- **Electrical Status:** **FORMAL HOLD / BLOCKED FOR 4-LAYER MIGRATION**.
- **Required Action:**
  1. Client formal approval of Engineering Change Request **ECR-003** (Stackup migration to 4-layer JLC04161H-7628 / JLC2313, 1.0 mm or 1.6 mm thickness).
  2. Estimated PCB fabrication unit cost delta: +$0.18 to +$0.25 per board in 1k volume; yields 100% controlled impedance, unbroken ground return, and zero-violation DRC closure.

---

### Blocker 03 (P1 — INDUSTRIAL DESIGN & HOUSING): USB-C Port Barrel Machining vs. Removable Rail Extraction
- **Description:** Method of user access to the lateral USB-C charging connector must be formally selected by the client.
- **Root Cause:**
  - Rear axial USB mounting was evaluated in Phase 3B Task 3A and conclusively proven **PHYSICALLY IMPOSSIBLE** due to the $9.80\text{ mm}$ connector width overhanging the $9.20\text{ mm}$ PCB edges and directly blocking the axial click-mechanism pushrod bore (`13_Click_Ratchet_and_Pushrod.step`).
  - Lateral side-mount USB orientation (0° rotation at $X=78.40\text{ mm}$, $Y=4.60\text{ mm}$) is 100% structurally and electrically sound on the PCB.
  - However, plugging a USB-C cable into the side port requires either:
    - **Architecture A (Seamless Slide-Out Rail):** Unlocking the rear bayonet, sliding out the internal chassis rail, and plugging in the cable. Preserves 100% outer barrel hoop strength, prevents water/dust ingress, and requires zero external barrel cutouts.
    - **Architecture B (External Barrel Cutout):** CNC machining a $9.5 \times 3.5\text{ mm}$ slot through the outer aluminum barrel wall, requiring an internal elastomeric sealing boot.
- **Industrial Design Status:** **BLOCKED PENDING CLIENT SELECTION**.
- **Required Action:** Client product management to confirm whether Architecture A (Slide-Out) or Architecture B (External Slot) is the production requirement.

---

### Blocker 04 (P1 — RF INTEGRATION): Metal Enclosure 2.4 GHz RF Shielding Mitigation
- **Description:** Complete metallic enclosure ($\varnothing 15.60\text{ mm}$ OD aluminum tube) attenuates 2.4 GHz Wi-Fi/BLE signals by $> 40\text{ dB}$.
- **Root Cause:**
  - A continuous metallic cylinder forms an electromagnetic Faraday cage around the internal ceramic chip antenna (`AE1`).
  - Radiated efficiency will be unacceptable without an RF-transparent window.
- **RF Status:** **DOCUMENTED HOLD FOR HOUSING DETAIL**.
- **Required Action:** Client industrial design must confirm an RF-transparent window material (ABS, Polycarbonate, or Zirconia Ceramic) on the pen nose cone or cap, or a longitudinal RF slot in the barrel wall.

---

## 3. Mandatory Client Gate Summary

Until the client provides formal sign-off on:
1. **ECR-003 (4-Layer Stackup Migration)**
2. **Li-Po Battery Cell Part Number & Verified Pouch Dimensions**
3. **USB-C Housing Access Selection (Option A vs Option B)**

The Smart Pen Revision G Main PCB design must remain in **DEVELOPMENT STATUS ON BRANCH `engineering/revg-production`**.

Physical fabrication of boards, ordering of SMT stencils, and merging into `main` are strictly prohibited.
