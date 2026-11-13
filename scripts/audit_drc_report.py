import re
from collections import Counter

with open('reports/RevF/SmartPen_drc_test.rpt', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# Find all violation types
violation_types = re.findall(r'\[([^\]]+)\]:', text)
counts = Counter(violation_types)

print("=== DRC VIOLATION BREAKDOWN ===")
for vtype, count in counts.most_common():
    print(f"{vtype:30s}: {count}")

# Print first 5 examples of each type
print("\n=== SAMPLES OF EACH TYPE ===")
blocks = text.split('\n\n')
samples = {}
for b in blocks:
    m = re.search(r'\[([^\]]+)\]:', b)
    if m:
        t = m.group(1)
        if t not in samples: samples[t] = []
        if len(samples[t]) < 3:
            samples[t].append(b.strip())

for t, b_list in samples.items():
    print(f"\n--- TYPE: {t} ---")
    for b in b_list:
        print(b)
        print("-" * 40)

