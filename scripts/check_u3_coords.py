import sys
sys.path.insert(0, '.')
from scripts.solve_zero_drc import run_check

pads, _, _, _ = run_check()
u3_pads = [p for p in pads if p['ref'] == 'U3']
for p in sorted(u3_pads, key=lambda x: int(x['pin']) if x['pin'].isdigit() else 99):
    print(f"Pin {p['pin']:>2}: net={p['net']:<18} at ({p['x']:.3f}, {p['y']:.3f})")
