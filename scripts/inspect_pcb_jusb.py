with open('output/RevG/SmartPen.kicad_pcb', 'r') as f:
    text = f.read()

idx = text.find('(property "Reference" "J_USB"')
start = text.rfind('(footprint "', 0, idx)
end = text.find('(footprint "', idx)
if end == -1: end = text.find('(zone', idx)
print(text[start:start+1200])

