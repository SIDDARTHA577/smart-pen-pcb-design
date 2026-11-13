import re

with open('output/RevF_Working/SmartPen.kicad_sch', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's see how U_ESD is instantiated in schematic
for name in ['U_ESD', 'J_USB', 'U3', 'SW3', 'J_BAT', 'J_MOT', 'J_PWR', 'J_RF']:
    m = re.findall(rf'\(symbol\s+\(lib_id\s+"[^"]*:{name}"\).*?\n\s+\)', text, re.DOTALL)
    if not m:
        # maybe symbol without lib_id
        m = re.findall(rf'\(symbol[^\n]*\n[^\n]*"{name}"[^\n]*\n.*?\n\s+\)', text, re.DOTALL)
    print(f"Instances of {name}: {len(m)}")
    for inst in m:
        # print properties and pin entries if any
        print(inst[:600])

