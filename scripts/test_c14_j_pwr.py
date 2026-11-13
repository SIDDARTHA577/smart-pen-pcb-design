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

# J_PWR is at [69.06, 5.26]. Pin 3 (3V3) at (70.014, 3.963).
# Place C14 directly South of J_PWR Pin 3:
# C14 horizontal at (69.50, 2.50) -> Pin 1 (3V3) at 68.75, Pin 2 (GND) at 70.25
# Or C14 vertical at (69.80, 2.40) -> Pin 1 (3V3) at (69.80, 3.15), Pin 2 (GND) at (69.80, 1.65)
coords['C14'] = [70.90, 2.00]
coords['C10'] = [73.90, 1.50]
coords['U_ESD'] = [71.80, 4.49]
coords['R8'] = [71.60, 7.50]
coords['R7'] = [73.00, 7.50]
coords['R5'] = [77.60, 6.70]
coords['R6'] = [79.20, 6.70]

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

# Vertical components: R9, R5, R6
for ref in ['R9', 'R5', 'R6']:
    for p in fp_defs[ref]:
        p['dx'], p['dy'] = p['dy'], p['dx']
        p['w'], p['h'] = p['h'], p['w']

# R7 and R8: vertical, Pin 1 (PORT) in North (dy = +0.475), Pin 2 (CORE) in South (dy = -0.475)
for ref in ['R7', 'R8']:
    for p in fp_defs[ref]:
        p['w'], p['h'] = p['h'], p['w']
        p['dx'] = 0.0
        p['dy'] = 0.475 if p['num'] == '1' else -0.475

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
