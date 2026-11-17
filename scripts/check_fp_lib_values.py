from pathlib import Path
import re
import sys
sys.path.append('scripts')
from inspect_exact_fp import parse_kicad_pcb_footprints

pcb_fps = parse_kicad_pcb_footprints('output/RevG/variants/FourLayer_ECR_R9_50mA/SmartPen.kicad_pcb')
fp_dir = Path('output/RevG/variants/FourLayer_ECR_R9_50mA/SmartPen.pretty')

print("Checking footprint value text vs PCB value:")
for f in sorted(fp_dir.glob('*.kicad_mod')):
    content = f.read_text(encoding='utf-8')
    val_m = re.search(r'\(fp_text\s+value\s+"([^"]+)"', content)
    ref_name = f.stem
    if ref_name in pcb_fps:
        pcb_val = pcb_fps[ref_name]['val']
        fp_val = val_m.group(1) if val_m else 'NONE'
        if fp_val != pcb_val:
            print(f"MISMATCH in {f.name}: mod value='{fp_val}' vs PCB value='{pcb_val}'")
    else:
        # Some footprints are shared (e.g. Q1 used by Q2, J_PWR used by U4)
        fp_val = val_m.group(1) if val_m else 'NONE'
        print(f"Footprint {f.name} (val='{fp_val}') not direct reference on PCB (might be shared)")
