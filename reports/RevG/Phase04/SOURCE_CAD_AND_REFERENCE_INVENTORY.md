# Smart Pen Rev G — Source CAD and Reference Inventory
**Document ID:** RPT-REVG-P4-SOURCE-INVENTORY  
**Project:** Smart Pen Hardware Architecture Revision G  
**Git Branch:** `engineering/revg-production`  
**Latest Verified Commit:** `5fdde5025c1d56b6d12d631a11ce1c643ea28bab`  
**Date:** November 16, 2026  
**Status:** Mandatory Source Verification & Cryptographic Checkpoint Established  

---

## 1. Executive Summary

In strict compliance with Section 1 of the Phase 4 engineering mandate, this document records the comprehensive inventory, physical paths, cryptographic SHA256 checksums, byte sizes, and geometric parameters of all authoritative electronic design files, mechanical CAD references, and generation tools used throughout Phase 4.

A recoverable pre-edit source checkpoint was created under `backups/Phase04_Source_Checkpoint/` prior to generating any Phase 4 artifacts. All historical Revision F files and Revision G Phase 3C electrical routing closure baselines were preserved without modification.

---

## 2. Authoritative Source File Cryptographic Checksum Table

| Subsystem | File Path | Byte Size | SHA256 Checksum | Verification Status |
| :--- | :--- | :---: | :--- | :---: |
| **Main Four-Layer PCB** | `output/RevG/variants/FourLayer_Candidate/SmartPen.kicad_pcb` | 687,116 | `6329d55062810222b0667beae6add3c09b0b0c8a4631fefcec84d652b1f865af` | **VERIFIED (Authoritative)** |
| **Main Schematic** | `output/RevG/variants/FourLayer_Candidate/SmartPen.kicad_sch` | 161,404 | `b8d922a86c5b259e0505e627ffddde803bc34bc83196576e68da5c95d61044cc` | **VERIFIED (Authoritative)** |
| **Front MPU Board** | `output/RevG/Front_MPU/Front_MPU.kicad_pcb` | 13,257 | `ec59f0dcbee3e9dd3231dc533178eb0d25fb1a9afd5e983fe39afc4b4a08ffcd` | **VERIFIED (Authoritative)** |
| **MicroSD Carrier Board**| `output/RevG/MicroSD_Carrier/MicroSD_Carrier.kicad_pcb` | 11,035 | `96eb291ed0d287f9330e7d8a10a91abe855cec65021ab33c689ba4fe58685768` | **VERIFIED (Authoritative)** |
| **Touch Sensor Board** | `output/RevG/Touch_Sensor/Touch_Sensor.kicad_pcb` | 7,702 | `4aaa69c937a5476380753dba0b68f1fe2ebb37bafbb97c2e6675055f04dc4f49` | **VERIFIED (Authoritative)** |
| **RevF Complete Assembly**| `output/RevF_Client_Delivery/07_3D_STEP/SmartPen_Complete_Assembly.step` | 742,970 | `47aa0fe58224853d329c2b641ae5b7ceb381bc66ce7ede89c50c8c2d875284e4` | **REFERENCE (Preserved)** |
| **RevF Click Ratchet** | `output/RevF_Client_Delivery/07_3D_STEP/13_Click_Ratchet_and_Pushrod.step` | 40,809 | `07de9e1416fbb5cc1a336891946a85a401ea78055ba308e344970cea6dc648a2` | **REFERENCE (Preserved)** |
| **RevF Bayonet Collar** | `output/RevF_Client_Delivery/07_3D_STEP/14_Bayonet_Locking_Collar.step` | 93,298 | `b9dc04c500a769786400d3c75bcc8e7117791ec53d86b0c4b26c7db47ca9e9bf` | **REFERENCE (Preserved)** |

---

## 3. Physical Dimensions & Geometric Parameters of Electronic Assemblies

### 3.1 Main Electronics Board (`SmartPen.kicad_pcb`)
- **Layer Count:** 4 layers (`F.Cu`, `In1.Cu`, `In2.Cu`, `B.Cu`).
- **Board Thickness:** $1.60\text{ mm}$ nominal.
- **Outline Dimensions:** Length $84.000\text{ mm}$ ($X = 0.000\text{ to }84.000\text{ mm}$), Width $9.200\text{ mm}$ ($Y = 0.000\text{ to }9.200\text{ mm}$).
- **Total Footprints:** 64 SMD components.
- **Key Interface Locations:**
  - `J_IMU` (JST 4-pin receptacle): $(3.200, 4.600)$ on `F.Cu` — front edge.
  - `D1` / `D2` (Green / Red Status LEDs): $(17.200, 2.200)$ and $(17.200, 4.400)$.
  - `SW1` (ERASE Pushbutton): $(32.956, 1.500)$ on `F.Cu`.
  - `U1` (ESP32-C3FH4X MCU): $(42.880, 4.835)$ on `F.Cu`.
  - `SW2` (MODE Pushbutton): $(47.104, 1.500)$ on `F.Cu`.
  - `J_RF` (Hirose U.FL Receptacle): $(54.850, 5.150)$ on `F.Cu`.
  - `J_SD` (Hirose 6-pin FFC Receptacle): $(58.400, 4.200)$ on `F.Cu`.
  - `J_BAT` (JST 2-pin Battery Receptacle): $(62.800, 1.720)$ on `F.Cu`.
  - `SW3` (Slide Power Switch): $(62.963, 6.824)$ on `F.Cu`.
  - `U2` (MCP73831 Charger): $(67.000, 4.070)$ on `F.Cu`.
  - `J_USB` (Mid-mount Type-C Receptacle): $(78.400, 4.600)$ on `F.Cu` — rear edge.

### 3.2 Front MPU Daughterboard (`Front_MPU.kicad_pcb`)
- **Dimensions:** Length $10.000\text{ mm}$ ($Y = 0.000\text{ to }10.000\text{ mm}$), Width $7.200\text{ mm}$ ($X = 0.000\text{ to }7.200\text{ mm}$).
- **Thickness:** $0.80\text{ mm}$.
- **Connector:** JST `SM04B-SRSS-TB` (4-pin 1.0 mm pitch horizontal SMT) @ $(3.600, 1.400)$.
- **Sensor:** InvenSense MPU-6050 / ICM-42670 class QFN-24 ($4.00 \times 4.00\text{ mm}$) @ $(3.600, 5.600)$.

### 3.3 MicroSD Carrier Daughterboard (`MicroSD_Carrier.kicad_pcb`)
- **Dimensions:** Length $16.000\text{ mm}$ ($Y = 0.000\text{ to }16.000\text{ mm}$), Width $11.400\text{ mm}$ ($X = 0.000\text{ to }11.400\text{ mm}$).
- **Thickness:** $0.80\text{ mm}$.
- **Connector:** 6-pin $0.5\text{ mm}$ pitch bottom-contact FFC receptacle @ $(5.700, 2.000)$.
- **Card Socket:** Push-push TF-01A MicroSD socket @ $(5.700, 11.200)$.

### 3.4 Touch Sensor Daughterboard (`Touch_Sensor.kicad_pcb`)
- **Dimensions:** Length $18.000\text{ mm}$ ($Y = 0.000\text{ to }18.000\text{ mm}$), Width $6.000\text{ mm}$ ($X = 0.000\text{ to }6.000\text{ mm}$).
- **Thickness:** $0.80\text{ mm}$.
- **Connector:** JST 3-pin SH series connector @ $(3.000, 2.200)$.
- **Electrode:** Exposed copper capacitive touch sensor pad ($5.00 \times 10.00\text{ mm}$) @ $(3.000, 13.500)$.

---

## 4. CAD & Simulation Tooling Verification

| Tool / Binary | Location / Command | Version | Capability Utilized | Status |
| :--- | :--- | :---: | :--- | :---: |
| **KiCad CLI** | `C:\Users\goran\AppData\Local\Programs\KiCad\10.0\bin\kicad-cli.exe` | 10.0.7 | Direct STEP BRep export of all 4 PCBs | **ACTIVE** |
| **Python 3** | `python.exe` (Python 3.11.9 AMD64) | 3.11.9 | Master Parametric CAD generator, collision solver | **ACTIVE** |
| **NumPy** | Python package `numpy` | 2.4.6 | Vector cross products, normals, coordinate transforms | **ACTIVE** |
| **SciPy** | Python package `scipy` | 1.17.1 | Spatial KD-tree and mesh geometric validation | **ACTIVE** |
| **Matplotlib** | Python package `matplotlib` | 3.11.1 | 2D/3D high-resolution engineering section generation | **ACTIVE** |
| **Pytest** | Python package `pytest` | 9.1.1 | Automated 7-test Phase 4 verification suite | **ACTIVE** |

---

## 5. Recoverable Checkpoint Verification

A byte-for-byte duplicate backup was established at:
`c:\Users\goran\Downloads\SmartPen_RevD_AutoLinked_Footprints_Review_ONLY\backups\Phase04_Source_Checkpoint\`

Files backed up:
- `SmartPen.kicad_pcb` (687,116 bytes)
- `SmartPen.kicad_sch` (161,404 bytes)
- `Front_MPU.kicad_pcb` (13,257 bytes)
- `MicroSD_Carrier.kicad_pcb` (11,035 bytes)
- `Touch_Sensor.kicad_pcb` (7,702 bytes)

All hashes match the working-tree source files exactly. No files were corrupted or overwritten.
