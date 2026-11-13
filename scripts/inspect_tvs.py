import sys; sys.path.insert(0, '.')
from scripts.solve_zero_drc_final import solve

pads, _, _, _ = solve()
print("=== TVS and USB resistors pads ===")
for p in pads:
    if p['ref'] in ['U_ESD', 'R7', 'R8']:
        print(f"  {p['ref']}.{p['pin']} ({p['net']:<15}) at ({p['x']:.2f}, {p['y']:.2f}) w={p['w']:.2f} h={p['h']:.2f}")
