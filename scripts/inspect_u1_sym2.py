with open('output/RevF_Working/SmartPen.kicad_sch', 'r', encoding='utf-8') as f:
    sch = f.read()

pos = sch.find('NC/INTERNAL FLASH')
print(sch[pos:pos+1500])
