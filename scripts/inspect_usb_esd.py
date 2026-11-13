import re

with open('output/RevF_Working/SmartPen.kicad_sch', 'r', encoding='utf-8') as f:
    sch = f.read()

p = sch.find('(symbol "SmartPen_Lib:J_USB"')
print(sch[p:p+3000])
