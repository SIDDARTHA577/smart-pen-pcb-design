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
coords['C12'] = [68.15, 1.40] # Moved West by 0.15mm to clear C14
coords['C10'] = [74.50, 1.50]
coords['R8'] = [71.60, 7.50]
coords['R7'] = [73.00, 7.50]
coords['R5'] = [77.60, 6.70]
coords['R6'] = [79.20, 6.70]
coords['U_ESD'] = [72.00, 4.49]
coords['C14'] = [70.014, 2.00] # Vertical C14 directly below J_PWR.3

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

# Vertical components: R9, R5, R6, C14
for ref in ['R9', 'R5', 'R6', 'C14']:
    for p in fp_defs[ref]:
        p['dx'], p['dy'] = p['dy'], p['dx']
        p['w'], p['h'] = p['h'], p['w']

# For C14: Pin 1 (3V3) in North (dy = +0.75), Pin 2 (GND) in South (dy = -0.75)
for p in fp_defs['C14']:
    p['dy'] = 0.75 if p['num'] == '1' else -0.75

# R7 and R8: vertical, Pin 1 (PORT) in North (dy = +0.475), Pin 2 (CORE) in South (dy = -0.475)
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

# 1. USB_CC1: J_USB.5 (77.60, 3.10) to R5.1 (77.60, 6.225)
add_seg(77.60, 3.10, 77.60, 6.225, "F.Cu", "USB_CC1")

# 2. USB_CC2: J_USB.6 (79.20, 3.10) to R6.1 (79.20, 6.225)
add_seg(79.20, 3.10, 79.20, 6.225, "F.Cu", "USB_CC2")

# 3. USB_VBUS: B.Cu highway at Y = 4.85
add_seg(67.45, 4.85, 80.80, 4.85, "B.Cu", "USB_VBUS")
add_seg(80.80, 3.10, 80.80, 4.85, "F.Cu", "USB_VBUS")
add_via(80.80, 4.85, "USB_VBUS")
add_seg(76.00, 3.10, 76.00, 4.85, "F.Cu", "USB_VBUS")
add_via(76.00, 4.85, "USB_VBUS")
add_seg(72.00, 4.85, 72.00, 5.79, "F.Cu", "USB_VBUS")
add_via(72.00, 4.85, "USB_VBUS")
# C10.1 (73.75, 1.50)
add_seg(73.75, 1.50, 73.75, 0.70, "F.Cu", "USB_VBUS")
add_seg(73.75, 0.70, 76.00, 0.70, "F.Cu", "USB_VBUS")
add_seg(76.00, 0.70, 76.00, 3.10, "F.Cu", "USB_VBUS")

# 4. USB_DP_CORE:
# B.Cu highway at Y = 7.60
add_seg(54.50, 7.60, 70.80, 7.60, "B.Cu", "USB_DP_CORE")
add_via(70.80, 7.60, "USB_DP_CORE")
add_seg(70.80, 7.60, 71.05, 7.60, "F.Cu", "USB_DP_CORE")
add_seg(71.05, 7.60, 71.05, 5.79, "F.Cu", "USB_DP_CORE") # U_ESD.6
add_seg(71.05, 7.025, 71.60, 7.025, "F.Cu", "USB_DP_CORE") # to R8.2

# 5. USB_DM_CORE:
# B.Cu highway at Y = 7.15
add_seg(53.50, 7.15, 72.95, 7.15, "B.Cu", "USB_DM_CORE")
add_via(72.95, 7.15, "USB_DM_CORE")
add_seg(72.95, 7.15, 72.95, 5.79, "F.Cu", "USB_DM_CORE") # U_ESD.4
add_seg(72.95, 7.025, 73.00, 7.025, "F.Cu", "USB_DM_CORE") # to R7.2

# 6. USB_DP_PORT:
# Branch A: J_USB.7 (78.15, 3.10) to U_ESD.1 (71.05, 3.19) via B.Cu highway at Y = 1.20
add_seg(78.15, 3.10, 78.15, 1.20, "F.Cu", "USB_DP_PORT")
add_via(78.15, 1.20, "USB_DP_PORT")
add_seg(71.05, 1.20, 78.15, 1.20, "B.Cu", "USB_DP_PORT")
add_via(71.05, 1.20, "USB_DP_PORT")
add_seg(71.05, 1.20, 71.05, 3.19, "F.Cu", "USB_DP_PORT")
# Branch B (North): J_USB.7 (78.15, 3.10) to R8.1 (71.60, 7.975) via B.Cu highway at Y = 8.65
add_seg(78.15, 3.10, 78.15, 8.65, "F.Cu", "USB_DP_PORT")
add_via(78.15, 8.65, "USB_DP_PORT")
add_seg(71.60, 8.65, 78.15, 8.65, "B.Cu", "USB_DP_PORT")
add_via(71.60, 8.65, "USB_DP_PORT")
add_seg(71.60, 8.65, 71.60, 7.975, "F.Cu", "USB_DP_PORT")

# 7. USB_DM_PORT:
# Branch A: J_USB.9 (78.65, 3.10) to U_ESD.2 (72.00, 3.19) via B.Cu highway at Y = 0.55
add_seg(78.65, 3.10, 78.65, 0.55, "F.Cu", "USB_DM_PORT")
add_via(78.65, 0.55, "USB_DM_PORT")
add_seg(72.00, 0.55, 78.65, 0.55, "B.Cu", "USB_DM_PORT")
add_via(72.00, 0.55, "USB_DM_PORT")
add_seg(72.00, 0.55, 72.00, 3.19, "F.Cu", "USB_DM_PORT")
# Branch B (North): J_USB.9 (78.65, 3.10) to R7.1 (73.00, 7.975) via B.Cu highway at Y = 8.05
add_seg(78.65, 3.10, 78.65, 8.05, "F.Cu", "USB_DM_PORT")
add_via(78.65, 8.05, "USB_DM_PORT")
add_seg(73.00, 8.05, 78.65, 8.05, "B.Cu", "USB_DM_PORT")
add_via(73.00, 8.05, "USB_DM_PORT")
add_seg(73.00, 8.05, 73.00, 7.975, "F.Cu", "USB_DM_PORT")

# 8. C14 (3V3 Decoupling):
# C14.1 is at (70.014, 2.75). J_PWR.3 is at (70.014, 3.963).
add_seg(70.014, 3.963, 70.014, 2.75, "F.Cu", "3V3")

errs = check_pcb_geometry(pads, segments, list(vias))
print(f"Total Subsystem 9 errors: {len(errs)}")
for e in errs:
    print(" ", e)
