import subprocess
import os

os.makedirs('reports/RevG/Phase03B/raw/after', exist_ok=True)

kicad_cli = r'C:\Users\goran\AppData\Local\Programs\KiCad\10.0\bin\kicad-cli.exe'

commands = [
    # Main PCB DRC
    [kicad_cli, 'pcb', 'drc', '--severity-all', '--schematic-parity', '--all-track-errors', '--refill-zones', '--format', 'report', '-o', 'reports/RevG/Phase03B/raw/after/Main_SmartPen_drc.rpt', 'output/RevG/SmartPen.kicad_pcb'],
    [kicad_cli, 'pcb', 'drc', '--severity-all', '--schematic-parity', '--all-track-errors', '--refill-zones', '--format', 'json', '-o', 'reports/RevG/Phase03B/raw/after/Main_SmartPen_drc.json', 'output/RevG/SmartPen.kicad_pcb'],
    # Main PCB ERC
    [kicad_cli, 'sch', 'erc', '--severity-all', '--format', 'report', '-o', 'reports/RevG/Phase03B/raw/after/Main_SmartPen_erc.rpt', 'output/RevG/SmartPen.kicad_sch'],
    [kicad_cli, 'sch', 'erc', '--severity-all', '--format', 'json', '-o', 'reports/RevG/Phase03B/raw/after/Main_SmartPen_erc.json', 'output/RevG/SmartPen.kicad_sch'],
    # Front MPU DRC & ERC
    [kicad_cli, 'pcb', 'drc', '--severity-all', '--schematic-parity', '--all-track-errors', '--refill-zones', '--format', 'report', '-o', 'reports/RevG/Phase03B/raw/after/Front_MPU_drc.rpt', 'output/RevG/Front_MPU/Front_MPU.kicad_pcb'],
    [kicad_cli, 'pcb', 'drc', '--severity-all', '--schematic-parity', '--all-track-errors', '--refill-zones', '--format', 'json', '-o', 'reports/RevG/Phase03B/raw/after/Front_MPU_drc.json', 'output/RevG/Front_MPU/Front_MPU.kicad_pcb'],
    [kicad_cli, 'sch', 'erc', '--severity-all', '--format', 'report', '-o', 'reports/RevG/Phase03B/raw/after/Front_MPU_erc.rpt', 'output/RevG/Front_MPU/Front_MPU.kicad_sch'],
    [kicad_cli, 'sch', 'erc', '--severity-all', '--format', 'json', '-o', 'reports/RevG/Phase03B/raw/after/Front_MPU_erc.json', 'output/RevG/Front_MPU/Front_MPU.kicad_sch'],
    # MicroSD Carrier DRC & ERC
    [kicad_cli, 'pcb', 'drc', '--severity-all', '--schematic-parity', '--all-track-errors', '--refill-zones', '--format', 'report', '-o', 'reports/RevG/Phase03B/raw/after/MicroSD_Carrier_drc.rpt', 'output/RevG/MicroSD_Carrier/MicroSD_Carrier.kicad_pcb'],
    [kicad_cli, 'pcb', 'drc', '--severity-all', '--schematic-parity', '--all-track-errors', '--refill-zones', '--format', 'json', '-o', 'reports/RevG/Phase03B/raw/after/MicroSD_Carrier_drc.json', 'output/RevG/MicroSD_Carrier/MicroSD_Carrier.kicad_pcb'],
    [kicad_cli, 'sch', 'erc', '--severity-all', '--format', 'report', '-o', 'reports/RevG/Phase03B/raw/after/MicroSD_Carrier_erc.rpt', 'output/RevG/MicroSD_Carrier/MicroSD_Carrier.kicad_sch'],
    [kicad_cli, 'sch', 'erc', '--severity-all', '--format', 'json', '-o', 'reports/RevG/Phase03B/raw/after/MicroSD_Carrier_erc.json', 'output/RevG/MicroSD_Carrier/MicroSD_Carrier.kicad_sch'],
    # Touch Sensor DRC & ERC
    [kicad_cli, 'pcb', 'drc', '--severity-all', '--schematic-parity', '--all-track-errors', '--refill-zones', '--format', 'report', '-o', 'reports/RevG/Phase03B/raw/after/Touch_Sensor_drc.rpt', 'output/RevG/Touch_Sensor/Touch_Sensor.kicad_pcb'],
    [kicad_cli, 'pcb', 'drc', '--severity-all', '--schematic-parity', '--all-track-errors', '--refill-zones', '--format', 'json', '-o', 'reports/RevG/Phase03B/raw/after/Touch_Sensor_drc.json', 'output/RevG/Touch_Sensor/Touch_Sensor.kicad_pcb'],
    [kicad_cli, 'sch', 'erc', '--severity-all', '--format', 'report', '-o', 'reports/RevG/Phase03B/raw/after/Touch_Sensor_erc.rpt', 'output/RevG/Touch_Sensor/Touch_Sensor.kicad_sch'],
    [kicad_cli, 'sch', 'erc', '--severity-all', '--format', 'json', '-o', 'reports/RevG/Phase03B/raw/after/Touch_Sensor_erc.json', 'output/RevG/Touch_Sensor/Touch_Sensor.kicad_sch'],
]

for cmd in commands:
    print("Running:", " ".join(cmd[:4]), "->", cmd[-2])
    res = subprocess.run(cmd, capture_output=True, text=True)
    print("  Exit code:", res.returncode)
