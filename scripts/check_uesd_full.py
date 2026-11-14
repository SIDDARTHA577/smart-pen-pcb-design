with open('output/RevG/SmartPen.kicad_sch', 'r') as f:
    text = f.read()

idx = text.find('(property "Reference" "U_ESD"')
idx2 = text.find('(symbol "SmartPen_Lib:U_ESD"', idx-200)
idx3 = text.find(')', text.find('(pin', idx2+300))
print(text[idx2:idx2+1200])

