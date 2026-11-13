import re
from collections import defaultdict

with open('reports/RevF/SmartPen.net', 'r', encoding='utf-8') as f:
    text = f.read()

nets = re.split(r'\(net\s+', text)[1:]
net_dict = {}
for n in nets:
    name_m = re.search(r'\(name\s+"([^"]+)"\)', n)
    if not name_m:
        continue
    name = name_m.group(1)
    nodes = re.findall(r'\(ref\s+"([^"]+)"\)\s+\(pin\s+"([^"]+)"\)', n)
    net_dict[name] = [f"{ref}.{pin}" for ref, pin in nodes]

print(f"Parsed {len(net_dict)} nets from netlist.")
for name, pins in sorted(net_dict.items()):
    print(f"{name:<20} ({len(pins):2d} pins): {', '.join(pins)}")
