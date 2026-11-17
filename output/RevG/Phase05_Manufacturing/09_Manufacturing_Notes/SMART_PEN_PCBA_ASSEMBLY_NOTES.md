# SMART PEN REV G — PCBA ASSEMBLY & PROCESS SPECIFICATION

**Document ID:** SRG-MFG-NOT-002  
**Revision:** Rev G Production Baseline  
**Date:** November 17, 2026  

---

## 1. APPLICABLE STANDARDS
- IPC-A-610 Class 2 (Acceptability of Electronic Assemblies).
- J-STD-001 (Requirements for Soldered Electrical and Electronic Assemblies).
- IPC-7711/7721 (Rework, Modification and Repair of Electronic Assemblies).

## 2. ASSEMBLY PROCESS REQUIREMENTS
1. **Solder Paste & Alloy:** SAC305 (Sn96.5 / Ag3.0 / Cu0.5), Lead-Free, RoHS compliant, Type 4 or Type 5 powder for 0402 and fine-pitch QFN apertures.
2. **Reflow Profile:** Standard lead-free convection reflow profile:
   - Peak Temperature: $240^\circ\text{C}$ to $245^\circ\text{C}$.
   - Time above liquidus ($217^\circ\text{C}$): $60\text{--}90\text{ seconds}$.
   - Ramp rate: $\le 2.5^\circ\text{C/second}$.
3. **Moisture Sensitivity:** All active ICs (ESP32-C3FH4X, MCP73831, MCP23008, MPU-6050, TTP223) must be baked per J-STD-033 prior to surface mount if moisture exposure time exceeded.
4. **Automated Inspection:**
   - 100% Automated Optical Inspection (AOI) on all SMD components.
   - Automated X-Ray Inspection (AXI) required on ESP32-C3 QFN-32 exposed thermal pad and MPU-6050 QFN-24 center pad to verify voiding $\le 20\%$.
5. **No Clean Flux:** Assemblies must use Halide-Free No-Clean solder paste.
