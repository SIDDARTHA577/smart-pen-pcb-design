import json, sys
sys.path.insert(0, '.')
from scripts.verify_smartpen_geometry import check_pcb_geometry

with open('output/RevF_Working/solved_coords.json') as f:
    coords = json.load(f)

# Coordinates
coords['C1'] = [39.80, 1.52]
coords['R18'] = [55.00, 2.35]
coords['FB1'] = [46.23, 7.55]
coords['J_BAT'] = [62.80, 1.72]
coords['U2'] = [67.00, 4.07]
coords['R9'] = [66.30, 6.70]
coords['C11'] = [68.00, 7.75]
coords['C12'] = [68.30, 1.40]
coords['C14'] = [71.05, 1.40]

# USB components layout:
# J_USB pins at Y = 3.10:
# J_USB.2 (VBUS) at 76.00
# J_USB.5 (CC1) at 77.60
# J_USB.7 (DP_PORT) at 78.15
# J_USB.9 (DM_PORT) at 78.65
# J_USB.6 (CC2) at 79.20
# J_USB.10 (VBUS) at 80.80

# South zone placement:
# R6 (CC2 pull-down): near Pin 6
coords['R6'] = [79.675, 1.80] # Pin 1 (CC2) at 79.20, Pin 2 (GND) at 80.15
# R8 (DP series resistor): near Pin 7
coords['R8'] = [77.675, 1.80] # Pin 1 (DP_PORT) at 78.15, Pin 2 (DP_CORE) at 77.20
# R7 (DM series resistor): near Pin 9
coords['R7'] = [78.650, 1.00] # Pin 1 (DM_PORT) at 78.65, Pin 2 (DM_CORE) at ... wait, rotated vertical or horizontal

with open('output/RevF_Working/SmartPen_RevE_PCB.json') as f:
    pcb_json = json.load(f)

fp_defs = {}
for item in pcb_json['shape']:
    if isinstance(item, str) and item.startswith('LIB~'):
        subs = item.split('#@$')
        ref = ''
        for sub in subs:
            if sub.startswith('TEXT~P~'): ref = sub.split('~')[10]
        if not ref: continue
        orig_x, orig_y = float(subs[0].split('~')[1]), float(subs[0].split('~')[2])
        pads_sub = []
        for sub in subs:
            if sub.startswith('PAD~'):
                ptoks = sub.split('~')
                dx = (float(ptoks[2]) - orig_x) * 0.254
                dy = (float(ptoks[3]) - orig_y) * 0.254
                pads_sub.append({
                    'num': ptoks[8], 'net': ptoks[7],
                    'dx': round(dx, 4), 'dy': round(dy, 4),
                    'w': round(float(ptoks[4]) * 0.254, 4),
                    'h': round(float(ptoks[5]) * 0.254, 4)
                })
        fp_defs[ref] = pads_sub

# Make R9 vertical
for p in fp_defs['R9']:
    p['dx'], p['dy'] = p['dy'], p['dx']
    p['w'], p['h'] = p['h'], p['w']

pads = []
for ref, (cx, cy) in coords.items():
    if ref in fp_defs:
        for p in fp_defs[ref]:
            pads.append({
                'ref': ref, 'pin': p['num'], 'net': p['net'],
                'x': round(cx + p['dx'], 4), 'y': round(cy + p['dy'], 4),
                'w': p['w'], 'h': p['h']
            })

errs = check_pcb_geometry(pads, [], [])
print(f"Pads check: {len(errs)} errors")
for e in errs:
    print(" ", e)

