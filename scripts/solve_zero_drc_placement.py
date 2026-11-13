"""Deterministic exact collision resolver."""
import json
import sys
sys.path.insert(0, '.')
from scripts.relax_placement import count_collisions, fp_pads

with open('output/RevF_Working/solved_coords.json') as f:
    coords = json.load(f)

fixed = set(['J_USB', 'J_IMU'])

# Greedy coordinate adjuster
step = 0.05
for iteration in range(500):
    cols = count_collisions(coords, clearance=0.15)
    if not cols:
        print(f"STRICT ZERO COLLISIONS ACHIEVED AT ITERATION {iteration}!")
        break

    ref1, ref2, dx, dy, diff_x, diff_y = cols[0]
    # Try 4 directions for ref2
    best_move = None
    min_c = len(cols)

    for ref_to_move in ([ref2] if ref2 not in fixed else [ref1]):
        orig_x, orig_y = coords[ref_to_move]
        for dx_try, dy_try in [(0.2, 0), (-0.2, 0), (0, 0.2), (0, -0.2), (0.4, 0), (-0.4, 0), (0, 0.4), (0, -0.4)]:
            new_x = max(5.0, min(75.5, orig_x + dx_try))
            new_y = max(1.2, min(8.0, orig_y + dy_try))
            coords[ref_to_move] = [new_x, new_y]
            c_test = len(count_collisions(coords, clearance=0.15))
            if c_test < min_c:
                min_c = c_test
                best_move = (ref_to_move, new_x, new_y)
        coords[ref_to_move] = [orig_x, orig_y]

    if best_move:
        coords[best_move[0]] = [best_move[1], best_move[2]]
    else:
        # random jitter if local minimum
        ref_jitter = ref1 if ref1 not in fixed else ref2
        coords[ref_jitter][0] += (0.1 if diff_x > 0 else -0.1)
        coords[ref_jitter][1] += (0.1 if diff_y > 0 else -0.1)

final_cols = count_collisions(coords, clearance=0.15)
print(f"Final collision count: {len(final_cols)}")
for c in final_cols:
    print(f"  {c[0]} vs {c[1]}: dx={c[2]:.3f}, dy={c[3]:.3f}")

if not final_cols:
    with open('output/RevF_Working/solved_coords.json', 'w') as f:
        json.dump(coords, f, indent=2)
    print("SAVED 100% COLLISION-FREE COORDINATES!")

