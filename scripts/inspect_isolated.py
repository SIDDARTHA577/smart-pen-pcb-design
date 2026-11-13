with open('reports/RevF/SmartPen_clean_drc.rpt', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.finditer(r'\[(isolated_copper|starved_thermal)\]:.*?(?=\n\[|\n\*\*|\Z)', text, re.DOTALL)
for m in matches:
    print("---------------------------------")
    print(m.group(0))
