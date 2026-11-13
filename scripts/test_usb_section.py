import json, math, sys
sys.path.insert(0, '.')
from scripts.verify_smartpen_geometry import check_pcb_geometry

with open('output/RevF_Working/solved_coords.json') as f:
    coords = json.load(f)
with open('output/RevF_Working/SmartPen_RevE_PCB.json') as f:
    pcb_json = json.load(f)

# Coords fine-tuning:
coords['C1'] = [39.80, 1.52]
coords['R18'] = [55.00, 2.35]
coords['J_BAT'] = [62.90, 1.72]
coords['U2'] = [67.00, 4.07]
coords['R9'] = [66.20, 6.80]
coords['C11'] = [67.95, 7.70]
coords['C12'] = [69.04, 1.50]

# USB components:
# J_PWR is at [69.064, 5.263]
# J_USB is at [78.40, 4.60]
# Available space in X: between 70.5 and 76.0
coords['C14'] = [70.50, 1.80]
coords['U_ESD'] = [72.20, 4.50]
coords['R8'] = [72.20, 7.80] # DP resistor (North)
coords['R7'] = [73.80, 7.80] # DM resistor (North)
coords['R5'] = [70.50, 7.80] # CC1 pull-down (North)
coords['C10'] = [74.50, 1.50] # VBUS cap (South)
coords['R6'] = [79.20, 1.50] # CC2 pull-down (South)

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

# Highway assignments for USB:
hw = {
    'USB_DP_CORE': 8.05,
    'USB_DM_CORE': 8.65,
    'USB_CC1':     8.45,
    'USB_DP_PORT': 1.60,
    'USB_DM_PORT': 1.00,
    'USB_VBUS':    4.85,
}

# R8 is DP resistor: center at [71.50, 7.80]. Pin 1 (PORT) at 71.025, Pin 2 (CORE) at 71.975.
# R7 is DM resistor: center at [73.50, 7.80]. Pin 1 (PORT) at 73.025, Pin 2 (CORE) at 73.975.
coords['R8'] = [71.50, 7.80]
coords['R7'] = [73.50, 7.80]
# R6: center at [79.675, 1.50], Pin 1 at 79.20!
coords['R6'] = [79.675, 1.50]
# C10: center at [74.50, 1.50]
coords['C10'] = [74.50, 1.50]

# 1. USB_DP_CORE:
# U1.26 (44.13, 7.24) -> via at (44.13, 8.05)
add_seg(44.13, 7.24, 44.13, hw['USB_DP_CORE'], "F.Cu", "USB_DP_CORE")
add_via(44.13, hw['USB_DP_CORE'], "USB_DP_CORE")
add_seg(44.13, hw['USB_DP_CORE'], 71.975, hw['USB_DP_CORE'], "B.Cu", "USB_DP_CORE")
# Via at (71.975, 8.05) connects to R8.2 (71.975, 7.80) and U_ESD.6 (71.25, 5.80)
add_via(71.975, hw['USB_DP_CORE'], "USB_DP_CORE")
add_seg(71.975, hw['USB_DP_CORE'], 71.975, 7.80, "F.Cu", "USB_DP_CORE")
add_seg(71.975, 7.80, 71.25, 7.80, "F.Cu", "USB_DP_CORE")
add_seg(71.25, 7.80, 71.25, 5.80, "F.Cu", "USB_DP_CORE")

# 2. USB_DM_CORE:
# U1.25 (44.63, 7.24) -> via at (44.63, 8.65)
# Wait, UART_TX is at 8.65 up to 55.95, so east of 55.95 Y=8.65 is empty!
# But between 44.63 and 55.95, UART_TX uses 8.65.
# So at U1, USB_DM_CORE can use Y = 7.60 or 7.15 or 8.35:
# Pin 25 escapes North to 8.05? But USB_DP_CORE is at 8.05.
# Let's check Y for USB_DM_CORE at U1:
# U1.25 is at (44.63, 7.24). Via at (45.30, 8.65) or (45.00, 7.60)?
# East of U1: at (45.50, 7.24), open!
add_seg(44.63, 7.24, 45.40, 7.24, "F.Cu", "USB_DM_CORE")
add_seg(45.40, 7.24, 45.40, 7.45, "F.Cu", "USB_DM_CORE")
add_via(45.40, 7.45, "USB_DM_CORE")
add_seg(45.40, 7.45, 73.975, 7.45, "B.Cu", "USB_DM_CORE")
add_via(73.975, 7.45, "USB_DM_CORE")
add_seg(73.975, 7.45, 73.975, 7.80, "F.Cu", "USB_DM_CORE")
add_seg(73.975, 7.80, 73.15, 7.80, "F.Cu", "USB_DM_CORE")
add_seg(73.15, 7.80, 73.15, 5.80, "F.Cu", "USB_DM_CORE")

# 3. USB_DP_PORT:
# R8.1 (71.025, 7.80) to U_ESD.1 (71.25, 3.20) and J_USB.7 (78.15, 3.10)
# Route around West of U_ESD on F.Cu:
add_seg(71.025, 7.80, 70.30, 7.80, "F.Cu", "USB_DP_PORT")
add_seg(70.30, 7.80, 70.30, 3.20, "F.Cu", "USB_DP_PORT")
add_seg(70.30, 3.20, 71.25, 3.20, "F.Cu", "USB_DP_PORT")
# Via at (70.30, 1.60) to B.Cu highway at 1.60
add_seg(70.30, 3.20, 70.30, hw['USB_DP_PORT'], "F.Cu", "USB_DP_PORT")
add_via(70.30, hw['USB_DP_PORT'], "USB_DP_PORT")
# J_USB.7 (78.15, 3.10) to via at (78.15, 1.60)
add_seg(78.15, 3.10, 78.15, hw['USB_DP_PORT'], "F.Cu", "USB_DP_PORT")
add_via(78.15, hw['USB_DP_PORT'], "USB_DP_PORT")
add_seg(70.30, hw['USB_DP_PORT'], 78.15, hw['USB_DP_PORT'], "B.Cu", "USB_DP_PORT")

# 4. USB_DM_PORT:
# R7.1 (73.025, 7.80) to U_ESD.2 (72.20, 3.20) and J_USB.9 (78.65, 3.10)
# Between U_ESD.1 and U_ESD.2 or under U_ESD:
# Pin 2 is at (72.20, 3.20).
# From Pin 2, go South to via at (72.20, 1.00)
add_seg(72.20, 3.20, 72.20, hw['USB_DM_PORT'], "F.Cu", "USB_DM_PORT")
add_via(72.20, hw['USB_DM_PORT'], "USB_DM_PORT")
# J_USB.9 (78.65, 3.10) to via at (78.65, 1.00)
add_seg(78.65, 3.10, 78.65, hw['USB_DM_PORT'], "F.Cu", "USB_DM_PORT")
add_via(78.65, hw['USB_DM_PORT'], "USB_DM_PORT")
add_seg(72.20, hw['USB_DM_PORT'], 78.65, hw['USB_DM_PORT'], "B.Cu", "USB_DM_PORT")
# Connect R7.1 (73.025, 7.80) to U_ESD.2:
# Route between R7 and R8 on F.Cu:
add_seg(73.025, 7.80, 72.60, 7.80, "F.Cu", "USB_DM_PORT")
add_seg(72.60, 7.80, 72.60, 6.20, "F.Cu", "USB_DM_PORT")
add_seg(72.60, 6.20, 72.20, 6.20, "F.Cu", "USB_DM_PORT")
add_seg(72.20, 6.20, 72.20, 3.20, "F.Cu", "USB_DM_PORT")

# 5. USB_CC1:
# R5.1 (70.025, 7.80) to J_USB.5 (77.60, 3.10)
add_seg(70.025, 7.80, 70.025, hw['USB_CC1'], "F.Cu", "USB_CC1")
add_via(70.025, hw['USB_CC1'], "USB_CC1")
add_seg(77.60, 3.10, 77.60, hw['USB_CC1'], "F.Cu", "USB_CC1")
add_via(77.60, hw['USB_CC1'], "USB_CC1")
add_seg(70.025, hw['USB_CC1'], 77.60, hw['USB_CC1'], "B.Cu", "USB_CC1")

# 6. USB_CC2:
# J_USB.6 (79.20, 3.10) straight down on F.Cu to R6.1 (79.20, 1.50)
add_seg(79.20, 3.10, 79.20, 1.50, "F.Cu", "USB_CC2")

# 7. USB_VBUS:
# From Charger U2 via (67.45, 4.85) to U_ESD.5 (72.20, 5.80), C10.1 (74.025, 1.50), J_USB.2 (76.00, 3.10), J_USB.10 (80.80, 3.10)
add_seg(67.45, hw['USB_VBUS'], 72.20, hw['USB_VBUS'], "B.Cu", "USB_VBUS")
add_seg(72.20, 5.80, 72.20, hw['USB_VBUS'], "F.Cu", "USB_VBUS")
add_via(72.20, hw['USB_VBUS'], "USB_VBUS")

add_seg(72.20, hw['USB_VBUS'], 76.00, hw['USB_VBUS'], "B.Cu", "USB_VBUS")
add_seg(76.00, 3.10, 76.00, hw['USB_VBUS'], "F.Cu", "USB_VBUS")
add_via(76.00, hw['USB_VBUS'], "USB_VBUS")

add_seg(76.00, hw['USB_VBUS'], 80.80, hw['USB_VBUS'], "B.Cu", "USB_VBUS")
add_seg(80.80, 3.10, 80.80, hw['USB_VBUS'], "F.Cu", "USB_VBUS")
add_via(80.80, hw['USB_VBUS'], "USB_VBUS")

# C10.1 connects to J_USB.2:
# C10 is at (74.50, 1.50), Pin 1 is at 74.025.
# Route North to 2.20, then East to 76.00, then North to J_USB.2 (76.00, 3.10)
add_seg(74.025, 1.50, 74.025, 2.20, "F.Cu", "USB_VBUS")
add_seg(74.025, 2.20, 76.00, 2.20, "F.Cu", "USB_VBUS")
add_seg(76.00, 2.20, 76.00, 3.10, "F.Cu", "USB_VBUS")

errs = check_pcb_geometry(pads, segments, list(vias))
print(f"Total USB section errors: {len(errs)}")
for e in errs:
    print(" ", e)
