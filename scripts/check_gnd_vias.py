with open('output/RevF_Working/SmartPen.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

import re
vias = re.findall(r'\(via\s+.*?\)', text)
gnd_vias = [v for v in vias if '"/GND"' in v]
print(f'Total vias: {len(vias)}, GND vias: {len(gnd_vias)}')
for gv in gnd_vias:
    print('  ', gv)
