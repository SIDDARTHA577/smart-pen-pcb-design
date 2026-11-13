with open('reports/RevF/test_0.rpt', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.finditer(r'\[isolated_copper\]:.*?\n\s+@(.*?): Zone', text)
for m in matches:
    print(m.group(1))
