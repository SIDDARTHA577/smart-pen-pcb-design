import json

with open("drc_current.json") as f:
    d = json.load(f)

print(f"VIOLATIONS: {len(d.get('violations', []))}")
for v in d.get('violations', []):
    items_desc = [it.get('description', '') for it in v.get('items', [])]
    print(f"  [{v.get('type')}] {v.get('description')}: {items_desc}")

print(f"\nUNCONNECTED: {len(d.get('unconnected_items', []))}")
for u in d.get('unconnected_items', []):
    items_desc = [it.get('description', '') for it in u.get('items', [])]
    print(f"  [{u.get('type')}] {u.get('description')}: {items_desc}")
