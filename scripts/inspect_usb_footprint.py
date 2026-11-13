import re

with open('output/RevF_Working/SmartPen.kicad_pcb', 'r', encoding='utf-8') as f:
    pcb = f.read()

p = pcb.find('(footprint "SmartPen:J_USB"')
if p == -1:
    p = pcb.find('J_USB')
    p = pcb.rfind('(footprint', 0, p)

end = pcb.find('(footprint', p + 10)
print(pcb[p:end if end != -1 else p+3000])
