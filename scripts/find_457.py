with open('output/RevF_Working/SmartPen.kicad_sch', 'r', encoding='utf-8') as f:
    sch = f.read()

pos = sch.find('457.20')
while pos != -1:
    print("Found 457.20 at", pos)
    print(sch[max(0, pos-200):min(len(sch), pos+300)])
    pos = sch.find('457.20', pos+1)
