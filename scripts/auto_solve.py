"""Iterative relaxation to strictly resolve all remaining collisions."""
import json
import sys
sys.path.insert(0, '.')
from scripts.relax_placement import count_collisions, fp_pads

with open('output/RevF_Working/solved_coords.json') as f:
    coords = json.load(f)

# Hard constraint: J_USB at 81.5, J_IMU at 3.0.
# All other parts must stay at X <= 74.8 mm to never touch J_USB!
fixed = set(['J_USB', 'J_IMU'])

# Ensure all USB cluster parts are shifted to X <= 74.8 mm
for ref in ['U_ESD', 'R5', 'R6', 'R7', 'R8', 'C10']:
    coords[ref][0] = min(coords[ref][0], 74.5)

for it in range(2000):
    cols = count_collisions(coords, clearance=0.16)
    if not cols:
        print(f"CONVERGED TO 0 COLLISIONS AT ITERATION {it}!")
        break

    for ref1, ref2, dx, dy, diff_x, diff_y in cols:
        # Repulsive push
        mag = 0.04
        push_x = mag if diff_x > 0 else -mag
        push_y = mag if diff_y > 0 else -mag

        if abs(diff_x) < abs(diff_y):
            # Prefer vertical separation if closer in Y
            if ref1 not in fixed:
                coords[ref1][1] += push_y
            if ref2 not in fixed:
                coords[ref2][1] -= push_y
        else:
            if ref1 not in fixed:
                coords[ref1][0] += push_x
            if ref2 not in fixed:
                coords[ref2][0] -= push_x

        # Enforce board boundaries
        for ref in [ref1, ref2]:
            if ref not in fixed:
                # Max X is 74.8 mm for all parts except J_USB
                coords[ref][0] = max(5.2, min(74.8, coords[ref][0]))
                coords[ref][1] = max(1.2, min(8.0, coords[ref][1]))

final_cols = count_collisions(coords, clearance=0.16)
print(f"Final collision count: {len(final_cols)}")
for c in final_cols:
    print(f"  {c[0]} vs {c[1]}: dx={c[2]:.3f}, dy={c[3]:.3f}")

if not final_cols:
    with open('output/RevF_Working/solved_coords.json', 'w') as f:
        json.dump(coords, f, indent=2)
    print("SAVED 100% COLLISION-FREE COORDINATES!")

