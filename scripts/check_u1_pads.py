import sys
sys.path.insert(0, '.')
from scripts.solve_zero_drc import run_check

pads, _, _, _ = run_check()
u1_pads = [p for p in pads if p['ref'] == 'U1']
for p in sorted(u1_pads, key=lambda x: int(x['pin']) if x['pin'].isdigit() else 99):
    print(f"U1 Pin {p['pin']:>2}: net={p['net']:<18} at ({p['x']:.3f}, {p['y']:.3f})")
