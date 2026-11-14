with open('output/RevG/SmartPen.kicad_sch', 'r') as f:
    text = f.read()

# Look for (symbol (lib_id "SmartPen_Lib:U_ESD") or similar
idx = 0
while True:
    idx = text.find('U_ESD', idx)
    if idx == -1: break
    start = text.rfind('(', 0, idx)
    print(text[start:start+300])
    print('---')
    idx += 5

