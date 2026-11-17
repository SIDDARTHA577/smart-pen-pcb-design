#!/usr/bin/env python3
"""
Apply ECR-ELEC-REVG-001 (R9 = 20.0 kΩ, 50 mA Charge Current) to FourLayer_ECR_R9_50mA variant.
Preserves FourLayer_Candidate and 2-layer baseline.
"""
import os
import re

def update_schematic():
    sch_path = 'output/RevG/variants/FourLayer_ECR_R9_50mA/SmartPen.kicad_sch'
    with open(sch_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    if 'RC0402FR-0720KL' in text:
        print("SmartPen.kicad_sch already has RC0402FR-0720KL")
        return

    lines = text.splitlines(keepends=True)
    updated_lib = False
    updated_inst = False
    in_r9_lib = False
    in_r9_inst = False

    for i, line in enumerate(lines):
        if '(symbol "SmartPen_Lib:R9"' in line:
            in_r9_lib = True
        elif in_r9_lib:
            if '(property "Value" "RC0402FR-0710KL"' in line:
                lines[i] = line.replace('RC0402FR-0710KL', 'RC0402FR-0720KL')
                updated_lib = True
                in_r9_lib = False
            elif line.strip().startswith('(symbol ') or line.strip().startswith(')'):
                in_r9_lib = False

        if '(symbol (lib_id "SmartPen_Lib:R9")' in line:
            in_r9_inst = True
        elif in_r9_inst:
            if '(property "Value" "RC0402FR-0710KL"' in line:
                lines[i] = line.replace('RC0402FR-0710KL', 'RC0402FR-0720KL')
                updated_inst = True
                in_r9_inst = False
            elif line.strip().startswith(')') and not line.strip().startswith(') (effects'):
                in_r9_inst = False

    # Also update title block comment to reflect ECR
    for i, line in enumerate(lines):
        if '(comment 1 "Phase 3C Four-Layer Routing & Independent Quality Gate")' in line:
            lines[i] = '    (comment 1 "Phase 4C ECR-ELEC-REVG-001: R9=20k (50mA Charge)")\n'

    with open(sch_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print("Updated SmartPen.kicad_sch: R9 set to RC0402FR-0720KL")

def update_pcb():
    pcb_path = 'output/RevG/variants/FourLayer_ECR_R9_50mA/SmartPen.kicad_pcb'
    with open(pcb_path, 'r', encoding='utf-8') as f:
        text = f.read()

    if 'RC0402FR-0720KL' in text:
        print("SmartPen.kicad_pcb already has RC0402FR-0720KL")
        return

    lines = text.splitlines(keepends=True)
    updated_pcb = False
    in_r9_fp = False

    for i, line in enumerate(lines):
        if '(footprint "SmartPen:R9"' in line:
            in_r9_fp = True
        elif in_r9_fp:
            if '(property "Value" "RC0402FR-0710KL"' in line:
                lines[i] = line.replace('RC0402FR-0710KL', 'RC0402FR-0720KL')
                updated_pcb = True
                in_r9_fp = False
            elif line.startswith('\t(footprint '):
                in_r9_fp = False

    for i, line in enumerate(lines):
        if '(comment 1 "Phase 3C Four-Layer Routing & Independent Quality Gate")' in line:
            lines[i] = '\t\t(comment 1 "Phase 4C ECR-ELEC-REVG-001: R9=20k (50mA Charge)")\n'

    assert updated_pcb, "Failed to update R9 in PCB footprint"

    with open(pcb_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print("Updated SmartPen.kicad_pcb: R9 set to RC0402FR-0720KL")

def update_sym_lib():
    lib_path = 'output/RevG/variants/FourLayer_ECR_R9_50mA/SmartPen_Lib.kicad_sym'
    with open(lib_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    in_r9 = False
    updated = False
    for i, line in enumerate(lines):
        if '(symbol "R9"' in line:
            in_r9 = True
        elif in_r9:
            if '(property "Value" "RC0402FR-0710KL"' in line:
                lines[i] = line.replace('RC0402FR-0710KL', 'RC0402FR-0720KL')
                updated = True
                in_r9 = False
            elif line.startswith('  (symbol '):
                in_r9 = False

    if updated:
        with open(lib_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print("Updated SmartPen_Lib.kicad_sym: R9 set to RC0402FR-0720KL")
    else:
        print("SmartPen_Lib.kicad_sym already updated or not found")

if __name__ == '__main__':
    update_schematic()
    update_pcb()
    update_sym_lib()
