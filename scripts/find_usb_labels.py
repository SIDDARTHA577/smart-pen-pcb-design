with open('output/RevF_Working/SmartPen.kicad_sch', 'r', encoding='utf-8') as f:
    sch = f.read()

import re
for net in ['USB_DP', 'USB_DM', 'USB_DP_PORT', 'USB_DM_PORT', 'USB_DP_CORE', 'USB_DM_CORE']:
    matches = re.findall(rf'\(label\s+"({net}[^"]*)"\s+\(at\s+([0-9.]+)\s+([0-9.]+)', sch)
    print(f"Net {net}: {len(matches)} occurrences: {matches}")
