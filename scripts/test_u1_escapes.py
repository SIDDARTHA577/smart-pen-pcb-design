import json, math, sys
sys.path.insert(0, '.')

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

def is_via_legal(vx, vy, net_name):
    if vx - 0.25 < 0.35 or vx + 0.25 > 83.65: return False
    if vy - 0.25 < 0.35 or vy + 0.25 > 8.85: return False
    for pad in all_pads:
        if pad['net'] == net_name: continue
        px, py, pw, ph = pad['x'], pad['y'], pad['w'], pad['h']
        dx = max(0.0, abs(vx - px) - pw/2.0)
        dy = max(0.0, abs(vy - py) - ph/2.0)
        if math.hypot(dx, dy) < 0.25 + 0.13:
            return False
    return True

u1_pads = [p for p in all_pads if p['ref'] == 'U1' and p['net'] and p['net'] != 'GND']
print(f"U1 active signal pads: {len(u1_pads)}")

for p in sorted(u1_pads, key=lambda x: int(x['pin'])):
    px, py = p['x'], p['y']
    net = p['net']
    pin = int(p['pin'])
    # Determine escape direction
    found = None
    if 1 <= pin <= 8: # West
        for dx in range(8, 25): # 0.8 to 2.5 mm west
            for dy in range(-10, 11):
                vx = round(px - dx*0.1, 2)
                vy = round(py + dy*0.1, 2)
                if is_via_legal(vx, vy, net):
                    found = (vx, vy)
                    break
            if found: break
    elif 9 <= pin <= 16: # South
        for dy in range(8, 25): # 0.8 to 2.5 mm south
            for dx in range(-10, 11):
                vx = round(px + dx*0.1, 2)
                vy = round(py - dy*0.1, 2)
                if is_via_legal(vx, vy, net):
                    found = (vx, vy)
                    break
            if found: break
    elif 17 <= pin <= 24: # East
        for dx in range(8, 25): # 0.8 to 2.5 mm east
            for dy in range(-10, 11):
                vx = round(px + dx*0.1, 2)
                vy = round(py + dy*0.1, 2)
                if is_via_legal(vx, vy, net):
                    found = (vx, vy)
                    break
            if found: break
    else: # North (25 <= pin <= 32)
        for dy in range(8, 25): # 0.8 to 2.5 mm north
            for dx in range(-10, 11):
                vx = round(px + dx*0.1, 2)
                vy = round(py + dy*0.1, 2)
                if is_via_legal(vx, vy, net):
                    found = (vx, vy)
                    break
            if found: break
    print(f"Pin {pin:2d} ({net:16s}) at ({px:.2f}, {py:.2f}) -> via {found}")

