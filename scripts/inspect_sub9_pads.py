import json, sys
sys.path.insert(0, '.')

with open('output/RevF_Working/solved_coords.json') as f:
    coords = json.load(f)

# Update Subsystems 7 & 8 coordinates
coords['C1'] = [39.80, 1.52]
coords['R18'] = [55.00, 2.35]
coords['J_BAT'] = [62.90, 1.72]
coords['U2'] = [67.00, 4.07]
coords['R9'] = [66.20, 6.80]
coords['C11'] = [67.95, 7.70]
coords['C12'] = [69.04, 1.50]
coords['FB1'] = [46.23, 7.55]

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

sub9_refs = ['C14', 'U_ESD', 'R5', 'R6', 'R7', 'R8', 'C10', 'J_USB']
for ref in sub9_refs:
    cx, cy = coords[ref]
    print(f"=== {ref} at ({cx:.3f}, {cy:.3f}) ===")
    for p in fp_defs[ref]:
        px = cx + p['dx']
        py = cy + p['dy']
        print(f"  Pin {p['num']:2s}: ({px:6.3f}, {py:6.3f}), net={p['net']}")

