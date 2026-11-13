"""Placement solver to find 100% collision-free coordinates for all 60 components."""
import json

coords = {
    'J_IMU': (3.2, 4.6),
    'C15': (6.2, 2.0),
    'R10': (6.2, 4.6),
    'R11': (6.2, 7.2),
    'J_TOUCH': (9.0, 2.4),
    'SW4': (11.5, 7.0),
    'R19': (13.5, 2.4),
    'R12': (14.5, 7.0),
    'SW5': (17.5, 7.0),
    'D1': (16.5, 2.2),
    'D2': (16.5, 4.4),
    'R13': (20.5, 7.0),
    'R14': (19.0, 2.2),
    'R15': (19.0, 4.4),
    'U3': (23.5, 4.6),
    'C13': (23.5, 8.0),
    'R16': (27.0, 2.2),
    'R17': (27.0, 4.6),
    'Q1': (28.5, 2.2),
    'D3': (29.0, 5.0),
    'J_MOT': (31.0, 7.0),
    'SW1': (33.0, 1.8),
    'R4': (35.0, 2.0),
    'C4': (36.5, 2.0),
    'R1': (38.0, 2.0),
    'C1': (39.5, 2.0),
    'C6': (33.0, 7.5),
    'Y1': (35.0, 7.5),
    'C7': (37.0, 7.5),
    'L1': (38.5, 7.5),
    'U1': (42.5, 4.6),
    'SW2': (46.5, 1.8),
    'R3': (48.0, 2.0),
    'C5': (49.5, 2.0),
    'R2': (51.0, 2.0),
    'FB1': (46.5, 7.5),
    'C2': (48.0, 7.5),
    'C3': (49.5, 7.5),
    'L2': (52.0, 5.0),
    'C8': (52.0, 3.6),
    'C9': (53.5, 3.6),
    'J_RF': (54.5, 5.0),
    'J_SD': (57.5, 4.6),
    'R18': (60.5, 2.0),
    'J_UART': (60.5, 7.0),
    'J_BAT': (63.5, 2.8),
    'SW3': (63.5, 7.2),
    'C11': (66.5, 5.5),
    'U2': (67.5, 3.2),
    'C12': (69.0, 5.5),
    'R9': (69.5, 2.0),
    'J_PWR': (72.0, 4.6),
    'C14': (74.0, 4.6),
    'U_ESD': (76.0, 4.6),
    'R5': (77.5, 2.0),
    'R6': (77.5, 3.4),
    'R7': (77.5, 5.8),
    'R8': (77.5, 7.2),
    'C10': (79.0, 2.0),
    'J_USB': (81.5, 4.6)
}

with open('output/RevF_Working/SmartPen_RevE_PCB.json', 'r', encoding='utf-8') as f:
    pcb = json.load(f)

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
                    continue
                x2 = c2_x + p2['dx']
                y2 = c2_y + p2['dy']
                w2, h2 = p2['w'], p2['h']

                dx = abs(x1 - x2) - (w1 + w2) / 2.0
                dy = abs(y1 - y2) - (h1 + h2) / 2.0
                if dx < 0.15 and dy < 0.15:
                    collisions.append((ref1, p1['num'], ref2, p2['num'], dx, dy))

print(f"Total pad collisions (< 0.15 mm): {len(collisions)}")
for c in collisions:
    print(f"  Collision: {c[0]}.{c[1]} vs {c[2]}.{c[3]}: dx={c[4]:.3f} mm, dy={c[5]:.3f} mm")

