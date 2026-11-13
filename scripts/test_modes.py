import subprocess

kicad_cli = r'C:\Users\goran\AppData\Local\Programs\KiCad\10.0\bin\kicad-cli.exe'

for mode in [0, 1, 2]:
    with open('output/RevF_Working/SmartPen.kicad_pcb', 'r', encoding='utf-8') as f:
        t = f.read()
    t_mod = t.replace('(fill yes (thermal_gap 0.15) (thermal_bridge_width 0.25))', f'(fill yes (thermal_gap 0.15) (thermal_bridge_width 0.25) (island_removal_mode {mode}))')
    with open('output/RevF_Working/test_mode.kicad_pcb', 'w', encoding='utf-8') as f:
        f.write(t_mod)
    res = subprocess.run([kicad_cli, 'pcb', 'drc', '--severity-all', '--refill-zones', '-o', f'reports/RevF/test_{mode}.rpt', 'output/RevF_Working/test_mode.kicad_pcb'], capture_output=True, text=True)
    with open(f'reports/RevF/test_{mode}.rpt', 'r') as rf:
        rpt = rf.read()
    print(f'Mode {mode}: isolated_copper count = {rpt.count("[isolated_copper]")}')
