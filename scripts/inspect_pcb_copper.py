import re

# Parse PCB file to inspect tracks and vias
with open('output/RevG/SmartPen.kicad_pcb', 'r') as f:
    pcb = f.read()

# Extract all segments: (segment (start X Y) (end X Y) (width W) (layer L) (net N) (uuid U))
segments = re.findall(r'\(segment\s+\(start\s+([-\d\.]+)\s+([-\d\.]+)\)\s+\(end\s+([-\d\.]+)\s+([-\d\.]+)\)\s+\(width\s+([-\d\.]+)\)\s+\(layer\s+"([^"]+)"\)\s+\(net\s+(\d+)\)\s+\(uuid\s+"([^"]+)"\)\)', pcb)

# Extract all vias: (via (at X Y) (size S) (drill D) (layers L1 L2) (net N) (uuid U))
vias = re.findall(r'\(via\s+\(at\s+([-\d\.]+)\s+([-\d\.]+)\)\s+\(size\s+([-\d\.]+)\)\s+\(drill\s+([-\d\.]+)\)\s+\(layers\s+"([^"]+)"\s+"([^"]+)"\)\s+\(net\s+(\d+)\)\s+\(uuid\s+"([^"]+)"\)\)', pcb)

print(f'Total segments in PCB: {len(segments)}')
print(f'Total vias in PCB: {len(vias)}')

# Extract net mapping: (net N "Name")
net_defs = dict(re.findall(r'\(net\s+(\d+)\s+"([^"]+)"\)', pcb))
print(f'Total nets defined: {len(net_defs)}')

