import sys; sys.path.insert(0, '.')
from scripts.solve_zero_drc_perfect import run_check

pads, _, _, _ = run_check()
q1_pads = [p for p in pads if p['ref'] == 'Q1']
for p in q1_pads:
    print(f"  Q1.{p['pin']} ({p['net']}) at ({p['x']:.3f}, {p['y']:.3f}) w={p['w']} h={p['h']}")
