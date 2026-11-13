with open('reports/RevF/SmartPen_clean_drc.rpt', 'r', encoding='utf-8') as f:
    text = f.read()

import re
blocks = text.split('\n\n')
by_type = {}
for b in blocks:
    b = b.strip()
    if not b:
        continue
    m = re.search(r'\[([a-z_]+)\]:\s*(.*)', b)
    if m:
        vtype = m.group(1)
        if vtype not in by_type:
            by_type[vtype] = []
        by_type[vtype].append(b)

for vtype, items in sorted(by_type.items()):
    print(f"=== {vtype} ({len(items)}) ===")
    for item in items[:5]: # print up to 5 examples
        print("---")
        print(item)
    if len(items) > 5:
        print(f"... and {len(items)-5} more")
