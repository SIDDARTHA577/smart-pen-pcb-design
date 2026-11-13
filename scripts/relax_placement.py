"""Automatic placement relaxation solver to achieve 0 collisions."""
import json

with open('output/RevF_Working/SmartPen_RevE_PCB.json', 'r') as f:
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

# Initial coords from logical floorplan
coords = {
    'J_IMU': [3.2, 4.6],
    'C15': [6.2, 2.0],
    'R10': [6.2, 4.6],
    'R11': [6.2, 7.2],
    'J_TOUCH': [9.0, 2.4],
    'SW4': [11.5, 7.0],
    'R19': [13.5, 2.4],
    'R12': [14.5, 7.0],
    'SW5': [17.5, 7.0],
    'D1': [16.5, 2.2],
    'D2': [16.5, 4.4],
    'R13': [20.5, 7.0],
    'R14': [19.0, 2.2],
    'R15': [19.0, 4.4],
    'U3': [23.5, 4.6],
    'C13': [23.5, 8.0],
    'R16': [27.0, 2.2],
    'R17': [27.0, 4.6],
    'Q1': [28.8, 2.2],
    'D3': [29.5, 5.0],
    'J_MOT': [31.5, 7.0],
    'SW1': [33.5, 1.8],
    'R4': [35.5, 2.0],
    'C4': [37.0, 2.0],
    'R1': [38.5, 2.0],
    'C1': [40.0, 2.0],
    'C6': [33.5, 7.5],
    'Y1': [35.5, 7.5],
    'C7': [37.5, 7.5],
    'L1': [39.0, 7.5],
    'U1': [43.0, 4.6],
    'SW2': [47.0, 1.8],
    'R3': [48.5, 2.0],
    'C5': [50.0, 2.0],
    'R2': [51.5, 2.0],
    'FB1': [47.0, 7.5],
    'C2': [48.5, 7.5],
    'C3': [50.0, 7.5],
    'L2': [52.5, 5.0],
    'C8': [52.5, 3.6],
    'C9': [54.0, 3.6],
    'J_RF': [55.0, 5.0],
    'J_SD': [58.0, 4.6],
    'R18': [61.0, 2.0],
    'J_UART': [61.0, 7.0],
    'J_BAT': [64.0, 2.8],
    'SW3': [64.0, 7.2],
    'C11': [66.5, 5.5],
    'U2': [68.0, 3.2],
    'C12': [69.5, 5.5],
    'R9': [70.5, 2.0],
    'J_PWR': [72.5, 4.6],
    'C14': [74.5, 4.6],
    'U_ESD': [76.0, 4.6],
    'R5': [77.5, 2.0],
    'R6': [77.5, 3.4],
    'R7': [77.5, 5.8],
    'R8': [77.5, 7.2],
    'C10': [79.0, 2.0],
    'J_USB': [81.5, 4.6]
}

# Fixed parts that must not move
fixed = set(['J_IMU', 'J_USB'])

def count_collisions(c_map, clearance=0.18):
    collisions = []
    for ref1, p1_list in fp_pads.items():
        c1_x, c1_y = c_map[ref1]
        for ref2, p2_list in fp_pads.items():
            if ref1 >= ref2:
                continue
            c2_x, c2_y = c_map[ref2]
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
                    if dx < clearance and dy < clearance:
                        collisions.append((ref1, ref2, dx, dy, x1 - x2, y1 - y2))
    return collisions

def run_relaxation():
    print("Initial collisions:", len(count_collisions(coords)))

    # Optimization loop
    for iteration in range(500):
        cols = count_collisions(coords, clearance=0.18)
        if not cols:
            print(f"Converged with 0 collisions at iteration {iteration}!")
            break

        for ref1, ref2, dx, dy, diff_x, diff_y in cols:
            step_x = 0.05 if diff_x > 0 else -0.05
            step_y = 0.05 if diff_y > 0 else -0.05

            if ref1 not in fixed:
                coords[ref1][0] += step_x
                coords[ref1][1] += step_y
            if ref2 not in fixed:
                coords[ref2][0] -= step_x
                coords[ref2][1] -= step_y

            # Clamp boundaries
            for ref in [ref1, ref2]:
                if ref not in fixed:
                    coords[ref][0] = max(3.0, min(80.0, coords[ref][0]))
                    coords[ref][1] = max(1.5, min(7.8, coords[ref][1]))

    final_cols = count_collisions(coords, clearance=0.18)
    print(f"Final collisions: {len(final_cols)}")

    # Save final coords to json
    with open('output/RevF_Working/solved_coords.json', 'w') as f:
        json.dump({k: [round(v[0], 3), round(v[1], 3)] for k, v in coords.items()}, f, indent=2)

    print("Saved solved_coords.json")

if __name__ == '__main__':
    run_relaxation()
