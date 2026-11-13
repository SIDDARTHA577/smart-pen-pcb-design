with open('output/RevF_Working/SmartPen.kicad_pcb', 'r', encoding='utf-8') as f:
    pcb = f.read()

import re
fp_pos = pcb.find('"SmartPen:J_USB"')
end = pcb.find('(footprint', fp_pos + 10)
block = pcb[fp_pos:end]
pads = re.findall(r'\(pad\s+"([^"]+)"\s+\w+\s+\w+\s+\(at\s+([0-9.-]+)\s+([0-9.-]+)\).*?\(net\s+\d+\s+"([^"]+)"\)', block)
for p in sorted(pads, key=lambda x: float(x[1])):
    print(f"Pad {p[0]:>2} at X={float(p[1]):+5.2f}, Y={float(p[2]):+5.2f} net={p[3]}")
