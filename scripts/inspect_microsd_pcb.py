import re

with open('output/RevG/MicroSD_Carrier/MicroSD_Carrier.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

print("Length of file:", len(text))
print("Filled polygons in file:", text.count('(filled_polygon'))
for m in re.finditer(r'\(zone\b', text):
    start = m.start()
    depth = 0
    for i in range(start, len(text)):
        if text[i] == '(':
            depth += 1
        elif text[i] == ')':
            depth -= 1
            if depth == 0:
                zone_block = text[start:i+1]
                net_m = re.search(r'\(net_name\s+"([^"]+)"\)', zone_block)
                layer_m = re.search(r'\(layers?\s+([^\)]+)\)', zone_block)
                filled_m = '(filled_polygon' in zone_block
                print(f"Zone: net={net_m.group(1) if net_m else 'None'}, layer={layer_m.group(1) if layer_m else 'None'}, filled={filled_m}")
                break
