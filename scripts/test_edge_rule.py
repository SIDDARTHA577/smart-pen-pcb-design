import subprocess
from pathlib import Path

kicad_cli = r"C:\Users\goran\AppData\Local\Programs\KiCad\10.0\bin\kicad-cli.exe"

test_pcb = """(kicad_pcb (version 20221018) (generator pcbnew) (generator_version "8.0")
  (general (thickness 0.8))
  (paper "A4")
  (layers (0 "F.Cu" signal) (31 "B.Cu" signal) (44 "Edge.Cuts" user))
  (setup (pad_to_mask_clearance 0.0))
  (net 0 "")
  (net 1 "GND")
  (gr_line (start 0 0) (end 10 0) (layer "Edge.Cuts") (width 0.15))
  (gr_line (start 10 0) (end 10 10) (layer "Edge.Cuts") (width 0.15))
  (gr_line (start 10 10) (end 0 10) (layer "Edge.Cuts") (width 0.15))
  (gr_line (start 0 10) (end 0 0) (layer "Edge.Cuts") (width 0.15))
  (via (at 0.40 5.0) (size 0.50) (drill 0.30) (layers "F.Cu" "B.Cu") (net 1))
)"""

p = Path("output/test_edge.kicad_pcb")
p.write_text(test_pcb)

res = subprocess.run([kicad_cli, "pcb", "drc", "--severity-all", str(p)], capture_output=True, text=True)
print("Default DRC:\n", res.stdout)

