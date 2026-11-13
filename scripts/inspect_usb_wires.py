import re

with open('output/RevF_Working/SmartPen.kicad_sch', 'r', encoding='utf-8') as f:
    sch = f.read()

# Find J_USB symbol instance
pos = sch.find('"(lib_id "SmartPen_Lib:J_USB")')
if pos == -1:
    pos = sch.find('"TYPE-C-31-M-12"')
# print lines around it
start = max(0, pos - 500)
end = min(len(sch), pos + 1500)
print(sch[start:end])
