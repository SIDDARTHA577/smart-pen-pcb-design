import json, math, csv

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
            pnet = p['net']
            all_pads.append({
                'ref': ref, 'pin': p['num'], 'net': pnet,
                'x': round(cx + p['dx'], 4), 'y': round(cy + p['dy'], 4),
                'w': p['w'], 'h': p['h']
            })

def is_via_pos_clear(vx, vy, my_net):
    # Via dia 0.50 (radius 0.25). Min clearance to edge: 0.35 mm
    if vx - 0.25 < 0.35 or vx + 0.25 > 83.65: return False
    if vy - 0.25 < 0.35 or vy + 0.25 > 8.85: return False
    
    # Check clearance against all pads on F.Cu
    # Pad is rect [px - w/2, px + w/2] x [py - h/2, py + h/2]
    # For different nets, clearance must be >= 0.15 mm
    for pad in all_pads:
        pnet = pad['net']
        if pnet == my_net:
            continue # Same net is allowed
        # Distance from circle (vx, vy, r=0.25) to rect
        px, py, pw, ph = pad['x'], pad['y'], pad['w'], pad['h']
        dx = max(0.0, abs(vx - px) - pw/2.0)
        dy = max(0.0, abs(vy - py) - ph/2.0)
        dist = math.hypot(dx, dy)
        if dist < 0.25 + 0.15: # via copper radius + clearance
            return False
    return True

# Test finding via position for each pad
found_vias = 0
total_pads = 0
for pad in all_pads:
    if not pad['net'] or pad['net'] == 'GND': continue
    total_pads += 1
    px, py = pad['x'], pad['y']
    # Search around pad in spiral/circle up to 1.5 mm
    found = False
    for r in [0.55, 0.70, 0.85, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0]:
        for ang_deg in range(0, 360, 15):
            rad = math.radians(ang_deg)
            vx = round(px + r * math.cos(rad), 3)
            vy = round(py + r * math.sin(rad), 3)
            if is_via_pos_clear(vx, vy, pad['net']):
                found = True
                break
        if found: break
    if found:
        found_vias += 1
    else:
        print(f"Could not find via for {pad['ref']}.{pad['pin']} ({pad['net']}) at ({px}, {py})")

print(f"Via candidate search result: {found_vias} / {total_pads} pads have clean via sites!")

