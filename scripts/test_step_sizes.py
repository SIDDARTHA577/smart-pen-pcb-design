import json, sys
sys.path.insert(0, '.')
from scripts.pcb_geom import dist_segment_to_rect

with open('output/RevF_Working/solved_coords.json') as f:
    coords = json.load(f)
with open('output/RevF_Working/SmartPen_RevE_PCB.json') as f:
    pcb_json = json.load(f)

fp_defs = {}
for item in pcb_json['shape']:
    if isinstance(item, str) and item.startswith('LIB~'):
        subs = item.split('#@$')
        ref = ''
        for sub in subs:
            if sub.startswith('TEXT~P~'):
                ref = sub.split('~')[10]
        if not ref: continue
        lib_toks = subs[0].split('~')
        orig_x, orig_y = float(lib_toks[1]), float(lib_toks[2])
        pads = []
        for sub in subs:
            if sub.startswith('PAD~'):
                ptoks = sub.split('~')
                dx = (float(ptoks[2]) - orig_x) * 0.254
                dy = (float(ptoks[3]) - orig_y) * 0.254
                pw = float(ptoks[4]) * 0.254
                ph = float(ptoks[5]) * 0.254
                pads.append({'num': ptoks[8], 'net': ptoks[7], 'dx': round(dx, 4), 'dy': round(dy, 4), 'w': round(pw, 4), 'h': round(ph, 4)})
        fp_defs[ref] = pads

all_pads = []
for ref, (cx, cy) in coords.items():
    if ref in fp_defs:
        for p in fp_defs[ref]:
            all_pads.append({
                'ref': ref, 'pin': p['num'], 'net': p['net'],
                'x': round(cx + p['dx'], 4), 'y': round(cy + p['dy'], 4),
                'w': p['w'], 'h': p['h']
            })

p1 = (73.56, 2.46)
for dist in [0.3, 0.4, 0.5, 0.6]:
    for name, (dx, dy) in [("West", (-dist, 0)), ("North", (0, dist)), ("South", (0, -dist))]:
        p_end = (p1[0] + dx, p1[1] + dy)
        min_d = float('inf')
        closest_pad = None
        for pad in all_pads:
            if pad['net'] == 'USB_CC2': continue
            d = dist_segment_to_rect(p1[0], p1[1], p_end[0], p_end[1], pad['x'], pad['y'], pad['w'], pad['h'])
            if d < min_d:
                min_d = d
                closest_pad = pad
        print(f"Step {dist:.1f} mm {name:5s}: min_d = {min_d:.3f} mm to {closest_pad['ref']}.{closest_pad['pin']} ({closest_pad['net']})")

