import re
from collections import Counter

with open("reports/drc_after_shorts_repair.rpt", "r") as f:
    text = f.read()

types = re.findall(r'\[([a-z_]+)\]', text)
counts = Counter(types)
print("Remaining violation types:")
for t, count in counts.most_common():
    print(f"  {t}: {count}")

print("Total reported items:", sum(counts.values()))

