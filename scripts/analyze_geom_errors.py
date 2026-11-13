import sys
sys.path.insert(0, '.')
from scripts.verify_smartpen_geometry import check_pcb_geometry
from scripts.test_smartpen_verifier import all_pads, segments, vias
from collections import Counter

errors = check_pcb_geometry(all_pads, segments, vias)
print(f"Total errors: {len(errors)}")

# Group by category
cats = Counter()
for e in errors:
    cat = e.split(':')[0].split('(')[0].strip()
    cats[cat] += 1

print("\nError categories:")
for c, count in cats.most_common():
    print(f"  {c:30s}: {count}")

# Print all via collisions
print("\n--- VIA COLLISIONS ---")
for e in errors:
    if "Via collision" in e or "via hole" in e:
        print(" ", e)

# Print all via-to-pad collisions
print("\n--- VIA-TO-PAD COLLISIONS ---")
for e in errors:
    if "Via " in e and "collides with" in e:
        print(" ", e)
