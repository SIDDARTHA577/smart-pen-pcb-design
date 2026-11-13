import subprocess

kicad_cli = r'C:\Users\goran\AppData\Local\Programs\KiCad\10.0\bin\kicad-cli.exe'

for par in [True, False]:
    cmd = [kicad_cli, 'pcb', 'drc', '--severity-all', '--refill-zones']
    if par:
        cmd.append('--schematic-parity')
    cmd.extend(['-o', f'reports/RevF/test_par_{par}.rpt', 'output/RevF_Working/SmartPen.kicad_pcb'])
    subprocess.run(cmd, capture_output=True)
    with open(f'reports/RevF/test_par_{par}.rpt', 'r') as f:
        t = f.read()
    print(f"Parity {par}: track_width={t.count('[track_width]')}, total violations={t.count('  [')}")
