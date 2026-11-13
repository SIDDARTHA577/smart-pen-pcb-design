import json, math, sys

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

pads = []
for ref, (cx, cy) in coords.items():
    if ref in fp_defs:
        for p in fp_defs[ref]:
            pads.append({
                'ref': ref, 'pin': p['num'], 'net': p['net'],
                'x': round(cx + p['dx'], 4), 'y': round(cy + p['dy'], 4),
                'w': p['w'], 'h': p['h']
            })

def test_vias(vlist):
    errs = []
    for i in range(len(vlist)):
        v1 = vlist[i]
        for j in range(i+1, len(vlist)):
            v2 = vlist[j]
            d = math.hypot(v1[0]-v2[0], v1[1]-v2[1])
            if d < 0.58: errs.append(f'Via dist {v1[2]} vs {v2[2]}: {d:.3f}')
        for p in pads:
            if p['net'] == v1[2]: continue
            dx = max(0.0, abs(v1[0] - p['x']) - p['w']/2.0)
            dy = max(0.0, abs(v1[1] - p['y']) - p['h']/2.0)
            d = math.hypot(dx, dy)
            if d < 0.38: errs.append(f'Via {v1[2]} at ({v1[0]},{v1[1]}) collides with {p["ref"]}.{p["pin"]} ({p["net"]}): dist={d:.3f}')
    return errs

vias = [
    (41.13, 1.15, 'SD_MOSI'),
    (41.63, 1.55, 'SD_MISO'),
    (42.13, 0.85, '3V3_RTC'),
    (42.63, 1.55, 'SD_SCK'),
    (43.13, 0.85, 'SD_CS'),
    (44.13, 1.45, 'BOOT9'),
]
errs = test_vias(vias)
print(f'Candidate errors: {len(errs)}')
for e in errs: print(' ', e)
