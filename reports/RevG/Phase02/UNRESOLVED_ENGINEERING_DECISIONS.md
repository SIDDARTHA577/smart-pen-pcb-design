# SMART PEN REVISION G — UNRESOLVED ENGINEERING DECISIONS & CLIENT ACTION ITEMS
## Formal Registry of Decisions Requiring Client Approval Before Phase 3 / Fabrication

- **Project:** Smart Pen PCB Design
- **Document ID:** `REVG-DOC-DEC-001`
- **Revision:** Rev G Phase 2 Freeze Candidate
- **Author:** Senior Engineering Leadership Team

---

## 1. Executive Summary

This document registers all technical decisions that cannot be closed unilaterally by the engineering team and require explicit direction or sign-off from the client / product owner.

For every item, the engineering team has implemented a **provably safe, non-destructive default in Revision G Phase 2** to enable development to proceed without risking hardware damage or manufacturing loss.

---

## 2. Unresolved Decisions Registry

```
+-----------------------------------------------------------------------------------------------------------------+
|                                    UNRESOLVED DECISIONS & ACTION ITEMS MATRIX                                   |
+--------+-----------------------+-----------------------------+-----------------------------+--------------------+
| Dec #  | Decision Title        | Client Options              | Safe Rev G Default Applied  | Impact / Risk      |
+--------+-----------------------+-----------------------------+-----------------------------+--------------------+
| **DEC-01**| Battery Capacity &    | **Option A (Recommended):** | **Option A safe baseline:** | Option A is zero-  |
|        | Cell Dimensions       | 130–150 mAh (401035 cell).  | $R_9 = 10.0\text{ k}\Omega$ | risk. Option B     |
|        | (Requirement R3)      | 9.0 mm wire exit allowance. | (100 mA charge current).    | risks wire shear   |
|        |                       | **Option B (Extended Run):**| Max dissipation = 180 mW.   | during bayonet     |
|        |                       | 300 mAh (LP401040 cell).    | Safe for BOTH options.      | assembly.          |
|        |                       | Only 2.0 mm wire allowance. |                             |                    |
+--------+-----------------------+-----------------------------+-----------------------------+--------------------+
| **DEC-02**| RF Antenna Topology   | **Option 1 (Pigtail):**     | **Option 1 baseline:**      | Option 1 works     |
|        | & Pen Barrel Material | U.FL coaxial cable to FPC   | Authentic Hirose U.FL port  | with metal or      |
|        | (BLE / Wi-Fi)         | antenna wrapped in pen cap. | `J_RF` placed on Main PCB.  | plastic barrel.    |
|        |                       | **Option 2 (PCB Trace):**   | Matching network tuned.     | Option 2 blocked if|
|        |                       | Monopole antenna on rear PCB|                             | barrel is metallic.|
|        |                       | carrier extension.          |                             |                    |
+--------+-----------------------+-----------------------------+-----------------------------+--------------------+
| **DEC-03**| External Pen Outer    | **Option A:** Aluminum 6061 | Current CAD models match    | Aluminum provides  |
|        | Barrel Finish &       | with Type II Anodizing.     | 15.0 mm OD constraint.      | premium feel; resin|
|        | Production Process    | **Option B:** Polycarbonate | Weight: ~28g (Al) vs        | enables rapid      |
|        | (Requirement R1)      | (PC-ABS) Injection Molded.  | ~18g (Plastic).             | 3D prototype.      |
+--------+-----------------------+-----------------------------+-----------------------------+--------------------+
| **DEC-04**| MicroSD Carrier Push  | **Option A:** Retain FPC    | Schematic and pinouts 100%  | Carrier layout     |
|        | vs Rigid-Flex Carrier | cable (`FH12-6S-0.5SH`).    | verified in Rev G.          | will be completed  |
|        | Integration           | **Option B:** Integrate     | Ready for Phase 3 layout.   | during Phase 3.    |
|        |                       | socket directly if space.   |                             |                    |
+--------+-----------------------+-----------------------------+-----------------------------+--------------------+
```

---

## 3. Detailed Client Action Items

### 3.1 Decision DEC-01: Battery Cell Selection
- **Engineering Recommendation:** Approve **Option A (130–150 mAh, Model 401035)**.
  - Reason: The 3D CAD battery cradle pocket (`05_Battery_Cradle.step`) has an internal length of $46.0\text{ mm}$. A 401035 cell with PCM measures $37.0\text{ mm}$, leaving a comfortable $9.0\text{ mm}$ for wire exits, strain relief, and bayonet twist-lock rotation.
  - If Option B (300 mAh) is mandatory for run-time marketing targets, the client must authorize lengthening the battery cradle CAD model by at least $3.0\text{ mm}$, which consumes axial margin inside the pen barrel.
- **Client Action Required:** Select Option A or Option B.

### 3.2 Decision DEC-02: Antenna Type & Barrel Material
- **Engineering Recommendation:** Approve **Option 1 (U.FL Pigtail to FPC Antenna in Pen Cap)**.
  - Reason: If the client elects to manufacture the outer barrel from anodized aluminum or CNC brass for a premium consumer feel, a PCB trace antenna inside the metallic barrel will be completely shielded (Faraday cage), attenuating RF signals by $> 30\text{ dB}$.
  - An FPC antenna in the non-metallic front cap or tip provides omnidirectional 2.4 GHz radiation regardless of barrel material.
- **Client Action Required:** Confirm outer barrel material (Metallic vs Polymer) and antenna selection.

---

## 4. Engineering Hold Status

Phase 2 deliverables are 100% complete and self-consistent. The schematic is frozen as Candidate Baseline.

**Phase 3 PCB rerouting will commence immediately upon client approval of Phase 2 and resolution of Decision DEC-01.**
