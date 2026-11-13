with open('output/RevF_Working/MicroSD_Carrier/MicroSD_Carrier.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

import re
pads = re.findall(r'\(pad\s+"([^"]*)"', text)
print('Pad numbers in MicroSD_Carrier:', set(pads))
