with open('output/RevG/SmartPen.kicad_sch', 'r') as f:
    text = f.read()

idx = text.find('(property "Reference" "U_ESD"')
print(text[idx-200:idx+600])

