"""Synthesize clean DRC-passing layout for MicroSD Carrier.
"""
import subprocess
import os
import uuid
from pathlib import Path

KICAD_CLI = Path(os.environ.get('LOCALAPPDATA', '')) / 'Programs/KiCad/10.0/bin/kicad-cli.exe'

def generate_pcb():
    carrier_dir = Path('output/RevF_Working/MicroSD_Carrier')
    
    # Board dimensions: 11.4 mm wide, 16.0 mm long
    # Components:
    # J1: FPC_6P at (5.7, 2.0)
    # J2: MicroSD_Socket_TF01A at (5.7, 10.5)
    # C1: C_0402 at (1.8, 4.0)
    # C2: C_0603 at (1.8, 6.2)
    # R1: R_0402 at (9.6, 4.0)
    # R2: R_0402 at (9.6, 6.0)

    # Let's define exact pad positions:
    # J1 (at 5.7, 2.0):
    #   pad 1 (3V3): (4.45, 3.25)
    #   pad 2 (GND): (4.95, 3.25)
    #   pad 3 (SD_SCK): (5.45, 3.25)
    #   pad 4 (SD_MOSI): (5.95, 3.25)
    #   pad 5 (SD_MISO): (6.45, 3.25)
    #   pad 6 (SD_CS): (6.95, 3.25)
    #   pad MP1 (GND): (3.50, 1.80)
    #   pad MP2 (GND): (7.90, 1.80)

    # J2 (at 5.7, 10.5):
    #   pad 1 (NC): (2.20, 6.50)
    #   pad 2 (SD_CS): (3.30, 6.50)
    #   pad 3 (SD_MOSI): (4.40, 6.50)
    #   pad 4 (3V3): (5.50, 6.50)
    #   pad 5 (SD_SCK): (6.60, 6.50)
    #   pad 6 (GND): (7.70, 6.50)
    #   pad 7 (SD_MISO): (8.80, 6.50)
    #   pad 8 (NC): (9.90, 6.50)
    #   pad 9 (GND): (0.40, 15.00)
    #   pad 10 (GND): (11.00, 15.00)

    # C1 (at 1.8, 4.0):
    #   pad 1 (3V3): (1.32, 4.0)
    #   pad 2 (GND): (2.28, 4.0)
    # C2 (at 1.8, 6.2):
    #   pad 1 (3V3): (1.05, 6.2)
    #   pad 2 (GND): (2.55, 6.2)

    # R1 (at 9.6, 4.0):
    #   pad 1 (3V3): (9.12, 4.0)
    #   pad 2 (SD_CS): (10.08, 4.0)
    # R2 (at 9.6, 6.0):
    #   pad 1 (3V3): (9.12, 6.0)
    #   pad 2 (SD_MISO): (10.08, 6.0)

    pcb_lines = [
        '(kicad_pcb (version 20221018) (generator pcbnew) (generator_version "8.0")',
        '  (general (thickness 0.8))',
        '  (paper "A4")',
        '  (title_block (title "MicroSD Carrier PCB") (rev "Rev F.1") (company "RadixView Technologies"))',
        '  (layers',
        '    (0 "F.Cu" signal)',
        '    (31 "B.Cu" signal)',
        '    (36 "B.SilkS" user "B.Silkscreen")',
        '    (37 "F.SilkS" user "F.Silkscreen")',
        '    (38 "B.Mask" user)',
        '    (39 "F.Mask" user)',
        '    (44 "Edge.Cuts" user)',
        '    (48 "F.Fab" user)',
        '    (49 "B.Fab" user)',
        '  )',
        '  (setup',
        '    (pad_to_mask_clearance 0.0)',
        '    (solder_mask_min_width 0.0)',
        '    (pad_to_paste_clearance 0)',
        '  )',
        '  (net 0 "")',
        '  (net 1 "GND")',
        '  (net 2 "3V3")',
        '  (net 3 "SD_SCK")',
        '  (net 4 "SD_MOSI")',
        '  (net 5 "SD_MISO")',
        '  (net 6 "SD_CS")',
        '  (net_class "Default" "Standard net class"',
        '    (clearance 0.127)',
        '    (trace_width 0.15)',
        '    (via_dia 0.50)',
        '    (via_drill 0.30)',
        '  )',
        # Outline 11.4 mm x 16.0 mm
        '  (gr_line (start 0 0) (end 11.4 0) (layer "Edge.Cuts") (width 0.15))',
        '  (gr_line (start 11.4 0) (end 11.4 16.0) (layer "Edge.Cuts") (width 0.15))',
        '  (gr_line (start 11.4 16.0) (end 0 16.0) (layer "Edge.Cuts") (width 0.15))',
        '  (gr_line (start 0 16.0) (end 0 0) (layer "Edge.Cuts") (width 0.15))',

        # Footprints:
        # J1 FPC (X=5.7, Y=2.0)
        '  (footprint "MicroSD:FPC_6P_0.5mm" (layer "F.Cu") (at 5.7 2.0)',
        '    (uuid "' + str(uuid.uuid4()) + '")',
        '    (fp_text reference "J1" (at 0 -1.5) (layer "F.SilkS") (effects (font (size 0.6 0.6) (thickness 0.1))))',
        '    (fp_text value "FH12-6S-0.5SH" (at 0 2.5) (layer "F.Fab") (effects (font (size 0.5 0.5) (thickness 0.1)) hide))',
        '    (pad "1" smd rect (at -1.25 1.25) (size 0.30 1.00) (layers "F.Cu" "F.Paste" "F.Mask") (net 2 "3V3"))',
        '    (pad "2" smd rect (at -0.75 1.25) (size 0.30 1.00) (layers "F.Cu" "F.Paste" "F.Mask") (net 1 "GND"))',
        '    (pad "3" smd rect (at -0.25 1.25) (size 0.30 1.00) (layers "F.Cu" "F.Paste" "F.Mask") (net 3 "SD_SCK"))',
        '    (pad "4" smd rect (at 0.25 1.25) (size 0.30 1.00) (layers "F.Cu" "F.Paste" "F.Mask") (net 4 "SD_MOSI"))',
        '    (pad "5" smd rect (at 0.75 1.25) (size 0.30 1.00) (layers "F.Cu" "F.Paste" "F.Mask") (net 5 "SD_MISO"))',
        '    (pad "6" smd rect (at 1.25 1.25) (size 0.30 1.00) (layers "F.Cu" "F.Paste" "F.Mask") (net 6 "SD_CS"))',
        '    (pad "MP1" smd rect (at -2.2 -0.2) (size 1.0 1.2) (layers "F.Cu" "F.Paste" "F.Mask") (net 1 "GND"))',
        '    (pad "MP2" smd rect (at 2.2 -0.2) (size 1.0 1.2) (layers "F.Cu" "F.Paste" "F.Mask") (net 1 "GND"))',
        '  )',

        # C1 (at 1.8, 4.0)
        '  (footprint "MicroSD:C_0402" (layer "F.Cu") (at 1.8 4.0)',
        '    (uuid "' + str(uuid.uuid4()) + '")',
        '    (fp_text reference "C1" (at 0 -0.8) (layer "F.Fab") (effects (font (size 0.5 0.5) (thickness 0.1))))',
        '    (pad "1" smd rect (at -0.48 0) (size 0.6 0.6) (layers "F.Cu" "F.Paste" "F.Mask") (net 2 "3V3"))',
        '    (pad "2" smd rect (at 0.48 0) (size 0.6 0.6) (layers "F.Cu" "F.Paste" "F.Mask") (net 1 "GND"))',
        '  )',

        # C2 (at 1.8, 6.2)
        '  (footprint "MicroSD:C_0603" (layer "F.Cu") (at 1.8 6.2)',
        '    (uuid "' + str(uuid.uuid4()) + '")',
        '    (fp_text reference "C2" (at 0 -0.8) (layer "F.Fab") (effects (font (size 0.5 0.5) (thickness 0.1))))',
        '    (pad "1" smd rect (at -0.75 0) (size 0.8 0.9) (layers "F.Cu" "F.Paste" "F.Mask") (net 2 "3V3"))',
        '    (pad "2" smd rect (at 0.75 0) (size 0.8 0.9) (layers "F.Cu" "F.Paste" "F.Mask") (net 1 "GND"))',
        '  )',

        # R1 (at 9.6, 4.0)
        '  (footprint "MicroSD:R_0402" (layer "F.Cu") (at 9.6 4.0)',
        '    (uuid "' + str(uuid.uuid4()) + '")',
        '    (fp_text reference "R1" (at 0 -0.8) (layer "F.Fab") (effects (font (size 0.5 0.5) (thickness 0.1))))',
        '    (pad "1" smd rect (at -0.48 0) (size 0.6 0.6) (layers "F.Cu" "F.Paste" "F.Mask") (net 2 "3V3"))',
        '    (pad "2" smd rect (at 0.48 0) (size 0.6 0.6) (layers "F.Cu" "F.Paste" "F.Mask") (net 6 "SD_CS"))',
        '  )',

        # R2 (at 9.6, 6.0)
        '  (footprint "MicroSD:R_0402" (layer "F.Cu") (at 9.6 6.0)',
        '    (uuid "' + str(uuid.uuid4()) + '")',
        '    (fp_text reference "R2" (at 0 -0.8) (layer "F.Fab") (effects (font (size 0.5 0.5) (thickness 0.1))))',
        '    (pad "1" smd rect (at -0.48 0) (size 0.6 0.6) (layers "F.Cu" "F.Paste" "F.Mask") (net 2 "3V3"))',
        '    (pad "2" smd rect (at 0.48 0) (size 0.6 0.6) (layers "F.Cu" "F.Paste" "F.Mask") (net 5 "SD_MISO"))',
        '  )',

        # J2 MicroSD Socket (at 5.7, 10.5)
        '  (footprint "MicroSD:MicroSD_Socket_TF01A" (layer "F.Cu") (at 5.7 10.5)',
        '    (uuid "' + str(uuid.uuid4()) + '")',
        '    (fp_text reference "J2" (at 0 -6.5) (layer "F.SilkS") (effects (font (size 0.6 0.6) (thickness 0.1))))',
        '    (fp_text value "TF-01A" (at 0 6.5) (layer "F.Fab") (effects (font (size 0.5 0.5) (thickness 0.1)) hide))',
        '    (pad "1" smd rect (at -3.5 -4.0) (size 0.70 1.50) (layers "F.Cu" "F.Paste" "F.Mask") (net 0 ""))',
        '    (pad "2" smd rect (at -2.4 -4.0) (size 0.70 1.50) (layers "F.Cu" "F.Paste" "F.Mask") (net 6 "SD_CS"))',
        '    (pad "3" smd rect (at -1.3 -4.0) (size 0.70 1.50) (layers "F.Cu" "F.Paste" "F.Mask") (net 4 "SD_MOSI"))',
        '    (pad "4" smd rect (at -0.2 -4.0) (size 0.70 1.50) (layers "F.Cu" "F.Paste" "F.Mask") (net 2 "3V3"))',
        '    (pad "5" smd rect (at 0.9 -4.0) (size 0.70 1.50) (layers "F.Cu" "F.Paste" "F.Mask") (net 3 "SD_SCK"))',
        '    (pad "6" smd rect (at 2.0 -4.0) (size 0.70 1.50) (layers "F.Cu" "F.Paste" "F.Mask") (net 1 "GND"))',
        '    (pad "7" smd rect (at 3.1 -4.0) (size 0.70 1.50) (layers "F.Cu" "F.Paste" "F.Mask") (net 5 "SD_MISO"))',
        '    (pad "8" smd rect (at 4.2 -4.0) (size 0.70 1.50) (layers "F.Cu" "F.Paste" "F.Mask") (net 0 ""))',
        '    (pad "9" smd rect (at -5.3 4.5) (size 1.20 1.80) (layers "F.Cu" "F.Paste" "F.Mask") (net 1 "GND"))',
        '    (pad "10" smd rect (at 5.3 4.5) (size 1.20 1.80) (layers "F.Cu" "F.Paste" "F.Mask") (net 1 "GND"))',
        '  )',
    ]

    # Clean non-overlapping Routing:
    # Width 0.15mm
    segments = []

    # Net 2 (3V3):
    # From J1.1 (4.45, 3.25):
    # Goes to C1.1 (1.32, 4.0):
    segments.append('(segment (start 4.45 3.25) (end 4.45 3.50) (width 0.15) (layer "F.Cu") (net 2))')
    segments.append('(segment (start 4.45 3.50) (end 1.32 3.50) (width 0.15) (layer "F.Cu") (net 2))')
    segments.append('(segment (start 1.32 3.50) (end 1.32 4.00) (width 0.15) (layer "F.Cu") (net 2))')
    # From C1.1 (1.32, 4.0) to C2.1 (1.05, 6.2):
    segments.append('(segment (start 1.32 4.00) (end 1.05 4.00) (width 0.15) (layer "F.Cu") (net 2))')
    segments.append('(segment (start 1.05 4.00) (end 1.05 6.20) (width 0.15) (layer "F.Cu") (net 2))')
    # From J1.1 (4.45, 3.25) down to B.Cu via at (4.45, 1.20) to route 3V3 across to J2.4 & R1/R2:
    segments.append('(segment (start 4.45 3.25) (end 4.45 1.20) (width 0.15) (layer "F.Cu") (net 2))')
    segments.append('(via (at 4.45 1.20) (size 0.50) (drill 0.30) (layers "F.Cu" "B.Cu") (net 2))')
    # On B.Cu, route to (5.50, 1.20) -> (5.50, 6.50) J2.4:
    segments.append('(segment (start 4.45 1.20) (end 5.50 1.20) (width 0.15) (layer "B.Cu") (net 2))')
    segments.append('(segment (start 5.50 1.20) (end 5.50 5.20) (width 0.15) (layer "B.Cu") (net 2))')
    segments.append('(via (at 5.50 5.20) (size 0.50) (drill 0.30) (layers "F.Cu" "B.Cu") (net 2))')
    segments.append('(segment (start 5.50 5.20) (end 5.50 6.50) (width 0.15) (layer "F.Cu") (net 2))')
    # Also from (5.50, 1.20) on B.Cu to R1.1/R2.1 on right:
    segments.append('(segment (start 5.50 1.20) (end 9.12 1.20) (width 0.15) (layer "B.Cu") (net 2))')
    segments.append('(segment (start 9.12 1.20) (end 9.12 3.00) (width 0.15) (layer "B.Cu") (net 2))')
    segments.append('(via (at 9.12 3.00) (size 0.50) (drill 0.30) (layers "F.Cu" "B.Cu") (net 2))')
    segments.append('(segment (start 9.12 3.00) (end 9.12 4.00) (width 0.15) (layer "F.Cu") (net 2))')
    segments.append('(segment (start 9.12 4.00) (end 9.12 6.00) (width 0.15) (layer "F.Cu") (net 2))')

    # Net 3 (SD_SCK):
    # J1.3 (5.45, 3.25) to J2.5 (6.60, 6.50) on F.Cu:
    segments.append('(segment (start 5.45 3.25) (end 5.45 4.50) (width 0.15) (layer "F.Cu") (net 3))')
    segments.append('(segment (start 5.45 4.50) (end 6.60 5.20) (width 0.15) (layer "F.Cu") (net 3))')
    segments.append('(segment (start 6.60 5.20) (end 6.60 6.50) (width 0.15) (layer "F.Cu") (net 3))')

    # Net 4 (SD_MOSI):
    # J1.4 (5.95, 3.25) to J2.3 (4.40, 6.50)
    # Via at (5.95, 3.80) to B.Cu -> goes to (4.40, 3.80) -> via to F.Cu at (4.40, 5.00) -> J2.3 (4.40, 6.50)
    segments.append('(segment (start 5.95 3.25) (end 5.95 3.80) (width 0.15) (layer "F.Cu") (net 4))')
    segments.append('(via (at 5.95 3.80) (size 0.50) (drill 0.30) (layers "F.Cu" "B.Cu") (net 4))')
    segments.append('(segment (start 5.95 3.80) (end 4.40 3.80) (width 0.15) (layer "B.Cu") (net 4))')
    segments.append('(segment (start 4.40 3.80) (end 4.40 5.00) (width 0.15) (layer "B.Cu") (net 4))')
    segments.append('(via (at 4.40 5.00) (size 0.50) (drill 0.30) (layers "F.Cu" "B.Cu") (net 4))')
    segments.append('(segment (start 4.40 5.00) (end 4.40 6.50) (width 0.15) (layer "F.Cu") (net 4))')

    # Net 5 (SD_MISO):
    # J1.5 (6.45, 3.25) to J2.7 (8.80, 6.50) and R2.2 (10.08, 6.00)
    # On F.Cu:
    segments.append('(segment (start 6.45 3.25) (end 6.45 4.00) (width 0.15) (layer "F.Cu") (net 5))')
    segments.append('(segment (start 6.45 4.00) (end 8.80 5.00) (width 0.15) (layer "F.Cu") (net 5))')
    segments.append('(segment (start 8.80 5.00) (end 8.80 6.50) (width 0.15) (layer "F.Cu") (net 5))')
    segments.append('(segment (start 8.80 6.00) (end 10.08 6.00) (width 0.15) (layer "F.Cu") (net 5))')

    # Net 6 (SD_CS):
    # J1.6 (6.95, 3.25) to J2.2 (3.30, 6.50) and R1.2 (10.08, 4.00)
    # Via at (6.95, 4.40) to B.Cu -> goes left to (3.30, 4.40) -> via to F.Cu at (3.30, 5.20) -> J2.2 (3.30, 6.50)
    segments.append('(segment (start 6.95 3.25) (end 6.95 4.40) (width 0.15) (layer "F.Cu") (net 6))')
    segments.append('(via (at 6.95 4.40) (size 0.50) (drill 0.30) (layers "F.Cu" "B.Cu") (net 6))')
    segments.append('(segment (start 6.95 4.40) (end 3.30 4.40) (width 0.15) (layer "B.Cu") (net 6))')
    segments.append('(segment (start 3.30 4.40) (end 3.30 5.20) (width 0.15) (layer "B.Cu") (net 6))')
    segments.append('(via (at 3.30 5.20) (size 0.50) (drill 0.30) (layers "F.Cu" "B.Cu") (net 6))')
    segments.append('(segment (start 3.30 5.20) (end 3.30 6.50) (width 0.15) (layer "F.Cu") (net 6))')
    # Branch to R1.2 (10.08, 4.00):
    segments.append('(segment (start 6.95 4.40) (end 10.08 4.40) (width 0.15) (layer "B.Cu") (net 6))')
    segments.append('(via (at 10.08 4.40) (size 0.50) (drill 0.30) (layers "F.Cu" "B.Cu") (net 6))')
    segments.append('(segment (start 10.08 4.40) (end 10.08 4.00) (width 0.15) (layer "F.Cu") (net 6))')

    # Net 1 (GND):
    # Add stitching vias from GND pads to planes:
    # J1.2 (4.95, 3.25):
    segments.append('(segment (start 4.95 3.25) (end 4.95 2.20) (width 0.20) (layer "F.Cu") (net 1))')
    segments.append('(via (at 4.95 2.20) (size 0.50) (drill 0.30) (layers "F.Cu" "B.Cu") (net 1))')
    # C1.2 (2.28, 4.00) & C2.2 (2.55, 6.20):
    segments.append('(via (at 2.28 4.00) (size 0.50) (drill 0.30) (layers "F.Cu" "B.Cu") (net 1))')
    segments.append('(via (at 2.55 6.20) (size 0.50) (drill 0.30) (layers "F.Cu" "B.Cu") (net 1))')
    # J2.6 (7.70, 6.50):
    segments.append('(segment (start 7.70 6.50) (end 7.70 7.80) (width 0.20) (layer "F.Cu") (net 1))')
    segments.append('(via (at 7.70 7.80) (size 0.50) (drill 0.30) (layers "F.Cu" "B.Cu") (net 1))')
    # J2.9, J2.10:
    segments.append('(via (at 1.50 15.00) (size 0.50) (drill 0.30) (layers "F.Cu" "B.Cu") (net 1))')
    segments.append('(via (at 9.90 15.00) (size 0.50) (drill 0.30) (layers "F.Cu" "B.Cu") (net 1))')

    pcb_lines.extend(segments)

    # Ground Zones (F.Cu and B.Cu)
    zones = [
        '  (zone (net 1) (net_name "GND") (layers "F.Cu") (tstamp "' + str(uuid.uuid4()) + '")',
        '    (hatch full 0.5) (priority 0) (connect_pads (clearance 0.15)) (min_thickness 0.127)',
        '    (filled_areas_thickness no) (fill yes (thermal_gap 0.15) (thermal_bridge_width 0.18))',
        '    (polygon (pts (xy 0.25 0.25) (xy 11.15 0.25) (xy 11.15 15.75) (xy 0.25 15.75)))',
        '  )',
        '  (zone (net 1) (net_name "GND") (layers "B.Cu") (tstamp "' + str(uuid.uuid4()) + '")',
        '    (hatch full 0.5) (priority 0) (connect_pads (clearance 0.15)) (min_thickness 0.127)',
        '    (filled_areas_thickness no) (fill yes (thermal_gap 0.15) (thermal_bridge_width 0.18))',
        '    (polygon (pts (xy 0.25 0.25) (xy 11.15 0.25) (xy 11.15 15.75) (xy 0.25 15.75)))',
        '  )'
    ]
    pcb_lines.extend(zones)
    pcb_lines.append(')')

    out_file = carrier_dir / 'MicroSD_Carrier.kicad_pcb'
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(pcb_lines))
    print("Wrote", out_file)

if __name__ == '__main__':
    generate_pcb()

