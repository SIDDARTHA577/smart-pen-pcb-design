import json, sys
sys.path.insert(0, '.')
from scripts.verify_smartpen_geometry import check_pcb_geometry

with open('output/RevF_Working/solved_coords.json') as f:
    coords = json.load(f)

# Coordinates
coords['C1'] = [39.80, 1.52]
coords['R18'] = [55.00, 2.35]
coords['FB1'] = [46.23, 7.55]
coords['J_BAT'] = [62.80, 1.72]
coords['U2'] = [67.00, 4.07]
coords['R9'] = [66.30, 6.70]
coords['C11'] = [68.00, 7.75]
coords['C12'] = [68.30, 1.40]
coords['C14'] = [71.05, 1.40]
coords['R5'] = [70.20, 7.70]

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

# Make R9 vertical: swap dx and dy, swap w and h
for p in fp_defs['R9']:
    p['dx'], p['dy'] = p['dy'], p['dx']
    p['w'], p['h'] = p['h'], p['w']

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

# Subsystem 8 Battery & Charger routing:
# 1. VBAT:
# SW3.1 (60.963, 6.824) -> via at (60.963, 5.00)
add_seg(60.963, 6.824, 60.963, 5.00, "F.Cu", "VBAT")
add_via(60.963, 5.00, "VBAT")

# J_BAT.1 is at (62.300, 1.720) [J_BAT at 62.80]
add_via(62.300, 5.00, "VBAT")
add_seg(60.963, 5.00, 62.300, 5.00, "B.Cu", "VBAT")
add_seg(62.300, 5.00, 62.300, 1.720, "F.Cu", "VBAT")

# From J_BAT.1 down to Y = 1.00 on F.Cu
add_seg(62.300, 1.720, 62.300, 1.00, "F.Cu", "VBAT")
add_via(62.300, 1.00, "VBAT")

# C12.1 is at (67.550, 1.400) [C12 at 68.30]
# Via at (67.550, 1.00)
add_via(67.550, 1.00, "VBAT")
add_seg(62.300, 1.00, 67.550, 1.00, "B.Cu", "VBAT")
add_seg(67.550, 1.00, 67.550, 1.400, "F.Cu", "VBAT")

# From C12.1 to U2.3 (67.950, 2.773) on F.Cu:
add_seg(67.550, 1.400, 67.950, 1.400, "F.Cu", "VBAT")
add_seg(67.950, 1.400, 67.950, 2.773, "F.Cu", "VBAT")

# 2. VBAT_SW:
add_seg(28.09, 4.40, 62.963, 4.40, "B.Cu", "VBAT_SW")
add_seg(62.963, 4.40, 68.114, 4.40, "B.Cu", "VBAT_SW")
add_seg(62.963, 6.824, 62.963, 4.40, "F.Cu", "VBAT_SW")
add_via(62.963, 4.40, "VBAT_SW")
add_seg(68.114, 3.963, 68.114, 4.40, "F.Cu", "VBAT_SW")
add_via(68.114, 4.40, "VBAT_SW")

# 3. CHG_STAT:
add_seg(18.80, 3.95, 66.049, 3.95, "B.Cu", "CHG_STAT")
add_via(66.049, 3.95, "CHG_STAT")
add_seg(66.049, 3.95, 66.049, 2.773, "F.Cu", "CHG_STAT")

# 4. CHG_PROG:
# U2.5 at (66.049, 5.373) to R9.1 at (66.300, 6.225)
add_seg(66.049, 5.373, 66.300, 5.373, "F.Cu", "CHG_PROG")
add_seg(66.300, 5.373, 66.300, 6.225, "F.Cu", "CHG_PROG")

# 5. USB_VBUS:
# U2.4 at (67.950, 5.373) to C11.1 at (67.250, 7.750)
# Via at (67.450, 4.850)
add_seg(67.950, 5.373, 67.450, 5.373, "F.Cu", "USB_VBUS")
add_seg(67.450, 5.373, 67.450, 4.850, "F.Cu", "USB_VBUS")
add_via(67.450, 4.850, "USB_VBUS")
add_seg(67.450, 5.373, 67.450, 7.750, "F.Cu", "USB_VBUS")
add_seg(67.450, 7.750, 67.250, 7.750, "F.Cu", "USB_VBUS")

errs = check_pcb_geometry(pads, segments, list(vias))
print(f"Subsystem 8 total errors: {len(errs)}")
for e in errs:
    print(" ", e)
