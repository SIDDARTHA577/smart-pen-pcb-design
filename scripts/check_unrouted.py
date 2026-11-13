import sys
sys.path.insert(0, '.')
from scripts.solve_zero_drc import run_check

pads, segs, vias, errs = run_check()

all_sch_nets = set(p['net'] for p in pads if p['net'])
routed_nets = set(s[5] for s in segs)

print("All nets with pads:", len(all_sch_nets))
print("Routed nets:", len(routed_nets))
print("Unrouted nets:")
for n in sorted(all_sch_nets - routed_nets):
    pad_list = [(p['ref'], p['pin'], p['x'], p['y']) for p in pads if p['net'] == n]
    print(f"  * {n} ({len(pad_list)} pads): {pad_list}")
