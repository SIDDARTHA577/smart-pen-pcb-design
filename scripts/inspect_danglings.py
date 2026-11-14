import json

with open('reports/current_main_drc.json', 'r') as f:
    data = json.load(f)

for v in data.get('violations', []):
    if v.get('type') in ('via_dangling', 'track_dangling'):
        print(f"{v.get('type')}: {v.get('description')}")
        for it in v.get('items', []):
            print(f"   {it.get('description')} at {it.get('pos')}")
