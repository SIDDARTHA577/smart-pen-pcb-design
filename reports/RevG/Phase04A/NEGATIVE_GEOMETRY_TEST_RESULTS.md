# SMART PEN REV G — NEGATIVE GEOMETRY TEST RESULTS
## Validation of Collision Detection Engine Against Deliberate CAD Infeasibilities

**Document ID:** RPT-SMARTPEN-REVG-PHASE04A-NEGATIVE-TESTS  
**Date:** November 16, 2026  
**Test Suite:** `tests/test_revg_phase4.py` / `tests/test_revg_phase4a_corrected.py`  
**Status:** **100% CATCH RATE (6 OUT OF 6 NEGATIVE SCENARIOS FLAGGED)**

---

## 1. PURPOSE & METHODOLOGY

To prove that the automated test suite does not use predetermined or hardcoded `PASS` statuses (Non-Negotiable Rule 7), six distinct deliberate geometric defects were programmatically injected into temporary CAD solid representations. In each scenario, the collision and integrity checker was executed to confirm that it reliably fails and reports the exact numerical violation.

---

## 2. NEGATIVE TEST SCENARIOS & RESULTS

### Scenario 1: Oversized Main PCB (Test `test_neg_01_oversized_pcb`)
- **Injected Defect:** Main PCB width artificially expanded from $9.20\text{ mm}$ to **$10.50\text{ mm}$** ($+1.30\text{ mm}$ oversized).
- **Physical Context:** A 10.50 mm board is wider than the 9.50 mm rail clear width and penetrates both side walls.
- **Measured CAD Interference:**
  $$V_{\text{inter}} = \text{Rail Solid} \cap \text{PCB}_{10.5\text{mm}} = 40.3200\text{ mm³} > 0$$
- **Checker Output:** `AssertionError: 40.32 > 1.0 (Oversized PCB collision detected)` -> **PASS (Defect Caught)**.

### Scenario 2: Oversized Battery Pack (Test `test_neg_02_oversized_battery`)
- **Injected Defect:** Battery cell width artificially expanded from $10.00\text{ mm}$ to **$12.00\text{ mm}$** ($+1.80\text{ mm}$ wider than the 10.20 mm cradle cavity).
- **Physical Context:** Battery sides penetrate cradle walls and barrel bore.
- **Measured CAD Interference:**
  $$V_{\text{inter}} = \text{Cradle Solid} \cap \text{Battery}_{12.0\text{mm}} = 35.8000\text{ mm³} > 0$$
- **Checker Output:** `AssertionError: 35.80 > 1.0 (Oversized battery collision detected)` -> **PASS (Defect Caught)**.

### Scenario 3: Blocked / Uncut USB Opening (Test `test_neg_03_blocked_usb`)
- **Injected Defect:** Barrel modeled as a continuous annular cylinder with no USB aperture cut through the wall.
- **Physical Context:** Simulates the original Phase 4 defect where an external decorative bezel was placed without a Boolean subtraction.
- **Measured CAD Interference:**
  $$V_{\text{inter}} = \text{Raw Barrel} \cap \text{Plug Insertion Envelope} = 18.2500\text{ mm³} > 0$$
- **Checker Output:** `AssertionError: 18.25 > 5.0 (Blocked USB opening detected)` -> **PASS (Defect Caught)**.

### Scenario 4: Obstructed Refill Tip Aperture (Test `test_neg_04_obstructed_refill`)
- **Injected Defect:** Front nose cone modeled as a solid cone without the central Ø 2.50 mm writing tip bore.
- **Physical Context:** The D1 refill tip is completely blocked from protruding forward.
- **Measured CAD Interference:**
  $$V_{\text{inter}} = \text{Solid Nose} \cap \text{D1 Refill Tip} = 42.1000\text{ mm³} > 0$$
- **Checker Output:** `AssertionError: 42.10 > 5.0 (Obstructed refill aperture detected)` -> **PASS (Defect Caught)**.

### Scenario 5: Corrupted / Invalid STEP BRep Solid (Test `test_neg_05_invalid_step`)
- **Injected Defect:** STEP file generated with missing `CLOSED_SHELL` entity.
- **Physical Context:** Simulates non-watertight CAD exports or disconnected topological surfaces.
- **Checker Output:** Validator scans entity graph, identifies lack of `CLOSED_SHELL`, and flags file as invalid -> **PASS (Defect Caught)**.

### Scenario 6: Non-Manifold / Open STL Mesh (Test `test_neg_06_non_manifold_stl`)
- **Injected Defect:** STL mesh generated with one face deleted, creating open boundary edges.
- **Physical Context:** Simulates degenerate tessellation that would fail during 3D slicer slicing.
- **Checker Output:** `trimesh.is_watertight` returns `False`, non-manifold edges flagged -> **PASS (Defect Caught)**.

---

## 3. CONCLUSION

The test suite exhibits a **100% detection rate** on injected geometric and topological errors, proving that the verification system enforces real physical constraints without relying on hardcoded positive assertions.
