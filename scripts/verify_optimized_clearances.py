"""Verify pad clearances for the optimized 60-component placement."""
import json

coords = {
    'J_IMU': (3.2, 4.6),
    'C15': (6.8, 2.0),
    'R10': (6.8, 4.6),
    'R11': (6.8, 7.2),
    'J_TOUCH': (10.0, 2.4),
    'SW4': (10.2, 7.0),
    'R19': (12.8, 2.4),
    'R12': (13.5, 7.0),
    'SW5': (16.5, 7.0),
    'D1': (16.0, 2.2),
    'D2': (16.0, 4.4),
    'R13': (19.2, 7.0),
    'R14': (18.5, 2.2),
    'R15': (18.5, 4.4),
    'U3': (22.0, 4.6),
    'C13': (22.0, 8.0),
    'R16': (25.0, 2.2),
    'R17': (25.0, 4.6),
    'Q1': (27.5, 2.4),
    'D3': (29.5, 2.4),
    'J_MOT': (28.5, 7.0),
    'C6': (31.5, 7.5),
    'R4': (31.5, 2.0),
    'Y1': (33.5, 7.5),
    'L1': (35.5, 8.2),
    'C4': (33.5, 2.0),
    'C7': (35.5, 6.8),
    'R1': (35.5, 2.0),
    'C1': (37.2, 2.0),
    'U1': (39.5, 4.6),
    'FB1': (39.5, 8.2),
    'SW1': (38.8, 1.8),
    'R3': (41.0, 2.0),
    'C2': (41.5, 8.2),
    'C3': (43.0, 7.5),
    'C5': (42.8, 2.0),
    'L2': (44.5, 5.0),
    'C8': (44.5, 3.8),
    'R2': (44.5, 2.0),
    'C9': (46.0, 3.8),
    'SW2': (46.2, 1.8),
    'J_RF': (47.5, 5.0),
    'J_SD': (51.5, 4.6),
    'R18': (54.5, 2.0),
    'J_UART': (55.5, 7.0),
    'J_BAT': (59.5, 2.8),
    'SW3': (59.5, 7.2),
    'C11': (63.5, 5.5),
    'U2': (65.0, 3.2),
    'C12': (66.5, 5.5),
    'R9': (68.0, 2.0),
    'J_PWR': (70.0, 4.6),
    'C14': (72.5, 4.6),
    'U_ESD': (74.5, 4.6),
    'R5': (76.5, 2.0),
    'R6': (76.5, 3.4),
    'R7': (76.5, 5.8),
    'R8': (76.5, 7.2),
    'C10': (78.5, 1.8),
    'J_USB': (81.5, 4.6)
}

with open('output/RevF_Working/SmartPen_RevE_PCB.json', 'r', encoding='utf-8') as f:
    pcb = json.load(f)

# Extract pads relative to component centers
fp_pads = {}
for item in pcb['shape']:
    if isinstance(item, str) and item.startswith('LIB~'):
        subs = item.split('#@$')
        ref = ''
        for sub in subs:
            if sub.startswith('TEXT~P~'):
                ref = sub.split('~')[10]
        lib_toks = subs[0].split('~')
        orig_x = float(lib_toks[1])
        orig_y = float(lib_toks[2])

        pads = []
        for sub in subs:
            if sub.startswith('PAD~'):
                ptoks = sub.split('~')
                dx = (float(ptoks[2]) - orig_x) * 0.254
                dy = (float(ptoks[3]) - orig_y) * 0.254
                pw = float(ptoks[4]) * 0.254
                ph = float(ptoks[5]) * 0.254
                net = ptoks[7]
                num = ptoks[8]
                pads.append({'num': num, 'net': net, 'dx': dx, 'dy': dy, 'w': pw, 'h': ph})
        fp_pads[ref] = pads

# Test collisions with new coords
collisions = []
for ref1, p1_list in fp_pads.items():
    c1_x, c1_y = coords[ref1]
    for ref2, p2_list in fp_pads.items():
        if ref1 >= ref2:
            continue
        c2_x, c2_y = coords[ref2]
        for p1 in p1_list:
            x1 = c1_x + p1['dx']
            y1 = c1_y + p1['dy']
            w1, h1 = p1['w'], p1['h']
            for p2 in p2_list:
                if p1['net'] == p2['net'] and p1['net']:
                    continue # same net
                x2 = c2_x + p2['dx']
                y2 = c2_y + p2['dy']
                w2, h2 = p2['w'], p2['h']

                dx = abs(x1 - x2) - (w1 + w2) / 2.0
                dy = abs(y1 - y2) - (h1 + h2) / 2.0
                if dx < 0.20 and dy < 0.20:
                    collisions.append((ref1, p1['num'], ref2, p2['num'], dx, dy))

print(f"Total collisions (< 0.20 mm): {len(collisions)}")
for c in collisions[:20]:
    print(f"  Collision: {c[0]}.{c[1]} vs {c[2]}.{c[3]}: dx={c[4]:.3f} mm, dy={c[5]:.3f} mm")

