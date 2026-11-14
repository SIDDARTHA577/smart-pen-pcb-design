import hashlib
from pathlib import Path

files = [
    'output/RevG/SmartPen.kicad_sch',
    'output/RevG/SmartPen.kicad_pcb',
    'output/RevG/SmartPen.pretty/J_USB.kicad_mod',
    'output/RevG/Front_MPU/Front_MPU.kicad_sch',
    'output/RevG/Front_MPU/Front_MPU.kicad_pcb',
    'output/RevG/MicroSD_Carrier/MicroSD_Carrier.kicad_sch',
    'output/RevG/MicroSD_Carrier/MicroSD_Carrier.kicad_pcb',
    'output/RevG/Touch_Sensor/Touch_Sensor.kicad_sch',
    'output/RevG/Touch_Sensor/Touch_Sensor.kicad_pcb',
    'reports/RevG/Phase03A/raw/Main_SmartPen_erc.rpt',
    'reports/RevG/Phase03A/raw/Main_SmartPen_netlist.net',
    'reports/RevG/Phase03A/raw/Main_SmartPen_drc.rpt',
    'reports/RevG/Phase03A/raw/Front_MPU_erc.rpt',
    'reports/RevG/Phase03A/raw/MicroSD_Carrier_erc.rpt',
    'reports/RevG/Phase03A/raw/Touch_Sensor_erc.rpt',
]

print("=== SOURCE & DELIVERABLE SHA-256 HASHES ===")
for f in files:
    p = Path(f)
    if p.exists():
        h = hashlib.sha256(p.read_bytes()).hexdigest()
        print(f"{p.name:<28} | Size: {p.stat().st_size:>7} bytes | SHA256: {h}")
    else:
        print(f"{p.name:<28} | NOT FOUND")
