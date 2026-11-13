import re
from collections import defaultdict

with open('output/RevF_Working/SmartPen.kicad_sch', 'r', encoding='utf-8') as f:
    sch = f.read()

# Let's find all labels and their coordinates, and pins
# Or we can read the netlist or DRC report nets
with open('output/RevF_Working/SmartPen.kicad_pcb', 'r', encoding='utf-8') as f:
    pcb = f.read()

nets = re.findall(r'\(net\s+(\d+)\s+"([^"]+)"\)', pcb)
net_map = {n[1]: int(n[0]) for n in nets}
print(f"Total nets defined in PCB: {len(nets)}")
for name, nid in sorted(net_map.items()):
    print(f"Net {nid:2d}: {name}")
