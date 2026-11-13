import sys
sys.path.insert(0, '.')
from scripts.solve_zero_drc_perfect import run_check

pads, segments, vias, n_err = run_check()

for arg in sys.argv[1:]:
    print(f"=== COMPONENT: {arg} ===")
    ref_pads = [p for p in pads if p['ref'] == arg]
    for p in ref_pads:
        print(f"  {p['ref']}.{p['pin']} ({p['net']}) at ({p['x']:.3f}, {p['y']:.3f}) w={p['w']} h={p['h']}")
