import sys
sys.path.insert(0, '.')
from scripts.solve_zero_drc import run_check

pads, segs, vias, errs = run_check()

print("F.Cu segments and pads between X=46 and X=52:")
for p in pads:
    if 46 <= p['x'] <= 52:
        print(f"  Pad {p['ref']}.{p['pin']} ({p['net']}) at ({p['x']:.2f}, {p['y']:.2f}) w={p['w']:.2f}, h={p['h']:.2f}")

for s in segs:
    if s[4] == "F.Cu" and (46 <= s[0] <= 52 or 46 <= s[2] <= 52):
        print(f"  Seg {s[5]} ({s[0]:.2f},{s[1]:.2f})->({s[2]:.2f},{s[3]:.2f})")
