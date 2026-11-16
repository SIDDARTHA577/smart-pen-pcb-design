import json, sys

fpath = sys.argv[1] if len(sys.argv) > 1 else 'scratch_test_clean_swap_drc.json'
with open(fpath, 'r') as f:
    d = json.load(f)

viols = d.get('violations', [])
print(f"Total violations: {len(viols)}")
for i, v in enumerate(viols):
    t = v.get('type')
    desc = v.get('description')
    items = v.get('items', [])
    print(f"\n[{i+1}] {t}: {desc}")
    for item in items:
        print(f"    - {item.get('item')}: pos={item.get('pos')}")

unconn = d.get('unconnected_items', [])
print(f"\nTotal unconnected items: {len(unconn)}")
for i, u in enumerate(unconn):
    print(f"[{i+1}] {u.get('description')}: {u.get('items', [])}")
