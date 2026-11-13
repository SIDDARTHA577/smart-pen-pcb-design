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

# MicroSD:
add_seg(41.13, 2.435, 41.13, 0.55, "F.Cu", "SD_MOSI")
add_via(41.13, 0.55, "SD_MOSI")
add_seg(41.13, 0.55, 58.65, 0.55, "B.Cu", "SD_MOSI")
add_via(58.65, 0.55, "SD_MOSI")
add_seg(58.65, 0.55, 58.65, 4.20, "F.Cu", "SD_MOSI")

add_seg(41.63, 2.435, 41.63, 1.15, "F.Cu", "SD_MISO")
add_via(41.63, 1.15, "SD_MISO")
add_seg(41.63, 1.15, 59.15, 1.15, "B.Cu", "SD_MISO")
add_via(59.15, 1.15, "SD_MISO")
add_seg(59.15, 1.15, 59.15, 4.20, "F.Cu", "SD_MISO")

add_seg(42.63, 2.435, 42.63, 1.75, "F.Cu", "SD_SCK")
add_via(42.63, 1.75, "SD_SCK")
add_seg(42.63, 1.75, 58.15, 1.75, "B.Cu", "SD_SCK")
add_via(58.15, 1.75, "SD_SCK")
add_seg(58.15, 1.75, 58.15, 4.20, "F.Cu", "SD_SCK")

add_seg(43.13, 2.435, 43.13, 0.85, "F.Cu", "SD_CS")
add_via(43.13, 0.85, "SD_CS")
add_seg(43.13, 0.85, 59.65, 0.85, "B.Cu", "SD_CS")
add_via(59.65, 0.85, "SD_CS")
add_seg(59.65, 0.85, 59.65, 4.20, "F.Cu", "SD_CS")
add_seg(55.475, 2.35, 55.475, 0.85, "F.Cu", "SD_CS")
add_via(55.475, 0.85, "SD_CS")

# Battery & Power Switch:
# SW3.1 (VBAT at 60.963, 6.824) to (60.963, 5.00)
add_seg(60.963, 6.824, 60.963, 5.00, "F.Cu", "VBAT")
add_via(60.963, 5.00, "VBAT")
add_seg(60.963, 5.00, 62.399, 5.00, "B.Cu", "VBAT")
add_via(62.399, 5.00, "VBAT")
add_seg(62.399, 5.00, 62.399, 1.722, "F.Cu", "VBAT")

# J_BAT.1 (VBAT at 62.399, 1.722) to (62.399, 1.00)
add_seg(62.399, 1.722, 62.399, 1.00, "F.Cu", "VBAT")
add_via(62.399, 1.00, "VBAT")

# U2.3 (VBAT at 67.949, 2.773) to C12.1 (68.287, 1.50) on F.Cu
add_seg(67.949, 2.773, 68.287, 2.773, "F.Cu", "VBAT")
add_seg(68.287, 2.773, 68.287, 1.50, "F.Cu", "VBAT")
add_seg(67.949, 2.773, 67.949, 1.00, "F.Cu", "VBAT")
add_via(67.949, 1.00, "VBAT")

# Connect VBAT highway on B.Cu at 1.00:
add_seg(62.399, 1.00, 67.949, 1.00, "B.Cu", "VBAT")

# SW3.2 (VBAT_SW at 62.963, 6.824) to (62.963, 4.40)
add_seg(62.963, 6.824, 62.963, 4.40, "F.Cu", "VBAT_SW")
add_via(62.963, 4.40, "VBAT_SW")
add_seg(28.09, 4.40, 62.963, 4.40, "B.Cu", "VBAT_SW")

# J_PWR.1 (VBAT_SW at 68.114, 3.963) to (68.114, 4.40)
add_seg(68.114, 3.963, 68.114, 4.40, "F.Cu", "VBAT_SW")
add_via(68.114, 4.40, "VBAT_SW")
add_seg(62.963, 4.40, 68.114, 4.40, "B.Cu", "VBAT_SW")

# Charger U2:
# Pin 1 (CHG_STAT at 66.049, 2.773)
add_seg(66.049, 2.773, 66.049, 3.95, "F.Cu", "CHG_STAT")
add_via(66.049, 3.95, "CHG_STAT")
add_seg(18.80, 3.95, 66.049, 3.95, "B.Cu", "CHG_STAT")

# Pin 5 (CHG_PROG at 66.049, 5.373) to R9.1 (65.725, 6.80) on F.Cu
add_seg(66.049, 5.373, 65.725, 5.373, "F.Cu", "CHG_PROG")
add_seg(65.725, 5.373, 65.725, 6.80, "F.Cu", "CHG_PROG")

# Pin 4 (USB_VBUS at 67.949, 5.373) -> via at (67.45, 4.85)
add_seg(67.949, 5.373, 67.45, 5.373, "F.Cu", "USB_VBUS")
add_seg(67.45, 5.373, 67.45, 4.85, "F.Cu", "USB_VBUS")
add_via(67.45, 4.85, "USB_VBUS")

# C11.1 (USB_VBUS at 67.475, 7.70) straight South to U2.4 on F.Cu
add_seg(67.475, 7.70, 67.475, 5.373, "F.Cu", "USB_VBUS")
add_seg(67.475, 5.373, 67.45, 5.373, "F.Cu", "USB_VBUS")

errs = check_pcb_geometry(pads, segments, list(vias))
print(f"Total errors: {len(errs)}")
for e in errs:
    print(" ", e)
