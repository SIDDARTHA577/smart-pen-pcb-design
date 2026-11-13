with open('reports/RevF/SmartPen_clean_drc.rpt', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'\[shorting_items\].*?(?=\n\[|\n\*\*|\Z)', text, re.DOTALL)
print(f"Total shorting items: {len(matches)}")
for i, m in enumerate(matches):
    print(f"--- Short {i+1} ---")
    print(m)
