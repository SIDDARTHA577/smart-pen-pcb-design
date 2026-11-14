import json

with open('reports/RevG/Phase03B/raw/before/Main_SmartPen_drc.json', 'r') as f:
    data = json.load(f)

mismatches = [v for v in data['violations'] if v.get('type') == 'lib_footprint_mismatch']
print(f'Total lib_footprint_mismatch: {len(mismatches)}')
for i, m in enumerate(mismatches, 1):
    print(f'#{i}: {m.get("description")}')
    for it in m.get('items', []):
        print(f'    item: {it}')

