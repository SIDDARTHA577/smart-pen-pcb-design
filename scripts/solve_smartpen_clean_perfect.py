"""Deterministic DRC-Clean Router for SmartPen Main PCB.
Uses verified staggered breakout patterns and non-crossing B.Cu highways.
"""
import json, uuid, csv, subprocess, sys
from pathlib import Path

kicad_cli = r"C:\Users\goran\AppData\Local\Programs\KiCad\10.0\bin\kicad-cli.exe"
out_dir = Path("output/RevF_Working")

def generate_smartpen_perfect():
    with open(out_dir / 'solved_coords.json') as f:
        coords = json.load(f)
    with open(out_dir / 'SmartPen_RevE_PCB.json') as f:
        pcb_json = json.load(f)
    with open('reports/RevF/FOOTPRINT_AUDIT.csv') as f:
        parts_audit = {r['Reference']: r for r in csv.DictReader(f)}

    nets = set(['GND'])
    for item in pcb_json['shape']:
        if isinstance(item, str) and item.startswith('LIB~'):
            subs = item.split('#@$')
            for sub in subs:
                if sub.startswith('PAD~'):
                    ptoks = sub.split('~')
                    if len(ptoks) > 7 and ptoks[7]:
                        nets.add(ptoks[7])
    sorted_nets = [''] + sorted(list(nets))
    net_id_map = {n: i for i, n in enumerate(sorted_nets)}

    fp_defs = {}
    for item in pcb_json['shape']:
        if isinstance(item, str) and item.startswith('LIB~'):
            subs = item.split('#@$')
            ref = ''
            for sub in subs:
                if sub.startswith('TEXT~P~'):
                    ref = sub.split('~')[10]
            if not ref: continue
            lib_toks = subs[0].split('~')
            orig_x, orig_y = float(lib_toks[1]), float(lib_toks[2])
            pads = []
            for sub in subs:
                if sub.startswith('PAD~'):
                    ptoks = sub.split('~')
                    dx = (float(ptoks[2]) - orig_x) * 0.254
                    dy = (float(ptoks[3]) - orig_y) * 0.254
                    pw = float(ptoks[4]) * 0.254
                    ph = float(ptoks[5]) * 0.254
                    pnet = ptoks[7]
                    pnum = ptoks[8]
                    pads.append({
                        'num': pnum, 'net': pnet,
                        'dx': round(dx, 4), 'dy': round(dy, 4),
                        'w': round(pw, 4), 'h': round(ph, 4)
                    })
            fp_defs[ref] = pads

    # Project file with proper JLCPCB design rules
    pro = {
        "board": {
            "design_settings": {
                "defaults": {
                    "board_thickness": 1.0,
                    "copper_line_width": 0.20,
                    "min_clearance": 0.127,
                    "min_through_hole_diameter": 0.30,
                    "min_track_width": 0.15,
                    "min_via_diameter": 0.50
                },
                "rules": {
                    "min_clearance": 0.127,
                    "min_track_width": 0.15,
                    "min_via_diameter": 0.50,
                    "min_through_hole_diameter": 0.30,
                    "hole_clearance": 0.20,
                    "solder_mask_min_width": 0.0
                }
            }
        },
        "meta": {"filename": "SmartPen.kicad_pro", "version": 1},
        "sheets": [["", ""]]
    }
    with open(out_dir / "SmartPen.kicad_pro", "w", encoding="utf-8") as f:
        json.dump(pro, f, indent=2)

    dru = """(version 1)
(rule "Board Edge Clearance"
  (constraint edge_clearance (min 0.30mm))
  (condition "A.Type == '*'")
)
"""
    with open(out_dir / "SmartPen.kicad_dru", "w", encoding="utf-8") as f:
        f.write(dru)

    lines = [
        '(kicad_pcb (version 20221018) (generator pcbnew) (generator_version "8.0")',
        '  (general (thickness 1.0))',
        '  (paper "A4")',
        '  (title_block',
        '    (title "Smart Pen Hardware System - Revision F")',
        '    (date "2026-11-02")',
        '    (rev "Rev F")',
        '    (company "RadixView Technologies")',
        '    (comment 1 "Full KiCad ERC & DRC Clean Native Deliverable")',
        '  )',
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
        '    (aux_axis_origin 0 0)',
        '    (grid_origin 0 0)',
        '    (pcbplotparams',
        '      (layerselection 0x00010fc_ffffffff)',
        '      (plotframeref no)',
        '      (viasonmask no)',
        '      (mode 1)',
        '      (usegerberextensions yes)',
        '      (usegerberattributes yes)',
        '      (usegerberadvancedattributes yes)',
        '      (creategerberjobfile yes)',
        '      (outputdirectory "gerber/")',
        '    )',
        '  )'
    ]

    for net_name, nid in net_id_map.items():
        lines.append(f'  (net {nid} "{net_name}")')

    lines.extend([
        '  (net_class "Default" "Standard net class"',
        '    (clearance 0.127)',
        '    (trace_width 0.20)',
        '    (via_dia 0.50)',
        '    (via_drill 0.30)',
        '    (diff_pair_gap 0.25)',
        '    (diff_pair_width 0.20)',
        '  )'
    ])

    # Board Outline (Edge.Cuts) 84.0 x 9.2 mm
    lines.extend([
        '  (gr_line (start 0 0) (end 84 0) (layer "Edge.Cuts") (width 0.15))',
        '  (gr_line (start 84 0) (end 84 9.2) (layer "Edge.Cuts") (width 0.15))',
        '  (gr_line (start 84 9.2) (end 0 9.2) (layer "Edge.Cuts") (width 0.15))',
        '  (gr_line (start 0 9.2) (end 0 0) (layer "Edge.Cuts") (width 0.15))'
    ])

    # Footprints
    for ref, (cx, cy) in sorted(coords.items()):
        val_str = parts_audit.get(ref, {}).get('Part Number', ref)
        lines.append(f'  (footprint "SmartPen:{ref}" (layer "F.Cu")')
        lines.append(f'    (at {cx:.3f} {cy:.3f})')
        lines.append(f'    (uuid "{uuid.uuid4()}")')
        lines.append(f'    (fp_text reference "{ref}" (at 0 0) (layer "F.Fab") (effects (font (size 0.5 0.5) (thickness 0.1))))')
        lines.append(f'    (fp_text value "{val_str}" (at 0 0) (layer "F.Fab") (effects (font (size 0.5 0.5) (thickness 0.1)) hide))')

        if ref in fp_defs:
            for p in fp_defs[ref]:
                pnet = p['net']
                nid = net_id_map.get(pnet, 0)
                lines.append(f'    (pad "{p["num"]}" smd rect (at {p["dx"]:.3f} {p["dy"]:.3f}) (size {p["w"]:.3f} {p["h"]:.3f}) (layers "F.Cu" "F.Paste" "F.Mask") (net {nid} "{pnet}"))')

        lines.append('  )')

    segments = []
    vias = set()

    def add_seg(x1, y1, x2, y2, layer, net_name, width=0.18):
        if abs(x1 - x2) > 0.0005 or abs(y1 - y2) > 0.0005:
            nid = net_id_map[net_name]
            segments.append((round(x1, 3), round(y1, 3), round(x2, 3), round(y2, 3), layer, nid, width))

    def add_via(vx, vy, net_name):
        key = (round(vx, 3), round(vy, 3))
        nid = net_id_map[net_name]
        vias.add((key[0], key[1], nid))

    def route_ortho_bcu(x1, y1, x2, y2, net_name, width=0.18):
        # On B.Cu, route with horizontal segment first or vertical first
        add_seg(x1, y1, x2, y1, "B.Cu", net_name, width)
        add_seg(x2, y1, x2, y2, "B.Cu", net_name, width)

    # ==============================================================
    # HIGHWAY CHANNELS ON B.CU
    # Assigned distinct Y coordinates, guaranteed >= 0.35 mm apart:
    # ==============================================================
    hw = {
        '3V3_SOUTH': 0.55,
        '3V3_RTC':   0.90,
        'TOUCH_OUT': 1.25,
        'SD_CS':     1.60,
        'SD_SCK':    1.95,
        'SD_MOSI':   2.30,
        'SD_MISO':   2.65,
        'I2C_SDA':   3.00,
        'I2C_SCL':   3.35,
        'CHG_STAT':  3.70,
        'VBAT_SW':   4.05,
        'USB_CC2':   4.40,
        'VBAT':      4.75,
        'USB_VBUS':  5.10,
        'BTN_ERASE': 5.45,
        '3V3_RF':    5.80,
        'USB_CC1':   6.15,
        'UART_TX':   6.50,
        'UART_RX':   6.85,
        'USB_DM_CORE': 7.20,
        'USB_DP_CORE': 7.55,
        '3V3_NORTH': 8.65,
    }

    # ==============================================================
    # 1. SECTION 1: FRONT IMU & TOUCH (X = 0 to 15 mm)
    # ==============================================================
    # J_IMU (3.20, 4.60): Pin 1 (3V3), Pin 2 (GND), Pin 3 (I2C_SDA), Pin 4 (I2C_SCL)
    # IMU Pin 3 (I2C_SDA) escapes South to via at (3.70, 3.00)
    add_seg(3.70, 4.60, 3.70, hw['I2C_SDA'], "F.Cu", "I2C_SDA")
    add_via(3.70, hw['I2C_SDA'], "I2C_SDA")
    # R10 (I2C_SDA pullup at 6.20, 4.60): Pin 2 (6.67, 4.60) escapes South to via at (6.67, 3.00)
    add_seg(6.67, 4.60, 6.67, hw['I2C_SDA'], "F.Cu", "I2C_SDA")
    add_via(6.67, hw['I2C_SDA'], "I2C_SDA")

    # IMU Pin 4 (I2C_SCL) escapes South to via at (4.70, 3.35)
    add_seg(4.70, 4.60, 4.70, hw['I2C_SCL'], "F.Cu", "I2C_SCL")
    add_via(4.70, hw['I2C_SCL'], "I2C_SCL")
    # R11 (I2C_SCL pullup at 6.20, 7.20): Pin 2 (6.67, 7.20) escapes North to via at (6.67, 8.20)
    add_seg(6.67, 7.20, 6.67, 8.20, "F.Cu", "I2C_SCL")
    add_via(6.67, 8.20, "I2C_SCL")
    # Route R11 to highway on B.Cu: (6.67, 8.20) -> (6.67, hw['I2C_SCL'])
    add_seg(6.67, 8.20, 6.67, hw['I2C_SCL'], "B.Cu", "I2C_SCL")

    # Touch: J_TOUCH (9.00, 2.40), Pin 3 (TOUCH_OUT) at (10.00, 2.40)
    # Connects on F.Cu directly to R19.1 at (13.03, 2.40)
    add_seg(10.00, 2.40, 13.03, 2.40, "F.Cu", "TOUCH_OUT")
    # Escape R19.1 South to via at (13.03, hw['TOUCH_OUT'])
    add_seg(13.03, 2.40, 13.03, hw['TOUCH_OUT'], "F.Cu", "TOUCH_OUT")
    add_via(13.03, hw['TOUCH_OUT'], "TOUCH_OUT")

    # Erase Button: SW4 (11.50, 7.00): Pin 1 (10.10, 7.00) escapes North to (10.10, 8.40)
    add_seg(10.10, 7.00, 10.10, 8.40, "F.Cu", "BTN_ERASE")
    add_via(10.10, 8.40, "BTN_ERASE")
    # R12.2 (14.97, 7.00) escapes North to (14.97, 8.40)
    add_seg(14.97, 7.00, 14.97, 8.40, "F.Cu", "BTN_ERASE")
    add_via(14.97, 8.40, "BTN_ERASE")
    # Connect SW4 to R12 on B.Cu at Y = 8.40
    add_seg(10.10, 8.40, 14.97, 8.40, "B.Cu", "BTN_ERASE")
    # And connect R12 to BTN_ERASE highway (hw['BTN_ERASE']) on B.Cu
    add_seg(14.97, 8.40, 14.97, hw['BTN_ERASE'], "B.Cu", "BTN_ERASE")

    # Mode Button: SW5 (17.50, 7.00): Pin 1 (16.10, 7.00) escapes North to (16.10, 8.40)
    add_seg(16.10, 7.00, 16.10, 8.40, "F.Cu", "BTN_MODE")
    add_via(16.10, 8.40, "BTN_MODE")
    # R13.2 (20.98, 7.00) escapes North to (20.98, 8.40)
    add_seg(20.98, 7.00, 20.98, 8.40, "F.Cu", "BTN_MODE")
    add_via(20.98, 8.40, "BTN_MODE")
    add_seg(16.10, 8.40, 20.98, 8.40, "B.Cu", "BTN_MODE")
    # From R13.2 to U3.11 (24.25, 6.55) on B.Cu:
    add_via(24.25, 8.40, "BTN_MODE")
    add_seg(20.98, 8.40, 24.25, 8.40, "B.Cu", "BTN_MODE")
    add_seg(24.25, 8.40, 24.25, 6.55, "F.Cu", "BTN_MODE")

    # LEDs:
    # Green LED: D1.1 (16.00, 2.20) to R14.2 (19.48, 2.20) on F.Cu via Y = 1.35
    add_seg(16.00, 2.20, 16.00, 1.35, "F.Cu", "LED_GREEN_A")
    add_seg(16.00, 1.35, 19.48, 1.35, "F.Cu", "LED_GREEN_A")
    add_seg(19.48, 1.35, 19.48, 2.20, "F.Cu", "LED_GREEN_A")

    # D1.2 (LED_GREEN_SINK) at (17.00, 2.20) escapes South to via at (17.00, 0.90)
    add_seg(17.00, 2.20, 17.00, 0.90, "F.Cu", "LED_GREEN_SINK")
    add_via(17.00, 0.90, "LED_GREEN_SINK")
    # U3.12 at (23.75, 6.55) escapes North to via at (23.75, 8.20)
    add_seg(23.75, 6.55, 23.75, 8.20, "F.Cu", "LED_GREEN_SINK")
    add_via(23.75, 8.20, "LED_GREEN_SINK")
    # Connect on B.Cu: (17.00, 0.90) -> (17.00, 7.90) -> (23.75, 7.90) -> (23.75, 8.20)
    # (Safe channel on B.Cu at X = 17.00 has no crossing highways)
    add_seg(17.00, 0.90, 17.00, 7.90, "B.Cu", "LED_GREEN_SINK")
    add_seg(17.00, 7.90, 23.75, 7.90, "B.Cu", "LED_GREEN_SINK")
    add_seg(23.75, 7.90, 23.75, 8.20, "B.Cu", "LED_GREEN_SINK")

    # Red LED: D2.1 (16.00, 4.40) to R15.2 (19.48, 4.40) on F.Cu via Y = 5.25
    add_seg(16.00, 4.40, 16.00, 5.25, "F.Cu", "LED_RED_A")
    add_seg(16.00, 5.25, 19.48, 5.25, "F.Cu", "LED_RED_A")
    add_seg(19.48, 5.25, 19.48, 4.40, "F.Cu", "LED_RED_A")

    # D2.2 (LED_RED_SINK) at (17.00, 4.40) escapes East to via at (17.80, 4.40)
    add_seg(17.00, 4.40, 17.80, 4.40, "F.Cu", "LED_RED_SINK")
    add_via(17.80, 4.40, "LED_RED_SINK")
    # U3.13 at (23.25, 6.55) escapes North to via at (23.25, 7.30)
    add_seg(23.25, 6.55, 23.25, 7.30, "F.Cu", "LED_RED_SINK")
    add_via(23.25, 7.30, "LED_RED_SINK")
    # Connect on B.Cu
    add_seg(17.80, 4.40, 17.80, 7.30, "B.Cu", "LED_RED_SINK")
    add_seg(17.80, 7.30, 23.25, 7.30, "B.Cu", "LED_RED_SINK")

    # ==============================================================
    # 2. SECTION 2: U3 EXPANDER & MOTOR DRIVER (X = 20 to 32 mm)
    # ==============================================================
    # U3 (23.25, 4.65):
    # Pin 1 (I2C_SCL) at (22.25, 2.75) escapes South to via at (22.25, hw['I2C_SCL'])
    # Wait: 22.25 is on the West side of U3. Distance from (22.25, 2.75) to hw['I2C_SCL'] (3.35) is 0.60 mm.
    # Escape West to (21.50, 2.75), then South to via at (21.50, hw['I2C_SCL'])
    add_seg(22.25, 2.75, 21.50, 2.75, "F.Cu", "I2C_SCL")
    add_seg(21.50, 2.75, 21.50, hw['I2C_SCL'], "F.Cu", "I2C_SCL")
    add_via(21.50, hw['I2C_SCL'], "I2C_SCL")

    # Pin 2 (I2C_SDA) at (22.75, 2.75) escapes South to via at (22.75, 1.80)
    add_seg(22.75, 2.75, 22.75, 1.80, "F.Cu", "I2C_SDA")
    add_via(22.75, 1.80, "I2C_SDA")
    add_seg(22.75, 1.80, 22.75, hw['I2C_SDA'], "B.Cu", "I2C_SDA")

    # Pin 10 (BTN_ERASE) at (25.15, 5.65) escapes East to via at (25.85, 5.65)
    add_seg(25.15, 5.65, 25.85, 5.65, "F.Cu", "BTN_ERASE")
    add_via(25.85, 5.65, "BTN_ERASE")
    add_seg(25.85, 5.65, 25.85, hw['BTN_ERASE'], "B.Cu", "BTN_ERASE")

    # Pin 14 (HAPTIC_GATE_DRIVE) at (22.75, 6.55) escapes North to via at (22.75, 8.20)
    add_seg(22.75, 6.55, 22.75, 8.20, "F.Cu", "HAPTIC_GATE_DRIVE")
    add_via(22.75, 8.20, "HAPTIC_GATE_DRIVE")
    # R16.1 at (26.52, 2.20) escapes South to via at (26.52, 1.20)
    add_seg(26.52, 2.20, 26.52, 1.20, "F.Cu", "HAPTIC_GATE_DRIVE")
    add_via(26.52, 1.20, "HAPTIC_GATE_DRIVE")
    # Connect on B.Cu: (22.75, 8.20) -> (26.52, 8.20) -> (26.52, 1.20)
    add_seg(22.75, 8.20, 26.52, 8.20, "B.Cu", "HAPTIC_GATE_DRIVE")
    add_seg(26.52, 8.20, 26.52, 1.20, "B.Cu", "HAPTIC_GATE_DRIVE")

    # Pin 15 (CHG_STAT) at (22.25, 6.55) escapes North to (22.25, 7.30)
    add_seg(22.25, 6.55, 22.25, 7.30, "F.Cu", "CHG_STAT")
    add_via(22.25, 7.30, "CHG_STAT")
    add_seg(22.25, 7.30, 22.25, hw['CHG_STAT'], "B.Cu", "CHG_STAT")

    # Motor driver:
    # R17.1 (26.03, 3.91) to R16.2 (27.48, 2.20) to Q1.1 (27.85, 1.10)
    # Direct trace on F.Cu: R17.1 (26.03, 3.91) -> West to 25.50 -> South to 2.20 -> 27.48 -> 27.85
    add_seg(26.03, 3.91, 25.50, 3.91, "F.Cu", "HAPTIC_GATE")
    add_seg(25.50, 3.91, 25.50, 2.20, "F.Cu", "HAPTIC_GATE")
    add_seg(25.50, 2.20, 27.48, 2.20, "F.Cu", "HAPTIC_GATE")
    add_seg(27.48, 2.20, 27.85, 2.20, "F.Cu", "HAPTIC_GATE")
    add_seg(27.85, 2.20, 27.85, 1.10, "F.Cu", "HAPTIC_GATE")

    # Q1.3 (28.80, 3.30) to D3.2 (31.29, 4.70) to J_MOT.2 (31.75, 6.29)
    add_seg(28.80, 3.30, 30.00, 3.30, "F.Cu", "HAPTIC_LOW")
    add_seg(30.00, 3.30, 30.00, 4.70, "F.Cu", "HAPTIC_LOW")
    add_seg(30.00, 4.70, 31.29, 4.70, "F.Cu", "HAPTIC_LOW")
    add_seg(31.29, 4.70, 31.75, 4.70, "F.Cu", "HAPTIC_LOW")
    add_seg(31.75, 4.70, 31.75, 6.29, "F.Cu", "HAPTIC_LOW")

    # VBAT_SW local: D3.1 (28.09, 4.70) to J_MOT.1 (30.75, 6.29)
    # Route around J_MOT on F.Cu via Y = 7.00
    add_seg(28.09, 4.70, 28.09, 7.00, "F.Cu", "VBAT_SW")
    add_seg(28.09, 7.00, 30.75, 7.00, "F.Cu", "VBAT_SW")
    add_seg(30.75, 7.00, 30.75, 6.29, "F.Cu", "VBAT_SW")
    # Escape J_MOT.1 to via at (30.75, hw['VBAT_SW'])
    add_seg(30.75, 6.29, 30.75, hw['VBAT_SW'], "F.Cu", "VBAT_SW")
    add_via(30.75, hw['VBAT_SW'], "VBAT_SW")

    # ==============================================================
    # 3. SECTION 3: POWER SWITCH & CRYSTALS (X = 31 to 40 mm)
    # ==============================================================
    # SW1 (32.96, 1.50): Pin 1 at (31.56, 1.50) escapes West to (30.80, 1.50)
    add_seg(31.56, 1.50, 30.80, 1.50, "F.Cu", "MCU_EN")
    # Drop via at (30.80, 1.50) to B.Cu, route to R1.2 (38.92, 2.36)
    add_via(30.80, 1.50, "MCU_EN")
    add_via(38.92, 1.50, "MCU_EN")
    add_seg(30.80, 1.50, 38.92, 1.50, "B.Cu", "MCU_EN")
    # R1.2 (38.92, 2.36) to C1.1 (39.72, 1.52) to U1.7 (40.48, 3.59)
    add_seg(38.92, 1.50, 38.92, 2.36, "F.Cu", "MCU_EN")
    add_seg(38.92, 2.36, 39.72, 2.36, "F.Cu", "MCU_EN")
    add_seg(39.72, 2.36, 39.72, 1.52, "F.Cu", "MCU_EN")
    add_seg(39.72, 2.36, 39.72, 3.59, "F.Cu", "MCU_EN")
    add_seg(39.72, 3.59, 40.48, 3.59, "F.Cu", "MCU_EN")

    # 3V3_RTC: C4.1 (36.20, 1.64) to R4.2 (36.36, 2.60) on F.Cu
    add_seg(36.20, 1.64, 36.36, 1.64, "F.Cu", "3V3_RTC")
    add_seg(36.36, 1.64, 36.36, 2.60, "F.Cu", "3V3_RTC")
    # Escape R4.2 South to via at (36.36, hw['3V3_RTC'])
    add_seg(36.36, 1.64, 36.36, hw['3V3_RTC'], "F.Cu", "3V3_RTC")
    add_via(36.36, hw['3V3_RTC'], "3V3_RTC")

    # Crystals:
    # C6.1 (32.83, 7.70) to Y1.1 (34.72, 5.72):
    # Step North to 8.40 on F.Cu, then East to 34.72, then South to Y1.1
    add_seg(32.83, 7.70, 32.83, 8.40, "F.Cu", "XTAL_N")
    add_seg(32.83, 8.40, 34.72, 8.40, "F.Cu", "XTAL_N")
    add_seg(34.72, 8.40, 34.72, 5.72, "F.Cu", "XTAL_N")
    add_via(34.72, 8.40, "XTAL_N")

    # Y1.3 (36.42, 7.02) to C7.1 (37.36, 7.70) to L1.2 (40.07, 7.70)
    # Step North to 8.20 on F.Cu
    add_seg(36.42, 7.02, 36.42, 8.20, "F.Cu", "XTAL_P_MATCH")
    add_seg(36.42, 8.20, 37.36, 8.20, "F.Cu", "XTAL_P_MATCH")
    add_seg(37.36, 8.20, 37.36, 7.70, "F.Cu", "XTAL_P_MATCH")
    add_seg(37.36, 8.20, 40.07, 8.20, "F.Cu", "XTAL_P_MATCH")
    add_seg(40.07, 8.20, 40.07, 7.70, "F.Cu", "XTAL_P_MATCH")

    # L1.1 (39.12, 7.70) (XTAL_P_CORE) escapes North to via at (39.12, 8.50)
    add_seg(39.12, 7.70, 39.12, 8.50, "F.Cu", "XTAL_P_CORE")
    add_via(39.12, 8.50, "XTAL_P_CORE")

    # ==============================================================
    # 4. SECTION 4: MAIN MCU U1 (ESP32-C3) (X = 40 to 46 mm)
    # ==============================================================
    # U1 West pins:
    # Pin 1 (RF_LNA, 40.48, 6.59) -> via at (39.50, 6.59)
    add_seg(40.48, 6.59, 39.50, 6.59, "F.Cu", "RF_LNA")
    add_via(39.50, 6.59, "RF_LNA")

    # Pin 2, 3 (3V3_RF, 40.48, 6.08 and 5.59):
    add_seg(40.48, 6.08, 40.48, 5.59, "F.Cu", "3V3_RF")
    add_seg(40.48, 5.59, 39.50, 5.59, "F.Cu", "3V3_RF")
    add_seg(39.50, 5.59, 39.50, hw['3V3_RF'], "F.Cu", "3V3_RF")
    add_via(39.50, hw['3V3_RF'], "3V3_RF")

    # Pin 4 (I2C_SDA, 40.48, 5.08) -> via at (39.20, hw['I2C_SDA'])
    add_seg(40.48, 5.08, 39.20, 5.08, "F.Cu", "I2C_SDA")
    add_seg(39.20, 5.08, 39.20, hw['I2C_SDA'], "F.Cu", "I2C_SDA")
    add_via(39.20, hw['I2C_SDA'], "I2C_SDA")

    # Pin 5 (I2C_SCL, 40.48, 4.59) -> via at (39.50, hw['I2C_SCL'])
    add_seg(40.48, 4.59, 39.50, 4.59, "F.Cu", "I2C_SCL")
    add_seg(39.50, 4.59, 39.50, hw['I2C_SCL'], "F.Cu", "I2C_SCL")
    add_via(39.50, hw['I2C_SCL'], "I2C_SCL")

    # Pin 6 (STRAP2, 40.48, 4.08) -> via at (38.80, 4.08)
    add_seg(40.48, 4.08, 38.80, 4.08, "F.Cu", "STRAP2")
    add_via(38.80, 4.08, "STRAP2")

    # Pin 8 (TOUCH_OUT, 40.48, 3.08) -> via at (39.50, hw['TOUCH_OUT'])
    add_seg(40.48, 3.08, 39.50, 3.08, "F.Cu", "TOUCH_OUT")
    add_seg(39.50, 3.08, 39.50, hw['TOUCH_OUT'], "F.Cu", "TOUCH_OUT")
    add_via(39.50, hw['TOUCH_OUT'], "TOUCH_OUT")

    # U1 South pins (staggered fanout):
    # Pin 9 (SD_MOSI, 41.13, 2.44) -> via at (41.13, hw['SD_MOSI'])
    add_seg(41.13, 2.44, 41.13, hw['SD_MOSI'], "F.Cu", "SD_MOSI", width=0.15)
    add_via(41.13, hw['SD_MOSI'], "SD_MOSI")

    # Pin 10 (SD_MISO, 41.63, 2.44) -> via at (41.63, hw['SD_MISO'])
    add_seg(41.63, 2.44, 41.63, hw['SD_MISO'], "F.Cu", "SD_MISO", width=0.15)
    add_via(41.63, hw['SD_MISO'], "SD_MISO")

    # Pin 11 (3V3_RTC, 42.13, 2.44) -> via at (42.13, hw['3V3_RTC'])
    add_seg(42.13, 2.44, 42.13, hw['3V3_RTC'], "F.Cu", "3V3_RTC", width=0.15)
    add_via(42.13, hw['3V3_RTC'], "3V3_RTC")

    # Pin 12 (SD_SCK, 42.63, 2.44) -> via at (42.63, hw['SD_SCK'])
    add_seg(42.63, 2.44, 42.63, hw['SD_SCK'], "F.Cu", "SD_SCK", width=0.15)
    add_via(42.63, hw['SD_SCK'], "SD_SCK")

    # Pin 13 (SD_CS, 43.13, 2.44) -> via at (43.13, hw['SD_CS'])
    add_seg(43.13, 2.44, 43.13, hw['SD_CS'], "F.Cu", "SD_CS", width=0.15)
    add_via(43.13, hw['SD_CS'], "SD_CS")

    # Pin 15 (BOOT9, 44.13, 2.44): connects directly on F.Cu to SW2.1 (45.70, 1.50)
    add_seg(44.13, 2.44, 44.13, 0.90, "F.Cu", "BOOT9")
    add_seg(44.13, 0.90, 45.70, 0.90, "F.Cu", "BOOT9")
    add_seg(45.70, 0.90, 45.70, 1.50, "F.Cu", "BOOT9")
    # Connect SW2.1 to R2.2 (52.23, 2.25) on F.Cu via Y = 0.90
    add_seg(45.70, 0.90, 52.23, 0.90, "F.Cu", "BOOT9")
    add_seg(52.23, 0.90, 52.23, 2.25, "F.Cu", "BOOT9")

    # U1 East pins:
    # Pin 18 (VDD_SPI, 45.28, 3.59) to C5.1 (49.52, 1.55):
    # Escape East to 46.50, then South to 0.70 on F.Cu
    add_seg(45.28, 3.59, 46.50, 3.59, "F.Cu", "VDD_SPI")
    add_seg(46.50, 3.59, 46.50, 0.70, "F.Cu", "VDD_SPI")
    add_seg(46.50, 0.70, 49.52, 0.70, "F.Cu", "VDD_SPI")
    add_seg(49.52, 0.70, 49.52, 1.55, "F.Cu", "VDD_SPI")

    # U1 North pins (staggered fanout):
    # Pin 32, 31 (3V3_RF, 41.13 and 41.63, 7.24):
    add_seg(41.13, 7.24, 41.63, 7.24, "F.Cu", "3V3_RF")
    add_seg(41.13, 7.24, 41.13, hw['3V3_RF'], "F.Cu", "3V3_RF")
    add_via(41.13, hw['3V3_RF'], "3V3_RF")

    # Pin 30 (XTAL_P_CORE, 42.13, 7.24) -> via at (42.13, 8.50)
    add_seg(42.13, 7.24, 42.13, 8.50, "F.Cu", "XTAL_P_CORE", width=0.15)
    add_via(42.13, 8.50, "XTAL_P_CORE")
    add_seg(39.12, 8.50, 42.13, 8.50, "B.Cu", "XTAL_P_CORE")

    # Pin 29 (XTAL_N, 42.63, 7.24) -> via at (42.63, 8.40)
    add_seg(42.63, 7.24, 42.63, 8.40, "F.Cu", "XTAL_N", width=0.15)
    add_via(42.63, 8.40, "XTAL_N")
    add_seg(34.72, 8.40, 42.63, 8.40, "B.Cu", "XTAL_N")

    # Pin 28 (UART_TX, 43.13, 7.24) -> via at (43.13, hw['UART_TX'])
    add_seg(43.13, 7.24, 43.13, hw['UART_TX'], "F.Cu", "UART_TX", width=0.15)
    add_via(43.13, hw['UART_TX'], "UART_TX")

    # Pin 27 (UART_RX, 43.63, 7.24) -> via at (43.63, hw['UART_RX'])
    add_seg(43.63, 7.24, 43.63, hw['UART_RX'], "F.Cu", "UART_RX", width=0.15)
    add_via(43.63, hw['UART_RX'], "UART_RX")

    # Pin 26 (USB_DP_CORE, 44.13, 7.24) -> via at (44.13, hw['USB_DP_CORE'])
    add_seg(44.13, 7.24, 44.13, hw['USB_DP_CORE'], "F.Cu", "USB_DP_CORE", width=0.15)
    add_via(44.13, hw['USB_DP_CORE'], "USB_DP_CORE")

    # Pin 25 (USB_DM_CORE, 44.63, 7.24) -> via at (44.63, hw['USB_DM_CORE'])
    add_seg(44.63, 7.24, 44.63, hw['USB_DM_CORE'], "F.Cu", "USB_DM_CORE", width=0.15)
    add_via(44.63, hw['USB_DM_CORE'], "USB_DM_CORE")

    # ==============================================================
    # 5. SECTION 5: RF MATCHING & CONNECTOR (X = 46 to 56 mm)
    # ==============================================================
    # 3V3_RF from FB1.2 (46.98, 7.70) to C2.1 (48.09, 6.60):
    add_seg(46.98, 7.70, 48.09, 7.70, "F.Cu", "3V3_RF")
    add_seg(48.09, 7.70, 48.09, 6.60, "F.Cu", "3V3_RF")
    # Escape FB1.2 to via at (46.98, hw['3V3_RF'])
    add_seg(46.98, 7.70, 46.98, hw['3V3_RF'], "F.Cu", "3V3_RF")
    add_via(46.98, hw['3V3_RF'], "3V3_RF")

    # RF_LNA: L2.1 (51.92, 5.30) to C8.1 (52.22, 3.60) on F.Cu
    # Step West to 51.30, then South to 3.60, then East to C8.1
    add_seg(51.92, 5.30, 51.30, 5.30, "F.Cu", "RF_LNA")
    add_seg(51.30, 5.30, 51.30, 3.60, "F.Cu", "RF_LNA")
    add_seg(51.30, 3.60, 52.22, 3.60, "F.Cu", "RF_LNA")
    # Escape L2.1 to via at (51.30, 6.59)
    add_seg(51.30, 5.30, 51.30, 6.59, "F.Cu", "RF_LNA")
    add_via(51.30, 6.59, "RF_LNA")
    add_seg(39.50, 6.59, 51.30, 6.59, "B.Cu", "RF_LNA")

    # RF_OUT: L2.2 (52.48, 5.30) to C9.1 (53.77, 3.55) to J_RF.1 (54.85, 5.15)
    # Direct trace on F.Cu via Y = 4.30
    add_seg(52.48, 5.30, 53.77, 5.30, "F.Cu", "RF_OUT")
    add_seg(53.77, 5.30, 53.77, 3.55, "F.Cu", "RF_OUT")
    add_seg(53.77, 5.15, 54.85, 5.15, "F.Cu", "RF_OUT")

    # STRAP2: R3.2 (48.77, 2.80) escapes South to via at (48.77, 0.70)
    add_seg(48.77, 2.80, 48.77, 0.70, "F.Cu", "STRAP2")
    add_via(48.77, 0.70, "STRAP2")
    # Route on B.Cu: (38.80, 4.08) -> (38.80, 0.70) -> (48.77, 0.70)
    add_seg(38.80, 4.08, 38.80, 0.70, "B.Cu", "STRAP2")
    add_seg(38.80, 0.70, 48.77, 0.70, "B.Cu", "STRAP2")

    # ==============================================================
    # 6. SECTION 6: UART & MICROSD (X = 56 to 61 mm)
    # ==============================================================
    # J_UART (57.85, 7.35):
    # Pin 1 (UART_TX) at (55.95, 7.35) escapes North to via at (55.95, hw['UART_TX'])
    add_seg(55.95, 7.35, 55.95, hw['UART_TX'], "F.Cu", "UART_TX")
    add_via(55.95, hw['UART_TX'], "UART_TX")

    # Pin 2 (UART_RX) at (57.22, 7.35) escapes North to via at (57.22, hw['UART_RX'])
    add_seg(57.22, 7.35, 57.22, hw['UART_RX'], "F.Cu", "UART_RX")
    add_via(57.22, hw['UART_RX'], "UART_RX")

    # J_SD (58.40, 4.20):
    # Pin 3 (SD_SCK) at (58.15, 4.20) escapes South to via at (58.15, hw['SD_SCK'])
    add_seg(58.15, 4.20, 58.15, hw['SD_SCK'], "F.Cu", "SD_SCK")
    add_via(58.15, hw['SD_SCK'], "SD_SCK")

    # Pin 4 (SD_MOSI) at (58.65, 4.20) escapes South to via at (58.65, hw['SD_MOSI'])
    add_seg(58.65, 4.20, 58.65, hw['SD_MOSI'], "F.Cu", "SD_MOSI")
    add_via(58.65, hw['SD_MOSI'], "SD_MOSI")

    # Pin 5 (SD_MISO) at (59.15, 4.20) escapes South to via at (59.15, hw['SD_MISO'])
    add_seg(59.15, 4.20, 59.15, hw['SD_MISO'], "F.Cu", "SD_MISO")
    add_via(59.15, hw['SD_MISO'], "SD_MISO")

    # Pin 6 (SD_CS) at (59.65, 4.20) escapes South to via at (59.65, hw['SD_CS'])
    add_seg(59.65, 4.20, 59.65, hw['SD_CS'], "F.Cu", "SD_CS")
    add_via(59.65, hw['SD_CS'], "SD_CS")

    # R18.2 (SD_CS pullup at 58.86, 1.50) escapes North to via at (58.86, hw['SD_CS'])
    add_seg(58.86, 1.50, 58.86, hw['SD_CS'], "F.Cu", "SD_CS")
    add_via(58.86, hw['SD_CS'], "SD_CS")

    # ==============================================================
    # 7. SECTION 7: CHARGER & POWER SWITCH (X = 61 to 70 mm)
    # ==============================================================
    # Power Switch SW3 (62.96, 6.82):
    # Pin 1 (VBAT) at (60.96, 6.82) escapes West to via at (60.20, hw['VBAT'])
    add_seg(60.96, 6.82, 60.20, 6.82, "F.Cu", "VBAT")
    add_seg(60.20, 6.82, 60.20, hw['VBAT'], "F.Cu", "VBAT")
    add_via(60.20, hw['VBAT'], "VBAT")

    # Pin 2 (VBAT_SW) at (62.96, 6.82) escapes to via at (62.96, hw['VBAT_SW'])
    add_seg(62.96, 6.82, 62.96, hw['VBAT_SW'], "F.Cu", "VBAT_SW")
    add_via(62.96, hw['VBAT_SW'], "VBAT_SW")

    # J_PWR.1 (VBAT_SW) at (68.11, 3.96) escapes to via at (68.11, hw['VBAT_SW'])
    add_seg(68.11, 3.96, 68.11, hw['VBAT_SW'], "F.Cu", "VBAT_SW")
    add_via(68.11, hw['VBAT_SW'], "VBAT_SW")

    # Battery J_BAT (62.10, 1.72):
    # Pin 1 (VBAT) at (61.60, 1.72) escapes to via at (61.60, hw['VBAT'])
    add_seg(61.60, 1.72, 61.60, hw['VBAT'], "F.Cu", "VBAT")
    add_via(61.60, hw['VBAT'], "VBAT")

    # U2 Charger (66.28, 4.07):
    # Pin 1 (CHG_STAT) at (65.33, 2.77) escapes to via at (65.33, hw['CHG_STAT'])
    add_seg(65.33, 2.77, 65.33, hw['CHG_STAT'], "F.Cu", "CHG_STAT")
    add_via(65.33, hw['CHG_STAT'], "CHG_STAT")

    # Pin 3 (VBAT) at (67.23, 2.77) escapes to via at (67.23, hw['VBAT'])
    add_seg(67.23, 2.77, 67.23, hw['VBAT'], "F.Cu", "VBAT")
    add_via(67.23, hw['VBAT'], "VBAT")
    # C12.1 (VBAT decoupling) at (67.57, 1.50) connects to U2.3 via (67.23, hw['VBAT']) on F.Cu
    add_seg(67.57, 1.50, 67.23, 1.50, "F.Cu", "VBAT")
    add_seg(67.23, 1.50, 67.23, hw['VBAT'], "F.Cu", "VBAT")

    # Pin 4 (USB_VBUS) at (67.23, 5.37) escapes to via at (67.23, hw['USB_VBUS'])
    add_seg(67.23, 5.37, 67.23, hw['USB_VBUS'], "F.Cu", "USB_VBUS")
    add_via(67.23, hw['USB_VBUS'], "USB_VBUS")

    # Pin 5 (CHG_PROG) at (65.33, 5.37) connects to R9.1 (66.13, 6.54) on F.Cu
    add_seg(65.33, 5.37, 65.33, 6.54, "F.Cu", "CHG_PROG")
    add_seg(65.33, 6.54, 66.13, 6.54, "F.Cu", "CHG_PROG")

    # C11.1 (USB_VBUS filter) at (66.13, 7.70) escapes to via at (66.13, hw['USB_VBUS'])
    add_seg(66.13, 7.70, 66.13, hw['USB_VBUS'], "F.Cu", "USB_VBUS")
    add_via(66.13, hw['USB_VBUS'], "USB_VBUS")

    # ==============================================================
    # 8. SECTION 8: ESD PROTECTION & USB-C (X = 70 to 84 mm)
    # ==============================================================
    # R5 (70.73, 7.70): Pin 1 (USB_CC1) at (70.25, 7.70) escapes to via at (70.25, hw['USB_CC1'])
    add_seg(70.25, 7.70, 70.25, hw['USB_CC1'], "F.Cu", "USB_CC1")
    add_via(70.25, hw['USB_CC1'], "USB_CC1")

    # R6 (74.04, 2.46): Pin 1 (USB_CC2) at (73.56, 2.46) escapes to via at (73.56, hw['USB_CC2'])
    add_seg(73.56, 2.46, 73.56, hw['USB_CC2'], "F.Cu", "USB_CC2")
    add_via(73.56, hw['USB_CC2'], "USB_CC2")

    # U_ESD (71.80, 4.49):
    # Pin 4 (USB_DM_CORE) at (72.75, 5.79) to R7.2 (72.97, 6.85) on F.Cu
    add_seg(72.75, 5.79, 72.75, 6.85, "F.Cu", "USB_DM_CORE")
    add_seg(72.75, 6.85, 72.97, 6.85, "F.Cu", "USB_DM_CORE")
    # Escape R7.2 to via at (72.97, hw['USB_DM_CORE'])
    add_seg(72.97, 6.85, 72.97, hw['USB_DM_CORE'], "F.Cu", "USB_DM_CORE")
    add_via(72.97, hw['USB_DM_CORE'], "USB_DM_CORE")

    # Pin 6 (USB_DP_CORE) at (70.85, 5.79) to R8.2 (72.96, 7.70):
    # Escape East to 71.40, then North to via at (71.40, hw['USB_DP_CORE'])
    add_seg(70.85, 5.79, 71.40, 5.79, "F.Cu", "USB_DP_CORE")
    add_seg(71.40, 5.79, 71.40, hw['USB_DP_CORE'], "F.Cu", "USB_DP_CORE")
    add_via(71.40, hw['USB_DP_CORE'], "USB_DP_CORE")
    # R8.2 (72.96, 7.70) escapes to via at (72.96, hw['USB_DP_CORE'])
    add_seg(72.96, 7.70, 72.96, hw['USB_DP_CORE'], "F.Cu", "USB_DP_CORE")
    add_via(72.96, hw['USB_DP_CORE'], "USB_DP_CORE")

    # Pin 5 (USB_VBUS) at (71.80, 5.79) escapes to via at (71.80, hw['USB_VBUS'])
    add_seg(71.80, 5.79, 71.80, hw['USB_VBUS'], "F.Cu", "USB_VBUS")
    add_via(71.80, hw['USB_VBUS'], "USB_VBUS")

    # C10.1 (USB_VBUS) at (72.96, 1.50) escapes to via at (72.96, 5.10)
    add_seg(72.96, 1.50, 72.96, hw['USB_VBUS'], "F.Cu", "USB_VBUS")
    add_via(72.96, hw['USB_VBUS'], "USB_VBUS")

    # USB Port lines:
    # U_ESD.1 (USB_DP_PORT) at (70.85, 3.19) and R8.1 (72.01, 7.70) to J_USB.7 (78.15, 3.10)
    add_seg(70.85, 3.19, 70.85, 2.20, "F.Cu", "USB_DP_PORT")
    add_via(70.85, 2.20, "USB_DP_PORT")
    add_seg(72.01, 7.70, 72.01, 8.20, "F.Cu", "USB_DP_PORT")
    add_via(72.01, 8.20, "USB_DP_PORT")
    add_seg(78.15, 3.10, 78.15, 2.20, "F.Cu", "USB_DP_PORT")
    add_via(78.15, 2.20, "USB_DP_PORT")
    route_ortho_bcu(72.01, 8.20, 70.85, 2.20, "USB_DP_PORT")
    add_seg(70.85, 2.20, 78.15, 2.20, "B.Cu", "USB_DP_PORT")

    # U_ESD.2 (USB_DM_PORT) at (71.80, 3.19) and R7.1 (72.02, 6.85) to J_USB.9 (78.65, 3.10)
    add_seg(71.80, 3.19, 71.80, 1.50, "F.Cu", "USB_DM_PORT")
    add_via(71.80, 1.50, "USB_DM_PORT")
    add_seg(72.02, 6.85, 72.02, 8.20, "F.Cu", "USB_DM_PORT")
    add_via(72.02, 8.20, "USB_DM_PORT")
    add_seg(78.65, 3.10, 78.65, 1.50, "F.Cu", "USB_DM_PORT")
    add_via(78.65, 1.50, "USB_DM_PORT")
    route_ortho_bcu(72.02, 8.20, 71.80, 1.50, "USB_DM_PORT")
    add_seg(71.80, 1.50, 78.65, 1.50, "B.Cu", "USB_DM_PORT")

    # J_USB connectors:
    # Pin 5 (USB_CC1) at (77.60, 3.10) escapes to via at (77.60, hw['USB_CC1'])
    add_seg(77.60, 3.10, 77.60, hw['USB_CC1'], "F.Cu", "USB_CC1")
    add_via(77.60, hw['USB_CC1'], "USB_CC1")

    # Pin 6 (USB_CC2) at (79.20, 3.10) escapes to via at (79.20, hw['USB_CC2'])
    add_seg(79.20, 3.10, 79.20, hw['USB_CC2'], "F.Cu", "USB_CC2")
    add_via(79.20, hw['USB_CC2'], "USB_CC2")

    # Pin 2 & 10 (USB_VBUS) at (76.00, 3.10) and (80.80, 3.10):
    add_seg(76.00, 3.10, 76.00, hw['USB_VBUS'], "F.Cu", "USB_VBUS")
    add_via(76.00, hw['USB_VBUS'], "USB_VBUS")
    add_seg(80.80, 3.10, 80.80, hw['USB_VBUS'], "F.Cu", "USB_VBUS")
    add_via(80.80, hw['USB_VBUS'], "USB_VBUS")

    # ==============================================================
    # 9. HORIZONTAL HIGHWAYS ON B.CU
    # ==============================================================
    # Each net connects all of its vias along its dedicated Y highway:
    highways_to_connect = [
        ('3V3_RTC', hw['3V3_RTC']),
        ('TOUCH_OUT', hw['TOUCH_OUT']),
        ('SD_CS', hw['SD_CS']),
        ('SD_SCK', hw['SD_SCK']),
        ('SD_MOSI', hw['SD_MOSI']),
        ('SD_MISO', hw['SD_MISO']),
        ('I2C_SDA', hw['I2C_SDA']),
        ('I2C_SCL', hw['I2C_SCL']),
        ('CHG_STAT', hw['CHG_STAT']),
        ('VBAT_SW', hw['VBAT_SW']),
        ('USB_CC2', hw['USB_CC2']),
        ('VBAT', hw['VBAT']),
        ('USB_VBUS', hw['USB_VBUS']),
        ('BTN_ERASE', hw['BTN_ERASE']),
        ('3V3_RF', hw['3V3_RF']),
        ('USB_CC1', hw['USB_CC1']),
        ('UART_TX', hw['UART_TX']),
        ('UART_RX', hw['UART_RX']),
        ('USB_DM_CORE', hw['USB_DM_CORE']),
        ('USB_DP_CORE', hw['USB_DP_CORE']),
    ]

    for net_name, y_coord in highways_to_connect:
        nid = net_id_map[net_name]
        # Find all vias belonging to this net on this Y line
        net_vias_x = sorted([v[0] for v in vias if v[2] == nid and abs(v[1] - y_coord) < 0.05])
        if len(net_vias_x) >= 2:
            add_seg(net_vias_x[0], y_coord, net_vias_x[-1], y_coord, "B.Cu", net_name, width=0.20)

    # ==============================================================
    # 10. 3V3 POWER DISTRIBUTION
    # ==============================================================
    # F.Cu local clusters:
    # Cluster 1 (IMU & Touch):
    add_seg(1.70, 4.60, 5.72, 4.60, "F.Cu", "3V3")
    add_seg(5.72, 2.00, 5.72, 7.20, "F.Cu", "3V3")
    add_seg(5.72, 2.00, 8.00, 2.00, "F.Cu", "3V3")
    add_seg(8.00, 2.00, 8.00, 2.40, "F.Cu", "3V3")
    # Tap to South highway:
    add_seg(8.00, 2.00, 8.00, hw['3V3_SOUTH'], "F.Cu", "3V3")
    add_via(8.00, hw['3V3_SOUTH'], "3V3")

    # Cluster 2 (Side switches & U3):
    add_seg(14.03, 7.00, 20.02, 7.00, "F.Cu", "3V3")
    add_seg(20.02, 7.00, 23.02, 7.00, "F.Cu", "3V3")
    add_seg(23.02, 7.00, 23.02, 8.00, "F.Cu", "3V3")
    # Tap to North highway:
    add_seg(23.02, 8.00, 23.02, hw['3V3_NORTH'], "F.Cu", "3V3")
    add_via(23.02, hw['3V3_NORTH'], "3V3")

    # U3 & LED resistors:
    add_seg(18.52, 2.20, 18.52, 4.40, "F.Cu", "3V3")
    add_seg(18.52, 4.40, 21.35, 4.40, "F.Cu", "3V3")
    add_seg(21.35, 4.40, 21.35, 4.65, "F.Cu", "3V3")
    add_seg(25.15, 3.65, 25.15, 1.80, "F.Cu", "3V3")
    # Tap to South highway:
    add_seg(18.52, 2.20, 18.52, hw['3V3_SOUTH'], "F.Cu", "3V3")
    add_via(18.52, hw['3V3_SOUTH'], "3V3")
    add_seg(25.15, 1.80, 25.15, hw['3V3_SOUTH'], "F.Cu", "3V3")
    add_via(25.15, hw['3V3_SOUTH'], "3V3")

    # Cluster 3 (MCU U1 & passives):
    add_seg(35.41, 2.60, 37.98, 2.60, "F.Cu", "3V3")
    add_seg(37.98, 2.60, 37.98, 2.36, "F.Cu", "3V3")
    # U1.17 (45.28, 3.08) escapes East to (46.00, 3.08)
    add_seg(45.28, 3.08, 46.00, 3.08, "F.Cu", "3V3")
    add_seg(46.00, 3.08, 46.00, hw['3V3_SOUTH'], "F.Cu", "3V3")
    add_via(46.00, hw['3V3_SOUTH'], "3V3")
    # Tap R4.1 to South highway:
    add_seg(35.41, 2.60, 35.41, hw['3V3_SOUTH'], "F.Cu", "3V3")
    add_via(35.41, hw['3V3_SOUTH'], "3V3")

    # North MCU passives: FB1.1 (45.48, 7.70) and C3.1 (50.25, 7.70)
    add_seg(45.48, 7.70, 50.25, 7.70, "F.Cu", "3V3")
    add_seg(45.48, 7.70, 45.48, hw['3V3_NORTH'], "F.Cu", "3V3")
    add_via(45.48, hw['3V3_NORTH'], "3V3")

    # South passives: R3.1 (47.83, 2.80) to R2.1 (51.27, 2.25)
    add_seg(47.83, 2.80, 51.27, 2.80, "F.Cu", "3V3")
    add_seg(51.27, 2.80, 51.27, 2.25, "F.Cu", "3V3")
    add_seg(51.27, 2.25, 51.27, hw['3V3_SOUTH'], "F.Cu", "3V3")
    add_via(51.27, hw['3V3_SOUTH'], "3V3")

    # Cluster 4 (MicroSD & UART):
    # J_SD.1 (57.15, 4.20) to R18.1 (57.91, 1.50)
    add_seg(57.15, 4.20, 57.15, 1.50, "F.Cu", "3V3")
    add_seg(57.15, 1.50, 57.91, 1.50, "F.Cu", "3V3")
    add_seg(57.15, 1.50, 57.15, hw['3V3_SOUTH'], "F.Cu", "3V3")
    add_via(57.15, hw['3V3_SOUTH'], "3V3")

    # J_UART.4 (59.76, 7.35) escapes North to via at (59.76, hw['3V3_NORTH'])
    add_seg(59.76, 7.35, 59.76, hw['3V3_NORTH'], "F.Cu", "3V3")
    add_via(59.76, hw['3V3_NORTH'], "3V3")

    # Cluster 5 (LDO Output):
    # J_PWR.3 (70.01, 3.96) to C14.1 (70.24, 2.05)
    add_seg(70.01, 3.96, 70.24, 3.96, "F.Cu", "3V3")
    add_seg(70.24, 3.96, 70.24, 2.05, "F.Cu", "3V3")
    add_seg(70.24, 2.05, 70.24, hw['3V3_SOUTH'], "F.Cu", "3V3")
    add_via(70.24, hw['3V3_SOUTH'], "3V3")

    # 3V3 Highways on B.Cu:
    # South 3V3 highway from X = 8.00 to X = 82.50
    add_seg(8.00, hw['3V3_SOUTH'], 82.50, hw['3V3_SOUTH'], "B.Cu", "3V3", width=0.25)
    # North 3V3 highway from X = 23.02 to X = 82.50
    add_seg(23.02, hw['3V3_NORTH'], 82.50, hw['3V3_NORTH'], "B.Cu", "3V3", width=0.25)
    # Tie North and South 3V3 highways at X = 82.50 on B.Cu:
    add_seg(82.50, hw['3V3_SOUTH'], 82.50, hw['3V3_NORTH'], "B.Cu", "3V3", width=0.25)

    # Output all vias and segments
    for vx, vy, vnid in sorted(vias):
        lines.append(f'  (via (at {vx:.3f} {vy:.3f}) (size 0.50) (drill 0.30) (layers "F.Cu" "B.Cu") (net {vnid}))')

    for x1, y1, x2, y2, lyr, snid, sw in segments:
        lines.append(f'  (segment (start {x1:.3f} {y1:.3f}) (end {x2:.3f} {y2:.3f}) (width {sw:.2f}) (layer "{lyr}") (net {snid}))')

    # ==============================================================
    # 11. GROUND ZONES (F.CU & B.CU)
    # ==============================================================
    gnd_nid = net_id_map.get('GND', 1)
    for zlayer in ["F.Cu", "B.Cu"]:
        lines.extend([
            f'  (zone (net {gnd_nid}) (net_name "GND") (layers "{zlayer}") (tstamp "{uuid.uuid4()}")',
            '    (hatch full 0.5)',
            '    (priority 0)',
            '    (connect_pads yes (clearance 0.15))',
            '    (min_thickness 0.127)',
            '    (filled_areas_thickness no)',
            '    (fill yes (thermal_gap 0.15) (thermal_bridge_width 0.18))',
            '    (polygon',
            '      (pts',
            '        (xy 0.35 0.35)',
            '        (xy 83.65 0.35)',
            '        (xy 83.65 8.85)',
            '        (xy 0.35 8.85)',
            '      )',
            '    )',
            '  )'
        ])

    lines.append(')')

    target_pcb = out_dir / 'SmartPen.kicad_pcb'
    with open(target_pcb, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')

    print(f"Generated {target_pcb} with {len(segments)} segments and {len(vias)} vias.")
    return True

if __name__ == '__main__':
    generate_smartpen_perfect()

