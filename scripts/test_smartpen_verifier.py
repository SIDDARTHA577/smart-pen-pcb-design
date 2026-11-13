import json, sys
sys.path.insert(0, '.')
from scripts.verify_smartpen_geometry import check_pcb_geometry

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
net_id_map = {n: i for i, n in enumerate(sorted_nets)}

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

# Read generated SmartPen.kicad_pcb
import re
segments = []
vias = []
with open('output/RevF_Working/SmartPen.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

# Map net names to net ids
net_name_by_id = {}
for m in re.finditer(r'\(net\s+(\d+)\s+"([^"]*)"\)', text):
    net_name_by_id[int(m.group(1))] = m.group(2)

for m in re.finditer(r'\(via\s+\(at\s+([\d\.-]+)\s+([\d\.-]+)\).*?\(net\s+(\d+)\)', text):
    vx, vy, nid = float(m.group(1)), float(m.group(2)), int(m.group(3))
    vias.append((vx, vy, net_name_by_id.get(nid, '')))

for m in re.finditer(r'\(segment\s+\(start\s+([\d\.-]+)\s+([\d\.-]+)\)\s+\(end\s+([\d\.-]+)\s+([\d\.-]+)\)\s+\(width\s+([\d\.-]+)\)\s+\(layer\s+"([^"]+)"\)\s+\(net\s+(\d+)\)\)', text):
    x1, y1, x2, y2, w, lyr, nid = float(m.group(1)), float(m.group(2)), float(m.group(3)), float(m.group(4)), float(m.group(5)), m.group(6), int(m.group(7))
    segments.append((x1, y1, x2, y2, lyr, net_name_by_id.get(nid, ''), w))

print(f"Loaded {len(all_pads)} pads, {len(segments)} segments, {len(vias)} vias.")
errors = check_pcb_geometry(all_pads, segments, vias)
print(f"\nGeometric check found {len(errors)} errors:")
for e in errors[:30]:
    print("  ", e)
if len(errors) > 30:
    print(f"  ... and {len(errors) - 30} more.")
