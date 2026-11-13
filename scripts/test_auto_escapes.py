"""Test automated outward escape & via placement for all pads."""
import json, math, sys
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
                'w': p['w'], 'h': p['h'],
                'comp_x': cx, 'comp_y': cy
            })

def is_via_clear(vx, vy, my_net, existing_vias):
    if vx - 0.25 < 0.35 or vx + 0.25 > 83.65: return False
    if vy - 0.25 < 0.35 or vy + 0.25 > 8.85: return False
    
    for ex_v in existing_vias:
        if math.hypot(vx - ex_v[0], vy - ex_v[1]) < 0.60:
            return False
            
    for p in all_pads:
        if p['net'] == my_net: continue
        dx = max(0.0, abs(vx - p['x']) - p['w']/2.0)
        dy = max(0.0, abs(vy - p['y']) - p['h']/2.0)
        if math.hypot(dx, dy) < 0.25 + 0.13: # 0.38 mm
            return False
    return True

def is_stub_clear(px, py, vx, vy, my_net):
    # Two orthogonal segments: (px, py) -> (vx, py) -> (vx, vy) or (px, py) -> (px, vy) -> (vx, vy)
    for p in all_pads:
        if p['net'] == my_net: continue
        d1 = dist_segment_to_rect(px, py, vx, py, p['x'], p['y'], p['w'], p['h'])
        d2 = dist_segment_to_rect(vx, py, vx, vy, p['x'], p['y'], p['w'], p['h'])
        if min(d1, d2) < 0.10 + 0.13:
            return False
    return True

# Test finding via for each active pad
active_pads = [p for p in all_pads if p['net'] and p['net'] != 'GND']
print(f"Total active pads: {len(active_pads)}")

placed_vias = []
success = 0
for p in active_pads:
    px, py = p['x'], p['y']
    cx, cy = p['comp_x'], p['comp_y']
    net = p['net']
    
    # Priority direction: outward from component center
    dx_c = px - cx
    dy_c = py - cy
    base_ang = math.atan2(dy_c, dx_c) if (abs(dx_c) > 0.01 or abs(dy_c) > 0.01) else (math.pi/2 if py < 4.6 else -math.pi/2)
    
    found = None
    for r in [0.65, 0.80, 0.95, 1.10, 1.30, 1.50, 1.80, 2.10]:
        for ang_offset in [0, 45, -45, 90, -90, 135, -135, 180]:
            ang = base_ang + math.radians(ang_offset)
            vx = round(px + r * math.cos(ang), 3)
            vy = round(py + r * math.sin(ang), 3)
            if is_via_clear(vx, vy, net, placed_vias) and is_stub_clear(px, py, vx, vy, net):
                found = (vx, vy)
                break
        if found: break
    
    if found:
        placed_vias.append((found[0], found[1], net))
        success += 1
    else:
        print(f"Failed to find via for {p['ref']}.{p['pin']} ({net}) at ({px}, {py})")

print(f"\nResult: {success} / {len(active_pads)} pads successfully placed clean via + stub!")

