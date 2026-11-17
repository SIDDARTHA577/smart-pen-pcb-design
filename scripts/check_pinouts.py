from pathlib import Path
import re

sch_text = Path('output/RevG/variants/FourLayer_ECR_R9_50mA/SmartPen.kicad_sch').read_text(encoding='utf-8')
pcb_text = Path('output/RevG/variants/FourLayer_ECR_R9_50mA/SmartPen.kicad_pcb').read_text(encoding='utf-8')

# Find instances in schematic
print("=== SCHEMATIC INSTANCES ===")
for ref in ['Q1', 'Q2', 'U4']:
    # match instance like: (symbol (lib_id "SmartPen_Lib:Q1") (at ... (property "Reference" "Q1" ...
    matches = re.findall(r'\(symbol\s+\(lib_id\s+"[^"]+"\)\s+\(at\s+[^\)]+\).*?\(property\s+"Reference"\s+"' + ref + r'".*?\n  \)', sch_text, re.DOTALL)
    for m in matches:
        print(f"SCH Instance for {ref}:")
        print(m)

# Find PCB footprints
print("\n=== PCB FOOTPRINTS ===")
for ref in ['Q1', 'Q2', 'U4']:
    matches = re.findall(r'\(footprint\s+"[^"]+".*?\(property\s+"Reference"\s+"' + ref + r'".*?\n\t\)', pcb_text, re.DOTALL)
    for m in matches:
        print(f"PCB Footprint for {ref}:")
        # print header and pads
        lines = m.split('\n')
        for line in lines[:10]:
            print(" ", line)
        for line in lines:
            if '(pad ' in line:
                print(" ", line.strip())

