import json, math, sys
sys.path.insert(0, '.')
from scripts.verify_smartpen_geometry import check_pcb_geometry

with open('output/RevF_Working/solved_coords.json') as f:
    coords = json.load(f)
coords['FB1'] = [46.23, 7.55]
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

# 6 pins on U1 North:
# Pin 30: XTAL_P_CORE at (42.13, 7.24) -> via at (42.13, 8.65) -> West to 39.12 at 8.65
add_seg(42.13, 7.24, 42.13, 8.65, "F.Cu", "XTAL_P_CORE")
add_via(42.13, 8.65, "XTAL_P_CORE")
add_seg(39.12, 8.65, 42.13, 8.65, "B.Cu", "XTAL_P_CORE")

# Pin 29: XTAL_N at (42.63, 7.24) -> via at (42.63, 8.05) -> West to 32.83 at 8.05
add_seg(42.63, 7.24, 42.63, 8.05, "F.Cu", "XTAL_N")
add_via(42.63, 8.05, "XTAL_N")
add_seg(32.83, 8.05, 42.63, 8.05, "B.Cu", "XTAL_N")

# Pin 28: UART_TX at (43.13, 7.24) -> via at (43.13, 8.65) -> East to 55.95 at 8.65
add_seg(43.13, 7.24, 43.13, 8.65, "F.Cu", "UART_TX")
add_via(43.13, 8.65, "UART_TX")
add_seg(43.13, 8.65, 55.95, 8.65, "B.Cu", "UART_TX")
add_via(55.95, 8.65, "UART_TX")
add_seg(55.95, 8.65, 55.95, 7.347, "F.Cu", "UART_TX")

# Pin 27: UART_RX at (43.63, 7.24) -> via at (43.63, 8.05) -> East to 57.22 at 8.05
add_seg(43.63, 7.24, 43.63, 8.05, "F.Cu", "UART_RX")
add_via(43.63, 8.05, "UART_RX")
add_seg(43.63, 8.05, 57.22, 8.05, "B.Cu", "UART_RX")
add_via(57.22, 8.05, "UART_RX")
add_seg(57.22, 8.05, 57.22, 7.347, "F.Cu", "UART_RX")

# Pin 26: USB_DP_CORE at (44.13, 7.24) -> goes to higher track Y = 8.65
add_seg(44.13, 7.24, 44.13, 8.65, "F.Cu", "USB_DP_CORE")
add_seg(44.13, 8.65, 54.50, 8.65, "F.Cu", "USB_DP_CORE")
add_seg(54.50, 8.65, 54.50, 7.60, "F.Cu", "USB_DP_CORE")
add_via(54.50, 7.60, "USB_DP_CORE")
add_seg(54.50, 7.60, 71.50, 7.60, "B.Cu", "USB_DP_CORE")

# Pin 25: USB_DM_CORE at (44.63, 7.24) -> goes to lower track Y = 8.35
add_seg(44.63, 7.24, 44.63, 8.35, "F.Cu", "USB_DM_CORE")
add_seg(44.63, 8.35, 53.50, 8.35, "F.Cu", "USB_DM_CORE")
add_seg(53.50, 8.35, 53.50, 7.15, "F.Cu", "USB_DM_CORE")
add_via(53.50, 7.15, "USB_DM_CORE")
add_seg(53.50, 7.15, 73.00, 7.15, "B.Cu", "USB_DM_CORE")

errs = check_pcb_geometry(pads, segments, list(vias))
print(f"Total errors: {len(errs)}")
for e in errs:
    print(" ", e)
