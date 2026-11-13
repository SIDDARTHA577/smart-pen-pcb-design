import json, math, sys
sys.path.insert(0, '.')
from scripts.verify_smartpen_geometry import check_pcb_geometry

with open('output/RevF_Working/solved_coords.json') as f:
    coords = json.load(f)
with open('output/RevF_Working/SmartPen_RevE_PCB.json') as f:
    pcb_json = json.load(f)

# Coordinates
coords['C1'] = [39.80, 1.52]
coords['R18'] = [55.00, 2.35]
coords['J_BAT'] = [62.90, 1.72]
coords['U2'] = [67.00, 4.07]
coords['R9'] = [66.20, 6.80]
coords['C11'] = [67.95, 7.70]
coords['C12'] = [69.04, 1.50]
coords['FB1'] = [46.23, 7.55]

# USB area:
coords['C14'] = [70.80, 2.00]
coords['U_ESD'] = [72.00, 5.00]
coords['R8'] = [77.50, 1.80] # DP resistor in Zone 3
coords['R7'] = [78.65, 1.00] # DM resistor in Zone 3
coords['R5'] = [77.60, 7.50] # CC1 resistor in Zone 2
coords['C10'] = [76.00, 1.80] # VBUS cap in Zone 3
coords['R6'] = [80.00, 1.80] # CC2 resistor in Zone 3

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

segments = []
vias = set()

def add_seg(x1, y1, x2, y2, layer, net_name, width=0.18):
    if abs(x1 - x2) > 0.0005 or abs(y1 - y2) > 0.0005:
        segments.append((round(x1, 3), round(y1, 3), round(x2, 3), round(y2, 3), layer, net_name, width))

def add_via(vx, vy, net_name):
    vias.add((round(vx, 3), round(vy, 3), net_name))

# Let's inspect pad positions of R8 and R7:
# R8 is at (77.50, 1.80): Pin 1 (PORT) at (77.025, 1.80), Pin 2 (CORE) at (77.975, 1.80)
# R7 is at (78.65, 1.00): Pin 1 (PORT) at (78.175, 1.00), Pin 2 (CORE) at (79.125, 1.00)
# J_USB.7 (DP_PORT) at (78.15, 3.10)
# J_USB.9 (DM_PORT) at (78.65, 3.10)

usb_pads = [p for p in pads if p['x'] >= 70]
# 1. USB_CC1: J_USB.5 to R5.1
add_seg(77.60, 3.10, 77.60, 7.50, "F.Cu", "USB_CC1")

# 2. USB_CC2: J_USB.6 to R6.1
add_seg(79.20, 3.10, 79.20, 1.80, "F.Cu", "USB_CC2")
add_seg(79.20, 1.80, 79.525, 1.80, "F.Cu", "USB_CC2")

# 3. USB_VBUS:
add_seg(76.00, 3.10, 76.00, 1.80, "F.Cu", "USB_VBUS")
add_seg(76.00, 1.80, 75.525, 1.80, "F.Cu", "USB_VBUS")
add_seg(76.00, 3.10, 76.00, 4.85, "F.Cu", "USB_VBUS")
add_via(76.00, 4.85, "USB_VBUS")

add_seg(80.80, 3.10, 80.80, 4.85, "F.Cu", "USB_VBUS")
add_via(80.80, 4.85, "USB_VBUS")

add_seg(72.00, 6.30, 72.00, 4.85, "F.Cu", "USB_VBUS")
add_via(72.00, 4.85, "USB_VBUS")

add_seg(67.45, 4.85, 80.80, 4.85, "B.Cu", "USB_VBUS")

# 4. USB_DP_PORT:
add_seg(78.15, 3.10, 78.15, 1.80, "F.Cu", "USB_DP_PORT")
add_seg(78.15, 1.80, 77.025, 1.80, "F.Cu", "USB_DP_PORT")
add_seg(77.025, 1.80, 77.025, 1.30, "F.Cu", "USB_DP_PORT")
add_via(77.025, 1.30, "USB_DP_PORT")

add_seg(71.05, 3.70, 71.05, 1.30, "F.Cu", "USB_DP_PORT")
add_via(71.05, 1.30, "USB_DP_PORT")
add_seg(71.05, 1.30, 77.025, 1.30, "B.Cu", "USB_DP_PORT")

# 5. USB_DM_PORT:
add_seg(78.65, 3.10, 78.65, 1.00, "F.Cu", "USB_DM_PORT")
add_seg(78.65, 1.00, 78.175, 1.00, "F.Cu", "USB_DM_PORT")
add_seg(78.175, 1.00, 78.175, 0.60, "F.Cu", "USB_DM_PORT")
add_via(78.175, 0.60, "USB_DM_PORT")

add_seg(72.00, 3.70, 72.00, 0.60, "F.Cu", "USB_DM_PORT")
add_via(72.00, 0.60, "USB_DM_PORT")
add_seg(72.00, 0.60, 78.175, 0.60, "B.Cu", "USB_DM_PORT")

# 6. USB_DP_CORE:
add_seg(71.05, 6.30, 71.05, 7.60, "F.Cu", "USB_DP_CORE")
add_via(71.05, 7.60, "USB_DP_CORE")
add_seg(77.975, 1.80, 77.975, 7.60, "F.Cu", "USB_DP_CORE")
add_via(77.975, 7.60, "USB_DP_CORE")
add_seg(54.50, 7.60, 77.975, 7.60, "B.Cu", "USB_DP_CORE")

# 7. USB_DM_CORE:
add_seg(72.95, 6.30, 72.95, 7.15, "F.Cu", "USB_DM_CORE")
add_via(72.95, 7.15, "USB_DM_CORE")
add_seg(79.125, 1.00, 79.125, 7.15, "F.Cu", "USB_DM_CORE")
add_via(79.125, 7.15, "USB_DM_CORE")
add_seg(53.50, 7.15, 79.125, 7.15, "B.Cu", "USB_DM_CORE")

errs = check_pcb_geometry(pads, segments, list(vias))
print(f"Errors after routing: {len(errs)}")
for e in errs:
    print(" ", e)
