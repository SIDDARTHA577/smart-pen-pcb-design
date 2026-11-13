import sys
sys.path.insert(0, '.')
from scripts.solve_zero_drc import run_check
from scripts.verify_smartpen_geometry import check_pcb_geometry

pads, segments, vias, err_count = run_check()
errors = check_pcb_geometry(pads, segments, vias)

by_cat = {}
for e in errors:
    cat = e.split(':')[0].strip()
    if cat not in by_cat: by_cat[cat] = []
    by_cat[cat].append(e)

print(f"Total errors: {len(errors)}")
for cat, items in sorted(by_cat.items()):
    print(f"\n=== {cat} ({len(items)}) ===")
    for it in items:
        print(" ", it)
