import subprocess, re

kicad_cli = r'C:\Users\goran\AppData\Local\Programs\KiCad\10.0\bin\kicad-cli.exe'

with open('output/RevF_Working/SmartPen.kicad_pcb', 'r', encoding='utf-8') as f:
    t = f.read()

# Fix setup
t = t.replace('(pad_to_mask_clearance 0.05)', '(pad_to_mask_clearance 0.0)')
t = t.replace('(solder_mask_min_width 0.08)', '(solder_mask_min_width 0.0)')

# Fix J_BAT pads 3, 4
t = re.sub(r'(\(footprint "SmartPen:J_BAT".*?)\(pad "3" smd rect \(at -2.100 0.000\)', r'\1(pad "" smd rect (at -2.100 0.000)', t, flags=re.DOTALL)
t = re.sub(r'(\(footprint "SmartPen:J_BAT".*?)\(pad "4" smd rect \(at 2.100 0.000\)', r'\1(pad "" smd rect (at 2.100 0.000)', t, flags=re.DOTALL)

# Fix J_MOT pads 3, 4
t = re.sub(r'(\(footprint "SmartPen:J_MOT".*?)\(pad "3" smd rect \(at -2.100 0.000\)', r'\1(pad "" smd rect (at -2.100 0.000)', t, flags=re.DOTALL)
t = re.sub(r'(\(footprint "SmartPen:J_MOT".*?)\(pad "4" smd rect \(at 2.100 0.000\)', r'\1(pad "" smd rect (at 2.100 0.000)', t, flags=re.DOTALL)

# Fix J_PWR pads 4, 5
t = re.sub(r'(\(footprint "SmartPen:J_PWR".*?)\(pad "4" smd rect', r'\1(pad "" smd rect', t, flags=re.DOTALL)
t = re.sub(r'(\(footprint "SmartPen:J_PWR".*?)\(pad "5" smd rect', r'\1(pad "" smd rect', t, flags=re.DOTALL)

# Fix J_RF pad 3
t = re.sub(r'(\(footprint "SmartPen:J_RF".*?)\(pad "3" smd rect', r'\1(pad "" smd rect', t, flags=re.DOTALL)

# Fix SW3 pad 3
t = re.sub(r'(\(footprint "SmartPen:SW3".*?)\(pad "3" smd rect', r'\1(pad "" smd rect', t, flags=re.DOTALL)

# Fix U3 pad 21
t = re.sub(r'(\(footprint "SmartPen:U3".*?)\(pad "21" smd rect', r'\1(pad "" smd rect', t, flags=re.DOTALL)

# Fix U_ESD pads 4, 5, 6
t = re.sub(r'(\(footprint "SmartPen:U_ESD".*?)\(pad "4" smd rect', r'\1(pad "" smd rect', t, flags=re.DOTALL)
t = re.sub(r'(\(footprint "SmartPen:U_ESD".*?)\(pad "5" smd rect', r'\1(pad "" smd rect', t, flags=re.DOTALL)
t = re.sub(r'(\(footprint "SmartPen:U_ESD".*?)\(pad "6" smd rect', r'\1(pad "" smd rect', t, flags=re.DOTALL)

with open('output/RevF_Working/test_parity.kicad_pcb', 'w', encoding='utf-8') as f:
    f.write(t)

res = subprocess.run([kicad_cli, 'pcb', 'drc', '--severity-all', '--schematic-parity', '-o', 'reports/RevF/test_parity.rpt', 'output/RevF_Working/test_parity.kicad_pcb'], capture_output=True, text=True)

with open('reports/RevF/test_parity.rpt', 'r') as f:
    rpt = f.read()

import re
net_conflicts = re.findall(r'\[net_conflict\].*', rpt)
solder_bridges = re.findall(r'\[solder_mask_bridge\].*', rpt)
print(f"Remaining net_conflicts: {len(net_conflicts)}")
for nc in net_conflicts:
    print("  ", nc)
print(f"Remaining solder_mask_bridges: {len(solder_bridges)}")
