with open('reports/RevF/test_0.rpt', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'\[isolated_copper\].*?(?=\n\[|\n\*\*|\Z)', text, re.DOTALL)
for m in matches:
    print(m)
