import json, sys
sys.path.insert(0, '.')
from scripts.verify_smartpen_geometry import check_pcb_geometry

with open('output/RevF_Working/solved_coords.json') as f:
    coords = json.load(f)

# Subsystems 1-8 coordinates
coords['C1'] = [39.80, 1.52]
coords['R18'] = [55.00, 2.35]
coords['FB1'] = [46.23, 7.55]
coords['J_BAT'] = [62.80, 1.72]
coords['U2'] = [67.00, 4.07]
coords['R9'] = [66.50, 6.60]
coords['C11'] = [67.95, 7.70]
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

# Subsystem 7 MicroSD traces:
add_seg(43.13, 1.45, 43.13, 0.85, "F.Cu", "SD_CS")
add_seg(43.13, 0.85, 59.65, 0.85, "B.Cu", "SD_CS")
add_seg(59.65, 0.85, 59.65, 3.40, "F.Cu", "SD_CS")

add_seg(41.13, 1.45, 41.13, 0.55, "F.Cu", "SD_MOSI")
add_seg(41.13, 0.55, 58.65, 0.55, "B.Cu", "SD_MOSI")
add_seg(58.65, 0.55, 58.65, 3.40, "F.Cu", "SD_MOSI")

add_seg(41.63, 1.45, 41.63, 1.15, "F.Cu", "SD_MISO")
add_seg(41.63, 1.15, 59.15, 1.15, "B.Cu", "SD_MISO")
add_seg(59.15, 1.15, 59.15, 3.40, "F.Cu", "SD_MISO")

add_seg(42.63, 1.45, 42.63, 1.75, "F.Cu", "SD_SCK")
add_seg(42.63, 1.75, 58.15, 1.75, "B.Cu", "SD_SCK")
add_seg(58.15, 1.75, 58.15, 3.40, "F.Cu", "SD_SCK")

# UART:
add_seg(43.13, 7.24, 43.13, 8.65, "F.Cu", "UART_TX")
add_via(43.13, 8.65, "UART_TX")
add_seg(43.13, 8.65, 55.95, 8.65, "B.Cu", "UART_TX")
add_via(55.95, 8.65, "UART_TX")
add_seg(55.95, 8.65, 55.95, 7.35, "F.Cu", "UART_TX")

add_seg(43.63, 7.24, 43.63, 8.05, "F.Cu", "UART_RX")
add_via(43.63, 8.05, "UART_RX")
add_seg(43.63, 8.05, 57.22, 8.05, "B.Cu", "UART_RX")
add_via(57.22, 8.05, "UART_RX")
add_seg(57.22, 8.05, 57.22, 7.35, "F.Cu", "UART_RX")

# Subsystem 8 Battery & Charger:
# VBAT:
# SW3.1 (60.963, 6.824) -> via at (60.963, 5.00)
add_seg(60.963, 6.824, 60.963, 5.00, "F.Cu", "VBAT")
add_via(60.963, 5.00, "VBAT")
# J_BAT.1 is at (62.300, 1.720) [since J_BAT is at 62.80]
add_via(62.300, 5.00, "VBAT")
add_seg(60.963, 5.00, 62.300, 5.00, "B.Cu", "VBAT")
add_seg(62.300, 5.00, 62.300, 1.720, "F.Cu", "VBAT")
# From J_BAT.1 down to Y = 1.00 on F.Cu
add_seg(62.300, 1.720, 62.300, 1.00, "F.Cu", "VBAT")
add_via(62.300, 1.00, "VBAT")
# C12.1 is at (67.550, 1.400) [since C12 is at 68.30]
add_via(67.550, 1.00, "VBAT")
add_seg(62.300, 1.00, 67.550, 1.00, "B.Cu", "VBAT")
add_seg(67.550, 1.00, 67.550, 1.400, "F.Cu", "VBAT")
# From C12.1 to U2.3 (67.950, 2.770) on F.Cu:
add_seg(67.550, 1.400, 67.950, 1.400, "F.Cu", "VBAT")
add_seg(67.950, 1.400, 67.950, 2.770, "F.Cu", "VBAT")

# VBAT_SW:
add_seg(28.09, 4.40, 62.963, 4.40, "B.Cu", "VBAT_SW")
add_seg(62.963, 4.40, 68.114, 4.40, "B.Cu", "VBAT_SW")
add_seg(62.963, 6.824, 62.963, 4.40, "F.Cu", "VBAT_SW")
add_via(62.963, 4.40, "VBAT_SW")
add_seg(68.114, 5.26, 68.114, 4.40, "F.Cu", "VBAT_SW")
add_via(68.114, 4.40, "VBAT_SW")

# CHG_STAT:
add_seg(18.80, 3.95, 66.049, 3.95, "B.Cu", "CHG_STAT")
add_via(18.80, 3.95, "CHG_STAT")
add_seg(18.80, 3.95, 18.80, 3.52, "F.Cu", "CHG_STAT")
add_seg(18.80, 3.52, 17.00, 3.52, "F.Cu", "CHG_STAT")
add_via(66.049, 3.95, "CHG_STAT")
add_seg(66.049, 3.95, 66.049, 2.77, "F.Cu", "CHG_STAT")

# CHG_PROG:
# U2.5 at (66.050, 5.370) to R9.1 at (66.025, 6.600)
add_seg(66.050, 5.370, 66.025, 6.600, "F.Cu", "CHG_PROG")

# USB_VBUS to U2.4 and C11.1:
# U2.4 at (67.950, 5.370) to C11.1 at (67.200, 7.700)
add_seg(67.950, 5.370, 67.200, 5.370, "F.Cu", "USB_VBUS")
add_seg(67.200, 5.370, 67.200, 7.700, "F.Cu", "USB_VBUS")
add_seg(67.200, 4.850, 67.200, 5.370, "F.Cu", "USB_VBUS")
add_via(67.200, 4.850, "USB_VBUS")

errs = check_pcb_geometry(pads, segments, list(vias))
print(f"Subsystems 7 & 8 geometry errors: {len(errs)}")
for e in errs:
    print(" ", e)

