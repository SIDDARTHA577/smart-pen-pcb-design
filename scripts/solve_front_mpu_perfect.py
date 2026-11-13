"""Front MPU Perfect Clean Router.
Zero violations, zero unconnected items, zero parity errors.
"""
import subprocess
import re
import uuid
import json
from pathlib import Path

kicad_cli = r"C:\Users\goran\AppData\Local\Programs\KiCad\10.0\bin\kicad-cli.exe"
prj_dir = Path("output/RevF_Working/Front_MPU")
prj_dir.mkdir(parents=True, exist_ok=True)
fp_dir = prj_dir / "Front_MPU.pretty"
fp_dir.mkdir(parents=True, exist_ok=True)

# 1. Project file
pro = {
    "board": {
        "design_settings": {
            "defaults": {
                "board_thickness": 0.8,
                "copper_line_width": 0.20,
                "min_clearance": 0.127,
                "min_through_hole_diameter": 0.30,
                "min_track_width": 0.20,
                "min_via_diameter": 0.50
            },
            "rules": {
                "min_clearance": 0.127,
                "min_track_width": 0.20,
                "min_via_diameter": 0.50,
                "min_through_hole_diameter": 0.30,
                "hole_clearance": 0.20,
                "solder_mask_min_width": 0.0
            }
        }
    },
    "meta": {"filename": "Front_MPU.kicad_pro", "version": 1},
    "sheets": [["", ""]]
}
with open(prj_dir / "Front_MPU.kicad_pro", "w", encoding="utf-8") as f:
    json.dump(pro, f, indent=2)

dru_content = """(version 1)
(rule "Board Edge Clearance"
  (constraint edge_clearance (min 0.30mm))
  (condition "A.Type == '*'")
)
"""
with open(prj_dir / "Front_MPU.kicad_dru", "w", encoding="utf-8") as f:
    f.write(dru_content)

# Footprints
qfn_lines = [
    '(footprint "Front_MPU:QFN-24_4x4mm" (version 20221018) (generator pcbnew)',
    '  (layer "F.Cu")',
    '  (fp_text reference "REF**" (at 0 0) (layer "F.SilkS") hide (effects (font (size 0.8 0.8) (thickness 0.12))))',
    '  (fp_text value "MPU-6050" (at 0 0) (layer "F.Fab") hide (effects (font (size 0.8 0.8) (thickness 0.12))))',
    '  (pad "25" smd rect (at 0 0) (size 2.2 2.2) (layers "F.Cu" "F.Paste" "F.Mask"))',
    '  (pad "1" smd rect (at -1.90 -1.25) (size 0.65 0.25) (layers "F.Cu" "F.Paste" "F.Mask"))',
    '  (pad "2" smd rect (at -1.90 -0.75) (size 0.65 0.25) (layers "F.Cu" "F.Paste" "F.Mask"))',
    '  (pad "3" smd rect (at -1.90 -0.25) (size 0.65 0.25) (layers "F.Cu" "F.Paste" "F.Mask"))',
    '  (pad "4" smd rect (at -1.90 0.25) (size 0.65 0.25) (layers "F.Cu" "F.Paste" "F.Mask"))',
    '  (pad "5" smd rect (at -1.90 0.75) (size 0.65 0.25) (layers "F.Cu" "F.Paste" "F.Mask"))',
    '  (pad "6" smd rect (at -1.90 1.25) (size 0.65 0.25) (layers "F.Cu" "F.Paste" "F.Mask"))',
    '  (pad "7" smd rect (at -1.25 1.90) (size 0.25 0.65) (layers "F.Cu" "F.Paste" "F.Mask"))',
    '  (pad "8" smd rect (at -0.75 1.90) (size 0.25 0.65) (layers "F.Cu" "F.Paste" "F.Mask"))',
    '  (pad "9" smd rect (at -0.25 1.90) (size 0.25 0.65) (layers "F.Cu" "F.Paste" "F.Mask"))',
    '  (pad "10" smd rect (at 0.25 1.90) (size 0.25 0.65) (layers "F.Cu" "F.Paste" "F.Mask"))',
    '  (pad "11" smd rect (at 0.75 1.90) (size 0.25 0.65) (layers "F.Cu" "F.Paste" "F.Mask"))',
    '  (pad "12" smd rect (at 1.25 1.90) (size 0.25 0.65) (layers "F.Cu" "F.Paste" "F.Mask"))',
    '  (pad "13" smd rect (at 1.90 1.25) (size 0.65 0.25) (layers "F.Cu" "F.Paste" "F.Mask"))',
    '  (pad "14" smd rect (at 1.90 0.75) (size 0.65 0.25) (layers "F.Cu" "F.Paste" "F.Mask"))',
    '  (pad "15" smd rect (at 1.90 0.25) (size 0.65 0.25) (layers "F.Cu" "F.Paste" "F.Mask"))',
    '  (pad "16" smd rect (at 1.90 -0.25) (size 0.65 0.25) (layers "F.Cu" "F.Paste" "F.Mask"))',
    '  (pad "17" smd rect (at 1.90 -0.75) (size 0.65 0.25) (layers "F.Cu" "F.Paste" "F.Mask"))',
    '  (pad "18" smd rect (at 1.90 -1.25) (size 0.65 0.25) (layers "F.Cu" "F.Paste" "F.Mask"))',
    '  (pad "19" smd rect (at 1.25 -1.90) (size 0.25 0.65) (layers "F.Cu" "F.Paste" "F.Mask"))',
    '  (pad "20" smd rect (at 0.75 -1.90) (size 0.25 0.65) (layers "F.Cu" "F.Paste" "F.Mask"))',
    '  (pad "21" smd rect (at 0.25 -1.90) (size 0.25 0.65) (layers "F.Cu" "F.Paste" "F.Mask"))',
    '  (pad "22" smd rect (at -0.25 -1.90) (size 0.25 0.65) (layers "F.Cu" "F.Paste" "F.Mask"))',
    '  (pad "23" smd rect (at -0.75 -1.90) (size 0.25 0.65) (layers "F.Cu" "F.Paste" "F.Mask"))',
    '  (pad "24" smd rect (at -1.25 -1.90) (size 0.25 0.65) (layers "F.Cu" "F.Paste" "F.Mask"))',
    ')'
]
with open(fp_dir / "QFN-24_4x4mm.kicad_mod", "w", encoding="utf-8") as f:
    f.write('\n'.join(qfn_lines) + '\n')

jst4_lines = [
    '(footprint "Front_MPU:JST_SH_4P" (version 20221018) (generator pcbnew)',
    '  (layer "F.Cu")',
    '  (fp_text reference "REF**" (at 0 0) (layer "F.SilkS") hide (effects (font (size 0.8 0.8) (thickness 0.12))))',
    '  (fp_text value "JST_SH_4P" (at 0 0) (layer "F.Fab") hide (effects (font (size 0.8 0.8) (thickness 0.12))))',
    '  (pad "1" smd rect (at -1.5 0) (size 0.6 1.0) (layers "F.Cu" "F.Paste" "F.Mask"))',
    '  (pad "2" smd rect (at -0.5 0) (size 0.6 1.0) (layers "F.Cu" "F.Paste" "F.Mask"))',
    '  (pad "3" smd rect (at 0.5 0) (size 0.6 1.0) (layers "F.Cu" "F.Paste" "F.Mask"))',
    '  (pad "4" smd rect (at 1.5 0) (size 0.6 1.0) (layers "F.Cu" "F.Paste" "F.Mask"))',
    '  (pad "5" smd rect (at -2.5 0) (size 0.5 1.0) (layers "F.Cu" "F.Paste" "F.Mask"))',
    '  (pad "5" smd rect (at 2.5 0) (size 0.5 1.0) (layers "F.Cu" "F.Paste" "F.Mask"))',
    ')'
]
with open(fp_dir / "JST_SH_4P.kicad_mod", "w", encoding="utf-8") as f:
    f.write('\n'.join(jst4_lines) + '\n')

def make_pass_fp(name):
    return [
        f'(footprint "Front_MPU:{name}" (version 20221018) (generator pcbnew)',
        '  (layer "F.Cu")',
        '  (fp_text reference "REF**" (at 0 0) (layer "F.SilkS") hide (effects (font (size 0.8 0.8) (thickness 0.12))))',
        f'  (fp_text value "{name}" (at 0 0) (layer "F.Fab") hide (effects (font (size 0.8 0.8) (thickness 0.12))))',
        '  (pad "1" smd rect (at 0 -0.45) (size 0.5 0.5) (layers "F.Cu" "F.Paste" "F.Mask"))',
        '  (pad "2" smd rect (at 0 0.45) (size 0.5 0.5) (layers "F.Cu" "F.Paste" "F.Mask"))',
        ')'
    ]
with open(fp_dir / "C_0402.kicad_mod", "w", encoding="utf-8") as f:
    f.write('\n'.join(make_pass_fp("C_0402")) + '\n')
with open(fp_dir / "R_0402.kicad_mod", "w", encoding="utf-8") as f:
    f.write('\n'.join(make_pass_fp("R_0402")) + '\n')

# 3. PCB Layout with clean topology and exact schematic net parity
pcb = f"""(kicad_pcb (version 20221018) (generator pcbnew) (generator_version "8.0")
  (general (thickness 0.8))
  (paper "A4")
  (title_block (title "Front MPU Daughterboard") (rev "Rev F.1") (company "RadixView Technologies"))
  (layers
    (0 "F.Cu" signal)
    (31 "B.Cu" signal)
    (36 "B.SilkS" user "B.Silkscreen")
    (37 "F.SilkS" user "F.Silkscreen")
    (38 "B.Mask" user)
    (39 "F.Mask" user)
    (44 "Edge.Cuts" user)
    (48 "F.Fab" user)
    (49 "B.Fab" user)
  )
  (setup
    (pad_to_mask_clearance 0.0)
    (solder_mask_min_width 0.0)
    (pad_to_paste_clearance 0)
  )
  (net 0 "")
  (net 1 "/GND")
  (net 2 "/3V3")
  (net 3 "/I2C_SDA")
  (net 4 "/I2C_SCL")
  (net 5 "/REGOUT")
  (net 6 "/CPOUT")
  (net 7 "unconnected-(U1-INT-Pad12)")
  (net_class "Default" "Standard net class"
    (clearance 0.127)
    (trace_width 0.20)
    (via_dia 0.50)
    (via_drill 0.30)
  )
  (gr_line (start 0 0) (end 7.2 0) (layer "Edge.Cuts") (width 0.15))
  (gr_line (start 7.2 0) (end 7.2 10.0) (layer "Edge.Cuts") (width 0.15))
  (gr_line (start 7.2 10.0) (end 0 10.0) (layer "Edge.Cuts") (width 0.15))
  (gr_line (start 0 10.0) (end 0 0) (layer "Edge.Cuts") (width 0.15))

  (footprint "Front_MPU:JST_SH_4P" (layer "F.Cu") (at 3.6 1.4)
    (uuid "{uuid.uuid4()}")
    (fp_text reference "J1" (at 0 -0.8) (layer "F.SilkS") hide (effects (font (size 0.8 0.8) (thickness 0.12))))
    (fp_text value "SM04B-SRSS-TB" (at 0 0) (layer "F.Fab") hide (effects (font (size 0.8 0.8) (thickness 0.12))))
    (pad "1" smd rect (at -1.5 0) (size 0.6 1.0) (layers "F.Cu" "F.Paste" "F.Mask") (net 2 "/3V3"))
    (pad "2" smd rect (at -0.5 0) (size 0.6 1.0) (layers "F.Cu" "F.Paste" "F.Mask") (net 1 "/GND"))
    (pad "3" smd rect (at 0.5 0) (size 0.6 1.0) (layers "F.Cu" "F.Paste" "F.Mask") (net 3 "/I2C_SDA"))
    (pad "4" smd rect (at 1.5 0) (size 0.6 1.0) (layers "F.Cu" "F.Paste" "F.Mask") (net 4 "/I2C_SCL"))
    (pad "5" smd rect (at -2.5 0) (size 0.5 1.0) (layers "F.Cu" "F.Paste" "F.Mask") (net 1 "/GND"))
    (pad "5" smd rect (at 2.5 0) (size 0.5 1.0) (layers "F.Cu" "F.Paste" "F.Mask") (net 1 "/GND"))
  )

  (footprint "Front_MPU:QFN-24_4x4mm" (layer "F.Cu") (at 3.6 5.6)
    (uuid "{uuid.uuid4()}")
    (fp_text reference "U1" (at 0 0) (layer "F.SilkS") hide (effects (font (size 0.8 0.8) (thickness 0.12))))
    (fp_text value "MPU-6050" (at 0 0) (layer "F.Fab") hide (effects (font (size 0.8 0.8) (thickness 0.12))))
    (pad "25" smd rect (at 0 0) (size 2.2 2.2) (layers "F.Cu" "F.Paste" "F.Mask") (net 1 "/GND"))
    (pad "1" smd rect (at -1.90 -1.25) (size 0.65 0.25) (layers "F.Cu" "F.Paste" "F.Mask") (net 1 "/GND"))
    (pad "2" smd rect (at -1.90 -0.75) (size 0.65 0.25) (layers "F.Cu" "F.Paste" "F.Mask") (net 0 ""))
    (pad "3" smd rect (at -1.90 -0.25) (size 0.65 0.25) (layers "F.Cu" "F.Paste" "F.Mask") (net 0 ""))
    (pad "4" smd rect (at -1.90 0.25) (size 0.65 0.25) (layers "F.Cu" "F.Paste" "F.Mask") (net 0 ""))
    (pad "5" smd rect (at -1.90 0.75) (size 0.65 0.25) (layers "F.Cu" "F.Paste" "F.Mask") (net 0 ""))
    (pad "6" smd rect (at -1.90 1.25) (size 0.65 0.25) (layers "F.Cu" "F.Paste" "F.Mask") (net 0 ""))
    (pad "7" smd rect (at -1.25 1.90) (size 0.25 0.65) (layers "F.Cu" "F.Paste" "F.Mask") (net 0 ""))
    (pad "8" smd rect (at -0.75 1.90) (size 0.25 0.65) (layers "F.Cu" "F.Paste" "F.Mask") (net 2 "/3V3"))
    (pad "9" smd rect (at -0.25 1.90) (size 0.25 0.65) (layers "F.Cu" "F.Paste" "F.Mask") (net 1 "/GND"))
    (pad "10" smd rect (at 0.25 1.90) (size 0.25 0.65) (layers "F.Cu" "F.Paste" "F.Mask") (net 5 "/REGOUT"))
    (pad "11" smd rect (at 0.75 1.90) (size 0.25 0.65) (layers "F.Cu" "F.Paste" "F.Mask") (net 1 "/GND"))
    (pad "12" smd rect (at 1.25 1.90) (size 0.25 0.65) (layers "F.Cu" "F.Paste" "F.Mask") (net 7 "unconnected-(U1-INT-Pad12)"))
    (pad "13" smd rect (at 1.90 1.25) (size 0.65 0.25) (layers "F.Cu" "F.Paste" "F.Mask") (net 2 "/3V3"))
    (pad "14" smd rect (at 1.90 0.75) (size 0.65 0.25) (layers "F.Cu" "F.Paste" "F.Mask") (net 0 ""))
    (pad "15" smd rect (at 1.90 0.25) (size 0.65 0.25) (layers "F.Cu" "F.Paste" "F.Mask") (net 0 ""))
    (pad "16" smd rect (at 1.90 -0.25) (size 0.65 0.25) (layers "F.Cu" "F.Paste" "F.Mask") (net 0 ""))
    (pad "17" smd rect (at 1.90 -0.75) (size 0.65 0.25) (layers "F.Cu" "F.Paste" "F.Mask") (net 0 ""))
    (pad "18" smd rect (at 1.90 -1.25) (size 0.65 0.25) (layers "F.Cu" "F.Paste" "F.Mask") (net 1 "/GND"))
    (pad "19" smd rect (at 1.25 -1.90) (size 0.25 0.65) (layers "F.Cu" "F.Paste" "F.Mask") (net 0 ""))
    (pad "20" smd rect (at 0.75 -1.90) (size 0.25 0.65) (layers "F.Cu" "F.Paste" "F.Mask") (net 6 "/CPOUT"))
    (pad "21" smd rect (at 0.25 -1.90) (size 0.25 0.65) (layers "F.Cu" "F.Paste" "F.Mask") (net 0 ""))
    (pad "22" smd rect (at -0.25 -1.90) (size 0.25 0.65) (layers "F.Cu" "F.Paste" "F.Mask") (net 0 ""))
    (pad "23" smd rect (at -0.75 -1.90) (size 0.25 0.65) (layers "F.Cu" "F.Paste" "F.Mask") (net 4 "/I2C_SCL"))
    (pad "24" smd rect (at -1.25 -1.90) (size 0.25 0.65) (layers "F.Cu" "F.Paste" "F.Mask") (net 3 "/I2C_SDA"))
  )

  (footprint "Front_MPU:R_0402" (layer "F.Cu") (at 1.00 8.90)
    (uuid "{uuid.uuid4()}")
    (fp_text reference "R2" (at 0 0) (layer "F.SilkS") hide (effects (font (size 0.8 0.8) (thickness 0.12))))
    (fp_text value "4.7k" (at 0 0) (layer "F.Fab") hide (effects (font (size 0.8 0.8) (thickness 0.12))))
    (pad "1" smd rect (at 0 -0.45) (size 0.5 0.5) (layers "F.Cu" "F.Paste" "F.Mask") (net 2 "/3V3"))
    (pad "2" smd rect (at 0 0.45) (size 0.5 0.5) (layers "F.Cu" "F.Paste" "F.Mask") (net 3 "/I2C_SDA"))
  )

  (footprint "Front_MPU:R_0402" (layer "F.Cu") (at 1.90 8.90)
    (uuid "{uuid.uuid4()}")
    (fp_text reference "R1" (at 0 0) (layer "F.SilkS") hide (effects (font (size 0.8 0.8) (thickness 0.12))))
    (fp_text value "4.7k" (at 0 0) (layer "F.Fab") hide (effects (font (size 0.8 0.8) (thickness 0.12))))
    (pad "1" smd rect (at 0 -0.45) (size 0.5 0.5) (layers "F.Cu" "F.Paste" "F.Mask") (net 2 "/3V3"))
    (pad "2" smd rect (at 0 0.45) (size 0.5 0.5) (layers "F.Cu" "F.Paste" "F.Mask") (net 4 "/I2C_SCL"))
  )

  (footprint "Front_MPU:C_0402" (layer "F.Cu") (at 2.80 8.90)
    (uuid "{uuid.uuid4()}")
    (fp_text reference "C2" (at 0 0) (layer "F.SilkS") hide (effects (font (size 0.8 0.8) (thickness 0.12))))
    (fp_text value "0.1uF" (at 0 0) (layer "F.Fab") hide (effects (font (size 0.8 0.8) (thickness 0.12))))
    (pad "1" smd rect (at 0 -0.45) (size 0.5 0.5) (layers "F.Cu" "F.Paste" "F.Mask") (net 2 "/3V3"))
    (pad "2" smd rect (at 0 0.45) (size 0.5 0.5) (layers "F.Cu" "F.Paste" "F.Mask") (net 1 "/GND"))
  )

  (footprint "Front_MPU:C_0402" (layer "F.Cu") (at 3.75 8.90)
    (uuid "{uuid.uuid4()}")
    (fp_text reference "C4" (at 0 0) (layer "F.SilkS") hide (effects (font (size 0.8 0.8) (thickness 0.12))))
    (fp_text value "0.1uF" (at 0 0) (layer "F.Fab") hide (effects (font (size 0.8 0.8) (thickness 0.12))))
    (pad "1" smd rect (at 0 -0.45) (size 0.5 0.5) (layers "F.Cu" "F.Paste" "F.Mask") (net 5 "/REGOUT"))
    (pad "2" smd rect (at 0 0.45) (size 0.5 0.5) (layers "F.Cu" "F.Paste" "F.Mask") (net 1 "/GND"))
  )

  (footprint "Front_MPU:C_0402" (layer "F.Cu") (at 5.25 8.90)
    (uuid "{uuid.uuid4()}")
    (fp_text reference "C1" (at 0 0) (layer "F.SilkS") hide (effects (font (size 0.8 0.8) (thickness 0.12))))
    (fp_text value "0.1uF" (at 0 0) (layer "F.Fab") hide (effects (font (size 0.8 0.8) (thickness 0.12))))
    (pad "1" smd rect (at 0 -0.45) (size 0.5 0.5) (layers "F.Cu" "F.Paste" "F.Mask") (net 2 "/3V3"))
    (pad "2" smd rect (at 0 0.45) (size 0.5 0.5) (layers "F.Cu" "F.Paste" "F.Mask") (net 1 "/GND"))
  )

  (footprint "Front_MPU:C_0402" (layer "F.Cu") (at 6.20 8.90)
    (uuid "{uuid.uuid4()}")
    (fp_text reference "C3" (at 0 0) (layer "F.SilkS") hide (effects (font (size 0.8 0.8) (thickness 0.12))))
    (fp_text value "2.2nF" (at 0 0) (layer "F.Fab") hide (effects (font (size 0.8 0.8) (thickness 0.12))))
    (pad "1" smd rect (at 0 -0.45) (size 0.5 0.5) (layers "F.Cu" "F.Paste" "F.Mask") (net 6 "/CPOUT"))
    (pad "2" smd rect (at 0 0.45) (size 0.5 0.5) (layers "F.Cu" "F.Paste" "F.Mask") (net 1 "/GND"))
  )

  ;; ==========================================
  ;; TRACES & VIAS
  ;; ==========================================

  ;; --- Net 1: /GND ---
  ;; J1.2 at (3.10, 1.40) to via at (3.10, 0.65) on F.Cu
  (segment (start 3.10 1.40) (end 3.10 0.65) (width 0.20) (layer "F.Cu") (net 1))
  (via (at 3.10 0.65) (size 0.50) (drill 0.30) (layers "F.Cu" "B.Cu") (net 1))
  ;; Shields (1.10, 1.40) and (6.10, 1.40) to vias at Y=0.65
  (segment (start 1.10 1.40) (end 1.10 0.65) (width 0.20) (layer "F.Cu") (net 1))
  (via (at 1.10 0.65) (size 0.50) (drill 0.30) (layers "F.Cu" "B.Cu") (net 1))
  (segment (start 6.10 1.40) (end 6.10 0.65) (width 0.20) (layer "F.Cu") (net 1))
  (via (at 6.10 0.65) (size 0.50) (drill 0.30) (layers "F.Cu" "B.Cu") (net 1))

  ;; Connect J1 GND on B.Cu along Y = 0.65
  (segment (start 1.10 0.65) (end 3.10 0.65) (width 0.20) (layer "B.Cu") (net 1))
  (segment (start 3.10 0.65) (end 6.10 0.65) (width 0.20) (layer "B.Cu") (net 1))
  ;; Route on B.Cu at X = 3.60 to U1.EP (3.60, 5.60)
  (segment (start 3.10 0.65) (end 3.60 0.65) (width 0.20) (layer "B.Cu") (net 1))
  (segment (start 3.60 0.65) (end 3.60 5.60) (width 0.20) (layer "B.Cu") (net 1))
  (via (at 3.60 5.60) (size 0.50) (drill 0.30) (layers "F.Cu" "B.Cu") (net 1))

  ;; U1 ground pins to EP center (3.60, 5.60) on F.Cu:
  ;; U1.1 (1.70, 4.35) -> (3.60, 4.35) -> (3.60, 5.60)
  (segment (start 1.70 4.35) (end 3.60 4.35) (width 0.20) (layer "F.Cu") (net 1))
  (segment (start 3.60 4.35) (end 3.60 5.60) (width 0.20) (layer "F.Cu") (net 1))
  ;; U1.18 (5.50, 4.35) -> (3.60, 4.35)
  (segment (start 5.50 4.35) (end 3.60 4.35) (width 0.20) (layer "F.Cu") (net 1))
  ;; U1.9 (3.35, 7.50) -> (3.35, 5.60) -> (3.60, 5.60)
  (segment (start 3.35 7.50) (end 3.35 5.60) (width 0.20) (layer "F.Cu") (net 1))
  (segment (start 3.35 5.60) (end 3.60 5.60) (width 0.20) (layer "F.Cu") (net 1))
  ;; U1.11 (4.35, 7.50) -> (4.35, 5.60) -> (3.60, 5.60)
  (segment (start 4.35 7.50) (end 4.35 5.60) (width 0.20) (layer "F.Cu") (net 1))
  (segment (start 4.35 5.60) (end 3.60 5.60) (width 0.20) (layer "F.Cu") (net 1))

  ;; Connect U1.11 (4.35, 7.50) straight down on F.Cu to passives GND bus at (4.35, 9.35)
  (segment (start 4.35 7.50) (end 4.35 9.35) (width 0.20) (layer "F.Cu") (net 1))

  ;; Bottom GND bus on F.Cu: connects C2.2 (2.80), C4.2 (3.75), (4.35), C1.2 (5.25), C3.2 (6.20)
  (segment (start 2.80 9.35) (end 6.20 9.35) (width 0.20) (layer "F.Cu") (net 1))

  ;; --- Net 5: /REGOUT ---
  ;; U1.10 (3.85, 7.50) to C4.1 (3.75, 8.45) on F.Cu
  (segment (start 3.85 7.50) (end 3.75 7.80) (width 0.20) (layer "F.Cu") (net 5))
  (segment (start 3.75 7.80) (end 3.75 8.45) (width 0.20) (layer "F.Cu") (net 5))

  ;; --- Net 6: /CPOUT ---
  ;; U1.20 (4.35, 3.70) to C3.1 (6.20, 8.45) on B.Cu
  ;; Drop via at (4.35, 3.15) to B.Cu
  (segment (start 4.35 3.70) (end 4.35 3.15) (width 0.20) (layer "F.Cu") (net 6))
  (via (at 4.35 3.15) (size 0.50) (drill 0.30) (layers "F.Cu" "B.Cu") (net 6))
  (segment (start 4.35 3.15) (end 6.20 3.15) (width 0.20) (layer "B.Cu") (net 6))
  (segment (start 6.20 3.15) (end 6.20 8.45) (width 0.20) (layer "B.Cu") (net 6))
  (via (at 6.20 8.45) (size 0.50) (drill 0.30) (layers "F.Cu" "B.Cu") (net 6))

  ;; --- Net 3: /I2C_SDA ---
  ;; J1.3 at (4.10, 1.40) to U1.24 at (2.35, 3.70) on F.Cu at Y = 2.30
  (segment (start 4.10 1.40) (end 4.10 2.30) (width 0.20) (layer "F.Cu") (net 3))
  (segment (start 4.10 2.30) (end 2.35 2.30) (width 0.20) (layer "F.Cu") (net 3))
  (segment (start 2.35 2.30) (end 2.35 3.70) (width 0.20) (layer "F.Cu") (net 3))
  ;; Via to B.Cu in open space at (1.20, 3.00) to route down to R2.2 (1.00, 9.35)
  (segment (start 2.35 3.00) (end 1.20 3.00) (width 0.20) (layer "F.Cu") (net 3))
  (via (at 1.20 3.00) (size 0.50) (drill 0.30) (layers "F.Cu" "B.Cu") (net 3))
  (segment (start 1.20 3.00) (end 1.00 3.20) (width 0.20) (layer "B.Cu") (net 3))
  (segment (start 1.00 3.20) (end 1.00 9.35) (width 0.20) (layer "B.Cu") (net 3))
  (via (at 1.00 9.35) (size 0.50) (drill 0.30) (layers "F.Cu" "B.Cu") (net 3))

  ;; --- Net 4: /I2C_SCL ---
  ;; J1.4 at (5.10, 1.40) to U1.23 at (2.85, 3.70) on F.Cu at Y = 2.65
  (segment (start 5.10 1.40) (end 5.10 2.65) (width 0.20) (layer "F.Cu") (net 4))
  (segment (start 5.10 2.65) (end 2.85 2.65) (width 0.20) (layer "F.Cu") (net 4))
  (segment (start 2.85 2.65) (end 2.85 3.70) (width 0.20) (layer "F.Cu") (net 4))
  ;; Via to B.Cu directly at (2.85, 2.80) - same net as U1.23!
  (via (at 2.85 2.80) (size 0.50) (drill 0.30) (layers "F.Cu" "B.Cu") (net 4))
  (segment (start 2.85 2.80) (end 1.90 2.80) (width 0.20) (layer "B.Cu") (net 4))
  (segment (start 1.90 2.80) (end 1.90 9.35) (width 0.20) (layer "B.Cu") (net 4))
  (via (at 1.90 9.35) (size 0.50) (drill 0.30) (layers "F.Cu" "B.Cu") (net 4))

  ;; --- Net 2: /3V3 ---
  ;; J1.1 at (2.10, 1.40). Shift left immediately to X=1.65 (clear of SDA at 2.35 and shield at 1.10), down to Y=2.15, then to X=0.55
  (segment (start 2.10 1.40) (end 1.65 1.70) (width 0.20) (layer "F.Cu") (net 2))
  (segment (start 1.65 1.70) (end 1.65 2.15) (width 0.20) (layer "F.Cu") (net 2))
  (segment (start 1.65 2.15) (end 0.55 2.15) (width 0.20) (layer "F.Cu") (net 2))
  (segment (start 0.55 2.15) (end 0.55 8.45) (width 0.20) (layer "F.Cu") (net 2))

  ;; 3V3 bus on F.Cu at Y = 8.45: (0.55, 8.45) -> R2.1 (1.00) -> R1.1 (1.90) -> C2.1 (2.80)
  (segment (start 0.55 8.45) (end 1.00 8.45) (width 0.20) (layer "F.Cu") (net 2))
  (segment (start 1.00 8.45) (end 1.90 8.45) (width 0.20) (layer "F.Cu") (net 2))
  (segment (start 1.90 8.45) (end 2.80 8.45) (width 0.20) (layer "F.Cu") (net 2))
  ;; C2.1 (2.80, 8.45) to U1.8 (2.85, 7.50) on F.Cu
  (segment (start 2.80 8.45) (end 2.85 8.20) (width 0.20) (layer "F.Cu") (net 2))
  (segment (start 2.85 8.20) (end 2.85 7.50) (width 0.20) (layer "F.Cu") (net 2))

  ;; Route 3V3 across to C1.1 (5.25, 8.45) and U1.13 (5.50, 6.85) via B.Cu bridge at Y = 8.25:
  (segment (start 2.80 8.45) (end 2.80 8.25) (width 0.20) (layer "F.Cu") (net 2))
  (via (at 2.80 8.25) (size 0.50) (drill 0.30) (layers "F.Cu" "B.Cu") (net 2))
  (segment (start 2.80 8.25) (end 5.25 8.25) (width 0.20) (layer "B.Cu") (net 2))
  (via (at 5.25 8.25) (size 0.50) (drill 0.30) (layers "F.Cu" "B.Cu") (net 2))
  (segment (start 5.25 8.25) (end 5.25 8.45) (width 0.20) (layer "F.Cu") (net 2))
  ;; C1.1 (5.25, 8.45) to U1.13 (5.50, 6.85) on F.Cu
  (segment (start 5.25 8.45) (end 5.50 8.20) (width 0.20) (layer "F.Cu") (net 2))
  (segment (start 5.50 8.20) (end 5.50 6.85) (width 0.20) (layer "F.Cu") (net 2))
)"""

lines = [l for l in pcb.splitlines() if not l.strip().startswith(';')]
clean_pcb = '\n'.join(lines) + '\n'

with open(prj_dir / "Front_MPU.kicad_pcb", "w", encoding="utf-8") as f:
    f.write(clean_pcb)

print("Front_MPU.kicad_pcb written.")

rpt = prj_dir / "drc_perfect.rpt"
res = subprocess.run([
    kicad_cli, "pcb", "drc",
    "--severity-all",
    "--schematic-parity",
    "--exit-code-violations",
    "-o", str(rpt),
    str(prj_dir / "Front_MPU.kicad_pcb")
], capture_output=True, text=True)

print(f"DRC Exit Code: {res.returncode}")
print("STDOUT:", res.stdout)
if rpt.exists():
    with open(rpt) as f:
        content = f.read()
    violations = re.findall(r'\[(.*?)\]: (.*)', content)
    print(f"Total violations found: {len(violations)}")
    for v in violations:
        print(f"  {v[0]}: {v[1]}")
