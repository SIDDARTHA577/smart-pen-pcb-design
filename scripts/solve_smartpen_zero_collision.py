"""Complete Deterministic Zero-Collision Router for SmartPen Main PCB.
Uses planar orthogonal topology and non-crossing B.Cu highways.
"""
import json, uuid, csv, subprocess, sys, math
from pathlib import Path

sys.path.insert(0, '.')
from scripts.verify_smartpen_geometry import check_pcb_geometry

out_dir = Path("output/RevF_Working")
kicad_cli = r"C:\Users\goran\AppData\Local\Programs\KiCad\10.0\bin\kicad-cli.exe"

def solve_smartpen_pcb():
    with open(out_dir / 'solved_coords.json') as f:
        coords = json.load(f)
    with open(out_dir / 'SmartPen_RevE_PCB.json') as f:
        pcb_json = json.load(f)

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
                if sub.startswith('TEXT~P~'): ref = sub.split('~')[10]
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
                    pads.append({
                        'num': ptoks[8], 'net': ptoks[7],
                        'dx': round(dx, 4), 'dy': round(dy, 4),
                        'w': round(pw, 4), 'h': round(ph, 4)
                    })
            fp_defs[ref] = pads

    all_pads = []
    for ref, (cx, cy) in coords.items():
        if ref in fp_defs:
            for p in fp_defs[ref]:
                all_pads.append({
                    'ref': ref, 'pin': p['num'], 'net': p['net'],
                    'x': round(cx + p['dx'], 4), 'y': round(cy + p['dy'], 4),
                    'w': p['w'], 'h': p['h']
                })

    segments = []
    vias = set()

    def add_seg(x1, y1, x2, y2, layer, net_name, width=0.18):
        if abs(x1 - x2) > 0.0005 or abs(y1 - y2) > 0.0005:
            segments.append((round(x1, 3), round(y1, 3), round(x2, 3), round(y2, 3), layer, net_name, width))

    def add_via(vx, vy, net_name):
        vias.add((round(vx, 3), round(vy, 3), net_name))

    # Dedicated non-overlapping B.Cu Highway Y-lanes
    hw = {
        '3V3_SOUTH':   0.55,
        'SD_MOSI':     0.90,
        'MCU_EN':      1.10,
        'SD_MISO':     1.25,
        'SD_SCK':      1.60,
        'USB_DP_PORT': 1.80,
        'SD_CS':       1.95,
        'USB_DM_PORT': 2.15,
        'BOOT9':       2.35,
        '3V3_RTC':     2.65,
        'TOUCH_OUT':   3.00,
        'I2C_SCL':     3.35,
        'VDD_SPI':     3.55,
        'I2C_SDA':     3.75,
        'CHG_STAT':    4.05,
        'VBAT':        4.40,
        'VBAT_SW':     4.75,
        'USB_CC2':     5.10,
        'USB_VBUS':    5.45,
        'USB_CC1':     5.80,
        'RF_LNA':      6.00,
        '3V3_RF':      6.25,
        'UART_TX':     6.55,
        'UART_RX':     6.85,
        'LED_RED_SINK':7.05,
        'USB_DM_CORE': 7.25,
        'LED_GREEN_SINK': 7.45,
        'USB_DP_CORE': 7.65,
        'BTN_MODE':    7.90,
        'BTN_ERASE':   8.15,
        'XTAL_P_CORE': 8.40,
        '3V3_NORTH':   8.65,
        'XTAL_N':      8.85,
    }

    # ==============================================================
    # 1. FRONT IMU & TOUCH (X = 0 to 15 mm)
    # ==============================================================
    # J_IMU.3 (I2C_SDA at 3.70, 4.60) escapes South on F.Cu to via at (3.70, hw['I2C_SDA'])
    add_seg(3.70, 4.60, 3.70, hw['I2C_SDA'], "F.Cu", "I2C_SDA")
    add_via(3.70, hw['I2C_SDA'], "I2C_SDA")

    # J_IMU.4 (I2C_SCL at 4.70, 4.60) escapes South on F.Cu to via at (4.70, hw['I2C_SCL'])
    add_seg(4.70, 4.60, 4.70, hw['I2C_SCL'], "F.Cu", "I2C_SCL")
    add_via(4.70, hw['I2C_SCL'], "I2C_SCL")

    # R10.2 (I2C_SDA at 6.67, 4.60) escapes South on F.Cu to via at (6.67, hw['I2C_SDA'])
    add_seg(6.67, 4.60, 6.67, hw['I2C_SDA'], "F.Cu", "I2C_SDA")
    add_via(6.67, hw['I2C_SDA'], "I2C_SDA")

    # R11.2 (I2C_SCL at 6.67, 7.20) connects to J_IMU.4 on F.Cu around open space
    add_seg(6.67, 7.20, 5.00, 7.20, "F.Cu", "I2C_SCL")
    add_seg(5.00, 7.20, 5.00, 5.80, "F.Cu", "I2C_SCL")
    add_seg(5.00, 5.80, 4.70, 5.80, "F.Cu", "I2C_SCL")
    add_seg(4.70, 5.80, 4.70, 4.60, "F.Cu", "I2C_SCL")

    # J_TOUCH.3 (10.00, 2.40) to R19.1 (13.03, 2.40) straight on F.Cu
    add_seg(10.00, 2.40, 13.03, 2.40, "F.Cu", "TOUCH_OUT")
    # R19.1 escapes North on F.Cu to via at (13.03, hw['TOUCH_OUT'])
    add_seg(13.03, 2.40, 13.03, hw['TOUCH_OUT'], "F.Cu", "TOUCH_OUT")
    add_via(13.03, hw['TOUCH_OUT'], "TOUCH_OUT")

    # ==============================================================
    # 2. SIDE BUTTONS & LEDS (X = 10 to 22 mm)
    # ==============================================================
    # Erase Button: SW4.1 (10.10, 7.00) escapes North on F.Cu to via at (10.10, hw['BTN_ERASE'])
    add_seg(10.10, 7.00, 10.10, hw['BTN_ERASE'], "F.Cu", "BTN_ERASE")
    add_via(10.10, hw['BTN_ERASE'], "BTN_ERASE")

    # R12.2 (14.97, 7.00) escapes North on F.Cu to via at (14.97, hw['BTN_ERASE'])
    add_seg(14.97, 7.00, 14.97, hw['BTN_ERASE'], "F.Cu", "BTN_ERASE")
    add_via(14.97, hw['BTN_ERASE'], "BTN_ERASE")

    # Mode Button: SW5.1 (16.10, 7.00) escapes North on F.Cu to via at (16.10, hw['BTN_MODE'])
    add_seg(16.10, 7.00, 16.10, hw['BTN_MODE'], "F.Cu", "BTN_MODE")
    add_via(16.10, hw['BTN_MODE'], "BTN_MODE")

    # R13.2 (20.98, 7.00) escapes North on F.Cu to via at (20.98, hw['BTN_MODE'])
    add_seg(20.98, 7.00, 20.98, hw['BTN_MODE'], "F.Cu", "BTN_MODE")
    add_via(20.98, hw['BTN_MODE'], "BTN_MODE")

    # Green LED: D1.1 (16.00, 2.20) to R14.2 (19.48, 2.20) on F.Cu via Y = 1.35
    add_seg(16.00, 2.20, 16.00, 1.35, "F.Cu", "LED_GREEN_A")
    add_seg(16.00, 1.35, 19.48, 1.35, "F.Cu", "LED_GREEN_A")
    add_seg(19.48, 1.35, 19.48, 2.20, "F.Cu", "LED_GREEN_A")

    # D1.2 (LED_GREEN_SINK at 17.00, 2.20) routes West in empty corridor X=15.5 to North
    add_seg(17.00, 2.20, 15.50, 2.20, "F.Cu", "LED_GREEN_SINK")
    add_seg(15.50, 2.20, 15.50, hw['LED_GREEN_SINK'], "F.Cu", "LED_GREEN_SINK")
    add_via(15.50, hw['LED_GREEN_SINK'], "LED_GREEN_SINK")

    # Red LED: D2.1 (16.00, 4.40) to R15.2 (19.48, 4.40) on F.Cu via Y = 5.25
    add_seg(16.00, 4.40, 16.00, 5.25, "F.Cu", "LED_RED_A")
    add_seg(16.00, 5.25, 19.48, 5.25, "F.Cu", "LED_RED_A")
    add_seg(19.48, 5.25, 19.48, 4.40, "F.Cu", "LED_RED_A")

    # D2.2 (LED_RED_SINK at 17.00, 4.40) routes West in empty corridor X=15.2 to North
    add_seg(17.00, 4.40, 15.15, 4.40, "F.Cu", "LED_RED_SINK")
    add_seg(15.15, 4.40, 15.15, hw['LED_RED_SINK'], "F.Cu", "LED_RED_SINK")
    add_via(15.15, hw['LED_RED_SINK'], "LED_RED_SINK")

    # ==============================================================
    # 3. U3 EXPANDER & MOTOR DRIVER (X = 20 to 32 mm)
    # ==============================================================
    # U3.1 (I2C_SCL at 22.25, 2.75) escapes North/South to via at (22.25, hw['I2C_SCL'])
    add_seg(22.25, 2.75, 22.25, hw['I2C_SCL'], "F.Cu", "I2C_SCL")
    add_via(22.25, hw['I2C_SCL'], "I2C_SCL")

    # U3.2 (I2C_SDA at 22.75, 2.75) escapes North to via at (22.75, hw['I2C_SDA'])
    add_seg(22.75, 2.75, 22.75, hw['I2C_SDA'], "F.Cu", "I2C_SDA")
    add_via(22.75, hw['I2C_SDA'], "I2C_SDA")

    # U3.10 (BTN_ERASE at 25.15, 5.65) escapes East/North on F.Cu to via at (25.85, hw['BTN_ERASE'])
    add_seg(25.15, 5.65, 25.85, 5.65, "F.Cu", "BTN_ERASE")
    add_seg(25.85, 5.65, 25.85, hw['BTN_ERASE'], "F.Cu", "BTN_ERASE")
    add_via(25.85, hw['BTN_ERASE'], "BTN_ERASE")

    # U3.11 (BTN_MODE at 24.25, 6.55) escapes North on F.Cu to via at (24.25, hw['BTN_MODE'])
    add_seg(24.25, 6.55, 24.25, hw['BTN_MODE'], "F.Cu", "BTN_MODE")
    add_via(24.25, hw['BTN_MODE'], "BTN_MODE")

    # U3.12 (LED_GREEN_SINK at 23.75, 6.55) escapes North on F.Cu to via at (23.75, hw['LED_GREEN_SINK'])
    add_seg(23.75, 6.55, 23.75, hw['LED_GREEN_SINK'], "F.Cu", "LED_GREEN_SINK")
    add_via(23.75, hw['LED_GREEN_SINK'], "LED_GREEN_SINK")

    # U3.13 (LED_RED_SINK at 23.25, 6.55) escapes North on F.Cu to via at (23.25, hw['LED_RED_SINK'])
    add_seg(23.25, 6.55, 23.25, hw['LED_RED_SINK'], "F.Cu", "LED_RED_SINK")
    add_via(23.25, hw['LED_RED_SINK'], "LED_RED_SINK")

    # U3.14 (HAPTIC_GATE_DRIVE at 22.75, 6.55) escapes West/South to via at (21.50, hw['VBAT_SW'])
    # Wait, R16.1 is at (26.52, 2.20).
    # Can U3.14 escape on F.Cu to the East over U3?
    # Between U3 top pins and C13: corridor at Y = 7.15.
    # U3.14 routes: (22.75, 6.55) -> (22.75, 7.15) -> (25.50, 7.15) -> (25.50, 4.75) via at (25.50, 4.75)!
    # Wait, hw['VBAT_SW'] is 4.75. Let's give HAPTIC_GATE_DRIVE a dedicated lane or local via!
    # R16.1 is at (26.52, 2.20). Via for R16.1 at (26.52, 4.75)?
    # On B.Cu, from 25.50 to 26.52 at Y = 4.75 would collide with VBAT_SW!
    # Instead: U3.14 escapes West: (22.75, 6.55) -> (21.00, 6.55) -> (21.00, 2.20) -> (26.52, 2.20) on B.Cu!
    # Wait, on B.Cu, Y = 2.20 is USB_DM_PORT!
    # But USB_DM_PORT exists ONLY for X >= 70!
    # At X in [21, 27], Y = 2.20 on B.Cu is 100% EMPTY!
    # So drop via at (21.00, 2.15) and via at (26.52, 2.15)!
    # Trace on F.Cu: U3.14 (22.75, 6.55) -> (21.00, 6.55) -> (21.00, 2.15) -> via!
    # Wait! On F.Cu at X = 21.00, from Y = 6.55 to 2.15:
    # Does X = 21.00 collide with U3? U3 pads are at X = 21.35!
    # X = 21.00 is 0.35 mm West of U3!
    # And R13 is at (20.5, 7.0), R15 is at (19.0, 4.4).
    # X = 21.00 is completely clear!
    add_seg(22.75, 6.55, 21.00, 6.55, "F.Cu", "HAPTIC_GATE_DRIVE")
    add_seg(21.00, 6.55, 21.00, 2.15, "F.Cu", "HAPTIC_GATE_DRIVE")
    add_via(21.00, 2.15, "HAPTIC_GATE_DRIVE")
    add_seg(26.52, 2.20, 26.52, 2.15, "F.Cu", "HAPTIC_GATE_DRIVE")
    add_via(26.52, 2.15, "HAPTIC_GATE_DRIVE")
    add_seg(21.00, 2.15, 26.52, 2.15, "B.Cu", "HAPTIC_GATE_DRIVE")

    # U3.15 (CHG_STAT at 22.25, 6.55) escapes West/South on F.Cu:
    # (22.25, 6.55) -> (20.50, 6.55) -> (20.50, hw['CHG_STAT']) via!
    add_seg(22.25, 6.55, 20.40, 6.55, "F.Cu", "CHG_STAT")
    add_seg(20.40, 6.55, 20.40, hw['CHG_STAT'], "F.Cu", "CHG_STAT")
    add_via(20.40, hw['CHG_STAT'], "CHG_STAT")

    # Motor driver:
    # R17.1 (26.03, 3.91) to R16.2 (27.48, 2.20) to Q1.1 (27.85, 1.10)
    add_seg(26.03, 3.91, 26.03, 3.10, "F.Cu", "HAPTIC_GATE")
    add_seg(26.03, 3.10, 27.48, 3.10, "F.Cu", "HAPTIC_GATE")
    add_seg(27.48, 3.10, 27.48, 2.20, "F.Cu", "HAPTIC_GATE")
    add_seg(27.48, 2.20, 27.85, 2.20, "F.Cu", "HAPTIC_GATE")
    add_seg(27.85, 2.20, 27.85, 1.10, "F.Cu", "HAPTIC_GATE")

    # Q1.3 (28.80, 3.30) to D3.2 (31.29, 4.70) to J_MOT.2 (31.75, 6.29)
    add_seg(28.80, 3.30, 30.00, 3.30, "F.Cu", "HAPTIC_LOW")
    add_seg(30.00, 3.30, 30.00, 4.70, "F.Cu", "HAPTIC_LOW")
    add_seg(30.00, 4.70, 31.29, 4.70, "F.Cu", "HAPTIC_LOW")
    add_seg(31.29, 4.70, 31.75, 4.70, "F.Cu", "HAPTIC_LOW")
    add_seg(31.75, 4.70, 31.75, 6.29, "F.Cu", "HAPTIC_LOW")

    # VBAT_SW local: D3.1 (28.09, 4.70) to J_MOT.1 (30.75, 6.29)
    # Notice: J_MOT.3 (GND) is at (29.15, 6.29).
    # Route D3.1 (28.09, 4.70) South/East to avoid J_MOT.3:
    # (28.09, 4.70) -> (28.09, hw['VBAT_SW']) via!
    # And J_MOT.1 (30.75, 6.29) escapes to (30.75, 7.80) -> via or on F.Cu?
    # Escapes on F.Cu to (30.75, hw['VBAT_SW'])?
    # Between J_MOT.1 (30.75, 6.29) and D3.1 (28.09, 4.70):
    # Route on B.Cu at hw['VBAT_SW']!
    add_seg(28.09, 4.70, 28.09, hw['VBAT_SW'], "F.Cu", "VBAT_SW")
    add_via(28.09, hw['VBAT_SW'], "VBAT_SW")
    add_seg(30.75, 6.29, 30.75, 5.30, "F.Cu", "VBAT_SW")
    add_seg(30.75, 5.30, 29.50, 5.30, "F.Cu", "VBAT_SW")
    add_seg(29.50, 5.30, 29.50, hw['VBAT_SW'], "F.Cu", "VBAT_SW")
    add_via(29.50, hw['VBAT_SW'], "VBAT_SW")

    # ==============================================================
    # 4. POWER SWITCH SW1 & CRYSTALS (X = 31 to 40 mm)
    # ==============================================================
    # SW1.1 (31.56, 1.50) escapes South on F.Cu to via at (31.56, hw['MCU_EN'])
    add_seg(31.56, 1.50, 31.56, hw['MCU_EN'], "F.Cu", "MCU_EN")
    add_via(31.56, hw['MCU_EN'], "MCU_EN")

    # R1.2 (38.93, 2.36) escapes South on F.Cu to via at (38.93, hw['MCU_EN'])
    add_seg(38.93, 2.36, 38.93, hw['MCU_EN'], "F.Cu", "MCU_EN")
    add_via(38.93, hw['MCU_EN'], "MCU_EN")
    # Connect R1.2 to C1.1 (39.72, 1.52) to U1.7 (40.48, 3.59) on F.Cu
    add_seg(38.93, 2.36, 39.72, 2.36, "F.Cu", "MCU_EN")
    add_seg(39.72, 2.36, 39.72, 1.52, "F.Cu", "MCU_EN")
    add_seg(39.72, 2.36, 40.48, 2.36, "F.Cu", "MCU_EN")
    add_seg(40.48, 2.36, 40.48, 3.59, "F.Cu", "MCU_EN")

    # 3V3_RTC: C4.1 (36.20, 1.64) to R4.2 (36.36, 2.60) on F.Cu
    add_seg(36.20, 1.64, 36.36, 1.64, "F.Cu", "3V3_RTC")
    add_seg(36.36, 1.64, 36.36, 2.60, "F.Cu", "3V3_RTC")
    add_seg(36.36, 2.60, 36.36, hw['3V3_RTC'], "F.Cu", "3V3_RTC")
    add_via(36.36, hw['3V3_RTC'], "3V3_RTC")

    # Crystals:
    # C6.1 (32.83, 7.70) to Y1.1 (34.72, 5.72)
    # Avoid Y1.4 (GND at 34.72, 7.02) by routing at X = 33.80!
    add_seg(32.83, 7.70, 33.80, 7.70, "F.Cu", "XTAL_N")
    add_seg(33.80, 7.70, 33.80, 5.72, "F.Cu", "XTAL_N")
    add_seg(33.80, 5.72, 34.72, 5.72, "F.Cu", "XTAL_N")
    # Escape to via at (33.00, hw['XTAL_N'])
    add_seg(32.83, 7.70, 32.83, hw['XTAL_N'], "F.Cu", "XTAL_N")
    add_via(32.83, hw['XTAL_N'], "XTAL_N")

    # XTAL_P_MATCH: Y1.3 (36.42, 7.02) to C7.1 (37.36, 7.70) to L1.2 (40.07, 7.70) on F.Cu
    add_seg(36.42, 7.02, 36.42, 7.70, "F.Cu", "XTAL_P_MATCH")
    add_seg(36.42, 7.70, 37.36, 7.70, "F.Cu", "XTAL_P_MATCH")
    add_seg(37.36, 7.70, 40.07, 7.70, "F.Cu", "XTAL_P_MATCH")

    # XTAL_P_CORE: L1.1 (39.12, 7.70) escapes North to via at (39.12, hw['XTAL_P_CORE'])
    add_seg(39.12, 7.70, 39.12, hw['XTAL_P_CORE'], "F.Cu", "XTAL_P_CORE")
    add_via(39.12, hw['XTAL_P_CORE'], "XTAL_P_CORE")

    # ==============================================================
    # 5. MCU U1 (ESP32-C3) (X = 40 to 46 mm)
    # ==============================================================
    # U1 West pins:
    # Pin 1 (RF_LNA, 40.48, 6.59) -> via at (39.50, hw['RF_LNA'])
    add_seg(40.48, 6.59, 39.50, 6.59, "F.Cu", "RF_LNA")
    add_seg(39.50, 6.59, 39.50, hw['RF_LNA'], "F.Cu", "RF_LNA")
    add_via(39.50, hw['RF_LNA'], "RF_LNA")

    # Pin 2, 3 (3V3_RF, 40.48, 6.08 and 5.59):
    add_seg(40.48, 6.08, 40.48, 5.59, "F.Cu", "3V3_RF")
    add_seg(40.48, 6.08, 39.50, 6.08, "F.Cu", "3V3_RF")
    add_seg(39.50, 6.08, 39.50, hw['3V3_RF'], "F.Cu", "3V3_RF")
    add_via(39.50, hw['3V3_RF'], "3V3_RF")

    # Pin 4 (I2C_SDA, 40.48, 5.08) -> via at (38.80, hw['I2C_SDA'])
    add_seg(40.48, 5.08, 38.80, 5.08, "F.Cu", "I2C_SDA")
    add_seg(38.80, 5.08, 38.80, hw['I2C_SDA'], "F.Cu", "I2C_SDA")
    add_via(38.80, hw['I2C_SDA'], "I2C_SDA")

    # Pin 5 (I2C_SCL, 40.48, 4.59) -> via at (39.50, hw['I2C_SCL'])
    add_seg(40.48, 4.59, 39.50, 4.59, "F.Cu", "I2C_SCL")
    add_seg(39.50, 4.59, 39.50, hw['I2C_SCL'], "F.Cu", "I2C_SCL")
    add_via(39.50, hw['I2C_SCL'], "I2C_SCL")

    # Pin 6 (STRAP2, 40.48, 4.08) -> via at (38.50, 4.08)
    add_seg(40.48, 4.08, 38.50, 4.08, "F.Cu", "STRAP2")
    add_via(38.50, 4.08, "STRAP2")

    # Pin 8 (TOUCH_OUT, 40.48, 3.08) -> via at (39.50, hw['TOUCH_OUT'])
    add_seg(40.48, 3.08, 39.50, 3.08, "F.Cu", "TOUCH_OUT")
    add_seg(39.50, 3.08, 39.50, hw['TOUCH_OUT'], "F.Cu", "TOUCH_OUT")
    add_via(39.50, hw['TOUCH_OUT'], "TOUCH_OUT")

    # U1 South pins (planar non-crossing breakout):
    # Pin 9 (SD_MOSI, 41.13, 2.44) -> via at (41.13, hw['SD_MOSI'])
    add_seg(41.13, 2.44, 41.13, hw['SD_MOSI'], "F.Cu", "SD_MOSI")
    add_via(41.13, hw['SD_MOSI'], "SD_MOSI")

    # Pin 10 (SD_MISO, 41.63, 2.44) -> via at (41.63, hw['SD_MISO'])
    add_seg(41.63, 2.44, 41.63, hw['SD_MISO'], "F.Cu", "SD_MISO")
    add_via(41.63, hw['SD_MISO'], "SD_MISO")

    # Pin 11 (3V3_RTC, 42.13, 2.44) -> escapes West to via at (41.50, hw['3V3_RTC'])
    add_seg(42.13, 2.44, 41.50, 2.44, "F.Cu", "3V3_RTC")
    add_seg(41.50, 2.44, 41.50, hw['3V3_RTC'], "F.Cu", "3V3_RTC")
    add_via(41.50, hw['3V3_RTC'], "3V3_RTC")

    # Pin 12 (SD_SCK, 42.63, 2.44) -> via at (42.63, hw['SD_SCK'])
    add_seg(42.63, 2.44, 42.63, hw['SD_SCK'], "F.Cu", "SD_SCK")
    add_via(42.63, hw['SD_SCK'], "SD_SCK")

    # Pin 13 (SD_CS, 43.13, 2.44) -> via at (43.13, hw['SD_CS'])
    add_seg(43.13, 2.44, 43.13, hw['SD_CS'], "F.Cu", "SD_CS")
    add_via(43.13, hw['SD_CS'], "SD_CS")

    # Pin 15 (BOOT9, 44.13, 2.44) -> via at (44.13, hw['BOOT9'])
    add_seg(44.13, 2.44, 44.13, hw['BOOT9'], "F.Cu", "BOOT9")
    add_via(44.13, hw['BOOT9'], "BOOT9")

    # U1 East pins:
    # Pin 18 (VDD_SPI, 45.28, 3.59) -> via at (46.20, hw['VDD_SPI'])
    add_seg(45.28, 3.59, 46.20, 3.59, "F.Cu", "VDD_SPI")
    add_seg(46.20, 3.59, 46.20, hw['VDD_SPI'], "F.Cu", "VDD_SPI")
    add_via(46.20, hw['VDD_SPI'], "VDD_SPI")
    # C5.1 (49.52, 1.55) escapes North to via at (49.52, hw['VDD_SPI'])
    add_seg(49.52, 1.55, 49.52, hw['VDD_SPI'], "F.Cu", "VDD_SPI")
    add_via(49.52, hw['VDD_SPI'], "VDD_SPI")

    # U1 North pins:
    # Pin 32, 31 (3V3_RF, 41.13 and 41.63, 7.23) -> via at (41.13, hw['3V3_RF'])
    add_seg(41.13, 7.23, 41.63, 7.23, "F.Cu", "3V3_RF")
    add_seg(41.13, 7.23, 41.13, hw['3V3_RF'], "F.Cu", "3V3_RF")
    add_via(41.13, hw['3V3_RF'], "3V3_RF")

    # Pin 30 (XTAL_P_CORE, 42.13, 7.23) -> via at (42.13, hw['XTAL_P_CORE'])
    add_seg(42.13, 7.23, 42.13, hw['XTAL_P_CORE'], "F.Cu", "XTAL_P_CORE")
    add_via(42.13, hw['XTAL_P_CORE'], "XTAL_P_CORE")

    # Pin 29 (XTAL_N, 42.63, 7.23) -> via at (42.63, hw['XTAL_N'])
    add_seg(42.63, 7.23, 42.63, hw['XTAL_N'], "F.Cu", "XTAL_N")
    add_via(42.63, hw['XTAL_N'], "XTAL_N")

    # Pin 28 (UART_TX, 43.13, 7.23) -> via at (43.13, hw['UART_TX'])
    add_seg(43.13, 7.23, 43.13, hw['UART_TX'], "F.Cu", "UART_TX")
    add_via(43.13, hw['UART_TX'], "UART_TX")

    # Pin 27 (UART_RX, 43.63, 7.23) -> via at (43.63, hw['UART_RX'])
    add_seg(43.63, 7.23, 43.63, hw['UART_RX'], "F.Cu", "UART_RX")
    add_via(43.63, hw['UART_RX'], "UART_RX")

    # Pin 26 (USB_DP_CORE, 44.13, 7.23) -> via at (44.13, hw['USB_DP_CORE'])
    add_seg(44.13, 7.23, 44.13, hw['USB_DP_CORE'], "F.Cu", "USB_DP_CORE")
    add_via(44.13, hw['USB_DP_CORE'], "USB_DP_CORE")

    # Pin 25 (USB_DM_CORE, 44.63, 7.23) -> via at (44.63, hw['USB_DM_CORE'])
    add_seg(44.63, 7.23, 44.63, hw['USB_DM_CORE'], "F.Cu", "USB_DM_CORE")
    add_via(44.63, hw['USB_DM_CORE'], "USB_DM_CORE")

    # ==============================================================
    # 6. RF MATCHING & CONNECTOR (X = 46 to 56 mm)
    # ==============================================================
    # FB1.2 (46.98, 7.70) to C2.1 (48.09, 6.60) on F.Cu
    add_seg(46.98, 7.70, 48.09, 7.70, "F.Cu", "3V3_RF")
    add_seg(48.09, 7.70, 48.09, 6.60, "F.Cu", "3V3_RF")
    add_seg(46.98, 7.70, 46.98, hw['3V3_RF'], "F.Cu", "3V3_RF")
    add_via(46.98, hw['3V3_RF'], "3V3_RF")

    # L2.1 (51.92, 5.30) to C8.1 (52.22, 3.60) on F.Cu
    add_seg(51.92, 5.30, 51.50, 5.30, "F.Cu", "RF_LNA")
    add_seg(51.50, 5.30, 51.50, 3.60, "F.Cu", "RF_LNA")
    add_seg(51.50, 3.60, 52.22, 3.60, "F.Cu", "RF_LNA")
    add_seg(51.50, 5.30, 51.50, hw['RF_LNA'], "F.Cu", "RF_LNA")
    add_via(51.50, hw['RF_LNA'], "RF_LNA")

    # RF_OUT: L2.2 (52.48, 5.30) to C9.1 (53.77, 3.55) to J_RF.1 (54.85, 5.15)
    # Routes South of J_RF.2 to avoid collision
    add_seg(52.48, 5.30, 53.00, 5.30, "F.Cu", "RF_OUT")
    add_seg(53.00, 5.30, 53.00, 3.55, "F.Cu", "RF_OUT")
    add_seg(53.00, 3.55, 53.77, 3.55, "F.Cu", "RF_OUT")
    add_seg(53.77, 3.55, 54.85, 3.55, "F.Cu", "RF_OUT")
    add_seg(54.85, 3.55, 54.85, 5.15, "F.Cu", "RF_OUT")

    # STRAP2: R3.2 (48.77, 2.80) escapes North to via at (48.77, 4.08)
    add_seg(48.77, 2.80, 48.77, 4.08, "F.Cu", "STRAP2")
    add_via(48.77, 4.08, "STRAP2")
    add_seg(38.50, 4.08, 48.77, 4.08, "B.Cu", "STRAP2")

    # BOOT9: SW2.1 (45.70, 1.50) escapes North to via at (45.70, hw['BOOT9'])
    add_seg(45.70, 1.50, 45.70, hw['BOOT9'], "F.Cu", "BOOT9")
    add_via(45.70, hw['BOOT9'], "BOOT9")
    # R2.2 (52.23, 2.25) escapes North to via at (52.23, hw['BOOT9'])
    add_seg(52.23, 2.25, 52.23, hw['BOOT9'], "F.Cu", "BOOT9")
    add_via(52.23, hw['BOOT9'], "BOOT9")

    # ==============================================================
    # 7. UART & MICROSD (X = 56 to 61 mm)
    # ==============================================================
    # J_UART.1 (UART_TX at 55.95, 7.35) escapes South on F.Cu to via at (55.95, hw['UART_TX'])
    add_seg(55.95, 7.35, 55.95, hw['UART_TX'], "F.Cu", "UART_TX")
    add_via(55.95, hw['UART_TX'], "UART_TX")

    # J_UART.2 (UART_RX at 57.22, 7.35) escapes South on F.Cu to via at (57.22, hw['UART_RX'])
    add_seg(57.22, 7.35, 57.22, hw['UART_RX'], "F.Cu", "UART_RX")
    add_via(57.22, hw['UART_RX'], "UART_RX")

    # J_SD:
    # Pin 3 (SD_SCK at 58.15, 4.20) escapes South on F.Cu to via at (58.15, hw['SD_SCK'])
    add_seg(58.15, 4.20, 58.15, hw['SD_SCK'], "F.Cu", "SD_SCK")
    add_via(58.15, hw['SD_SCK'], "SD_SCK")

    # Pin 4 (SD_MOSI at 58.65, 4.20) escapes South on F.Cu to via at (57.50, hw['SD_MOSI'])
    add_seg(58.65, 4.20, 57.50, 4.20, "F.Cu", "SD_MOSI")
    add_seg(57.50, 4.20, 57.50, hw['SD_MOSI'], "F.Cu", "SD_MOSI")
    add_via(57.50, hw['SD_MOSI'], "SD_MOSI")

    # Pin 5 (SD_MISO at 59.15, 4.20) escapes South on F.Cu to via at (58.00, hw['SD_MISO'])
    add_seg(59.15, 4.20, 58.00, 4.20, "F.Cu", "SD_MISO")
    add_seg(58.00, 4.20, 58.00, hw['SD_MISO'], "F.Cu", "SD_MISO")
    add_via(58.00, hw['SD_MISO'], "SD_MISO")

    # Pin 6 (SD_CS at 59.65, 4.20) connects to R18.2 (58.86, 1.50)
    add_seg(59.65, 4.20, 58.86, 4.20, "F.Cu", "SD_CS")
    add_seg(58.86, 4.20, 58.86, 1.50, "F.Cu", "SD_CS")
    add_seg(58.86, 1.50, 58.86, hw['SD_CS'], "F.Cu", "SD_CS")
    add_via(58.86, hw['SD_CS'], "SD_CS")

    # ==============================================================
    # 8. CHARGER U2, BATTERY SW3, J_PWR (X = 61 to 70 mm)
    # ==============================================================
    # SW3.1 (VBAT at 60.96, 6.82) escapes South on F.Cu to via at (60.96, hw['VBAT'])
    add_seg(60.96, 6.82, 60.96, hw['VBAT'], "F.Cu", "VBAT")
    add_via(60.96, hw['VBAT'], "VBAT")

    # SW3.2 (VBAT_SW at 62.96, 6.82) escapes South on F.Cu to via at (62.96, hw['VBAT_SW'])
    add_seg(62.96, 6.82, 62.96, hw['VBAT_SW'], "F.Cu", "VBAT_SW")
    add_via(62.96, hw['VBAT_SW'], "VBAT_SW")

    # J_PWR.1 (VBAT_SW at 68.11, 3.96) escapes North on F.Cu to via at (68.11, hw['VBAT_SW'])
    add_seg(68.11, 3.96, 68.11, hw['VBAT_SW'], "F.Cu", "VBAT_SW")
    add_via(68.11, hw['VBAT_SW'], "VBAT_SW")

    # Battery J_BAT.1 (VBAT at 61.60, 1.72) escapes North on F.Cu to via at (61.60, hw['VBAT'])
    add_seg(61.60, 1.72, 61.60, hw['VBAT'], "F.Cu", "VBAT")
    add_via(61.60, hw['VBAT'], "VBAT")

    # Charger U2:
    # Pin 1 (CHG_STAT at 65.33, 2.77) escapes North on F.Cu to via at (65.33, hw['CHG_STAT'])
    add_seg(65.33, 2.77, 65.33, hw['CHG_STAT'], "F.Cu", "CHG_STAT")
    add_via(65.33, hw['CHG_STAT'], "CHG_STAT")

    # Pin 3 (VBAT at 67.23, 2.77) to C12.1 (67.57, 1.50) on F.Cu
    add_seg(67.23, 2.77, 67.57, 2.77, "F.Cu", "VBAT")
    add_seg(67.57, 2.77, 67.57, 1.50, "F.Cu", "VBAT")
    add_seg(67.23, 2.77, 67.23, hw['VBAT'], "F.Cu", "VBAT")
    add_via(67.23, hw['VBAT'], "VBAT")

    # Pin 4 (USB_VBUS at 67.23, 5.37) escapes to via at (67.23, hw['USB_VBUS'])
    add_seg(67.23, 5.37, 67.23, hw['USB_VBUS'], "F.Cu", "USB_VBUS")
    add_via(67.23, hw['USB_VBUS'], "USB_VBUS")

    # Pin 5 (CHG_PROG at 65.33, 5.37) to R9.1 (66.13, 6.54)
    # Avoid SW3.3 (GND at 64.96) by routing East at Y=5.37 first
    add_seg(65.33, 5.37, 66.13, 5.37, "F.Cu", "CHG_PROG")
    add_seg(66.13, 5.37, 66.13, 6.54, "F.Cu", "CHG_PROG")

    # C11.1 (USB_VBUS at 66.13, 7.70) escapes South on F.Cu to via at (66.13, hw['USB_VBUS'])
    add_seg(66.13, 7.70, 66.13, hw['USB_VBUS'], "F.Cu", "USB_VBUS")
    add_via(66.13, hw['USB_VBUS'], "USB_VBUS")

    # ==============================================================
    # 9. ESD PROTECTION & USB-C (X = 70 to 84 mm)
    # ==============================================================
    # R5.1 (USB_CC1 at 70.25, 7.70) escapes South on F.Cu to via at (70.25, hw['USB_CC1'])
    add_seg(70.25, 7.70, 70.25, hw['USB_CC1'], "F.Cu", "USB_CC1")
    add_via(70.25, hw['USB_CC1'], "USB_CC1")

    # R6.1 (USB_CC2 at 73.56, 2.46) escapes East/North on F.Cu to via at (74.80, hw['USB_CC2'])
    add_seg(73.56, 2.46, 74.80, 2.46, "F.Cu", "USB_CC2")
    add_seg(74.80, 2.46, 74.80, hw['USB_CC2'], "F.Cu", "USB_CC2")
    add_via(74.80, hw['USB_CC2'], "USB_CC2")

    # U_ESD:
    # Pin 4 (USB_DM_CORE at 72.75, 5.79) to R7.2 (72.97, 6.85) on F.Cu
    add_seg(72.75, 5.79, 72.97, 5.79, "F.Cu", "USB_DM_CORE")
    add_seg(72.97, 5.79, 72.97, 6.85, "F.Cu", "USB_DM_CORE")
    # Escape West to via at (71.50, hw['USB_DM_CORE'])
    add_seg(72.75, 5.79, 71.50, 5.79, "F.Cu", "USB_DM_CORE")
    add_seg(71.50, 5.79, 71.50, hw['USB_DM_CORE'], "F.Cu", "USB_DM_CORE")
    add_via(71.50, hw['USB_DM_CORE'], "USB_DM_CORE")

    # Pin 6 (USB_DP_CORE at 70.85, 5.79) to R8.2 (72.96, 7.70) on F.Cu
    add_seg(70.85, 5.79, 70.85, 7.70, "F.Cu", "USB_DP_CORE")
    add_seg(70.85, 7.70, 72.96, 7.70, "F.Cu", "USB_DP_CORE")
    # Via at (70.85, hw['USB_DP_CORE'])
    add_via(70.85, hw['USB_DP_CORE'], "USB_DP_CORE")

    # Pin 5 (USB_VBUS at 71.80, 5.79) escapes South on F.Cu to via at (71.80, hw['USB_VBUS'])
    add_seg(71.80, 5.79, 71.80, hw['USB_VBUS'], "F.Cu", "USB_VBUS")
    add_via(71.80, hw['USB_VBUS'], "USB_VBUS")

    # C10.1 (USB_VBUS at 72.96, 1.50) escapes North on F.Cu to via at (73.00, hw['USB_VBUS'])
    add_seg(72.96, 1.50, 73.00, 1.50, "F.Cu", "USB_VBUS")
    add_seg(73.00, 1.50, 73.00, hw['USB_VBUS'], "F.Cu", "USB_VBUS")
    add_via(73.00, hw['USB_VBUS'], "USB_VBUS")

    # USB Port lines:
    # R8.1 (USB_DP_PORT at 72.01, 7.70) to U_ESD.1 (70.85, 3.19) on F.Cu:
    # Route West at Y = 8.10, then down at X = 69.50 to (69.50, hw['USB_DP_PORT'])
    add_seg(72.01, 7.70, 72.01, 8.00, "F.Cu", "USB_DP_PORT")
    add_seg(72.01, 8.00, 69.50, 8.00, "F.Cu", "USB_DP_PORT")
    add_seg(69.50, 8.00, 69.50, 3.19, "F.Cu", "USB_DP_PORT")
    add_seg(69.50, 3.19, 70.85, 3.19, "F.Cu", "USB_DP_PORT")
    add_seg(69.50, 3.19, 69.50, hw['USB_DP_PORT'], "F.Cu", "USB_DP_PORT")
    add_via(69.50, hw['USB_DP_PORT'], "USB_DP_PORT")

    # J_USB.7 (USB_DP_PORT at 78.15, 3.10) escapes South on F.Cu to via at (78.15, hw['USB_DP_PORT'])
    add_seg(78.15, 3.10, 78.15, hw['USB_DP_PORT'], "F.Cu", "USB_DP_PORT")
    add_via(78.15, hw['USB_DP_PORT'], "USB_DP_PORT")
    add_seg(69.50, hw['USB_DP_PORT'], 78.15, hw['USB_DP_PORT'], "B.Cu", "USB_DP_PORT")

    # R7.1 (USB_DM_PORT at 72.02, 6.85) to U_ESD.2 (71.80, 3.19) on F.Cu:
    # Route West to X = 70.00, then down to (70.00, hw['USB_DM_PORT'])
    add_seg(72.02, 6.85, 70.00, 6.85, "F.Cu", "USB_DM_PORT")
    add_seg(70.00, 6.85, 70.00, 3.19, "F.Cu", "USB_DM_PORT")
    add_seg(70.00, 3.19, 71.80, 3.19, "F.Cu", "USB_DM_PORT")
    add_seg(70.00, 3.19, 70.00, hw['USB_DM_PORT'], "F.Cu", "USB_DM_PORT")
    add_via(70.00, hw['USB_DM_PORT'], "USB_DM_PORT")

    # J_USB.9 (USB_DM_PORT at 78.65, 3.10) escapes South on F.Cu to via at (78.65, hw['USB_DM_PORT'])
    add_seg(78.65, 3.10, 78.65, hw['USB_DM_PORT'], "F.Cu", "USB_DM_PORT")
    add_via(78.65, hw['USB_DM_PORT'], "USB_DM_PORT")
    add_seg(70.00, hw['USB_DM_PORT'], 78.65, hw['USB_DM_PORT'], "B.Cu", "USB_DM_PORT")

    # J_USB connector pins:
    # Pin 5 (USB_CC1 at 77.60, 3.10) escapes to via at (77.60, hw['USB_CC1'])
    add_seg(77.60, 3.10, 77.60, hw['USB_CC1'], "F.Cu", "USB_CC1")
    add_via(77.60, hw['USB_CC1'], "USB_CC1")

    # Pin 6 (USB_CC2 at 79.20, 3.10) escapes to via at (79.20, hw['USB_CC2'])
    add_seg(79.20, 3.10, 79.20, hw['USB_CC2'], "F.Cu", "USB_CC2")
    add_via(79.20, hw['USB_CC2'], "USB_CC2")

    # Pin 2 & 10 (USB_VBUS at 76.00, 3.10 and 80.80, 3.10)
    add_seg(76.00, 3.10, 76.00, hw['USB_VBUS'], "F.Cu", "USB_VBUS")
    add_via(76.00, hw['USB_VBUS'], "USB_VBUS")
    add_seg(80.80, 3.10, 80.80, hw['USB_VBUS'], "F.Cu", "USB_VBUS")
    add_via(80.80, hw['USB_VBUS'], "USB_VBUS")

    # ==============================================================
    # 10. POWER RAILS (3V3 NORTH & SOUTH)
    # ==============================================================
    # IMU / Touch:
    add_seg(1.70, 4.60, 1.00, 4.60, "F.Cu", "3V3")
    add_seg(1.00, 4.60, 1.00, hw['3V3_SOUTH'], "F.Cu", "3V3")
    add_via(1.00, hw['3V3_SOUTH'], "3V3")

    add_seg(5.73, 2.00, 5.73, 4.60, "F.Cu", "3V3")
    add_seg(5.73, 4.60, 5.73, 7.20, "F.Cu", "3V3")
    add_seg(5.73, 2.00, 5.73, hw['3V3_SOUTH'], "F.Cu", "3V3")
    add_via(5.73, hw['3V3_SOUTH'], "3V3")

    add_seg(8.00, 2.40, 8.00, hw['3V3_SOUTH'], "F.Cu", "3V3")
    add_via(8.00, hw['3V3_SOUTH'], "3V3")

    # Side switch pullups & U3:
    add_seg(14.03, 7.00, 14.03, hw['3V3_NORTH'], "F.Cu", "3V3")
    add_via(14.03, hw['3V3_NORTH'], "3V3")

    add_seg(20.02, 7.00, 20.02, hw['3V3_NORTH'], "F.Cu", "3V3")
    add_via(20.02, hw['3V3_NORTH'], "3V3")

    add_seg(23.02, 8.00, 23.02, hw['3V3_NORTH'], "F.Cu", "3V3")
    add_via(23.02, hw['3V3_NORTH'], "3V3")
    add_seg(21.35, 4.65, 21.35, 7.50, "F.Cu", "3V3")
    add_seg(21.35, 7.50, 23.02, 7.50, "F.Cu", "3V3")
    add_seg(23.02, 7.50, 23.02, 8.00, "F.Cu", "3V3")

    # U3 & LED resistors:
    add_seg(18.52, 4.40, 18.52, 2.20, "F.Cu", "3V3")
    add_seg(18.52, 2.20, 18.52, hw['3V3_SOUTH'], "F.Cu", "3V3")
    add_via(18.52, hw['3V3_SOUTH'], "3V3")

    add_seg(25.15, 3.65, 25.15, hw['3V3_SOUTH'], "F.Cu", "3V3")
    add_via(25.15, hw['3V3_SOUTH'], "3V3")

    # MCU U1:
    add_seg(35.41, 2.60, 37.98, 2.60, "F.Cu", "3V3")
    add_seg(37.98, 2.60, 37.98, 2.36, "F.Cu", "3V3")
    add_seg(35.41, 2.60, 35.41, hw['3V3_SOUTH'], "F.Cu", "3V3")
    add_via(35.41, hw['3V3_SOUTH'], "3V3")

    add_seg(45.28, 3.08, 45.00, 3.08, "F.Cu", "3V3")
    add_seg(45.00, 3.08, 45.00, hw['3V3_SOUTH'], "F.Cu", "3V3")
    add_via(45.00, hw['3V3_SOUTH'], "3V3")

    # North MCU passives: FB1.1 (45.48, 7.70) and C3.1 (50.25, 7.70)
    add_seg(45.48, 7.70, 45.48, hw['3V3_NORTH'], "F.Cu", "3V3")
    add_via(45.48, hw['3V3_NORTH'], "3V3")
    add_seg(50.25, 7.70, 50.25, hw['3V3_NORTH'], "F.Cu", "3V3")
    add_via(50.25, hw['3V3_NORTH'], "3V3")

    # South passives: R3.1 (47.82, 2.80) to R2.1 (51.27, 2.25)
    add_seg(47.82, 2.80, 47.82, hw['3V3_SOUTH'], "F.Cu", "3V3")
    add_via(47.82, hw['3V3_SOUTH'], "3V3")
    add_seg(51.27, 2.25, 51.27, hw['3V3_SOUTH'], "F.Cu", "3V3")
    add_via(51.27, hw['3V3_SOUTH'], "3V3")

    # MicroSD & UART:
    add_seg(57.15, 4.20, 57.15, 1.50, "F.Cu", "3V3")
    add_seg(57.15, 1.50, 57.91, 1.50, "F.Cu", "3V3")
    add_seg(57.15, 1.50, 57.15, hw['3V3_SOUTH'], "F.Cu", "3V3")
    add_via(57.15, hw['3V3_SOUTH'], "3V3")

    add_seg(59.76, 7.35, 59.76, hw['3V3_NORTH'], "F.Cu", "3V3")
    add_via(59.76, hw['3V3_NORTH'], "3V3")

    # LDO Output:
    add_seg(70.01, 3.96, 70.24, 3.96, "F.Cu", "3V3")
    add_seg(70.24, 3.96, 70.24, 2.05, "F.Cu", "3V3")
    add_seg(70.24, 2.05, 70.24, hw['3V3_SOUTH'], "F.Cu", "3V3")
    add_via(70.24, hw['3V3_SOUTH'], "3V3")

    # ==============================================================
    # 11. HORIZONTAL HIGHWAYS ON B.CU
    # ==============================================================
    # Connect every net's vias along its dedicated B.Cu horizontal Y-lane:
    for net_name, y_coord in hw.items():
        if net_name in ['3V3_SOUTH', '3V3_NORTH']: continue
        # Find all vias placed on this Y lane
        vlist = sorted([v[0] for v in vias if v[2] == net_name and abs(v[1] - y_coord) < 0.05])
        if len(vlist) >= 2:
            add_seg(vlist[0], y_coord, vlist[-1], y_coord, "B.Cu", net_name, width=0.18)

    # 3V3 Highways:
    south_vias = sorted([v[0] for v in vias if v[2] == '3V3' and abs(v[1] - hw['3V3_SOUTH']) < 0.05])
    if len(south_vias) >= 2:
        add_seg(south_vias[0], hw['3V3_SOUTH'], 82.50, hw['3V3_SOUTH'], "B.Cu", "3V3", width=0.25)

    north_vias = sorted([v[0] for v in vias if v[2] == '3V3' and abs(v[1] - hw['3V3_NORTH']) < 0.05])
    if len(north_vias) >= 2:
        add_seg(north_vias[0], hw['3V3_NORTH'], 82.50, hw['3V3_NORTH'], "B.Cu", "3V3", width=0.25)

    # Tie South and North rails at the far East edge
    add_seg(82.50, hw['3V3_SOUTH'], 82.50, hw['3V3_NORTH'], "B.Cu", "3V3", width=0.25)

    print(f"Total placed: {len(segments)} segments, {len(vias)} vias.")
    
    # Preflight geometry verification
    geom_errors = check_pcb_geometry(all_pads, segments, list(vias))
    print(f"\n--- PREFLIGHT GEOMETRIC VALIDATION: {len(geom_errors)} ERRORS ---")
    for i, e in enumerate(geom_errors):
        print(f"[{i+1:02d}] {e}")

    return len(geom_errors) == 0, segments, vias, all_pads, net_id_map, sorted_nets

if __name__ == '__main__':
    solve_smartpen_pcb()
