"""Modular Clean Router for SmartPen Main PCB.
Step-by-step verified construction.
"""
import json, sys, math
from pathlib import Path

sys.path.insert(0, '.')
from scripts.verify_smartpen_geometry import check_pcb_geometry

out_dir = Path("output/RevF_Working")

def build_modular():
    with open(out_dir / 'solved_coords.json') as f:
        coords = json.load(f)
    with open(out_dir / 'SmartPen_RevE_PCB.json') as f:
        pcb_json = json.load(f)

    # Extract all pads
    fp_defs = {}
    for item in pcb_json['shape']:
        if isinstance(item, str) and item.startswith('LIB~'):
            subs = item.split('#@$')
            ref = ''
            for sub in subs:
                if sub.startswith('TEXT~P~'): ref = sub.split('~')[10]
            if not ref: continue
            orig_x, orig_y = float(subs[0].split('~')[1]), float(subs[0].split('~')[2])
            pads = []
            for sub in subs:
                if sub.startswith('PAD~'):
                    ptoks = sub.split('~')
                    dx = (float(ptoks[2]) - orig_x) * 0.254
                    dy = (float(ptoks[3]) - orig_y) * 0.254
                    pads.append({
                        'num': ptoks[8], 'net': ptoks[7],
                        'dx': round(dx, 4), 'dy': round(dy, 4),
                        'w': round(float(ptoks[4]) * 0.254, 4),
                        'h': round(float(ptoks[5]) * 0.254, 4)
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

    hw = {
        '3V3_SOUTH':   0.55,
        'SD_MOSI':     0.95,
        'SD_MISO':     1.35,
        'SD_SCK':      1.75,
        'SD_CS':       2.15,
        'BOOT9':       2.55,
        'TOUCH_OUT':   2.95,
        'USB_CC2':     2.95,
        'MCU_EN':      3.35,
        'USB_DM_PORT': 3.35,
        'LED_RED_SINK':3.75,
        'USB_DP_PORT': 3.75,
        'CHG_STAT':    4.15,
        'VBAT_SW':     4.60,
        'I2C_SDA':     5.05,
        'USB_VBUS':    5.05,
        'I2C_SCL':     5.50,
        'VBAT':        5.50,
        '3V3_RF':      5.95,
        'RF_LNA':      6.40,
        'UART_RX':     6.85,
        'UART_TX':     7.30,
        'LED_GREEN_SINK':7.30,
        'USB_DM_CORE': 7.75,
        'BTN_MODE':    7.75,
        'USB_DP_CORE': 8.15,
        'BTN_ERASE':   8.15,
        'XTAL_N':      8.45,
        'USB_CC1':     8.45,
        '3V3_NORTH':   8.65,
    }

    # ==============================================================
    # 1. FRONT IMU & TOUCH (X = 0 to 15 mm)
    # ==============================================================
    # J_IMU.3 (I2C_SDA at 3.70, 4.60) escapes North on F.Cu to via at (3.70, hw['I2C_SDA'])
    add_seg(3.70, 4.60, 3.70, hw['I2C_SDA'], "F.Cu", "I2C_SDA")
    add_via(3.70, hw['I2C_SDA'], "I2C_SDA")

    # J_IMU.4 (I2C_SCL at 4.70, 4.60) escapes North on F.Cu to via at (4.70, hw['I2C_SCL'])
    add_seg(4.70, 4.60, 4.70, hw['I2C_SCL'], "F.Cu", "I2C_SCL")
    add_via(4.70, hw['I2C_SCL'], "I2C_SCL")

    # R10.2 (I2C_SDA at 6.67, 4.60) escapes North to via at (6.67, hw['I2C_SDA'])
    add_seg(6.67, 4.60, 6.67, hw['I2C_SDA'], "F.Cu", "I2C_SDA")
    add_via(6.67, hw['I2C_SDA'], "I2C_SDA")
    add_seg(3.70, hw['I2C_SDA'], 6.67, hw['I2C_SDA'], "B.Cu", "I2C_SDA")

    # R11.2 (I2C_SCL at 6.67, 7.20) escapes South on F.Cu to via at (7.50, hw['I2C_SCL'])
    add_seg(6.67, 7.20, 7.50, 7.20, "F.Cu", "I2C_SCL")
    add_seg(7.50, 7.20, 7.50, hw['I2C_SCL'], "F.Cu", "I2C_SCL")
    add_via(7.50, hw['I2C_SCL'], "I2C_SCL")
    add_seg(4.70, hw['I2C_SCL'], 7.50, hw['I2C_SCL'], "B.Cu", "I2C_SCL")

    # J_TOUCH.3 (TOUCH_OUT at 10.00, 2.40) to R19.1 (13.03, 2.40) straight on F.Cu
    add_seg(10.00, 2.40, 13.03, 2.40, "F.Cu", "TOUCH_OUT")
    # R19.1 escapes North on F.Cu to via at (13.03, hw['TOUCH_OUT'])
    add_seg(13.03, 2.40, 13.03, hw['TOUCH_OUT'], "F.Cu", "TOUCH_OUT")
    add_via(13.03, hw['TOUCH_OUT'], "TOUCH_OUT")

    errors = check_pcb_geometry(all_pads, segments, list(vias))
    print(f"Subsystem 1 (IMU & Touch): {len(errors)} errors.")
    for e in errors: print(" ", e)

    return len(errors) == 0

if __name__ == '__main__':
    build_modular()

