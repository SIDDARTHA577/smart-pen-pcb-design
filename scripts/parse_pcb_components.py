import sys
import re
from pathlib import Path

def parse_kicad_pcb(path):
    print(f"==================================================")
    print(f"Inspecting PCB: {path}")
    print(f"==================================================")
    content = Path(path).read_text(encoding='utf-8')
    
    # 1. Edge.Cuts
    lines = re.findall(r'\(gr_line\s+\(start\s+([\d\.\-]+)\s+([\d\.\-]+)\)\s+\(end\s+([\d\.\-]+)\s+([\d\.\-]+)\).*?\(layer\s+\"?Edge\.Cuts\"?\)', content)
    rects = re.findall(r'\(gr_rect\s+\(start\s+([\d\.\-]+)\s+([\d\.\-]+)\)\s+\(end\s+([\d\.\-]+)\s+([\d\.\-]+)\).*?\(layer\s+\"?Edge\.Cuts\"?\)', content)
    
    xs, ys = [], []
    for l in lines:
        xs.extend([float(l[0]), float(l[2])])
        ys.extend([float(l[1]), float(l[3])])
    for r in rects:
        xs.extend([float(r[0]), float(r[2])])
        ys.extend([float(r[1]), float(r[3])])
        
    if xs and ys:
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        print(f"Outline Bounding Box:")
        print(f"  X: [{min_x:.3f}, {max_x:.3f}] mm (Length: {max_x - min_x:.3f} mm)")
        print(f"  Y: [{min_y:.3f}, {max_y:.3f}] mm (Width:  {max_y - min_y:.3f} mm)")
    else:
        print("No Edge.Cuts lines found.")
        
    # Footprints
    # Format in KiCad 7/8/9/10: (footprint "..." ... (at X Y [rot]) ... (property "Reference" "REF" ...))
    fp_pattern = re.compile(
        r'\(footprint\s+\"([^\"]+)\".*?'
        r'\(at\s+([\d\.\-]+)\s+([\d\.\-]+)(?:\s+([\d\.\-]+))?\).*?'
        r'\(property\s+\"Reference\"\s+\"([^\"]+)\".*?'
        r'\(property\s+\"Value\"\s+\"([^\"]+)\"',
        re.DOTALL
    )
    
    matches = fp_pattern.findall(content)
    print(f"Found {len(matches)} footprints.")
    key_refs = ['U1', 'U2', 'U3', 'U4', 'J_USB', 'J_SD', 'J_RF', 'J_BAT', 'J_IMU', 'SW1', 'SW2', 'SW3', 'M1', 'D1', 'D2', 'D3', 'D4', 'R9', 'C8', 'C9', 'L1', 'L2', 'J1', 'J2', 'J3', 'U5']
    for fp in matches:
        fp_name = fp[0]
        x = float(fp[1])
        y = float(fp[2])
        rot = float(fp[3]) if fp[3] else 0.0
        ref = fp[4]
        val = fp[5]
        if ref in key_refs or len(matches) < 15:
            print(f"  {ref:8s} {val:15s} ({fp_name:30s}) at ({x:8.3f}, {y:8.3f}), rot={rot:5.1f}")

if __name__ == '__main__':
    parse_kicad_pcb('output/RevG/variants/FourLayer_Candidate/SmartPen.kicad_pcb')
    parse_kicad_pcb('output/RevG/Front_MPU/Front_MPU.kicad_pcb')
    parse_kicad_pcb('output/RevG/MicroSD_Carrier/MicroSD_Carrier.kicad_pcb')
    parse_kicad_pcb('output/RevG/Touch_Sensor/Touch_Sensor.kicad_pcb')
