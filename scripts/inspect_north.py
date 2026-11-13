import sys; sys.path.insert(0, '.')
from scripts.solve_clean_geometry import solve

pads, segments, vias, _ = solve()
print("=== Component Pads in X in [43, 50], Y >= 6.5 ===")
for p in pads:
    if 43 <= p['x'] <= 50 and p['y'] >= 6.5:
        print(f"  {p['ref']}.{p['pin']} ({p['net']:<12}) at ({p['x']:.2f}, {p['y']:.2f}) w={p['w']:.2f} h={p['h']:.2f}")

print("\n=== Vias in X in [43, 50], Y >= 6.5 ===")
for v in vias:
    if 43 <= v[0] <= 50 and v[1] >= 6.5:
        print(f"  {v[2]:<12} at ({v[0]:.2f}, {v[1]:.2f})")
