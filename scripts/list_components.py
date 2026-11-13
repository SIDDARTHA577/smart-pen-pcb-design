import re

with open('output/RevF_Working/SmartPen.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

footprints = re.findall(r'\(footprint\s+"([^"]+)".*?\(at\s+([0-9.]+)\s+([0-9.]+)(?:\s+([0-9.-]+))?\).*?\(fp_text\s+reference\s+"([^"]+)"', text, re.DOTALL)
print(f"Total footprints: {len(footprints)}")
for fp in sorted(footprints, key=lambda x: float(x[1])):
    rot = fp[3] if fp[3] else "0"
    print(f"Ref: {fp[4]:<8} Lib: {fp[0]:<20} at ({float(fp[1]):6.2f}, {float(fp[2]):5.2f}) rot: {rot}")
