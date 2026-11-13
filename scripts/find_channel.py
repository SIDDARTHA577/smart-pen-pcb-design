import sys
sys.path.insert(0, '.')
from scripts.test_perfect_architecture import test_architecture

pads, segs, vias, errs = test_architecture()

print("PADS between X=12 and X=23:")
for p in sorted(pads, key=lambda p: (p['x'], p['y'])):
    if 12.0 <= p['x'] <= 23.0:
        print(f"  {p['ref']}.{p['pin']} ({p['net']}): x={p['x']:.2f}, y={p['y']:.2f}, w={p['w']:.2f}, h={p['h']:.2f}")
