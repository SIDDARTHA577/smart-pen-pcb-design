# Smart Pen Rev G — Phase 4 Entry Gate Quality Decision
**Document ID:** QA-REVG-P3C-007  
**Project:** Smart Pen Hardware Architecture Revision G  
**Variant:** Four-Layer Evaluation Candidate (`output/RevG/variants/FourLayer_Candidate/SmartPen.kicad_pcb`)  
**Git Branch:** `engineering/revg-production`  
**Base Commit:** `f2a5f6abcaab005d61fdd049388b3ac86db68193`  
**Date:** November 16, 2026  
**Final Quality Gate Determination:** **PHASE 3C QA BLOCKED — CORRECTIONS STILL REQUIRED**  

---

## 1. Executive Summary & Purpose

This document constitutes the formal Quality Assurance and Phase Entry Decision for the Smart Pen Revision G project. It evaluates the engineering integrity, source code cleanliness, native KiCad 10 Design Rule Check (DRC) / Electrical Rules Check (ERC) performance, plane integrity, component identities, power safety, and mechanical envelope compatibility of the four-layer candidate PCB design.

While the physical PCB routing has achieved complete electrical closure with **0 DRC errors, 0 DRC warnings, 0 unconnected pads, and 0 schematic parity discrepancies**, several fundamental hardware specification and signal integrity blockers remain unresolved. Under strict independent engineering oversight, **Phase 4 (Production Gerber Generation, Panelization, and Enclosure Tooling) CANNOT proceed** until the client and engineering stakeholders resolve the critical hardware blockers detailed herein.

---

## 2. Comprehensive Quality Gate Audit Matrix (Tasks 1–8)

| Gate Task | Audit Focus | Verified Findings | Gate Status |
| :--- | :--- | :--- | :---: |
| **Task 1: Pending Files Audit** | 557 untracked Git files in working tree | All 557 files identified as temporary exploratory Python scripts. Full non-destructive ZIP archive created at `backups/Phase03C_uncommitted_scripts_backup.zip` (388 KB). 548 temporary files pruned; 9 reusable engineering scripts retained. `.gitignore` updated with narrow targeted rules. | **PASSED** |
| **Task 2: KiCad 10 DRC/ERC** | Native KiCad 10.0.7 verification of 4-layer candidate | Re-ran native `kicad-cli pcb drc` with `--schematic-parity` and `--all-track-errors`. **Exit Code: 0**. Violations: 0. Unconnected: 0. Parity errors: 0. Warnings: 0. Native `kicad-cli sch erc`: **Exit Code: 0**. 0 errors, 0 warnings. | **PASSED** |
| **Task 3: D4 Footprint Mismatch** | `1N5819HW-7-F` SOD-123 footprint conflict | Resolved library mismatch without compromising manufacturability. Created dedicated `SmartPen:D4` footprint (`output/RevG/variants/FourLayer_Candidate/SmartPen.pretty/D4.kicad_mod`) with 0.80 × 0.90 mm pads (IPC-7351 Level C compliant). Preserved `SmartPen:D3` for D3 (1.10 × 1.00 mm pads). Updated schematic, PCB, and symbol library. Library footprint mismatches reduced from 1 to **0**. | **PASSED** |
| **Task 4: Four-Layer Plane Audit** | Ground (`In1.Cu`) and 3.3V (`In2.Cu`) integrity | **Discrepancy Uncovered:** Previous reports claimed In1.Cu was an "uninterrupted, solid GND plane". Physical audit revealed **82 signal segments** (77 `/SD_MISO`, 5 `/SD_MOSI`) on In1.Cu spanning X=40.60 to 58.65 mm, creating a transverse slot under the RF matching network (L2, C8, C9) and J_RF. Furthermore, **34 signal segments** (including USB DP/DM) cross In2.Cu. Return path discontinuities and RF coupling risks documented. | **BLOCKED** *(Engineering Remediation Required)* |
| **Task 5: Component Reconciliation** | True BOM & interface definitions | Verified true silicon: U1 is bare QFN-32 SoC `ESP32-C3FH4X` (not an ESP32-C3-MINI-1 module). J_SD is a 6-pin 0.5 mm pitch FFC receptacle `FH12-6S-0.5SH(55)` leading to external carrier (not a directly mounted Molex socket). J_RF is a surface-mount `U.FL-R-SMT-1(10)` receptacle; **no antenna exists on-board**. Antenna pigtail and element missing from BOM. | **BLOCKED** *(Client BOM Selection Required)* |
| **Task 6: Battery & Power Audit** | Charging, power handover, LiPo safety | Verified 100 mA constant-current charge rate ($R_9 = 10\text{ k}\Omega$). Q2 P-MOSFET and D4 Schottky power handover verified. **Critical Safety Finding:** No battery protection IC exists on PCB. Mandatory requirement for external pouch cell with integrated PCM. However, no specific manufacturer part number, datasheet, or physical cell has been approved by the client. | **BLOCKED** *(Client Procurement Sign-off Required)* |
| **Task 7: Mechanical Preflight** | Pen envelope, USB cutout, FFC routing | Overall dimensions ($150\text{--}155\text{ mm}$ length, $15\text{--}16\text{ mm}$ OD, $84 \times 9.2\text{ mm}$ PCB) fit barrel ID ($13.5\text{ mm}$). USB-C receptacle ($3.16\text{ mm}$ height) requires precision side slot. FFC routing past refill clicker is tight ($1.5\text{ mm}$ clearance). Enclosure material constraint: Metal barrel blocks 2.4 GHz RF; plastic barrel or RF window mandatory. | **BLOCKED** *(Enclosure Material Sign-off Required)* |
| **Task 8: Doc & Test Repair** | Fix title blocks, thickness, test suite | Corrected PCB title block to "Smart Pen Hardware System - Revision G (4-Layer)". Reconciled project thickness default to 1.60 mm. Purged false claims of FCC/CE compliance and proven eye diagrams. Rewrote `tests/test_revg_phase3c.py` with direct S-expression parsing and live native DRC test runner. 104/104 tests passed. Raw evidence saved in `reports/RevG/Phase03C/qa_raw/`. | **PASSED** |

---

## 3. Detailed Audit of Preserved Blockers

### Blocker 1: Battery Specification & PCM Certification (Client Procurement Blocker)
- **Defect:** The design documentation previously cited generic or unverified "08250 120 mAh" cylindrical cells or arbitrary pouch cells without manufacturer verification.
- **Circuit Reality:** The main board lacks an onboard lithium-ion battery management protection circuit (over-charge, over-discharge, short-circuit cutoffs). If an unprotected bare cell is connected to `J_BAT`, severe fire and thermal runaway hazards exist.
- **Requirement:** The client must select and formally sign off on a specific, commercially available lithium-polymer pouch cell (or custom cylindrical cell) with:
  1. An identifiable manufacturer and exact part number.
  2. An official engineering datasheet with guaranteed physical dimensions ($\le 35.0 \times 10.5 \times 4.5\text{ mm}$).
  3. Integrated certified Protection Circuit Module (PCM) incorporating Seiko/RichTek or equivalent controller with dual MOSFET switch.
  4. Pre-crimped wire leads terminating in a JST SHR-02V-S-B connector matching `J_BAT` pinout (Pin 1: VBAT, Pin 2: GND).

### Blocker 2: External 2.4 GHz RF Antenna & Transmission Line Deliverable
- **Defect:** Engineering summaries claimed "verified RF performance". In reality, the board terminates RF output at `J_RF` (Hirose U.FL receptacle). There is no onboard trace antenna, ceramic chip antenna, or modeled radiator.
- **Integration Risk:** An RF transmitter without an antenna cannot operate. If a metal (aluminum/brass) pen enclosure is selected by the industrial design team, 2.4 GHz Wi-Fi/BLE signals will be completely shielded (Faraday cage effect).
- **Requirement:**
  1. Client ID team must specify enclosure material (plastic or metal with dielectric RF window).
  2. Specification and procurement of a miniature IPEX/U.FL coaxial pigtail cable ($0.81\text{ mm}$ or $1.13\text{ mm}$ OD) and flexible printed circuit (FPC) or wire dipole antenna.
  3. Physical routing path and antenna placement within the pen cap or nose cone must be modeled in Phase 4 CAD.

### Blocker 3: Ground Plane Slotting on In1.Cu Beneath RF Section
- **Defect:** 82 trace segments belonging to the high-speed SPI bus (`/SD_MISO` and `/SD_MOSI`) traverse internal layer `In1.Cu` between X=40.60 mm and X=58.65 mm.
- **Electrical Consequence:** This routing creates an $18\text{ mm}$ slot across the ground plane directly underneath the RF matching network (inductor L2, capacitors C8, C9) and the U.FL connector (`J_RF`).
- **Signal Integrity Risk:** High-frequency RF ground return currents cannot take the path of least inductance directly under the $50\,\Omega$ microstrip on F.Cu. Instead, return currents are forced around the slot, coupling 20–25 MHz SPI edge transients into the RF frontend and degrading receiver sensitivity.
- **Requirement:** While technically passing 2D geometric DRC, this routing layout represents an electrical defect. Engineering must determine whether to:
  - *Option A:* Reroute `/SD_MISO` and `/SD_MOSI` onto `B.Cu` (bottom layer) to restore an unbroken, continuous ground reference plane on `In1.Cu` beneath the entire RF and digital core.
  - *Option B:* Document and client-accept the signal integrity compromise prior to board release.

### Blocker 4: USB 2.0 Differential Pair Routing across Power Plane (`In2.Cu`)
- **Defect:** Traces `/USB_DP_PORT`, `/USB_DM_PORT`, `/USB_DP_CORE`, and `/USB_DM_CORE` route across internal layer `In2.Cu` (the $+3.3\text{V}$ power plane), introducing 34 segment discontinuities.
- **Consequence:** USB Full-Speed (12 Mbps) signals experience impedance mismatches and reference plane transitions without dedicated adjacent ground stitching vias.
- **Requirement:** Physical TDR or 3D field-solver modeling must verify differential impedance ($90\,\Omega \pm 10\%$), or traces should be consolidated onto external signal layers with continuous ground reference.

---

## 4. Integrity of Preserved Baselines

In strict adherence to project safety rules:
1. **Revision F Baselines:** Completely untouched.
   - `output/RevF_Client_Delivery/`: 0 files modified.
   - `output/RevF_Working/`: 0 files modified.
2. **Revision G 2-Layer Preserved Baseline:** Completely untouched.
   - `output/RevG/SmartPen.kicad_pcb` SHA-256: `8c009f538546edf97c99e08f7c750a99cba3f18931d3e7d77b7e5b2d2c4353dd` (Verified byte-for-byte identical to origin).
3. **Branch Hygiene:** Working tree cleaned of 548 temporary scripts, 9 permanent scripts retained, all uncommitted exploratory history preserved in `backups/Phase03C_uncommitted_scripts_backup.zip`.

---

## 5. Formal Quality Gate Determination

```
================================================================================
                    FINAL QUALITY GATE DECISION: PHASE 3C
================================================================================

 [X] PHASE 3C QA BLOCKED — CORRECTIONS STILL REQUIRED

     Rationale:
     Although the physical KiCad 10 layout achieves 100% routing closure and
     zero DRC/ERC/schematic parity errors, Phase 4 entry is strictly BLOCKED
     due to four critical dependencies:

     1. Unspecified battery cell part number, datasheet, and integrated PCM.
     2. Missing 2.4 GHz RF antenna specification and enclosure RF windowing.
     3. Signal return path slotting on In1.Cu beneath the RF front-end.
     4. Unverified USB differential impedance across the In2.Cu plane.

     Phase 4 mechanical enclosure design, panelization, and Gerber manufacturing
     CANNOT commence until the client formalizes these architecture decisions.
================================================================================
```

---

## 6. Action Plan for Phase 4 Unblocking

To achieve unblocking and authorize transition to Phase 4:

1. **Client Action 1 (Battery):** Authorize specific LiPo pouch cell manufacturer part number (e.g., Renata, EEMB, or Grepow) with integrated PCM meeting maximum dimensions $35.0 \times 10.5 \times 4.5\text{ mm}$.
2. **Client Action 2 (Antenna & ID):** Specify pen barrel material. If aluminum alloy, authorize plastic RF window or exterior dipole. Select U.FL pigtail cable part number and FPC antenna element.
3. **Engineering Action 3 (PCB Reroute):** Execute targeted reroute of `/SD_MISO` and `/SD_MOSI` from `In1.Cu` to `B.Cu` to close the ground plane slot under U1 and J_RF, restoring an unbroken GND plane on `In1.Cu`.
4. **Engineering Action 4 (Simulations):** Perform 2D/3D field solver simulation of USB 2.0 Full-Speed differential pairs to verify eye-diagram compliance prior to Gerber generation.

---
**Report Author:** Antigravity Senior Independent QA Auditor  
**Lead Verification Engineer:** KiCad 10 Native Automation Harness  
**Sign-off Status:** Submitted for Client Review — Execution Halted (STOP)
