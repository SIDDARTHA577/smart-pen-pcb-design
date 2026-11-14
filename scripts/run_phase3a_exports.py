import subprocess
from pathlib import Path
import hashlib

KICAD_CLI = r"C:\Users\goran\AppData\Local\Programs\KiCad\10.0\bin\kicad-cli.exe"

def run_cmd(args):
    print("Running:", " ".join(args))
    res = subprocess.run(args, capture_output=True, text=True)
    if res.stdout: print(res.stdout)
    if res.stderr: print(res.stderr)
    return res.returncode

def main():
    raw_dir = Path("reports/RevG/Phase03A/raw")
    raw_dir.mkdir(parents=True, exist_ok=True)

    # 1. Main SmartPen
    run_cmd([KICAD_CLI, "sch", "erc", "--severity-all", "--units", "mm", "-o", str(raw_dir / "Main_SmartPen_erc.rpt"), "output/RevG/SmartPen.kicad_sch"])
    run_cmd([KICAD_CLI, "sch", "export", "netlist", "-o", str(raw_dir / "Main_SmartPen_netlist.net"), "output/RevG/SmartPen.kicad_sch"])

    # 2. Front MPU
    run_cmd([KICAD_CLI, "sch", "erc", "--severity-all", "--units", "mm", "-o", str(raw_dir / "Front_MPU_erc.rpt"), "output/RevG/Front_MPU/Front_MPU.kicad_sch"])
    run_cmd([KICAD_CLI, "sch", "export", "netlist", "-o", str(raw_dir / "Front_MPU_netlist.net"), "output/RevG/Front_MPU/Front_MPU.kicad_sch"])

    # 3. MicroSD Carrier
    run_cmd([KICAD_CLI, "sch", "erc", "--severity-all", "--units", "mm", "-o", str(raw_dir / "MicroSD_Carrier_erc.rpt"), "output/RevG/MicroSD_Carrier/MicroSD_Carrier.kicad_sch"])
    run_cmd([KICAD_CLI, "sch", "export", "netlist", "-o", str(raw_dir / "MicroSD_Carrier_netlist.net"), "output/RevG/MicroSD_Carrier/MicroSD_Carrier.kicad_sch"])

    # 4. Touch Sensor
    run_cmd([KICAD_CLI, "sch", "erc", "--severity-all", "--units", "mm", "-o", str(raw_dir / "Touch_Sensor_erc.rpt"), "output/RevG/Touch_Sensor/Touch_Sensor.kicad_sch"])
    run_cmd([KICAD_CLI, "sch", "export", "netlist", "-o", str(raw_dir / "Touch_Sensor_netlist.net"), "output/RevG/Touch_Sensor/Touch_Sensor.kicad_sch"])

    # 5. Main PCB DRC
    run_cmd([KICAD_CLI, "pcb", "drc", "--severity-all", "--schematic-parity", "--units", "mm", "--all-track-errors", "--refill-zones", "-o", str(raw_dir / "Main_SmartPen_drc.rpt"), "output/RevG/SmartPen.kicad_pcb"])

    # Also JSON format DRC
    run_cmd([KICAD_CLI, "pcb", "drc", "--severity-all", "--schematic-parity", "--units", "mm", "--all-track-errors", "--refill-zones", "--format", "json", "-o", str(raw_dir / "Main_SmartPen_drc.json"), "output/RevG/SmartPen.kicad_pcb"])

    print("\nAll exports and reports generated in reports/RevG/Phase03A/raw/")

if __name__ == '__main__':
    main()

