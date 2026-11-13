with open('output/RevF_Working/SmartPen.kicad_sch', 'r', encoding='utf-8') as f:
    sch = f.read()

pos = sch.find('U0TXD/GPIO21')
print(sch[pos:pos+1000])
