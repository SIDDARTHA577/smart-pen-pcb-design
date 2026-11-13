with open('output/RevF_Working/SmartPen.kicad_sch', encoding='utf-8') as f:
    text = f.read()

import re
# Find J_IMU pins and connected wires/nets
idx = text.find('"J_IMU"')
print(text[idx-200:idx+1200])
