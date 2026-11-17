from pathlib import Path
import re
import csv

def inspect_board_bom(sch_path, pcb_path, name):
    print(f"\n=================== {name} ===================")
    sch_text = Path(sch_path).read_text(encoding='utf-8')
    pcb_text = Path(pcb_path).read_text(encoding='utf-8')
    
    # parse sch
    sym_blocks = re.findall(r'\(symbol\s+\(lib_id\s+"[^"]+"\).*?\n  \)', sch_text, re.DOTALL)
    sch_items = {}
    for block in sym_blocks:
        ref_m = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', block)
        val_m = re.search(r'\(property\s+"Value"\s+"([^"]+)"', block)
        fp_m = re.search(r'\(property\s+"Footprint"\s+"([^"]+)"', block)
        if ref_m and val_m:
            ref = ref_m.group(1)
            if not ref.startswith('#'):
                sch_items[ref] = {'val': val_m.group(1), 'fp': fp_m.group(1) if fp_m else ''}
                
    # parse pcb
    fp_blocks = re.findall(r'\(footprint\s+"[^"]+".*?\n\t\)', pcb_text, re.DOTALL)
    pcb_items = {}
    for block in fp_blocks:
        ref_m = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', block)
        val_m = re.search(r'\(property\s+"Value"\s+"([^"]+)"', block)
        if ref_m and val_m:
            ref = ref_m.group(1)
            pcb_items[ref] = {'val': val_m.group(1)}
            
    print(f"SCH Components: {len(sch_items)}, PCB Footprints: {len(pcb_items)}")
    for ref, info in sorted(sch_items.items()):
        pcb_val = pcb_items.get(ref, {}).get('val', 'MISSING')
        print(f"  {ref}: {info['val']} (FP: {info['fp']}) -> PCB: {pcb_val}")

inspect_board_bom('output/RevG/Front_MPU/Front_MPU.kicad_sch', 'output/RevG/Front_MPU/Front_MPU.kicad_pcb', 'Front_MPU')
inspect_board_bom('output/RevG/MicroSD_Carrier/MicroSD_Carrier.kicad_sch', 'output/RevG/MicroSD_Carrier/MicroSD_Carrier.kicad_pcb', 'MicroSD_Carrier')
inspect_board_bom('output/RevG/Touch_Sensor/Touch_Sensor.kicad_sch', 'output/RevG/Touch_Sensor/Touch_Sensor.kicad_pcb', 'Touch_Sensor')
