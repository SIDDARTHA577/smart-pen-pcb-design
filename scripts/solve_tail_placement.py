import json
import math

with open('output/RevF_Working/SmartPen_RevE_PCB.json', 'r') as f:
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
        ox, oy = float(lib_toks[1]), float(lib_toks[2])
        pads = []
        for s in subs:
            if s.startswith('PAD~'):
                pt = s.split('~')
                dx = (float(pt[2]) - ox) * 0.254
                dy = (float(pt[3]) - oy) * 0.254
                w = float(pt[4]) * 0.254
                h = float(pt[5]) * 0.254
                pads.append({'dx': dx, 'dy': dy, 'w': w, 'h': h})
        fp_pads[ref] = pads

with open('output/RevF_Working/solved_coords.json') as f:
    coords = json.load(f)

coords['J_USB'] = [78.4, 4.6]

tail_refs = [
    'R18', 'J_UART', 'J_BAT', 'SW3', 'U2', 'R9', 'C11', 
    'C12', 'J_PWR', 'C14', 'U_ESD', 'R5', 'C10', 'R6', 'R7', 'R8'
]

# Set clean initial arrangement for tail refs
initial_tail = {
    'R18': [60.2, 1.8],
    'J_UART': [60.5, 7.2],
    'J_BAT': [63.2, 2.5],
    'SW3': [63.5, 7.2],
    'U2': [66.2, 3.0],
    'R9': [66.5, 6.0],
    'C11': [66.5, 7.8],
    'C12': [68.5, 2.0],
    'J_PWR': [68.8, 6.0],
    'C14': [70.5, 2.0],
    'U_ESD': [71.2, 5.0],
    'R5': [71.2, 7.8],
    'C10': [72.8, 1.8],
    'R6': [72.8, 3.4],
    'R7': [73.2, 6.2],
    'R8': [73.2, 7.8],
}
for k, v in initial_tail.items():
    coords[k] = v

def count_collisions(c_map, clr=0.18):
    cols = []
    refs = list(c_map.keys())
    for i in range(len(refs)):
        r1 = refs[i]
        c1 = c_map[r1]
        for j in range(i+1, len(refs)):
            r2 = refs[j]
            c2 = c_map[r2]
            for p1 in fp_pads[r1]:
                x1_min = c1[0] + p1['dx'] - p1['w']/2 - clr
                x1_max = c1[0] + p1['dx'] + p1['w']/2 + clr
                y1_min = c1[1] + p1['dy'] - p1['h']/2 - clr
                y1_max = c1[1] + p1['dy'] + p1['h']/2 + clr
                for p2 in fp_pads[r2]:
                    x2_min = c2[0] + p2['dx'] - p2['w']/2
                    x2_max = c2[0] + p2['dx'] + p2['w']/2
                    y2_min = c2[1] + p2['dy'] - p2['h']/2
                    y2_max = c2[1] + p2['dy'] + p2['h']/2
                    if not (x1_max < x2_min or x1_min > x2_max or y1_max < y2_min or y1_min > y2_max):
                        diff_x = c1[0] - c2[0]
                        diff_y = c1[1] - c2[1]
                        cols.append((r1, r2, diff_x, diff_y))
                        break
                else:
                    continue
                break
    return cols

print("Starting tail optimization...")
fixed = set(['J_IMU', 'J_USB', 'J_SD'])

for step in range(1000):
    cols = count_collisions(coords, clr=0.18)
    if not cols:
        print(f"ZERO COLLISIONS ACHIEVED AT STEP {step}!")
        break

    for r1, r2, dx, dy in cols:
        dist = math.hypot(dx, dy) or 0.01
        step_x = (dx / dist) * 0.05
        step_y = (dy / dist) * 0.05

        if r1 not in fixed:
            coords[r1][0] += step_x
            coords[r1][1] += step_y
        if r2 not in fixed:
            coords[r2][0] -= step_x
            coords[r2][1] -= step_y

        # Clamp boundaries
        for r in [r1, r2]:
            if r not in fixed:
                coords[r][0] = max(5.0, min(75.0, coords[r][0]))
                coords[r][1] = max(1.5, min(7.7, coords[r][1]))

final_cols = count_collisions(coords, clr=0.18)
print(f"Final collisions: {len(final_cols)}")
for c in final_cols:
    print(f"  {c[0]} vs {c[1]}")

if not final_cols:
    with open('output/RevF_Working/solved_coords.json', 'w') as f:
        json.dump({k: [round(v[0], 3), round(v[1], 3)] for k, v in coords.items()}, f, indent=2)
    print("SAVED 100% COLLISION FREE COORDINATES TO solved_coords.json!")

