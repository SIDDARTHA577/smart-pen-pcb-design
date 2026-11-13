import re
from collections import Counter

with open('reports/RevF/SmartPen_drc_test.rpt', 'r', encoding='utf-8') as f:
    rpt = f.read()

# Find all violations: [type]: description
violations = re.findall(r'\[([^\]]+)\]:\s+([^\n]+)', rpt)
counts = Counter(v[0] for v in violations)

print(f"Total violations found: {len(violations)}")
for vtype, count in counts.most_common():
    print(f"  {vtype:35s}: {count}")

print("\nFirst 10 violations:")
for vtype, desc in violations[:10]:
    print(f"  [{vtype}] {desc}")
