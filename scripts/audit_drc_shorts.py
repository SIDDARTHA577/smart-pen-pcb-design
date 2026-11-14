import json

with open('reports/RevG/Phase03B/raw/before/Main_SmartPen_drc.json', 'r') as f:
    data = json.load(f)

shorts = [v for v in data['violations'] if v.get('type') == 'shorting_items']
print(f'Total shorting items found: {len(shorts)}')
for i, s in enumerate(shorts, 1):
    desc = s.get('description', '')
    items = s.get('items', [])
    item_str = []
    for it in items:
        pos = it.get('pos', {})
        item_str.append(f"{it.get('type')} on {it.get('layer')} at ({pos.get('x')}, {pos.get('y')}) [net {it.get('net')}]")
    print(f'#{i}: {desc}')
    for it_s in item_str:
        print(f'    - {it_s}')

