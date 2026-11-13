# Smart Pen Rev G — Phase 1: PCB Manufacturing Feasibility & DFM Audit

**Document ID**: `reports/RevG/Phase01/11_MANUFACTURING_FEASIBILITY_AUDIT.md`  
**Execution Date**: November 13, 2026  
**Revision Baseline**: Revision F  
**Target Development Revision**: Revision G  
**Branch**: `engineering/revg-production`  

---

## 1. Executive Summary

A Design for Manufacturing (DFM) and Design for Assembly (DFA) audit was conducted on all four Smart Pen printed circuit boards, comparing actual physical design geometry against declared manufacturing specifications (`output/RevF_Client_Delivery/06_Fabrication_Drawing/PCB_Fabrication_Specification.md`) and standard commercial PCB fabrication capabilities (e.g. JLCPCB / PCBWay standard 2-layer rigid process).

**Manufacturing Release Verdict**: **BLOCKED / NOT READY FOR FABRICATION**.  
The current layouts cannot be manufactured or assembled reliably due to **severe clearance violations, missing optical fiducials, board-edge copper encroachments, solder-mask web collapse on fine-pitch ICs, and unverified mid-mount connector routings**.

---

## 2. Fabrication Specification vs. Actual Layout Compliance

| Parameter | Declared Spec (`PCB_Fab_Spec.md`) | Commercial Limit (Standard SMT) | Main PCB Working | Main PCB Delivery | DFM Audit Status |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **Board Dimensions** | 84.00 x 9.20 mm (±0.10 mm) | Aspect ratio limit 8:1 | 84.00 x 9.20 mm (Aspect 9.1:1) | 84.00 x 9.20 mm | **PASS (Requires Panel Rails)** |
| **Board Thickness** | 1.00 mm (±10%) | 0.80 mm – 1.60 mm | 1.00 mm | 1.00 mm | **PASS** |
| **Layer Count** | 2 Copper Layers (1.0 oz / 35 µm) | 2 Layers | 2 Layers (F.Cu, B.Cu) | 2 Layers | **PASS** |
| **Surface Finish** | ENIG (Au: 1-2 µ", Ni: 100-200 µ") | ENIG mandatory for 0.5mm QFN | ENIG specified | ENIG specified | **PASS** |
| **Min Trace Width** | 0.20 mm (8 mils) | 0.127 mm (5 mils) | 0.15 mm – 0.20 mm | 0.15 mm – 0.20 mm | **PASS** |
| **Min Trace Clearance**| 0.127 mm (5 mils) | 0.127 mm (5 mils) | **38 violations (< 0.127 mm)** | **499 violations (< 0.127 mm)**| **FAIL** |
| **Min Via Hole Size** | 0.30 mm (12 mils) | 0.30 mm (standard drill) | 0.30 mm | 0.30 mm | **PASS** |
| **Min Via Pad Outer** | 0.50 mm (20 mils) | 0.45 mm (standard annular) | 0.50 mm (0.10 mm ring) | 0.50 mm | **PASS** |
| **Hole-to-Hole Spacing**| >= 0.25 mm (10 mils) | >= 0.25 mm (web strength) | **56 violations (< 0.25 mm)** | **59 violations (< 0.25 mm)** | **FAIL** |
| **Copper-to-Edge** | >= 0.50 mm (20 mils) | >= 0.30 mm (routing bit) | **0.25 mm (Encroachments)** | 0.25 mm | **FAIL** |
| **Solder Mask Web** | >= 0.10 mm (4 mils) | >= 0.08 mm (LPI Green) | **32 violations (< 0.08 mm)** | **170 violations (< 0.08 mm)**| **FAIL** |
| **Optical Fiducials** | >= 2 Global Fiducials | Mandatory for automated SMT | **0 Fiducials Present** | **0 Fiducials Present** | **FAIL** |
| **Polarity Silkscreen**| Pin 1 marked on all ICs/conns | Mandatory for inspection | **J_BAT has no +/- mark** | J_BAT has no +/- mark | **FAIL** |

---

## 3. High-Risk DFM Findings

### 1. Panelization & Aspect Ratio Risk (84.0 mm x 9.2 mm)
- The Main PCB has a high aspect ratio of **9.1 : 1** (length to width).
- An individual 84 x 9.2 mm x 1.0 mm board cannot be routed through automated surface-mount pick-and-place lines or reflow ovens without severe twisting, warping, or jamming in conveyor belts.
- **DFM Requirement**: The Main PCB must be panelized with 4 to 8 boards per panel, framed by **5.0 mm waste rails** on both sides with mouse-bites (perforated break-off tabs) and fiducial markers on the panel waste rails.

### 2. Solder Mask Web Collapse on Fine-Pitch ICs (32 Violations)
- Both `U1` (ESP32-C3, 0.50 mm pitch QFN-32) and `U3` (MCP23008, 0.50 mm pitch QFN-20) feature pad-to-pad copper spacing of approximately 0.25 mm.
- In `SmartPen.kicad_pcb`, the solder mask expansion is set to 0.05 mm, leaving a residual solder mask dam of:
  $$\text{Mask Dam} = 0.25\text{ mm} - (2 \times 0.05\text{ mm}) = 0.15\text{ mm}$$
- Because several pads are spaced tighter due to trace necking, 32 instances have mask bridges $< 0.08\text{ mm}$. During fabrication, mask dams below 0.08 mm break off, creating a contiguous aperture across adjacent pads and causing **solder bridging shorts during SMT reflow**.
- **DFM Requirement**: Set solder mask expansion to **0.025 mm (1 mil)** or use gang-mask apertures with 100% ENIG finish and proper solder-paste reduction.

### 3. Board-Edge Copper Clearance Encroachments
- Fabrication specifications require $\ge 0.50\text{ mm}$ clearance from copper to the board outline (`Edge.Cuts`).
- Ground polygon fills and highway routing traces on B.Cu approach within **0.25 mm** of the edge.
- When the PCB panel is routed with a mechanical 1.6 mm or 2.0 mm carbide bit, mechanical routing tolerances (±0.20 mm) can bite into copper traces, causing exposed copper, burrs, or ground shorts against the internal metal rail.

### 4. 0201 Component Placement (C8, C9)
- RF shunt capacitors `C8` and `C9` are `0201` imperial package ($0.60\text{ mm} \times 0.30\text{ mm}$).
- While standard high-volume assembly lines support 0201, low-volume prototype lines often struggle with tombstoning and component loss unless specific solder paste stencils (electro-polished stainless steel, 100 µm thickness, Type 4 paste) are used.
- **DFM Recommendation**: Validate whether `C8` and `C9` can be upgraded to `0402` package without degrading 2.4 GHz RF impedance matching.

### 5. Mid-Mount USB-C Connector (J_USB)
- `TYPE-C-31-M-12` is a mid-mount USB receptacle that sits in a routed cutout through the edge of the PCB.
- The PCB cutout must feature plated or non-plated routing with exact ±0.05 mm mechanical tolerances to ensure proper insertion depth through the pen enclosure without mechanical binding.

---

## 4. Daughterboard DFM Assessment

1. **Front MPU Daughterboard (`Front_MPU`)**:
   - Size: 7.20 mm x 10.00 mm x 0.80 mm.
   - SMT: Single-sided top placement. MPU-6050 (0.5mm QFN-24) requires high-accuracy stencil.
   - Board Thickness: 0.80 mm selected for ultra-low profile in tip carrier.
   - DFM Status: **PASS (Requires array panelization)**.
2. **MicroSD Carrier Daughterboard (`MicroSD_Carrier`)**:
   - Size: 11.40 mm x 16.00 mm x 1.00 mm.
   - SMT: Single-sided placement for TF-01A socket and FH12-6S connector.
   - DFM Status: **PASS (Requires array panelization)**.
3. **Touch Sensor Daughterboard (`Touch_Sensor`)**:
   - Size: 6.00 mm x 18.00 mm x 1.00 mm.
   - SMT: Single-sided placement. TTP223-BA6 (SOT-23-6) and 5x10mm copper touch electrode.
   - DFM Status: **PASS (Requires array panelization)**.

---

## 5. Manufacturing Audit Sign-Off

- **DFM Closure Status**: Current Main PCB layouts **CANNOT BE RELEASED TO MANUFACTURING**.
- **Panelization, fiducial, and clearance repairs required**: Scheduled for Phase 2 implementation.
- **Phase 1 Status**: **FAIL (Fabrication Release Blocked Pending Design Corrections)**.
