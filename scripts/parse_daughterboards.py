import re
from pathlib import Path

def parse_all_footprints(path):
    print(f"\n==================================================")
    print(f"Board: {path}")
    content = Path(path).read_text(encoding='utf-8')
    
    # KiCad footprints:
    # can be (footprint "name" ... ) or (module "name" ... )
    fp_starts = [m.start() for m in re.finditer(r'\((footprint|module)\s+', content)]
    print(f"Total footprint blocks: {len(fp_starts)}")
    
    for start in fp_starts:
        # get next 800 chars
        block = content[start:start+1200]
        # reference
        ref_m = re.search(r'\(property\s+\"Reference\"\s+\"([^\"]+)\"', block)
        val_m = re.search(r'\(property\s+\"Value\"\s+\"([^\"]+)\"', block)
        at_m = re.search(r'\(at\s+([\d\.\-]+)\s+([\d\.\-]+)(?:\s+([\d\.\-]+))?\)', block)
        layer_m = re.search(r'\(layer\s+\"([^\"]+)\"', block)
        name_m = re.search(r'\((?:footprint|module)\s+([^\s\)]+)', block)
        
        ref = ref_m.group(1) if ref_m else 'UNKNOWN'
        val = val_m.group(1) if val_m else ''
        at = (float(at_m.group(1)), float(at_m.group(2)), float(at_m.group(3) or 0)) if at_m else (0,0,0)
        layer = layer_m.group(1) if layer_m else ''
        name = name_m.group(1) if name_m else ''
        print(f"  {ref:8s} {val:18s} ({name:28s}) at ({at[0]:7.3f}, {at[1]:7.3f}, rot={at[2]:5.1f}) on {layer}")

if __name__ == '__main__':
    parse_all_footprints('output/RevG/Front_MPU/Front_MPU.kicad_pcb')
    parse_all_footprints('output/RevG/MicroSD_Carrier/MicroSD_Carrier.kicad_pcb')
    parse_all_footprints('output/RevG/Touch_Sensor/Touch_Sensor.kicad_pcb')
