# Smart Pen Revision F — PCB Fabrication Specification Drawing

**Project**: Smart Pen PCB and 3D Enclosure — RadixView Technologies  
**Date**: November 2, 2026  
**Revision**: Rev F Engineering Release  

---

## 1. PCB General Parameters
- **Board Outline Dimensions**: 84.00 mm x 9.20 mm (+/- 0.10 mm)
- **Board Thickness**: 1.00 mm (+/- 10%)
- **Layer Count**: 2 Copper Layers (Top F.Cu, Bottom B.Cu)
- **Base Material**: High-Tg FR-4 (Tg >= 150°C, Flammability UL94V-0)
- **Surface Finish**: Electroless Nickel Immersion Gold (ENIG) (Au: 1-2 u", Ni: 100-200 u")
- **Copper Weight**: 1.0 oz finished copper thickness (35 um) on outer layers
- **Solder Mask**: High-resolution Liquid Photoimageable (LPI), Matte Green
- **Silkscreen**: White, lead-free, high-adhesion epoxy ink (minimum text size: 0.6 mm)

---

## 2. Drilling & Clearances
- **Minimum Trace Width**: 0.20 mm (8 mils)
- **Minimum Electrical Clearance**: 0.127 mm (5 mils)
- **Minimum Via Pad Diameter**: 0.50 mm (20 mils)
- **Minimum Via Hole Size**: 0.30 mm (12 mils)
- **Board Edge to Copper Clearance**: >= 0.50 mm
- **Hole-to-Hole Minimum Spacing**: >= 0.25 mm
- **Via Treatment**: Tented with solder mask on both sides (no exposed copper on via rings)

---

## 3. Layer Stackup
| Layer Name | Type | Thickness | Material | Dielectric Constant (Er) |
| :--- | :--- | :--- | :--- | :--- |
| **Top Solder Mask** | Solder Mask | 15 um | Taiyo PSR-4000 (Green) | 3.5 |
| **Top Copper (F.Cu)** | Signal / Power / GND | 35 um (1 oz) | Copper Foil | - |
| **Core Dielectric** | Core Dielectric | 900 um | FR-4 Core | 4.4 |
| **Bottom Copper (B.Cu)**| Signal / Highway / GND| 35 um (1 oz) | Copper Foil | - |
| **Bottom Solder Mask** | Solder Mask | 15 um | Taiyo PSR-4000 (Green) | 3.5 |
| **Total Finished Thickness** | **2-Layer Rigid** | **1.00 mm (+/- 0.08 mm)** | - | - |
