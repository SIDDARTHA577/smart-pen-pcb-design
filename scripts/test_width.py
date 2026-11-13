import subprocess

kicad_cli = r'C:\Users\goran\AppData\Local\Programs\KiCad\10.0\bin\kicad-cli.exe'

with open('output/RevF_Working/test_parity.kicad_pcb', 'r', encoding='utf-8') as f:
    t = f.read()

# Add min_trace_width to setup or check setup syntax in kicad 10
# In KiCad 8/9/10, setup constraints are:
# (stackup ...) or (setup ...)
print("Testing kicad-cli on test_parity.kicad_pcb...")
res = subprocess.run([kicad_cli, 'pcb', 'drc', '--severity-all', '--refill-zones', '-o', 'reports/RevF/test_w.rpt', 'output/RevF_Working/test_parity.kicad_pcb'], capture_output=True, text=True)
print("Return code:", res.returncode)
print("Stdout:", res.stdout[:200])
print("Stderr:", res.stderr[:200])
