import json, sys
sys.path.insert(0, '.')
from scripts.verify_smartpen_geometry import check_pcb_geometry

# Load base solved coords
with open('output/RevF_Working/solved_coords.json') as f:
    coords = json.load(f)

# Apply all validated coordinate fixes:
coords['C1'] = [39.80, 1.52]
coords['FB1'] = [46.23, 7.55]
coords['R18'] = [55.00, 2.35]
coords['J_BAT'] = [62.80, 1.72]
coords['U2'] = [67.00, 4.07]
coords['R9'] = [66.30, 6.70]
coords['C11'] = [68.00, 7.75]
coords['C12'] = [68.15, 1.40]
coords['C14'] = [70.014, 2.00]
coords['U_ESD'] = [72.00, 4.49]
coords['C10'] = [74.50, 1.50]
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

# Vertical footprint definitions:
for ref in ['R9', 'R5', 'R6', 'C14']:
    for p in fp_defs[ref]:
        p['dx'], p['dy'] = p['dy'], p['dx']
        p['w'], p['h'] = p['h'], p['w']

for p in fp_defs['C14']:
    p['dy'] = 0.75 if p['num'] == '1' else -0.75

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

segments = []
vias = set()

def add_seg(x1, y1, x2, y2, layer, net_name, width=0.18):
    if abs(x1 - x2) > 0.0005 or abs(y1 - y2) > 0.0005:
        segments.append((round(x1, 3), round(y1, 3), round(x2, 3), round(y2, 3), layer, net_name, width))

def add_via(vx, vy, net_name):
    vias.add((round(vx, 3), round(vy, 3), net_name))

# ==================== SUBSYSTEMS 1 TO 6 ====================
# (From validated scripts/solve_smartpen_zero_drc.py)
exec(open('scripts/extract_sub1_to_6.py').read()) if False else None

print("Assembling and testing master PCB geometry...")

