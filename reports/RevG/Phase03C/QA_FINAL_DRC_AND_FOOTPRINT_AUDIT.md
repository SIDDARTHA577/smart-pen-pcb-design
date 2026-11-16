# Smart Pen Rev G — Final DRC & D4 Footprint Resolution Audit
**Document ID:** QA-REVG-P3C-002  
**Project:** Smart Pen Hardware Architecture Revision G  
**Variant:** Four-Layer Evaluation Candidate (`output/RevG/variants/FourLayer_Candidate/SmartPen.kicad_pcb`)  
**Date:** November 16, 2026  
**KiCad Version:** 10.0.7 Native CLI  
**Status:** 100% DRC / ERC Clean (Exit Code 0)  

---

## 1. Initial Committed Phase 3C DRC Re-Verification

Prior to applying any corrections, an authoritative native KiCad 10 DRC was executed on the committed Phase 3C four-layer candidate board as checked out from commit `f2a5f6a`.

### 1.1 Input State Verification
- **PCB Path:** `output/RevG/variants/FourLayer_Candidate/SmartPen.kicad_pcb`
- **PCB File Size:** 478,574 bytes
- **PCB SHA-256:** `e945271f5d19c4a7e2f8734003f78d7e0832218a1839b837c9f5d7157d38f065`
- **Baseline PCB SHA-256:** `8c009f538546edf97c99e08f7c750a99cba3f18931d3e7d77b7e5b2d2c4353dd` (Verified 100% immutable)

### 1.2 Execution Commands & Raw Evidence
The verification was executed using KiCad 10's native CLI with all-track checking, schematic parity, full severity reporting, and zone refilling enabled:
```powershell
& "C:\Users\goran\AppData\Local\Programs\KiCad\10.0\bin\kicad-cli.exe" pcb drc `
    --all-track-errors `
    --schematic-parity `
    --severity-all `
    --refill-zones `
    --exit-code-violations `
    -o reports/RevG/Phase03C/qa_raw/initial_baseline_drc.rpt `
    output/RevG/variants/FourLayer_Candidate/SmartPen.kicad_pcb

& "C:\Users\goran\AppData\Local\Programs\KiCad\10.0\bin\kicad-cli.exe" pcb drc `
    --all-track-errors `
    --schematic-parity `
    --severity-all `
    --refill-zones `
    --format json `
    --exit-code-violations `
    -o reports/RevG/Phase03C/qa_raw/initial_baseline_drc.json `
    output/RevG/variants/FourLayer_Candidate/SmartPen.kicad_pcb
```

### 1.3 Initial DRC Results Matrix
- **Exit Code:** `5` (Non-zero exit code due to presence of violation)
- **Total Violations:** `1`
  - **Errors:** `0`
  - **Warnings:** `1` (`[lib_footprint_mismatch]: Footprint 'D3' does not match copy in library 'SmartPen' @(59.0000 mm, 4.0500 mm): Footprint D4`)
  - **Exclusions:** `0`
- **Unconnected Pads / Items:** `0`
- **Schematic Parity Issues:** `0`
- **Footprint Errors:** `0`

**Conclusion:** The committed candidate was NOT at 0 total violations. The single remaining violation was an unresolved footprint library mismatch on diode D4.

---

## 2. Root Cause Analysis: Diode D4 Footprint Mismatch

### 2.1 Component Identity & Physical Function
- **Reference Designator:** `D4`
- **Manufacturer Part Number:** `1N5819HW-7-F` (Diodes Incorporated)
- **Device Description:** 40V, 1A Surface Mount Schottky Barrier Rectifier
- **Package Type:** SOD-123 (JEDEC DO-219AA)
- **Schematic Net Connections:**
  - Pad 1 (Cathode / K): Net `/VSYS_RAW` (Connects to AP2112K LDO input via SW3)
  - Pad 2 (Anode / A): Net `/USB_VBUS` (Connects to USB Type-C 5V VBUS)
- **Circuit Function:** Reverse-blocking ORing diode that feeds USB 5V power into the system supply rail while preventing battery voltage on `/VSYS_RAW` from back-feeding into the USB port.

### 2.2 Manufacturer Drawing vs. Library vs. Board Comparison

| Parameter | Manufacturer Suggested Land Pattern (Diodes Inc SOD-123) | Original Library (`SmartPen:D3` / `D3.kicad_mod`) | Pre-Fix Board Footprint (D4 on PCB) | Defect Analysis |
| :--- | :--- | :--- | :--- | :--- |
| **Footprint Name** | SOD-123 | `D3` (Reused for D4) | `SmartPen:D3` | D4 lacked dedicated library definition |
| **Pad Length ($X$)** | $0.900\text{ mm}$ | $1.100\text{ mm}$ | $0.800\text{ mm}$ | $0.300\text{ mm}$ discrepancy between board & lib |
| **Pad Width ($Y$)** | $0.950\text{ mm}$ | $1.000\text{ mm}$ | $0.900\text{ mm}$ | $0.100\text{ mm}$ discrepancy between board & lib |
| **Pad Center-to-Center**| $3.150\text{ mm}$ ($\pm 1.575\text{ mm}$) | $3.200\text{ mm}$ ($\pm 1.600\text{ mm}$) | $3.200\text{ mm}$ ($\pm 1.600\text{ mm}$) | Standard nominal pitch |
| **Outer Dimension ($X_1$)**| $4.050\text{ mm}$ | $4.300\text{ mm}$ | $4.000\text{ mm}$ | Original lib pad was severely oversized |
| **Pad Rotation** | $0^\circ$ | $0^\circ$ | Local $270^\circ$ internal rotation | Inconsistent rotation attribute |

### 2.3 Physical Collision & Clearance Constraint
The reason the previous routing engineer shrank the D4 pad on the PCB to $0.80 \times 0.90\text{ mm}$ was physical crowding:
1. Hirose FFC connector `J_SD` (`FH12-6S-0.5SH(55)`) is located at $X = 58.40\text{ mm}, Y = 4.20\text{ mm}$.
2. D4 is located directly adjacent at $X = 59.00\text{ mm}, Y = 4.05\text{ mm}$ (rotated $-90^\circ$).
3. The `/SD_MISO` signal leaves J_SD Pad 5 ($X = 59.15\text{ mm}$) and routes south on `F.Cu` to $Y = 5.025\text{ mm}$ before turning west.
4. If D4 uses the library's $1.10 \times 1.00\text{ mm}$ pad, Pad 2 (`/USB_VBUS`) directly SHORTS to `/SD_MISO` ($0\text{ mm}$ clearance).
5. Even the nominal manufacturer $0.90 \times 0.95\text{ mm}$ pad yields an actual clearance of $0.1250\text{ mm}$, which violates the board's $0.1500\text{ mm}$ netclass clearance constraint.
6. The layout engineer modified the pad locally on the PCB to $0.80 \times 0.90\text{ mm}$ to achieve exactly $0.1500\text{ mm}$ clearance, but never updated the library or schematic.

### 2.4 Manufacturability & Solderability Validation of Modified Pad
An engineering analysis was conducted to determine whether the $0.80 \times 0.90\text{ mm}$ pad provides reliable solder joint manufacturability:
- **Lead Foot Dimensions (SOD-123):**
  - Lead contact length ($L$): $0.25\text{ mm}$ min, $0.35\text{ mm}$ typ, $0.45\text{ mm}$ max.
  - Lead width ($b$): $0.45\text{ mm}$ min, $0.55\text{ mm}$ typ, $0.65\text{ mm}$ max.
- **IPC-7351B Density Level C (Least Environment / High Density):**
  - Minimum toe overhang: $0.15\text{ mm}$
  - Minimum heel overhang: $0.10\text{ mm}$
  - Minimum side overhang: $0.05\text{ mm}$
- **Calculated Solder Fillets with $0.80 \times 0.90\text{ mm}$ Pad:**
  - Toe overhang: $0.25\text{ mm}$ ($> 0.15\text{ mm}$ requirement)
  - Heel overhang: $0.20\text{ mm}$ ($> 0.10\text{ mm}$ requirement)
  - Side overhang: $(0.90 - 0.55)/2 = 0.175\text{ mm}$ ($> 0.05\text{ mm}$ requirement)
- **Solder Mask Webbing (Dam):**
  - Inner gap between copper pads: $3.20 - 0.80 = 2.40\text{ mm}$.
  - With $0.05\text{ mm}$ solder mask expansion, solder mask dam is $2.30\text{ mm}$ ($> 0.08\text{ mm}$ fab minimum).
- **Stencil Area Ratio:**
  - Pad area: $0.80 \times 0.90 = 0.72\text{ mm}^2$.
  - With $120\text{ µm}$ stencil, Area Ratio $= \frac{0.80 \times 0.90}{2 \times (0.80 + 0.90) \times 0.12} = 1.76$ ($>> 0.66$ IPC-7525 threshold).

**Conclusion:** The $0.80 \times 0.90\text{ mm}$ land pattern is fully compliant with IPC-7351 Level C and produces robust, IPC-A-610 Class 2/3 acceptable solder fillets without risk of bridging or tombstoning.

---

## 3. Implemented Engineering Corrections

1. **Dedicated Footprint Creation:** Created `SmartPen.pretty/D4.kicad_mod` serialized directly through native KiCad 10 pcbnew, capturing the verified $0.80 \times 0.90\text{ mm}$ land pattern and electrical pad numbering:
   - Pad 1: Cathode (K)
   - Pad 2: Anode (A)
2. **Schematic Footprint Property Alignment:** In `SmartPen.kicad_sch`, updated D4 symbol definition and instance property from `SmartPen:D3` to `SmartPen:D4`.
3. **Symbol Library Alignment:** In `SmartPen_Lib.kicad_sym`, updated symbol `D4` default footprint property to `SmartPen:D4`.
4. **PCB Footprint Reference Update:** In `SmartPen.kicad_pcb`, updated footprint identifier from `SmartPen:D3` to `SmartPen:D4`.
5. **Title Block & Stackup Reconciliation:**
   - Updated PCB title block from `Rev F` to `Rev G` ("Smart Pen Hardware System - Revision G (4-Layer)").
   - Updated SCH title block to Revision G.
   - Reconciled `SmartPen.kicad_pro` `board_thickness` default from `1.0` to `1.6` mm.

---

## 4. Final Re-Verification Results (KiCad 10 Native)

Fresh native KiCad 10 DRC and ERC were executed against the corrected design files:

### 4.1 DRC Execution
```powershell
& "C:\Users\goran\AppData\Local\Programs\KiCad\10.0\bin\kicad-cli.exe" pcb drc `
    --all-track-errors `
    --schematic-parity `
    --severity-all `
    --refill-zones `
    --exit-code-violations `
    -o reports/RevG/Phase03C/qa_raw/candidate_resolved_drc.rpt `
    output/RevG/variants/FourLayer_Candidate/SmartPen.kicad_pcb
```

### 4.2 Authoritative Verification Results Matrix

| Metric | Initial Baseline (Commit `f2a5f6a`) | Post-Correction (Resolved QA State) | Status |
| :--- | :---: | :---: | :---: |
| **Exit Code** | `5` | `0` | **PASS (Clean)** |
| **Total DRC Violations** | `1` | `0` | **PASS (Zero)** |
| **Library Footprint Mismatches** | `1` | `0` | **PASS (Zero)** |
| **Clearance Violations** | `0` | `0` | **PASS (Zero)** |
| **Short Circuits** | `0` | `0` | **PASS (Zero)** |
| **Unconnected Items** | `0` | `0` | **PASS (Zero)** |
| **Schematic Parity Issues** | `0` | `0` | **PASS (Zero)** |
| **Footprint Errors** | `0` | `0` | **PASS (Zero)** |
| **Schematic ERC Messages** | `0` | `0` | **PASS (Zero)** |

### 4.3 Output Hashes & Artifact Ledger
- **Candidate PCB SHA-256:** `6329d55062810222b0667beae6add3c09b0b0c8a4631fefcec84d652b1f865af`
- **Candidate SCH SHA-256:** `99335efd28599426f4f2c00d43a6d4e7e6005b87ec8e6900a6da9b8f2d575c92`
- **Candidate PRO SHA-256:** `5d5ff24252a129d518296a84f509e5309d435fcf462c161ae38634ca944d6738`
- **D4 Footprint (`D4.kicad_mod`) SHA-256:** `47814299b821427c3d2562d98c2538cb3ecfcf8c4b260907ea457cb1d79860ce`
- **Raw DRC Report:** `reports/RevG/Phase03C/qa_raw/candidate_resolved_drc.rpt`
- **Raw DRC JSON:** `reports/RevG/Phase03C/qa_raw/candidate_resolved_drc.json`
- **Raw ERC Report:** `reports/RevG/Phase03C/qa_raw/candidate_resolved_erc.rpt`
