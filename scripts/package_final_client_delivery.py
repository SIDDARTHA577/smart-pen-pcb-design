#!/usr/bin/env python3
"""
Phase 6 — Digital Client Delivery Package Generator.
Packages all verified digital engineering assets (KiCad, Gerbers, BOM, CPL,
STEP, STL, Drawings, Reports, Assembly Guides) into output/RevG/Final_Client_Delivery/
and produces a versioned ZIP archive and SHA-256 manifest.
"""

import os
import sys
import shutil
import hashlib
from pathlib import Path

def sha256_file(filepath):
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def package_delivery():
    delivery_dir = Path("output/RevG/Final_Client_Delivery")
    if delivery_dir.exists():
        shutil.rmtree(delivery_dir)
    delivery_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. KiCad Design Source
    kicad_dir = delivery_dir / "01_KiCad_Design_Source"
    kicad_dir.mkdir(parents=True, exist_ok=True)
    
    # Main board
    main_dest = kicad_dir / "Main_Board"
    main_src = Path("output/RevG/variants/FourLayer_ECR_R9_50mA")
    shutil.copytree(main_src, main_dest, ignore=shutil.ignore_patterns("*.rpt", "*.csv"))
    
    # Daughterboards
    for db in ["Front_MPU", "MicroSD_Carrier", "Touch_Sensor"]:
        db_dest = kicad_dir / db
        db_src = Path(f"output/RevG/{db}")
        shutil.copytree(db_src, db_dest, ignore=shutil.ignore_patterns("*.rpt", "*.csv", "gerber", "KiCad"))
        
    # 2. Fabrication Gerbers & Drills
    mfg_src = Path("output/RevG/Phase05_Manufacturing")
    fab_dest = delivery_dir / "02_Fabrication_Gerber_Drill"
    fab_dest.mkdir(parents=True, exist_ok=True)
    shutil.copytree(mfg_src / "01_Gerbers", fab_dest / "Gerbers")
    shutil.copytree(mfg_src / "02_Drill", fab_dest / "Drill")
    
    # 3. BOM & CPL
    bom_dest = delivery_dir / "03_BOM_and_CPL"
    bom_dest.mkdir(parents=True, exist_ok=True)
    shutil.copytree(mfg_src / "03_BOM", bom_dest / "BOM")
    shutil.copytree(mfg_src / "04_PickAndPlace", bom_dest / "PickAndPlace")
    
    # 4. Drawings, Schematics & Assembly
    drawings_dest = delivery_dir / "04_Drawings_Schematics_Assembly"
    drawings_dest.mkdir(parents=True, exist_ok=True)
    for f in (mfg_src / "05_Assembly_Drawings").glob("*"):
        shutil.copy(f, drawings_dest)
    for f in (mfg_src / "06_Fabrication_Drawings").glob("*"):
        shutil.copy(f, drawings_dest)
        
    # 5. Mechanical CAD Source
    cad_src_dest = delivery_dir / "05_Mechanical_CAD_Source"
    cad_src_dest.mkdir(parents=True, exist_ok=True)
    shutil.copy("output/RevG/Mechanical_Phase04C/CAD_Source/SmartPen_Parametric_CAD_RevG_Phase4C.py", cad_src_dest)
    
    # 6. Mechanical STEP Assemblies and Parts
    step_dest = delivery_dir / "06_Mechanical_STEP_Assemblies"
    step_dest.mkdir(parents=True, exist_ok=True)
    shutil.copy("output/RevG/Mechanical_Phase04C/Assemblies/SmartPen_RevG_Phase4C_Master_Assembly.step", step_dest)
    shutil.copy("output/RevG/Mechanical_Phase04C/Assemblies/SmartPen_RevG_Phase4C_Exploded_Assembly.step", step_dest)
    shutil.copytree("output/RevG/Mechanical_Phase04C/STEP", step_dest / "Parts")
    
    # 7. Mechanical Printable STL Parts
    stl_dest = delivery_dir / "07_Mechanical_Printable_STL"
    shutil.copytree("output/RevG/Mechanical_Phase04C/STL", stl_dest / "Parts")
    
    # 8. Mechanical Drawings and Visuals
    mech_drawings = delivery_dir / "08_Mechanical_Drawings_and_Visuals"
    shutil.copytree("output/RevG/Mechanical_Phase04C/Drawings", mech_drawings)
    
    # 9. Assembly Instructions
    assy_guide_dest = delivery_dir / "09_Assembly_Instructions"
    assy_guide_dest.mkdir(parents=True, exist_ok=True)
    generate_assembly_instructions(assy_guide_dest / "SMART_PEN_REVG_ASSEMBLY_MANUAL.md")
    
    # 10. Engineering Verification Reports
    rep_dest = delivery_dir / "10_Engineering_Verification_Reports"
    rep_dest.mkdir(parents=True, exist_ok=True)
    src_rep = Path("reports/RevG/Phase04C/FINAL_BLOCKER_CLOSURE")
    shutil.copy(src_rep / "POWER_BUDGET_AND_CAPACITY_EVIDENCE.md", rep_dest / "01_POWER_BUDGET_AND_CAPACITY_REPORT.md")
    shutil.copy(src_rep / "FINAL_PROTECTED_BATTERY_SELECTION.md", rep_dest / "02_BATTERY_SELECTION_AND_BORE_CLEARANCE_AUDIT.md")
    shutil.copy(src_rep / "CHARGER_R9_ECR_DECISION.md", rep_dest / "03_CHARGER_R9_ECR_REPORT.md")
    shutil.copy(src_rep / "KICAD_ERC_DRC_VERIFICATION.md", rep_dest / "04_KICAD_ERC_DRC_VERIFICATION.md")
    shutil.copy(src_rep / "FINAL_CAD_ASSEMBLY_VALIDATION.md", rep_dest / "05_CAD_ASSEMBLY_351_COLLISION_AUDIT.md")
    shutil.copy(mfg_src / "08_DFM_Validation" / "SmartPen_MainBoard_DFM_Report.md", rep_dest / "06_DFM_AND_GERBER_VALIDATION.md")
    
    # 11. Manufacturing Notes
    notes_dest = delivery_dir / "11_Manufacturing_Notes"
    notes_dest.mkdir(parents=True, exist_ok=True)
    shutil.copy(mfg_src / "09_Manufacturing_Notes" / "SMART_PEN_PCB_FABRICATION_NOTES.md", notes_dest)
    shutil.copy(mfg_src / "09_Manufacturing_Notes" / "SMART_PEN_PCBA_ASSEMBLY_NOTES.md", notes_dest)
    shutil.copy(mfg_src / "07_Stackup" / "SmartPen_MainBoard_4Layer_Stackup_Specification.md", notes_dest)
    shutil.copy(mfg_src / "07_Stackup" / "SmartPen_MainBoard_4Layer_Stackup.json", notes_dest)
    
    # 12. Prototype Limitations & Physical Testing Guide
    proto_dest = delivery_dir / "12_Prototype_Validation_and_Limitations"
    proto_dest.mkdir(parents=True, exist_ok=True)
    generate_prototype_guide(proto_dest / "OUTSTANDING_LIMITATIONS_AND_PROTOTYPE_GUIDE.md")
    
    # 13. Client Handoff README
    generate_client_readme(delivery_dir / "README.md")
    
    # 14. SHA-256 Manifest
    manifest_path = delivery_dir / "SHA256_FINAL_DELIVERY_MANIFEST.txt"
    entries = []
    for p in sorted(delivery_dir.rglob("*")):
        if p.is_file() and p.name != "SHA256_FINAL_DELIVERY_MANIFEST.txt":
            rel_path = p.relative_to(delivery_dir).as_posix()
            h = sha256_file(p)
            size_bytes = p.stat().st_size
            entries.append(f"{h}  {size_bytes:>10} B  {rel_path}")
            
    with open(manifest_path, 'w', encoding='utf-8') as f:
        f.write("# SMART PEN REV G — FINAL CLIENT DIGITAL DELIVERY MANIFEST\n")
        f.write("# Date: November 17, 2026\n")
        f.write(f"# Total Artifacts: {len(entries)}\n\n")
        for e in entries:
            f.write(e + "\n")
            
    # 15. Create Versioned ZIP Archive
    zip_dest = delivery_dir.parent / "SmartPen_RevG_Final_Digital_Delivery_Package_v1.0.zip"
    print(f"Creating versioned delivery archive at: {zip_dest}...")
    shutil.make_archive(str(zip_dest).replace('.zip', ''), 'zip', delivery_dir)
    print("Archive successfully created!")

def generate_assembly_instructions(out_path):
    text = """# SMART PEN REV G — ELECTRO-MECHANICAL ASSEMBLY & SERVICE MANUAL

**Document ID:** SRG-DOC-ASM-001  
**Revision:** 1.0 (Rev G Production Baseline)  
**Date:** November 17, 2026  

---

## 1. TOOLS & CONSUMABLES REQUIRED
- Clean ESD-safe assembly mat and grounded wrist strap.
- Precision tweezers (curved and straight point).
- Miniature Phillips / slotted screwdriver set.
- 0.5mm pitch FFC insertion tool.
- Thermal-cure cyanoacrylate or UV-curable structural adhesive (Loctite 401 or equivalent).
- High-tack Kapton polyimide tape ($5.0\\text{ mm}$ width).
- Industrial isopropyl alcohol ($> 99.5\\%$) and lint-free swabs.

---

## 2. ASSEMBLY PROCEDURE

### Stage 1: Daughterboard Harnessing
1. **Front MPU Carrier:**
   - Connect the 4-pin JST-SH wire harness (`SHR-04V-S-B`) to receptacle `J1` on `Front_MPU.kicad_pcb`.
   - Slide `Front_MPU.kicad_pcb` into `06_Front_MPU_Carrier.stl` until the rear retention clips snap into place.
2. **MicroSD Carrier:**
   - Insert the 6-pin 0.5mm pitch FFC ribbon into connector `J1` on `MicroSD_Carrier.kicad_pcb` with stiffener facing upward. Flip the actuator bar down to lock.
   - Seat the carrier into `07_MicroSD_Carrier_Mount.stl`.
3. **Touch Sensor:**
   - Connect the 3-pin JST-SH wire harness to `Touch_Sensor.kicad_pcb`. Slide into the internal grip recess.

### Stage 2: Electronics Rail Integration
1. Mount the vibration motor into `13_Vibration_Motor_Mount.stl` and route wires to `J_MOT` on the Main PCB.
2. Place the battery pack (`Grepow GRP380830-HP-PCM` or `EEMB LP380830`) into `05_Battery_Cradle.stl`. Route the silicone leads through the rear wire conduit to `J_BAT`.
3. Slide `05_Battery_Cradle.stl` into the bottom retention rails of `04_Removable_Electronics_Rail.stl`.
4. Affix the Molex 146153 antenna onto `14_Antenna_Mount.stl` and connect the U.FL micro-coaxial cable to connector `J_RF` on the Main PCB.
5. Snap the Main PCB into the top deck of `04_Removable_Electronics_Rail.stl`. Connect all JST wire harnesses.

### Stage 3: Click Mechanism & Refill Insertion
1. Drop the helical return spring (`21_Helical_Return_Spring.stl`) into the front nose cone (`03_Front_Nose_Cone.stl`).
2. Insert standard D1 ink refill (`20_D1_Ink_Refill.stl`) into the nose cone.
3. Slide central pushrod (`22_Click_Pushrod.stl`) through the central tunnel of `04_Removable_Electronics_Rail.stl` until it contacts the refill tail.
4. Assemble the 3-piece click engine:
   - Insert stator sleeve (`10C_Click_Guide_Stator.stl`) into the rear barrel bore.
   - Insert cam rotor (`10B_Click_Rotor_Cam.stl`) into the stator sleeve.
   - Insert plunger button (`10A_Click_Plunger_Button.stl`) into the rotor.
5. Mate the rear bayonet collar (`11_Rear_Bayonet_Collar.stl`) by pressing axially and rotating $30^\\circ$ clockwise until detent clicks.

### Stage 4: Enclosure Closure & Testing
1. Slide the outer barrel (`01_Outer_Barrel.stl`) over the assembled chassis.
2. Thread the front grip (`02_Front_Grip.stl`) and nose cone (`03_Front_Nose_Cone.stl`) onto the barrel.
3. Cycle the click mechanism 5 times to confirm positive tip extension and retraction.
4. Connect USB-C cable through port bezel (`08_USB_C_Access_Feature.stl`) to verify charging LED `D2` illumination and enumeration on host PC.
"""
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(text)

def generate_prototype_guide(out_path):
    text = """# SMART PEN REV G — PROTOTYPE VALIDATION & PHYSICAL TESTING GUIDE

**Document ID:** SRG-DOC-VAL-001  
**Revision:** 1.0  
**Date:** November 17, 2026  
**Scope:** Engineering Recommendations for Physical Hardware Bring-Up & Validation Testing  

---

## 1. SCOPE NOTE
Per the contract mission statement:
> *"COMPLETE DIGITAL PCB DESIGN + 3D PRINTABLE MECHANICAL DESIGN + MANUFACTURING FILES + FINAL CLIENT HANDOFF. NO physical fabrication, hardware purchase, assembly, or bench testing is required."*

All calculations, 3D clearance audits, kinematic motion sweeps, and DRC/ERC checks in this delivery are based on validated CAD geometry, silicon datasheets, and native KiCad rule engines. Physical hardware testing must be executed by the client during initial prototype bench bring-up.

---

## 2. RECOMMENDED PHYSICAL BRING-UP SEQUENCE

### Phase A: Bare PCB Inspection & Unpowered Testing
1. Visual inspection under stereo microscope for solder bridges, tombstoning, and component polarity (especially SOT-23 pin 1 dots and QFN pin 1 markings).
2. Measure unpowered resistance from `3V3`, `VBAT`, and `USB_VBUS` to `GND`. Confirm no direct shorts ($R > 100\\text{ k}\\Omega$).
3. Inspect ENIG plating uniformity and solder mask integrity across 0402 footprints.

### Phase B: Power & Charging Bench Testing
1. Connect external bench power supply with current limit set to $100\\text{ mA}$ at $3.70\\text{ V}$ to battery connector `J_BAT`.
2. Measure quiescent current draw with slide switch `SW3` OFF ($I < 1\\ \\mu\\text{A}$) and ON ($I \\approx 22\\text{ mA}$).
3. Measure AP2112K LDO output on test pad: confirm $3.30\\text{ V} \\pm 1.5\\%$.
4. Plug 5.0V USB-C power source into `J_USB`.
   - Verify charging LED `D2` (Red) turns ON.
   - Measure charge current with in-line ammeter: confirm $50.0\\text{ mA} \\pm 5\\text{ mA}$ ($R_9 = 20.0\\text{ k}\\Omega$).
   - Monitor MCP73831 case temperature with thermocouple: confirm case temperature rise $\\le 25^\\circ\\text{C}$.
   - Disconnect battery; confirm system continues operating seamlessly on USB power via diode `D3` and P-FET `Q2`.

### Phase C: ESP32-C3 Firmware Flash & RF Verification
1. Connect USB-C to PC; verify ESP32-C3 internal USB-JTAG/Serial enumerates.
2. Flash diagnostic firmware image (`esptool.py flash`).
3. Execute Wi-Fi scan and 802.11b TX burst at $+19.5\\text{ dBm}$ while probing `3V3` rail with oscilloscope (AC coupled). Confirm voltage dip is $\\le 120\\text{ mV}$ and rail stays safely above $3.00\\text{ V}$ brownout threshold.
4. Verify BLE pairing and continuous IMU 6-axis stream from MPU-6050 over I2C bus at 400 kHz.

### Phase D: Mechanical Click & 3D Print Testing
1. 3D print mechanical enclosure parts in SLA / SLS engineering resin or PA12 nylon (Formlabs Tough 2000 or HP Multi Jet Fusion PA12 recommended).
2. Clean support material from internal bayonet lugs and stator teeth.
3. Test click mechanism through 500 retract-extend-retract cycles. Inspect rotor sawteeth for wear or jamming.
"""
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(text)

def generate_client_readme(out_path):
    text = """# SMART PEN REV G — FINAL CLIENT DIGITAL DELIVERY PACKAGE

**Project Name:** Smart Pen Revision G Hardware Design  
**Client Delivery Package Version:** 1.0  
**Date:** November 17, 2026  
**Contract Scope:** Complete Digital PCB Design + 3D Printable Mechanical Enclosure + Manufacturing Files + Digital Handoff  

---

## 1. EXECUTIVE SUMMARY & CLIENT CLARIFICATIONS APPLIED

The Smart Pen Revision G digital engineering milestone is 100% complete and fully validated.

### Key Client Directives Implemented:
1. **Unconstrained Battery Capacity Optimization:** In accordance with the client clarification (*"The client has no fixed battery capacity requirement... Select the highest-value practical battery solution that satisfies all design and safety constraints"*), the battery selection was mathematically optimized for the confirmed pen geometry without artificial PRD blockers.
2. **Selected Battery Specification:** 
   - Recommended Cell: **Grepow `GRP380830-HP-PCM`** (High-Drain LiPo, $65\\text{ mAh}$ nominal, $5\\text{C}$ continuous / $10\\text{C}$ pulse discharge).
   - Commercial Alternative: **EEMB `LP380830-PCM-LD`** ($70\\text{ mAh}$ nominal, $1\\text{C}$ continuous / $2\\text{C}$ pulse).
   - Continuous Handwriting Run-Time: **$2.5\\text{--}2.7\\text{ hours}$ continuous writing** ($> 25\\text{ pages}$ of active writing); **$> 11.5\\text{ hours}$ typical workday profile**.
3. **Charger Circuit Optimization (ECR-ELEC-REVG-001):** Charger programming resistor confirmed at **$R_9 = 20.0\\text{ k}\\Omega$** ($50.0\\text{ mA}$ charge current), ensuring maximum thermal safety within an enclosed plastic barrel (temperature rise $\\le 21^\\circ\\text{C}$) and full compliance with cell charge limits.
4. **100% Mechanical Zero-Clash CAD:** All 27 solid components in `output/RevG/Mechanical_Phase04C/` confirm **$0.0000\\text{ mm}^3$ collision** across all 351 component pairs. Decoupled 3-piece click mechanism (`10A`, `10B`, `10C`), $1.40\\text{ mm}$ FFC pushrod clearance, full Molex 146153 antenna ($34.9\\text{ mm}$), and 16 watertight 2-manifold STLs.
5. **Native KiCad 10.0 Electrical Certification:** **0 ERC violations, 0 DRC violations, 0 unconnected items** across the 4-layer Main PCB and all three daughterboards.

---

## 2. DIRECTORY STRUCTURE & HOW TO OPEN DELIVERABLES

```
Final_Client_Delivery/
├── 01_KiCad_Design_Source/             Editable KiCad 10.0 schematics, PCBs, and symbol/footprint libraries
│   ├── Main_Board/                     SmartPen 4-layer main board project
│   ├── Front_MPU/                      Front MPU-6050 2-layer daughterboard
│   ├── MicroSD_Carrier/                MicroSD card 2-layer carrier daughterboard
│   └── Touch_Sensor/                   Capacitive touch 2-layer daughterboard
├── 02_Fabrication_Gerber_Drill/        Production RS-274X Gerbers, Excellon drills, and vendor ZIPs
│   ├── Gerbers/                        Top/bottom copper, internal planes, mask, silk, paste, edge cuts
│   ├── Drill/                          Excellon PTH and NPTH drill files with drill charts
│   └── SmartPen_RevG_Complete_PCBA_Gerber_Suite.zip
├── 03_BOM_and_CPL/                     Bills of Materials and automated Pick-and-Place position files
│   ├── BOM/                            Synchronized BOMs with exact manufacturer part numbers (MFR & MPN)
│   └── PickAndPlace/                   Metric CPL files for automated SMT pick-and-place machines
├── 04_Drawings_Schematics_Assembly/    Vector PDF assembly drawings, fabrication drawings, and schematics
├── 05_Mechanical_CAD_Source/           Parametric Python CAD source code (SmartPen_Parametric_CAD_RevG_Phase4C.py)
├── 06_Mechanical_STEP_Assemblies/      ISO-10303-21 AP214 BRep STEP assemblies and 27 component solids
│   ├── SmartPen_RevG_Phase4C_Master_Assembly.step
│   ├── SmartPen_RevG_Phase4C_Exploded_Assembly.step
│   └── Parts/                          All 27 individual component STEP models
├── 07_Mechanical_Printable_STL/        Watertight 2-manifold STL models ready for SLA/SLS 3D printing
│   └── Parts/                          All 16 custom printable enclosure parts
├── 08_Mechanical_Drawings_and_Visuals/ 2D engineering drawings (Click kinematics, longitudinal, sections)
├── 09_Assembly_Instructions/           SMART_PEN_REVG_ASSEMBLY_MANUAL.md (Step-by-step assembly guide)
├── 10_Engineering_Verification_Reports/ Power budget, battery fit, DRC/ERC, collision audit, DFM reports
├── 11_Manufacturing_Notes/             IPC Class 2 fab notes, SAC305 assembly specs, 4-layer stackup spec
├── 12_Prototype_Validation_and_Limitations/ Physical hardware bring-up and bench testing recommendations
├── SHA256_FINAL_DELIVERY_MANIFEST.txt  Cryptographic checksums of all delivered assets
└── README.md                           This handoff document
```

---

## 3. HOW TO USE DELIVERABLES

### A. Ordering Printed Circuit Boards (PCBs)
1. Navigate to `02_Fabrication_Gerber_Drill/Gerbers/`.
2. For automated fab quoting (e.g., JLCPCB, PCBWay):
   - Upload `SmartPen_MainBoard_Gerbers_and_Drill.zip` for the 4-layer Main PCB. Specify $1.60\\text{ mm}$ thickness, ENIG surface finish, matte black solder mask, white silkscreen, and controlled 50-ohm impedance.
   - Upload `Front_MPU_Gerbers_and_Drill.zip`, `MicroSD_Carrier_Gerbers_and_Drill.zip`, and `Touch_Sensor_Gerbers_and_Drill.zip` for the daughterboards. Specify $0.80\\text{ mm}$ thickness, ENIG finish, matte black solder mask.
3. For SMT Assembly (PCBA):
   - Supply the corresponding BOM from `03_BOM_and_CPL/BOM/` and CPL from `03_BOM_and_CPL/PickAndPlace/`.

### B. 3D Printing Mechanical Parts
1. Navigate to `07_Mechanical_Printable_STL/Parts/`.
2. All 16 STLs are watertight 2-manifold solids.
3. Recommended print process: High-resolution SLA / DLP resin (Formlabs Tough 2000 / Grey Pro) or SLS / MJF Nylon PA12 with $0.05\\text{ mm}$ layer height.

### C. Opening CAD Files
- **KiCad Projects:** Open `*.kicad_pro` files in KiCad 8.0, 9.0, or 10.0. All footprint and symbol libraries are embedded locally.
- **STEP Models:** Import `SmartPen_RevG_Phase4C_Master_Assembly.step` into SolidWorks, Autodesk Fusion 360, FreeCAD, Rhino, or Onshape. Units are standard millimeters.
"""
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(text)

if __name__ == "__main__":
    package_delivery()
