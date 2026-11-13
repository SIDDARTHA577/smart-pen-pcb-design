import sys; sys.path.insert(0, '.')
from scripts.solve_zero_drc_perfect import run_check

pads, segments, vias, _ = run_check()
print("=== B.Cu Segments in X in [30, 45] ===")
for s in sorted(segments, key=lambda x: (x[1], x[0])):
    if s[4] == 'B.Cu' and (30 <= s[0] <= 45 or 30 <= s[2] <= 45):
        print(f"  {s[5]:<15}: ({s[0]:.2f}, {s[1]:.2f}) -> ({s[2]:.2f}, {s[3]:.2f})")

print("=== Vias in X in [30, 45] ===")
for v in sorted(vias, key=lambda x: (x[1], x[0])):
    if 30 <= v[0] <= 45:
        print(f"  {v[2]:<15}: ({v[0]:.2f}, {v[1]:.2f})")
