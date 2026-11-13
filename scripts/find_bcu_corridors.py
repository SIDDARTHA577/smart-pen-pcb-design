import sys
sys.path.insert(0, '.')
from scripts.solve_zero_drc import run_check

pads, segs, vias, errs = run_check()

# Find all B.Cu segments and vias
b_segs = [s for s in segs if s[4] == "B.Cu"]
b_vias = vias # vias penetrate both layers

print(f"Total B.Cu segments: {len(b_segs)}, Total vias: {len(b_vias)}")

# For each Y from 0.5 to 8.7 in steps of 0.05, check how much continuous X length is free
for y_test in [round(0.5 + i*0.25, 2) for i in range(34)]:
    # Check if a horizontal trace at y_test collides with existing B.Cu segments
    blocked_x = []
    for s in b_segs:
        # Check if s is too close in Y
        y_min = min(s[1], s[3]) - 0.18/2 - 0.127
        y_max = max(s[1], s[3]) + 0.18/2 + 0.127
        if y_min <= y_test <= y_max:
            blocked_x.append((min(s[0], s[2]), max(s[0], s[2]), s[5]))
    
    # Check vias
    for v in b_vias:
        vy = v[1]
        if abs(vy - y_test) <= 0.25 + 0.127: # via radius + clearance
            vx = v[0]
            blocked_x.append((vx - 0.38, vx + 0.38, f"via_{v[2]}"))

    blocked_x.sort()
    # Merge overlapping intervals
    merged = []
    for start, end, name in blocked_x:
        if not merged:
            merged.append([start, end])
        else:
            if start <= merged[-1][1]:
                merged[-1][1] = max(merged[-1][1], end)
            else:
                merged.append([start, end])

    total_blocked = sum(end - start for start, end in merged)
    print(f"Y = {y_test:4.2f}: {len(merged)} blocks, {total_blocked:5.1f} mm blocked / 84 mm. Blocks: {merged[:3]}")
