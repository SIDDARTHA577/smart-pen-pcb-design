import json, sys
sys.path.insert(0, '.')
from scripts.verify_smartpen_geometry import check_pcb_geometry

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

def run_test(custom_coords=None, custom_segs=None, custom_vias=None):
    c = dict(coords)
    if custom_coords:
        c.update(custom_coords)
    pads = []
    for ref, (cx, cy) in c.items():
        if ref in fp_defs:
            for p in fp_defs[ref]:
                pads.append({
                    'ref': ref, 'pin': p['num'], 'net': p['net'],
                    'x': round(cx + p['dx'], 4), 'y': round(cy + p['dy'], 4),
                    'w': p['w'], 'h': p['h']
                })
    segs = custom_segs or []
    vias = custom_vias or []
    errs = check_pcb_geometry(pads, segs, vias)
    print(f"Total violations: {len(errs)}")
    for e in errs:
        print(" ", e)
    return len(errs)

if __name__ == '__main__':
    run_test()

