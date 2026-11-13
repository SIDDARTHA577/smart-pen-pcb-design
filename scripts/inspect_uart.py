import sys; sys.path.insert(0, '.')
from scripts.solve_clean_geometry import solve

pads, _, _, _ = solve()
print("=== UART pads ===")
for p in pads:
    if 'UART' in p['net']:
        print(f"  {p['ref']}.{p['pin']} ({p['net']:<12}) at ({p['x']:.2f}, {p['y']:.2f})")
