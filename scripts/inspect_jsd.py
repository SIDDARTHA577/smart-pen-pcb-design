import sys; sys.path.insert(0, '.')
from scripts.solve_zero_drc_perfect import run_check

pads, _, _, _ = run_check()
jsd_pads = [p for p in pads if p['ref'] == 'J_SD']
for p in sorted(jsd_pads, key=lambda x: int(x['pin']) if x['pin'].isdigit() else 99):
    print(f"  J_SD.{p['pin']:>2} ({p['net']:<12}) at ({p['x']:.3f}, {p['y']:.3f}) w={p['w']:.2f} h={p['h']:.2f}")
