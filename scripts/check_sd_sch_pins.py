with open('output/RevF_Working/MicroSD_Carrier/MicroSD_Carrier.kicad_sch', 'r', encoding='utf-8') as f:
    text = f.read()

import re
pins = re.findall(r'\(pin\s+"([^"]*)"', text)
print('Pins in MicroSD_Carrier.kicad_sch:', set(pins))
