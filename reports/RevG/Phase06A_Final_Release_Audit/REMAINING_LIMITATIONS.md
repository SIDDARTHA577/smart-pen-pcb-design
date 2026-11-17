# REMAINING ENGINEERING LIMITATIONS & PROTOTYPE BOUNDARY REPORT

**Document ID:** SRG-P6A-LIM-010  
**Revision:** 1.0  
**Date:** November 17, 2026  
**Status:** **TECHNICAL AUDIT COMPLETE — HONEST DISCLOSURE OF DIGITAL BOUNDARIES**

---

## 1. DIGITAL DESIGN VS PHYSICAL HARDWARE BOUNDARIES

This engineering release is strictly a **Digital Design Package**. In accordance with contractual mission instructions, no physical PCB fabrication, SMT assembly, component purchasing, or lab bench testing was authorized or performed. Consequently, certain real-world physical behaviors cannot be certified until physical prototypes are produced:

### 1.1 SMT Solder Joint Quality & Reflow Profiles
- **Limitation:** Footprint land patterns, paste masks, and solder stencils are designed to IPC-7351B standards. However, physical solder paste volume, tombstoning risks on 0201/0402 passives, and thermal profiles across the ground planes during convection reflow must be validated by the assembly house during first-article PCBA fabrication.
- **Mitigation:** Comprehensive pick-and-place files with exact component centroids, standard IPC package codes, and fiducial markers have been provided.

### 1.2 Over-The-Air (OTA) Antenna Performance
- **Limitation:** The Molex 146153 wideband flexible PCB antenna is integrated conformally along the inner barrel wall ($R=6.60\text{ mm}$), driven via a $50\ \Omega$ coplanar waveguide and U.FL micro-coax cable. While 3D clearances and ground plane boundaries are verified, real-world RF return loss ($S_{11}$) and radiation efficiency in close proximity to the user's hand (hand phantom effect) require physical chamber testing with a vector network analyzer (VNA).
- **Mitigation:** Ground clearance beneath the antenna element and 4-layer controlled stackup ($50\ \Omega$ CPW-G) were strictly designed according to Molex application specifications.

---

## 2. LOCAL WORKSTATION CAD TOOLING CONSTRAINT (WDAC)

- **Limitation:** Local workstation Windows Defender Application Control (WDAC) restricts the loading of unsigned native C++ Python binaries (`OCP.pyd`). Therefore, native OpenCASCADE and FreeCAD execution cannot run on this specific Windows host without elevated workstation policy changes.
- **Mitigation:** The workflow is deployed at `.github/workflows/cad-validation.yml` to execute on standard Ubuntu GitHub Actions runners where FreeCAD and OpenCASCADE are fully supported.

---

## 3. BATTERY RUNTIME & OPERATIONAL DISCHARGE ENVELOPE

- **Limitation:** Operating on a single-cell $50\text{ mAh}$ pouch battery (`LP300830-PCM`), continuous active writing runtime is mathematically bounded to **$1.89\text{ hours}$ ($113\text{ minutes}$)**. While this covers approximately 18–25 handwritten pages (or $1.5\text{ days}$ of typical intermittent note-taking), users requiring longer non-stop sessions must recharge via USB-C or place the pen in standby when not in motion.
- **Mitigation:** Microchip MCP73831 provides a full recharge in approximately 75 minutes ($50.0\text{ mA}$, $1.0\text{C}$ rate). Firmware sleep states reduce idle consumption to $0.85\text{ mA}$ (standby) and $15.0\ \mu\text{A}$ (deep sleep).

---

## 4. MECHANICAL 3D PRINTING MATERIAL SELECTION

- **Limitation:** The 16 STL components are designed for high-resolution stereolithography (SLA) or selective laser sintering (SLS) with layer thickness $\le 50\ \mu\text{m}$. Click mechanism components (Rotor Cam `10B` and Guide Stator `10C`) experience cyclic torsional wear during actuation.
- **Mitigation:** Engineering-grade resin (e.g., Formlabs Tough 2000 or Grey Pro) or SLS Nylon PA12 is strongly recommended for functional mechanism longevity. Minimum wall thicknesses ($\ge 0.60\text{ mm}$) and draft angles have been engineered into all CAD models.
