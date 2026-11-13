import json, sys
sys.path.insert(0, '.')
from scripts.verify_smartpen_geometry import check_pcb_geometry

with open('output/RevF_Working/solved_coords.json') as f:
    coords = json.load(f)

# Validated coordinates
coords['C1'] = [39.80, 1.52]
coords['R18'] = [55.00, 2.35]
coords['FB1'] = [46.23, 7.55]
coords['J_BAT'] = [62.80, 1.72]
coords['U2'] = [67.00, 4.07]
coords['R9'] = [66.30, 6.70]
coords['C11'] = [68.00, 7.75]
coords['C12'] = [68.30, 1.40]
coords['C14'] = [71.05, 1.40]
coords['C10'] = [73.90, 1.50]
coords['R6'] = [74.04, 2.46]
coords['U_ESD'] = [71.80, 4.49]
coords['R7'] = [72.50, 6.85]
coords['R8'] = [72.48, 7.70]
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

# ----------------- SUBSYSTEM 9 ROUTING -----------------
# 1. USB_CC1: J_USB.5 (77.60, 3.10) to R5.1 (69.725, 7.70)
add_seg(77.60, 3.10, 77.60, 8.45, "F.Cu", "USB_CC1")
add_via(77.60, 8.45, "USB_CC1")
add_seg(69.725, 8.45, 77.60, 8.45, "B.Cu", "USB_CC1")
add_via(69.725, 8.45, "USB_CC1")
add_seg(69.725, 8.45, 69.725, 7.70, "F.Cu", "USB_CC1")

# 2. USB_CC2: J_USB.6 (79.20, 3.10) to R6.1 (73.565, 2.46)
add_seg(79.20, 3.10, 79.20, 2.10, "F.Cu", "USB_CC2")
add_via(79.20, 2.10, "USB_CC2")
add_seg(73.565, 2.10, 79.20, 2.10, "B.Cu", "USB_CC2")
add_via(73.565, 2.10, "USB_CC2")
add_seg(73.565, 2.10, 73.565, 2.46, "F.Cu", "USB_CC2")

# 3. USB_VBUS: B.Cu highway at Y = 4.85
add_seg(67.45, 4.85, 80.80, 4.85, "B.Cu", "USB_VBUS")
# J_USB.10 (80.80, 3.10)
add_seg(80.80, 3.10, 80.80, 4.85, "F.Cu", "USB_VBUS")
add_via(80.80, 4.85, "USB_VBUS")
# J_USB.2 (76.00, 3.10)
add_seg(76.00, 3.10, 76.00, 4.85, "F.Cu", "USB_VBUS")
add_via(76.00, 4.85, "USB_VBUS")
# U_ESD.5 (71.80, 5.79)
add_seg(71.80, 4.85, 71.80, 5.79, "F.Cu", "USB_VBUS")
add_via(71.80, 4.85, "USB_VBUS")
# C10.1 (73.15, 1.50)
add_seg(73.15, 1.50, 73.15, 4.85, "F.Cu", "USB_VBUS")
add_via(73.15, 4.85, "USB_VBUS")

# 4. USB_DP_PORT:
# J_USB.7 (78.15, 3.10) to U_ESD.1 (70.85, 3.19) via South highway Y = 1.15
add_seg(78.15, 1.15, 78.15, 3.10, "F.Cu", "USB_DP_PORT")
add_via(78.15, 1.15, "USB_DP_PORT")
add_seg(70.85, 1.15, 78.15, 1.15, "B.Cu", "USB_DP_PORT")
add_via(70.85, 1.15, "USB_DP_PORT")
add_seg(70.85, 1.15, 70.85, 3.19, "F.Cu", "USB_DP_PORT")
# J_USB.7 to R8.1 (72.005, 7.70) via North highway Y = 8.05
add_seg(78.15, 3.10, 78.15, 8.05, "F.Cu", "USB_DP_PORT")
add_via(78.15, 8.05, "USB_DP_PORT")
add_seg(72.005, 8.05, 78.15, 8.05, "B.Cu", "USB_DP_PORT")
add_via(72.005, 8.05, "USB_DP_PORT")
add_seg(72.005, 8.05, 72.005, 7.70, "F.Cu", "USB_DP_PORT")

# 5. USB_DM_PORT:
# J_USB.9 (78.65, 3.10) to U_ESD.2 (71.80, 3.19) via South highway Y = 0.55
add_seg(78.65, 0.55, 78.65, 3.10, "F.Cu", "USB_DM_PORT")
add_via(78.65, 0.55, "USB_DM_PORT")
add_seg(71.80, 0.55, 78.65, 0.55, "B.Cu", "USB_DM_PORT")
add_via(71.80, 0.55, "USB_DM_PORT")
add_seg(71.80, 0.55, 71.80, 3.19, "F.Cu", "USB_DM_PORT")
# J_USB.9 to R7.1 (72.025, 6.85) via North highway Y = 8.65
add_seg(78.65, 3.10, 78.65, 8.65, "F.Cu", "USB_DM_PORT")
add_via(78.65, 8.65, "USB_DM_PORT")
add_seg(72.025, 8.65, 78.65, 8.65, "B.Cu", "USB_DM_PORT")
add_via(72.025, 8.65, "USB_DM_PORT")
add_seg(72.025, 8.65, 72.025, 6.85, "F.Cu", "USB_DM_PORT")

# 6. USB_DP_CORE:
add_seg(54.50, 7.60, 72.955, 7.60, "B.Cu", "USB_DP_CORE")
add_via(72.955, 7.60, "USB_DP_CORE")
add_seg(72.955, 7.60, 72.955, 7.70, "F.Cu", "USB_DP_CORE")
add_via(70.85, 7.60, "USB_DP_CORE")
add_seg(70.85, 7.60, 70.85, 5.79, "F.Cu", "USB_DP_CORE")

# 7. USB_DM_CORE:
# R7.2 is at (72.975, 6.85), U_ESD.4 is at (72.75, 5.79)
add_seg(53.50, 7.15, 72.975, 7.15, "B.Cu", "USB_DM_CORE")
# Via to R7.2 and U_ESD.4
# Distance between (72.955, 7.60) and (72.975, 7.15) would be 0.45mm.
# So place DM_CORE via at X = 72.00, Y = 7.15? But R7.1 is at (72.025, 6.85).
# Where can DM_CORE via be? Let's check below.

errs = check_pcb_geometry(pads, segments, list(vias))
print(f"Subsystem 9 errors: {len(errs)}")
for e in errs:
    print(" ", e)
