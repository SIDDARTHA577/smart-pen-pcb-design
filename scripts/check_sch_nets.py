import re

with open('output/RevF_Working/SmartPen.kicad_sch', 'r', encoding='utf-8') as f:
    sch = f.read()

labels = set(re.findall(r'\(label\s+"([^"]+)"', sch))
global_labels = set(re.findall(r'\(global_label\s+"([^"]+)"', sch))
hier_labels = set(re.findall(r'\(hierarchical_label\s+"([^"]+)"', sch))

print("Labels count:", len(labels))
print("Global labels count:", len(global_labels))
print("Hierarchical labels count:", len(hier_labels))
print("Labels:", sorted(labels))
