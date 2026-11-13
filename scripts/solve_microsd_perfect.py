import json
import uuid
import subprocess
from pathlib import Path

KICAD_CLI = Path("C:/Users/goran/AppData/Local/Programs/KiCad/10.0/bin/kicad-cli.exe")
CARRIER_DIR = Path("output/RevF_Working/MicroSD_Carrier")
CARRIER_DIR.mkdir(parents=True, exist_ok=True)
FP_DIR = CARRIER_DIR / "MicroSD.pretty"
FP_DIR.mkdir(parents=True, exist_ok=True)

def generate_carrier():
    print("=== Generating MicroSD Carrier Subsystem ===")
    
    # 1. Project file with standard JLCPCB rules
    pro_content = {
        "board": {
            "design_settings": {
                "defaults": {
                    "board_thickness": 0.8,
                    "copper_line_width": 0.20,
                    "min_clearance": 0.127,
                    "min_through_hole_diameter": 0.30,
                    "min_track_width": 0.127,
                    "min_via_diameter": 0.50
                },
                "rules": {
                    "min_clearance": 0.127,
                    "min_track_width": 0.127,
                    "min_via_diameter": 0.50,
                    "min_through_hole_diameter": 0.30,
                    "hole_clearance": 0.20,
                    "solder_mask_min_width": 0.0
                }
            }
        },
        "meta": {"filename": "MicroSD_Carrier.kicad_pro", "version": 1},
        "sheets": [["", ""]]
    }
    with open(CARRIER_DIR / 'MicroSD_Carrier.kicad_pro', 'w', encoding='utf-8') as f:
        json.dump(pro_content, f, indent=2)

    # 2. DRU Design Rules file
    dru_content = """(version 1)
(rule "Board Edge Clearance"
  (constraint edge_clearance (min 0.30mm))
  (condition "A.Type == '*'")
)
"""
    with open(CARRIER_DIR / 'MicroSD_Carrier.kicad_dru', 'w', encoding='utf-8') as f:
        f.write(dru_content)

    # 3. Symbol table & Footprint table
    with open(CARRIER_DIR / 'sym-lib-table', 'w', encoding='utf-8') as f:
        f.write('(sym_lib_table\n  (lib (name "MicroSD_Lib")(type "KiCad")(uri "${KIPRJMOD}/MicroSD_Lib.kicad_sym")(options "")(descr ""))\n)\n')
    with open(CARRIER_DIR / 'fp-lib-table', 'w', encoding='utf-8') as f:
        f.write('(fp_lib_table\n  (lib (name "MicroSD")(type "KiCad")(uri "${KIPRJMOD}/MicroSD.pretty")(options "")(descr ""))\n)\n')

    # 4. Symbol definitions
    symbols_def = [
        '    (symbol "MicroSD_Lib:FPC_6P" (in_bom yes) (on_board yes)',
        '      (property "Reference" "J1" (at 0 11.43 0) (effects (font (size 1.27 1.27))))',
        '      (property "Value" "FH12-6S-0.5SH" (at 0 -13.97 0) (effects (font (size 1.27 1.27))))',
        '      (property "Footprint" "MicroSD:FPC_6P_0.5mm" (at 0 -16.51 0) (effects (font (size 1.27 1.27)) hide))',
        '      (symbol "FPC_6P_0_1"',
        '        (rectangle (start -5.08 10.16) (end 5.08 -12.70) (stroke (width 0.254)) (fill (type background)))',
        '        (pin passive line (at -7.62 7.62 0) (length 2.54) (name "3V3" (effects (font (size 1 1)))) (number "1" (effects (font (size 1 1)))))',
        '        (pin passive line (at -7.62 5.08 0) (length 2.54) (name "GND" (effects (font (size 1 1)))) (number "2" (effects (font (size 1 1)))))',
        '        (pin passive line (at -7.62 2.54 0) (length 2.54) (name "SCK" (effects (font (size 1 1)))) (number "3" (effects (font (size 1 1)))))',
        '        (pin passive line (at -7.62 0.00 0) (length 2.54) (name "MOSI" (effects (font (size 1 1)))) (number "4" (effects (font (size 1 1)))))',
        '        (pin passive line (at -7.62 -2.54 0) (length 2.54) (name "MISO" (effects (font (size 1 1)))) (number "5" (effects (font (size 1 1)))))',
        '        (pin passive line (at -7.62 -5.08 0) (length 2.54) (name "CS" (effects (font (size 1 1)))) (number "6" (effects (font (size 1 1)))))',
        '        (pin passive line (at -7.62 -7.62 0) (length 2.54) (name "MP1" (effects (font (size 1 1)))) (number "MP1" (effects (font (size 1 1)))))',
        '        (pin passive line (at -7.62 -10.16 0) (length 2.54) (name "MP2" (effects (font (size 1 1)))) (number "MP2" (effects (font (size 1 1)))))',
        '      )',
        '    )',
        '    (symbol "MicroSD_Lib:MICROSD_SOCKET" (in_bom yes) (on_board yes)',
        '      (property "Reference" "J2" (at 0 13.97 0) (effects (font (size 1.27 1.27))))',
        '      (property "Value" "TF-01A" (at 0 -16.51 0) (effects (font (size 1.27 1.27))))',
        '      (property "Footprint" "MicroSD:MicroSD_Socket_TF01A" (at 0 -19.05 0) (effects (font (size 1.27 1.27)) hide))',
        '      (symbol "MICROSD_SOCKET_0_1"',
        '        (rectangle (start -7.62 12.70) (end 7.62 -15.24) (stroke (width 0.254)) (fill (type background)))',
        '        (pin passive line (at 10.16 10.16 180) (length 2.54) (name "DAT2" (effects (font (size 1 1)))) (number "1" (effects (font (size 1 1)))))',
        '        (pin passive line (at 10.16 7.62 180) (length 2.54) (name "CD_DAT3_CS" (effects (font (size 1 1)))) (number "2" (effects (font (size 1 1)))))',
        '        (pin passive line (at 10.16 5.08 180) (length 2.54) (name "CMD_MOSI" (effects (font (size 1 1)))) (number "3" (effects (font (size 1 1)))))',
        '        (pin passive line (at 10.16 2.54 180) (length 2.54) (name "VDD" (effects (font (size 1 1)))) (number "4" (effects (font (size 1 1)))))',
        '        (pin passive line (at 10.16 0.00 180) (length 2.54) (name "CLK_SCK" (effects (font (size 1 1)))) (number "5" (effects (font (size 1 1)))))',
        '        (pin passive line (at 10.16 -2.54 180) (length 2.54) (name "VSS_GND" (effects (font (size 1 1)))) (number "6" (effects (font (size 1 1)))))',
        '        (pin passive line (at 10.16 -5.08 180) (length 2.54) (name "DAT0_MISO" (effects (font (size 1 1)))) (number "7" (effects (font (size 1 1)))))',
        '        (pin passive line (at 10.16 -7.62 180) (length 2.54) (name "DAT1" (effects (font (size 1 1)))) (number "8" (effects (font (size 1 1)))))',
        '        (pin passive line (at 10.16 -10.16 180) (length 2.54) (name "SHIELD1" (effects (font (size 1 1)))) (number "9" (effects (font (size 1 1)))))',
        '        (pin passive line (at 10.16 -12.70 180) (length 2.54) (name "SHIELD2" (effects (font (size 1 1)))) (number "10" (effects (font (size 1 1)))))',
        '      )',
        '    )',
        '    (symbol "MicroSD_Lib:C_SMALL" (in_bom yes) (on_board yes)',
        '      (property "Reference" "C" (at 1.27 2.54 0) (effects (font (size 1.27 1.27))))',
        '      (property "Value" "C_Small" (at 1.27 -2.54 0) (effects (font (size 1.27 1.27))))',
        '      (property "Footprint" "MicroSD:C_0402" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))',
        '      (symbol "C_SMALL_0_1"',
        '        (polyline (pts (xy -1.27 0.508) (xy 1.27 0.508)) (stroke (width 0.254)))',
        '        (polyline (pts (xy -1.27 -0.508) (xy 1.27 -0.508)) (stroke (width 0.254)))',
        '        (pin passive line (at 0 2.54 270) (length 2.032) (name "1" (effects (font (size 1 1)))) (number "1" (effects (font (size 1 1)))))',
        '        (pin passive line (at 0 -2.54 90) (length 2.032) (name "2" (effects (font (size 1 1)))) (number "2" (effects (font (size 1 1)))))',
        '      )',
        '    )',
        '    (symbol "MicroSD_Lib:R_SMALL" (in_bom yes) (on_board yes)',
        '      (property "Reference" "R" (at 1.27 2.54 0) (effects (font (size 1.27 1.27))))',
        '      (property "Value" "R_Small" (at 1.27 -2.54 0) (effects (font (size 1.27 1.27))))',
        '      (property "Footprint" "MicroSD:R_0402" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))',
        '      (symbol "R_SMALL_0_1"',
        '        (rectangle (start -0.762 1.524) (end 0.762 -1.524) (stroke (width 0.254)) (fill (type none)))',
        '        (pin passive line (at 0 2.54 270) (length 1.016) (name "1" (effects (font (size 1 1)))) (number "1" (effects (font (size 1 1)))))',
        '        (pin passive line (at 0 -2.54 90) (length 1.016) (name "2" (effects (font (size 1 1)))) (number "2" (effects (font (size 1 1)))))',
        '      )',
        '    )'
    ]

    sym_file_lines = ['(kicad_symbol_lib (version 20231120) (generator "SmartPen_Engineer")']
    sym_file_lines.extend(symbols_def)
    sym_file_lines.append(')')
    with open(CARRIER_DIR / 'MicroSD_Lib.kicad_sym', 'w', encoding='utf-8') as f:
        f.write('\n'.join(sym_file_lines))

    # Write sch file
    sch_lines = [
        '(kicad_sch (version 20231120) (generator "SmartPen_Engineer")',
        f'  (uuid "{uuid.uuid4()}")',
        '  (paper "A4")',
        '  (title_block',
        '    (title "Smart Pen MicroSD Off-Board Carrier")',
        '    (date "2026-11-02")',
        '    (rev "Rev F.1")',
        '    (company "RadixView Technologies")',
        '    (comment 1 "Off-board miniature MicroSD SPI storage module")',
        '  )',
        '  (lib_symbols'
    ]
    sch_lines.extend(symbols_def)
    sch_lines.append('  )')

    instances = [
        f'  (symbol (lib_id "MicroSD_Lib:FPC_6P") (at 60.96 88.90 0) (unit 1) (in_bom yes) (on_board yes)',
        f'    (uuid "{uuid.uuid4()}")',
        '    (property "Reference" "J1" (at 60.96 73.66 0) (effects (font (size 1.27 1.27))))',
        '    (property "Value" "FH12-6S-0.5SH" (at 60.96 104.14 0) (effects (font (size 1.27 1.27))))',
        '    (property "Footprint" "MicroSD:FPC_6P_0.5mm" (at 60.96 106.68 0) (effects (font (size 1.27 1.27)) hide))',
        f'    (pin "1" (uuid "{uuid.uuid4()}"))',
        f'    (pin "2" (uuid "{uuid.uuid4()}"))',
        f'    (pin "3" (uuid "{uuid.uuid4()}"))',
        f'    (pin "4" (uuid "{uuid.uuid4()}"))',
        f'    (pin "5" (uuid "{uuid.uuid4()}"))',
        f'    (pin "6" (uuid "{uuid.uuid4()}"))',
        f'    (pin "MP1" (uuid "{uuid.uuid4()}"))',
        f'    (pin "MP2" (uuid "{uuid.uuid4()}"))',
        '  )',
        f'  (symbol (lib_id "MicroSD_Lib:MICROSD_SOCKET") (at 127.00 88.90 0) (unit 1) (in_bom yes) (on_board yes)',
        f'    (uuid "{uuid.uuid4()}")',
        '    (property "Reference" "J2" (at 127.00 71.12 0) (effects (font (size 1.27 1.27))))',
        '    (property "Value" "TF-01A" (at 127.00 106.68 0) (effects (font (size 1.27 1.27))))',
        '    (property "Footprint" "MicroSD:MicroSD_Socket_TF01A" (at 127.00 109.22 0) (effects (font (size 1.27 1.27)) hide))',
        f'    (pin "1" (uuid "{uuid.uuid4()}"))',
        f'    (pin "2" (uuid "{uuid.uuid4()}"))',
        f'    (pin "3" (uuid "{uuid.uuid4()}"))',
        f'    (pin "4" (uuid "{uuid.uuid4()}"))',
        f'    (pin "5" (uuid "{uuid.uuid4()}"))',
        f'    (pin "6" (uuid "{uuid.uuid4()}"))',
        f'    (pin "7" (uuid "{uuid.uuid4()}"))',
        f'    (pin "8" (uuid "{uuid.uuid4()}"))',
        f'    (pin "9" (uuid "{uuid.uuid4()}"))',
        f'    (pin "10" (uuid "{uuid.uuid4()}"))',
        '  )',
        f'  (symbol (lib_id "MicroSD_Lib:C_SMALL") (at 88.90 73.66 0) (unit 1) (in_bom yes) (on_board yes)',
        f'    (uuid "{uuid.uuid4()}")',
        '    (property "Reference" "C1" (at 91.44 71.12 0) (effects (font (size 1.27 1.27))))',
        '    (property "Value" "0.1uF" (at 91.44 73.66 0) (effects (font (size 1.27 1.27))))',
        '    (property "Footprint" "MicroSD:C_0402" (at 88.90 73.66 0) (effects (font (size 1.27 1.27)) hide))',
        f'    (pin "1" (uuid "{uuid.uuid4()}"))',
        f'    (pin "2" (uuid "{uuid.uuid4()}"))',
        '  )',
        f'  (symbol (lib_id "MicroSD_Lib:C_SMALL") (at 99.06 73.66 0) (unit 1) (in_bom yes) (on_board yes)',
        f'    (uuid "{uuid.uuid4()}")',
        '    (property "Reference" "C2" (at 101.60 71.12 0) (effects (font (size 1.27 1.27))))',
        '    (property "Value" "10uF" (at 101.60 73.66 0) (effects (font (size 1.27 1.27))))',
        '    (property "Footprint" "MicroSD:C_0603" (at 99.06 73.66 0) (effects (font (size 1.27 1.27)) hide))',
        f'    (pin "1" (uuid "{uuid.uuid4()}"))',
        f'    (pin "2" (uuid "{uuid.uuid4()}"))',
        '  )',
        f'  (symbol (lib_id "MicroSD_Lib:R_SMALL") (at 88.90 96.52 0) (unit 1) (in_bom yes) (on_board yes)',
        f'    (uuid "{uuid.uuid4()}")',
        '    (property "Reference" "R1" (at 91.44 93.98 0) (effects (font (size 1.27 1.27))))',
        '    (property "Value" "10k" (at 91.44 96.52 0) (effects (font (size 1.27 1.27))))',
        '    (property "Footprint" "MicroSD:R_0402" (at 88.90 96.52 0) (effects (font (size 1.27 1.27)) hide))',
        f'    (pin "1" (uuid "{uuid.uuid4()}"))',
        f'    (pin "2" (uuid "{uuid.uuid4()}"))',
        '  )',
        f'  (symbol (lib_id "MicroSD_Lib:R_SMALL") (at 99.06 96.52 0) (unit 1) (in_bom yes) (on_board yes)',
        f'    (uuid "{uuid.uuid4()}")',
        '    (property "Reference" "R2" (at 101.60 93.98 0) (effects (font (size 1.27 1.27))))',
        '    (property "Value" "10k" (at 101.60 96.52 0) (effects (font (size 1.27 1.27))))',
        '    (property "Footprint" "MicroSD:R_0402" (at 99.06 96.52 0) (effects (font (size 1.27 1.27)) hide))',
        f'    (pin "1" (uuid "{uuid.uuid4()}"))',
        f'    (pin "2" (uuid "{uuid.uuid4()}"))',
        '  )'
    ]
    sch_lines.extend(instances)

    wires = [
        # J1 pins
        '  (wire (pts (xy 53.34 81.28) (xy 45.72 81.28)) (stroke (width 0)))',
        '  (label "3V3" (at 45.72 81.28 180) (effects (font (size 1.27 1.27)) (justify right)))',
        '  (wire (pts (xy 53.34 83.82) (xy 45.72 83.82)) (stroke (width 0)))',
        '  (label "GND" (at 45.72 83.82 180) (effects (font (size 1.27 1.27)) (justify right)))',
        '  (wire (pts (xy 53.34 86.36) (xy 45.72 86.36)) (stroke (width 0)))',
        '  (label "SD_SCK" (at 45.72 86.36 180) (effects (font (size 1.27 1.27)) (justify right)))',
        '  (wire (pts (xy 53.34 88.90) (xy 45.72 88.90)) (stroke (width 0)))',
        '  (label "SD_MOSI" (at 45.72 88.90 180) (effects (font (size 1.27 1.27)) (justify right)))',
        '  (wire (pts (xy 53.34 91.44) (xy 45.72 91.44)) (stroke (width 0)))',
        '  (label "SD_MISO" (at 45.72 91.44 180) (effects (font (size 1.27 1.27)) (justify right)))',
        '  (wire (pts (xy 53.34 93.98) (xy 45.72 93.98)) (stroke (width 0)))',
        '  (label "SD_CS" (at 45.72 93.98 180) (effects (font (size 1.27 1.27)) (justify right)))',
        '  (wire (pts (xy 53.34 96.52) (xy 45.72 96.52)) (stroke (width 0)))',
        '  (label "GND" (at 45.72 96.52 180) (effects (font (size 1.27 1.27)) (justify right)))',
        '  (wire (pts (xy 53.34 99.06) (xy 45.72 99.06)) (stroke (width 0)))',
        '  (label "GND" (at 45.72 99.06 180) (effects (font (size 1.27 1.27)) (justify right)))',

        # J2 Socket Pins
        '  (no_connect (at 137.16 78.74))',  # Pin 1 DAT2
        '  (wire (pts (xy 137.16 81.28) (xy 144.78 81.28)) (stroke (width 0)))',
        '  (label "SD_CS" (at 144.78 81.28 0) (effects (font (size 1.27 1.27)) (justify left)))',
        '  (wire (pts (xy 137.16 83.82) (xy 144.78 83.82)) (stroke (width 0)))',
        '  (label "SD_MOSI" (at 144.78 83.82 0) (effects (font (size 1.27 1.27)) (justify left)))',
        '  (wire (pts (xy 137.16 86.36) (xy 144.78 86.36)) (stroke (width 0)))',
        '  (label "3V3" (at 144.78 86.36 0) (effects (font (size 1.27 1.27)) (justify left)))',
        '  (wire (pts (xy 137.16 88.90) (xy 144.78 88.90)) (stroke (width 0)))',
        '  (label "SD_SCK" (at 144.78 88.90 0) (effects (font (size 1.27 1.27)) (justify left)))',
        '  (wire (pts (xy 137.16 91.44) (xy 144.78 91.44)) (stroke (width 0)))',
        '  (label "GND" (at 144.78 91.44 0) (effects (font (size 1.27 1.27)) (justify left)))',
        '  (wire (pts (xy 137.16 93.98) (xy 144.78 93.98)) (stroke (width 0)))',
        '  (label "SD_MISO" (at 144.78 93.98 0) (effects (font (size 1.27 1.27)) (justify left)))',
        '  (no_connect (at 137.16 96.52))',  # Pin 8 DAT1
        '  (wire (pts (xy 137.16 99.06) (xy 144.78 99.06)) (stroke (width 0)))',
        '  (label "GND" (at 144.78 99.06 0) (effects (font (size 1.27 1.27)) (justify left)))',
        '  (wire (pts (xy 137.16 101.60) (xy 144.78 101.60)) (stroke (width 0)))',
        '  (label "GND" (at 144.78 101.60 0) (effects (font (size 1.27 1.27)) (justify left)))',

        # Decoupling Caps C1, C2
        '  (wire (pts (xy 88.90 71.12) (xy 88.90 66.04)) (stroke (width 0)))',
        '  (label "3V3" (at 88.90 66.04 90) (effects (font (size 1.27 1.27)) (justify left)))',
        '  (wire (pts (xy 88.90 76.20) (xy 88.90 81.28)) (stroke (width 0)))',
        '  (label "GND" (at 88.90 81.28 270) (effects (font (size 1.27 1.27)) (justify right)))',
        '  (wire (pts (xy 99.06 71.12) (xy 99.06 66.04)) (stroke (width 0)))',
        '  (label "3V3" (at 99.06 66.04 90) (effects (font (size 1.27 1.27)) (justify left)))',
        '  (wire (pts (xy 99.06 76.20) (xy 99.06 81.28)) (stroke (width 0)))',
        '  (label "GND" (at 99.06 81.28 270) (effects (font (size 1.27 1.27)) (justify right)))',

        # Pull-up Resistors R1 (CS), R2 (MISO)
        '  (wire (pts (xy 88.90 93.98) (xy 88.90 88.90)) (stroke (width 0)))',
        '  (label "3V3" (at 88.90 88.90 90) (effects (font (size 1.27 1.27)) (justify left)))',
        '  (wire (pts (xy 88.90 99.06) (xy 88.90 104.14)) (stroke (width 0)))',
        '  (label "SD_CS" (at 88.90 104.14 270) (effects (font (size 1.27 1.27)) (justify right)))',
        '  (wire (pts (xy 99.06 93.98) (xy 99.06 88.90)) (stroke (width 0)))',
        '  (label "3V3" (at 99.06 88.90 90) (effects (font (size 1.27 1.27)) (justify left)))',
        '  (wire (pts (xy 99.06 99.06) (xy 99.06 104.14)) (stroke (width 0)))',
        '  (label "SD_MISO" (at 99.06 104.14 270) (effects (font (size 1.27 1.27)) (justify right)))'
    ]
    sch_lines.extend(wires)
    sch_lines.append(')')
    with open(CARRIER_DIR / 'MicroSD_Carrier.kicad_sch', 'w', encoding='utf-8') as f:
        f.write('\n'.join(sch_lines))

    # Footprints
    fpc_fp = [
        '(footprint "MicroSD:FPC_6P_0.5mm" (version 20221018) (generator pcbnew)',
        '  (layer "F.Cu")',
        '  (fp_text reference "REF**" (at 0 -1.2) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.15))))',
        '  (fp_text value "FH12-6S-0.5SH" (at 0 2.5) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.15)) hide))',
        '  (pad "1" smd rect (at -1.25 1.25) (size 0.30 1.00) (layers "F.Cu" "F.Paste" "F.Mask"))',
        '  (pad "2" smd rect (at -0.75 1.25) (size 0.30 1.00) (layers "F.Cu" "F.Paste" "F.Mask"))',
        '  (pad "3" smd rect (at -0.25 1.25) (size 0.30 1.00) (layers "F.Cu" "F.Paste" "F.Mask"))',
        '  (pad "4" smd rect (at 0.25 1.25) (size 0.30 1.00) (layers "F.Cu" "F.Paste" "F.Mask"))',
        '  (pad "5" smd rect (at 0.75 1.25) (size 0.30 1.00) (layers "F.Cu" "F.Paste" "F.Mask"))',
        '  (pad "6" smd rect (at 1.25 1.25) (size 0.30 1.00) (layers "F.Cu" "F.Paste" "F.Mask"))',
        '  (pad "MP1" smd rect (at -2.2 -0.2) (size 0.8 1.0) (layers "F.Cu" "F.Paste" "F.Mask"))',
        '  (pad "MP2" smd rect (at 2.2 -0.2) (size 0.8 1.0) (layers "F.Cu" "F.Paste" "F.Mask"))',
        ')'
    ]
    with open(FP_DIR / 'FPC_6P_0.5mm.kicad_mod', 'w', encoding='utf-8') as f:
        f.write('\n'.join(fpc_fp))

    tf_fp = [
        '(footprint "MicroSD:MicroSD_Socket_TF01A" (version 20221018) (generator pcbnew)',
        '  (layer "F.Cu")',
        '  (fp_text reference "REF**" (at 0 4.0) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.15))))',
        '  (fp_text value "TF-01A" (at 0 4.0) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.15)) hide))',
        '  (pad "1" smd rect (at -3.5 -4.5) (size 0.60 1.40) (layers "F.Cu" "F.Paste" "F.Mask"))',
        '  (pad "2" smd rect (at -2.4 -4.5) (size 0.60 1.40) (layers "F.Cu" "F.Paste" "F.Mask"))',
        '  (pad "3" smd rect (at -1.3 -4.5) (size 0.60 1.40) (layers "F.Cu" "F.Paste" "F.Mask"))',
        '  (pad "4" smd rect (at -0.2 -4.5) (size 0.60 1.40) (layers "F.Cu" "F.Paste" "F.Mask"))',
        '  (pad "5" smd rect (at 0.9 -4.5) (size 0.60 1.40) (layers "F.Cu" "F.Paste" "F.Mask"))',
        '  (pad "6" smd rect (at 2.0 -4.5) (size 0.60 1.40) (layers "F.Cu" "F.Paste" "F.Mask"))',
        '  (pad "7" smd rect (at 3.1 -4.5) (size 0.60 1.40) (layers "F.Cu" "F.Paste" "F.Mask"))',
        '  (pad "8" smd rect (at 4.2 -4.5) (size 0.60 1.40) (layers "F.Cu" "F.Paste" "F.Mask"))',
        '  (pad "9" smd rect (at -4.7 3.5) (size 0.80 1.20) (layers "F.Cu" "F.Paste" "F.Mask"))',
        '  (pad "10" smd rect (at 4.7 3.5) (size 0.80 1.20) (layers "F.Cu" "F.Paste" "F.Mask"))',
        ')'
    ]
    with open(FP_DIR / 'MicroSD_Socket_TF01A.kicad_mod', 'w', encoding='utf-8') as f:
        f.write('\n'.join(tf_fp))

    def make_pass_fp(name, val, w, h, dx, pad1_right=False):
        p1_x = dx if pad1_right else -dx
        p2_x = -dx if pad1_right else dx
        return [
            f'(footprint "MicroSD:{name}" (version 20221018) (generator pcbnew)',
            '  (layer "F.Cu")',
            f'  (fp_text reference "REF**" (at 0 0) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.15))))',
            f'  (fp_text value "{val}" (at 0 0) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.15)) hide))',
            f'  (pad "1" smd rect (at {p1_x:.3f} 0) (size {w:.3f} {h:.3f}) (layers "F.Cu" "F.Paste" "F.Mask"))',
            f'  (pad "2" smd rect (at {p2_x:.3f} 0) (size {w:.3f} {h:.3f}) (layers "F.Cu" "F.Paste" "F.Mask"))',
            ')'
        ]

    with open(FP_DIR / 'C_0402.kicad_mod', 'w', encoding='utf-8') as f:
        f.write('\n'.join(make_pass_fp('C_0402', '0.1uF', 0.6, 0.6, 0.48, pad1_right=True)))
    with open(FP_DIR / 'C_0603.kicad_mod', 'w', encoding='utf-8') as f:
        f.write('\n'.join(make_pass_fp('C_0603', '10uF', 0.8, 0.9, 0.75, pad1_right=True)))
    with open(FP_DIR / 'R_0402.kicad_mod', 'w', encoding='utf-8') as f:
        f.write('\n'.join(make_pass_fp('R_0402', '10k', 0.6, 0.6, 0.48, pad1_right=True)))

def generate_carrier_pcb():
    print("=== Generating MicroSD Carrier PCB Layout ===")
    
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
        '  (net 1 "/GND")',
        '  (net 2 "/3V3")',
        '  (net 3 "/SD_SCK")',
        '  (net 4 "/SD_MOSI")',
        '  (net 5 "/SD_MISO")',
        '  (net 6 "/SD_CS")',
        '  (net 7 "unconnected-(J2-DAT2-Pad1)")',
        '  (net 8 "unconnected-(J2-DAT1-Pad8)")',
        '  (net_class "Default" "Standard net class"',
        '    (clearance 0.127)',
        '    (trace_width 0.20)',
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
        f'    (uuid "{uuid.uuid4()}")',
        '    (fp_text reference "J1" (at 0 -1.2) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.15))))',
        '    (fp_text value "FH12-6S-0.5SH" (at 0 2.5) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.15)) hide))',
        '    (pad "1" smd rect (at -1.25 1.25) (size 0.30 1.00) (layers "F.Cu" "F.Paste" "F.Mask") (net 2 "/3V3"))',
        '    (pad "2" smd rect (at -0.75 1.25) (size 0.30 1.00) (layers "F.Cu" "F.Paste" "F.Mask") (net 1 "/GND"))',
        '    (pad "3" smd rect (at -0.25 1.25) (size 0.30 1.00) (layers "F.Cu" "F.Paste" "F.Mask") (net 3 "/SD_SCK"))',
        '    (pad "4" smd rect (at 0.25 1.25) (size 0.30 1.00) (layers "F.Cu" "F.Paste" "F.Mask") (net 4 "/SD_MOSI"))',
        '    (pad "5" smd rect (at 0.75 1.25) (size 0.30 1.00) (layers "F.Cu" "F.Paste" "F.Mask") (net 5 "/SD_MISO"))',
        '    (pad "6" smd rect (at 1.25 1.25) (size 0.30 1.00) (layers "F.Cu" "F.Paste" "F.Mask") (net 6 "/SD_CS"))',
        '    (pad "MP1" smd rect (at -2.2 -0.2) (size 0.8 1.0) (layers "F.Cu" "F.Paste" "F.Mask") (net 1 "/GND"))',
        '    (pad "MP2" smd rect (at 2.2 -0.2) (size 0.8 1.0) (layers "F.Cu" "F.Paste" "F.Mask") (net 1 "/GND"))',
        '  )',

        # C1 (0402, 0.1uF) at (1.60, 3.40)
        '  (footprint "MicroSD:C_0402" (layer "F.Cu") (at 1.60 3.40)',
        f'    (uuid "{uuid.uuid4()}")',
        '    (fp_text reference "C1" (at 0 -0.8) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.15))))',
        '    (fp_text value "0.1uF" (at 0 0.8) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.15)) hide))',
        '    (pad "1" smd rect (at 0.48 0) (size 0.6 0.6) (layers "F.Cu" "F.Paste" "F.Mask") (net 2 "/3V3"))',
        '    (pad "2" smd rect (at -0.48 0) (size 0.6 0.6) (layers "F.Cu" "F.Paste" "F.Mask") (net 1 "/GND"))',
        '  )',

        # C2 (0603, 10uF) at (1.60, 5.20)
        '  (footprint "MicroSD:C_0603" (layer "F.Cu") (at 1.60 5.20)',
        f'    (uuid "{uuid.uuid4()}")',
        '    (fp_text reference "C2" (at 0 0.8) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.15))))',
        '    (fp_text value "10uF" (at 0 0.8) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.15)) hide))',
        '    (pad "1" smd rect (at 0.75 0) (size 0.8 0.9) (layers "F.Cu" "F.Paste" "F.Mask") (net 2 "/3V3"))',
        '    (pad "2" smd rect (at -0.75 0) (size 0.8 0.9) (layers "F.Cu" "F.Paste" "F.Mask") (net 1 "/GND"))',
        '  )',

        # R1 (0402, 10k) at (9.80, 3.40)
        '  (footprint "MicroSD:R_0402" (layer "F.Cu") (at 9.80 3.40)',
        f'    (uuid "{uuid.uuid4()}")',
        '    (fp_text reference "R1" (at 0 -0.8) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.15))))',
        '    (fp_text value "10k" (at 0 0.8) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.15)) hide))',
        '    (pad "1" smd rect (at 0.48 0) (size 0.6 0.6) (layers "F.Cu" "F.Paste" "F.Mask") (net 2 "/3V3"))',
        '    (pad "2" smd rect (at -0.48 0) (size 0.6 0.6) (layers "F.Cu" "F.Paste" "F.Mask") (net 6 "/SD_CS"))',
        '  )',

        # R2 (0402, 10k) at (9.80, 5.20)
        '  (footprint "MicroSD:R_0402" (layer "F.Cu") (at 9.80 5.20)',
        f'    (uuid "{uuid.uuid4()}")',
        '    (fp_text reference "R2" (at 0 0.8) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.15))))',
        '    (fp_text value "10k" (at 0 0.8) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.15)) hide))',
        '    (pad "1" smd rect (at 0.48 0) (size 0.6 0.6) (layers "F.Cu" "F.Paste" "F.Mask") (net 2 "/3V3"))',
        '    (pad "2" smd rect (at -0.48 0) (size 0.6 0.6) (layers "F.Cu" "F.Paste" "F.Mask") (net 5 "/SD_MISO"))',
        '  )',

        # J2 MicroSD Socket (X=5.70, Y=11.20)
        '  (footprint "MicroSD:MicroSD_Socket_TF01A" (layer "F.Cu") (at 5.70 11.20)',
        f'    (uuid "{uuid.uuid4()}")',
        '    (fp_text reference "J2" (at 0 4.0) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.15))))',
        '    (fp_text value "TF-01A" (at 0 4.0) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.15)) hide))',
        '    (pad "1" smd rect (at -3.5 -4.5) (size 0.60 1.40) (layers "F.Cu" "F.Paste" "F.Mask") (net 7 "unconnected-(J2-DAT2-Pad1)"))',
        '    (pad "2" smd rect (at -2.4 -4.5) (size 0.60 1.40) (layers "F.Cu" "F.Paste" "F.Mask") (net 6 "/SD_CS"))',
        '    (pad "3" smd rect (at -1.3 -4.5) (size 0.60 1.40) (layers "F.Cu" "F.Paste" "F.Mask") (net 4 "/SD_MOSI"))',
        '    (pad "4" smd rect (at -0.2 -4.5) (size 0.60 1.40) (layers "F.Cu" "F.Paste" "F.Mask") (net 2 "/3V3"))',
        '    (pad "5" smd rect (at 0.9 -4.5) (size 0.60 1.40) (layers "F.Cu" "F.Paste" "F.Mask") (net 3 "/SD_SCK"))',
        '    (pad "6" smd rect (at 2.0 -4.5) (size 0.60 1.40) (layers "F.Cu" "F.Paste" "F.Mask") (net 1 "/GND"))',
        '    (pad "7" smd rect (at 3.1 -4.5) (size 0.60 1.40) (layers "F.Cu" "F.Paste" "F.Mask") (net 5 "/SD_MISO"))',
        '    (pad "8" smd rect (at 4.2 -4.5) (size 0.60 1.40) (layers "F.Cu" "F.Paste" "F.Mask") (net 8 "unconnected-(J2-DAT1-Pad8)"))',
        '    (pad "9" smd rect (at -4.7 3.5) (size 0.80 1.20) (layers "F.Cu" "F.Paste" "F.Mask") (net 1 "/GND"))',
        '    (pad "10" smd rect (at 4.7 3.5) (size 0.80 1.20) (layers "F.Cu" "F.Paste" "F.Mask") (net 1 "/GND"))',
        '  )'
    ]

    segments = []
    vias = []

    def add_seg(x1, y1, x2, y2, layer, net, width=0.20):
        segments.append(f'  (segment (start {x1:.3f} {y1:.3f}) (end {x2:.3f} {y2:.3f}) (width {width:.3f}) (layer "{layer}") (net {net}))')

    def add_via(x, y, net, dia=0.50, drill=0.30):
        vias.append(f'  (via (at {x:.3f} {y:.3f}) (size {dia:.3f}) (drill {drill:.3f}) (layers "F.Cu" "B.Cu") (net {net}))')

    # Net 3: /SD_SCK (F.Cu only)
    # J1.3 (5.45, 3.25) -> straight south to Y=4.20 -> diagonal to (6.60, 5.45) -> J2.5 (6.60, 6.70)
    add_seg(5.45, 3.25, 5.45, 4.20, "F.Cu", 3)
    add_seg(5.45, 4.20, 6.60, 5.45, "F.Cu", 3)
    add_seg(6.60, 5.45, 6.60, 6.70, "F.Cu", 3)

    # Net 4: /SD_MOSI
    # J1.4 (5.95, 3.25) -> straight North on F.Cu to (5.95, 2.20) via -> B.Cu to (4.40, 5.20) via -> F.Cu to J2.3 (4.40, 6.70)
    add_seg(5.95, 3.25, 5.95, 2.20, "F.Cu", 4)
    add_via(5.95, 2.20, 4)
    add_seg(5.95, 2.20, 4.40, 5.20, "B.Cu", 4)
    add_via(4.40, 5.20, 4)
    add_seg(4.40, 5.20, 4.40, 6.70, "F.Cu", 4)

    # Net 6: /SD_CS
    # J1.6 (6.95, 3.25) -> R1.2 (9.32, 3.40) on F.Cu
    add_seg(6.95, 3.25, 6.95, 3.40, "F.Cu", 6)
    add_seg(6.95, 3.40, 9.32, 3.40, "F.Cu", 6)
    # J1.6 to North via (6.95, 1.20) -> B.Cu across to (2.50, 1.20) -> South to (2.50, 5.20) -> (3.30, 5.20) via -> F.Cu -> J2.2 (3.30, 6.70)
    add_seg(6.95, 3.25, 6.95, 1.20, "F.Cu", 6)
    add_via(6.95, 1.20, 6)
    add_seg(6.95, 1.20, 2.50, 1.20, "B.Cu", 6)
    add_seg(2.50, 1.20, 2.50, 5.20, "B.Cu", 6)
    add_seg(2.50, 5.20, 3.30, 5.20, "B.Cu", 6)
    add_via(3.30, 5.20, 6)
    add_seg(3.30, 5.20, 3.30, 6.70, "F.Cu", 6)

    # Net 5: /SD_MISO
    add_seg(6.45, 3.25, 6.45, 4.30, "F.Cu", 5)
    add_seg(6.45, 4.30, 8.80, 4.30, "F.Cu", 5)
    add_seg(8.80, 4.30, 8.80, 6.70, "F.Cu", 5)
    add_seg(8.80, 4.30, 8.80, 5.20, "F.Cu", 5)
    add_seg(8.80, 5.20, 9.32, 5.20, "F.Cu", 5)

    # Net 2: /3V3
    # J1.1 (4.45, 3.25) -> C1.1 (2.08, 3.40) & C2.1 (2.35, 5.20)
    add_seg(4.45, 3.25, 4.45, 3.40, "F.Cu", 2)
    add_seg(4.45, 3.40, 2.08, 3.40, "F.Cu", 2)
    add_seg(2.08, 3.40, 2.35, 3.40, "F.Cu", 2)
    add_seg(2.35, 3.40, 2.35, 5.20, "F.Cu", 2)

    # 3V3 across the top: J1.1 (4.45, 3.25) -> (4.25, 3.25) -> (4.25, 0.50) -> (10.60, 0.50) -> (10.60, 5.20)
    add_seg(4.45, 3.25, 4.25, 3.25, "F.Cu", 2)
    add_seg(4.25, 3.25, 4.25, 0.50, "F.Cu", 2)
    add_seg(4.25, 0.50, 10.60, 0.50, "F.Cu", 2)
    add_seg(10.60, 0.50, 10.60, 5.20, "F.Cu", 2)
    add_seg(10.60, 3.40, 10.28, 3.40, "F.Cu", 2)
    add_seg(10.60, 5.20, 10.28, 5.20, "F.Cu", 2)

    # 3V3 to J2.4 (5.50, 6.70):
    # From (10.60, 5.20) go to (10.75, 5.20) via -> B.Cu to (5.50, 5.80) via -> F.Cu to J2.4 (5.50, 6.70)
    add_seg(10.60, 5.20, 10.75, 5.20, "F.Cu", 2)
    add_via(10.75, 5.20, 2)
    add_seg(10.75, 5.20, 5.50, 5.80, "B.Cu", 2)
    add_via(5.50, 5.80, 2)
    add_seg(5.50, 5.80, 5.50, 6.70, "F.Cu", 2)

    # Net 1: /GND
    # J1.2 (4.95, 3.25) drops via North at (4.95, 1.80) to B.Cu zone
    add_seg(4.95, 3.25, 4.95, 1.80, "F.Cu", 1)
    add_via(4.95, 1.80, 1)

    # MP1 (3.50, 1.80) & MP2 (7.90, 1.80)
    add_via(3.50, 2.50, 1)
    add_seg(3.50, 1.80, 3.50, 2.50, "F.Cu", 1)
    add_via(8.70, 1.80, 1)
    add_seg(7.90, 1.80, 8.70, 1.80, "F.Cu", 1)

    # C1.2 (1.12, 3.40) & C2.2 (0.85, 5.20) on F.Cu connected to via at (0.85, 4.30)
    add_seg(1.12, 3.40, 0.85, 3.40, "F.Cu", 1)
    add_seg(0.85, 3.40, 0.85, 5.20, "F.Cu", 1)
    add_via(0.85, 4.30, 1)

    # J2.6 (7.70, 6.70) -> via at (7.70, 7.60)
    add_seg(7.70, 6.70, 7.70, 7.60, "F.Cu", 1)
    add_via(7.70, 7.60, 1)

    # J2.9 (1.00, 14.70) & J2.10 (10.40, 14.70) vias
    add_via(1.00, 13.50, 1)
    add_seg(1.00, 14.70, 1.00, 13.50, "F.Cu", 1)
    add_via(10.40, 13.50, 1)
    add_seg(10.40, 14.70, 10.40, 13.50, "F.Cu", 1)

    pcb_lines.extend(segments)
    pcb_lines.extend(vias)

    # B.Cu GND Zone
    zone_lines = [
        '  (zone (net 1) (net_name "/GND") (layer "B.Cu") (uuid "' + str(uuid.uuid4()) + '")',
        '    (hatch edge 0.5)',
        '    (connect_pads (clearance 0.15))',
        '    (min_thickness 0.15)',
        '    (filled_areas_thickness no)',
        '    (fill yes (thermal_gap 0.15) (thermal_bridge_width 0.30))',
        '    (polygon',
        '      (pts',
        '        (xy 0.35 0.35)',
        '        (xy 11.05 0.35)',
        '        (xy 11.05 15.65)',
        '        (xy 0.35 15.65)',
        '      )',
        '    )',
        '  )'
    ]
    pcb_lines.extend(zone_lines)
    pcb_lines.append(')')

    pcb_path = CARRIER_DIR / 'MicroSD_Carrier.kicad_pcb'
    with open(pcb_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(pcb_lines))
    print(f"Generated {pcb_path}")

if __name__ == '__main__':
    generate_carrier()
    generate_carrier_pcb()
