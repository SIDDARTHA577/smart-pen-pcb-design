# SMART PEN REV G — PCB FABRICATION SPECIFICATION & GENERAL NOTES

**Document ID:** SRG-MFG-NOT-001  
**Revision:** Rev G Production Baseline (ECR-ELEC-REVG-001)  
**Date:** November 17, 2026  

---

## 1. APPLICABLE STANDARDS
- IPC-A-600 Class 2 (Acceptability of Printed Boards).
- IPC-6012 Class 2 (Qualification and Performance Specification for Rigid Printed Boards).
- IPC-2221 (Generic Standard on Printed Board Design).
- RoHS Directive 2011/65/EU and 2015/863 (Lead-Free / Hazardous Substances Free).

## 2. BOARD SPECIFICATIONS
1. **Material:** High-Tg FR-4 ($T_g \ge 150^\circ\text{C}$, $T_d \ge 340^\circ\text{C}$, CTE-z $\le 45\text{ ppm/}^\circ\text{C}$).
2. **Finished Board Thickness:**
   - Main PCB: $1.60\text{ mm} \pm 10\%$.
   - Front MPU, MicroSD Carrier, Touch Sensor: $0.80\text{ mm} \pm 10\%$.
3. **Copper Thickness:**
   - Outer Layers (F.Cu, B.Cu): $1.0\text{ oz}$ ($35\ \mu\text{m}$) finished copper.
   - Inner Layers (In1.Cu, In2.Cu): $0.5\text{ oz}$ ($18\ \mu\text{m}$) base copper.
4. **Surface Finish:** ENIG (Electroless Nickel Immersion Gold per IPC-4552A).
   - Immersion Gold: $0.05\text{--}0.10\ \mu\text{m}$ ($2\text{--}4\ \mu\text{in}$).
   - Electroless Nickel: $3.0\text{--}6.0\ \mu\text{m}$ ($120\text{--}240\ \mu\text{in}$).
5. **Solder Mask:**
   - Color: **Matte Black**.
   - Type: Photoimageable Liquid Solder Mask (LPI), halogen-free.
   - Thickness: Minimum $10\ \mu\text{m}$ over trace corners, $20\ \mu\text{m}$ over flat copper.
   - Via Tenting: Both sides tented with solder mask.
6. **Silkscreen:**
   - Color: **White**, non-conductive, high contrast.
   - Clipping: Silkscreen clipped $0.05\text{ mm}$ clear of all solder mask openings.
7. **Holes & Routing:**
   - Minimum Drill: $0.30\text{ mm}$. Minimum Annular Ring: $0.15\text{ mm}$.
   - Edge Routing: CNC route to outline per `Edge.Cuts` layer. Tolerance $\pm 0.10\text{ mm}$.
   - V-scoring or Tab-routing permitted for panelization; breakout tabs must be ground flush.
