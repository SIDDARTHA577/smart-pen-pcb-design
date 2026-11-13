import json, sys
sys.path.insert(0, '.')
from scripts.pcb_geom import dist_segment_to_rect

with open('output/RevF_Working/solved_coords.json') as f:
    coords = json.load(f)
with open('output/RevF_Working/SmartPen_RevE_PCB.json') as f:
    pcb_json = json.load(f)

nets = set(['GND'])
for item in pcb_json['shape']:
    if isinstance(item, str) and item.startswith('LIB~'):
        for sub in item.split('#@$'):
            if sub.startswith('PAD~'):
                ptoks = sub.split('~')
                if len(ptoks) > 7 and ptoks[7]:
                    nets.add(ptoks[7])
sorted_nets = [''] + sorted(list(nets))

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

# Check escape path for R6.1: from (73.56, 2.46) East to (75.5, 2.46), then to a via at (75.5, 1.0)
p1 = (73.56, 2.46)
v_test = (75.5, 1.0)

# Check segment (73.56, 2.46) -> (75.5, 2.46)
seg1_clear = True
for pad in all_pads:
    if pad['net'] == 'USB_CC2': continue
    d = dist_segment_to_rect(p1[0], p1[1], v_test[0], p1[1], pad['x'], pad['y'], pad['w'], pad['h'])
    if d < 0.10 + 0.13:
        seg1_clear = False
        print(f"Seg1 collides with {pad['ref']}.{pad['pin']} ({pad['net']}) dist={d:.3f}")

# Check segment (75.5, 2.46) -> (75.5, 1.0)
seg2_clear = True
for pad in all_pads:
    if pad['net'] == 'USB_CC2': continue
    d = dist_segment_to_rect(v_test[0], p1[1], v_test[0], v_test[1], pad['x'], pad['y'], pad['w'], pad['h'])
    if d < 0.10 + 0.13:
        seg2_clear = False
        print(f"Seg2 collides with {pad['ref']}.{pad['pin']} ({pad['net']}) dist={d:.3f}")

print(f"Escape path to via (75.5, 1.0): Seg1={seg1_clear}, Seg2={seg2_clear}")

