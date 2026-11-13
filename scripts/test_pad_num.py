import subprocess

kicad_cli = r'C:\Users\goran\AppData\Local\Programs\KiCad\10.0\bin\kicad-cli.exe'

with open('output/RevF_Working/SmartPen.kicad_pcb', 'r', encoding='utf-8') as f:
    t = f.read()

# Let's change J_BAT pad 3 and 4 to "" and see if DRC still reports net_conflict
t_mod = t.replace('(pad "3" smd rect (at -2.100 0.000) (size 1.200 1.800) (layers "F.Cu" "F.Paste" "F.Mask") (net 9 "/GND"))',
                  '(pad "" smd rect (at -2.100 0.000) (size 1.200 1.800) (layers "F.Cu" "F.Paste" "F.Mask") (net 9 "/GND"))')
t_mod = t_mod.replace('(pad "4" smd rect (at 2.100 0.000) (size 1.200 1.800) (layers "F.Cu" "F.Paste" "F.Mask") (net 9 "/GND"))',
                      '(pad "" smd rect (at 2.100 0.000) (size 1.200 1.800) (layers "F.Cu" "F.Paste" "F.Mask") (net 9 "/GND"))')

with open('output/RevF_Working/test_jbat.kicad_pcb', 'w', encoding='utf-8') as f:
    f.write(t_mod)

res = subprocess.run([kicad_cli, 'pcb', 'drc', '--severity-all', '--schematic-parity', '-o', 'reports/RevF/test_jbat.rpt', 'output/RevF_Working/test_jbat.kicad_pcb'], capture_output=True, text=True)

with open('reports/RevF/test_jbat.rpt', 'r') as f:
    rpt = f.read()

print("J_BAT in report:", "J_BAT" in rpt)
if "J_BAT" in rpt:
    for line in rpt.splitlines():
        if "J_BAT" in line:
            print("  ", line)
else:
    print("SUCCESS: J_BAT has 0 errors/warnings!")
