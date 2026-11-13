with open('output/RevF_Working/SmartPen.kicad_sch', 'r', encoding='utf-8') as f:
    sch = f.read()

import re
pos = sch.find('(symbol "SmartPen_Lib:U1"')
print(sch[pos:pos+4000])
