import json, sys, math
sys.path.insert(0, '.')
from scripts.verify_smartpen_geometry import check_pcb_geometry

with open('output/RevF_Working/solved_coords.json') as f:
    coords = json.load(f)

# Subsystems 1 to 8 coordinates
coords['C1'] = [39.80, 1.52]
coords['R18'] = [55.00, 2.35]
coords['FB1'] = [46.23, 7.55]
coords['J_BAT'] = [62.80, 1.72]
coords['U2'] = [67.00, 4.07]
coords['R9'] = [66.30, 6.70]
coords['C11'] = [68.00, 7.75]
coords['C12'] = [68.30, 1.40]
coords['C14'] = [71.05, 1.40]

# Subsystem 9 components:
# J_USB is at (78.40, 4.60)
# C10 at (75.20, 1.50) (VBUS cap)
coords['C10'] = [75.20, 1.50]
# R5 at (76.80, 1.80) (CC1 pull-down)
coords['R5'] = [76.80, 1.80]
# R8 at (78.15, 1.90) (DP resistor)
coords['R8'] = [78.15, 1.90]
# R7 at (78.65, 1.90) (DM resistor)
# Wait, distance between 78.15 and 78.65 is 0.50 mm. Two 0402s side-by-side need width ~0.60 mm.
# Can R7 be staggered (e.g. at Y = 1.00 or R8 at Y = 2.10, R7 at Y = 1.20)?
coords['R8'] = [78.15, 2.20]
coords['R7'] = [78.65, 1.20]
coords['R6'] = [79.70, 1.80]

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

# Make R9, R7, R8 vertical
for ref in ['R9', 'R7', 'R8']:
    for p in fp_defs[ref]:
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

