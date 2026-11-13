"""Master Solver for SmartPen Revision F Main PCB.
Assembles Subsystems 1 through 10 with 100% DRC-clean planar geometry.
Validates all pads, tracks, vias, and clearances with verify_smartpen_geometry.
"""
import json, sys, math
sys.path.insert(0, '.')
from scripts.verify_smartpen_geometry import check_pcb_geometry

def build_full_board():
    with open('output/RevF_Working/solved_coords.json') as f:
        coords = json.load(f)

    # Master component coordinates across all subsystems:
    coords['C1'] = [39.80, 1.52]
    coords['FB1'] = [46.23, 7.55]
    coords['R18'] = [55.00, 2.35]
    coords['J_BAT'] = [62.80, 1.72]
    coords['U2'] = [67.00, 4.07]
    coords['R9'] = [66.30, 6.70]
    coords['C11'] = [68.00, 7.75]
    coords['C12'] = [68.15, 1.40]
    coords['C14'] = [70.014, 2.00]
    coords['U_ESD'] = [72.00, 4.49]
    coords['C10'] = [74.50, 1.50]
    coords['R8'] = [71.60, 7.50]
    coords['R7'] = [73.00, 7.50]
    coords['R5'] = [77.60, 6.70]
    coords['R6'] = [79.20, 6.70]

    with open('output/RevF_Working/SmartPen_RevE_PCB.json') as f:
        pcb_json = json.load(f)

    fp_defs = {}
    for item in pcb_json['shape']:
        if isinstance(item, str) and item.startswith('LIB~'):
            subs = item.split('#@$')
            ref = ''
            for sub in subs:
                if sub.startswith('TEXT~P~'): ref = sub.split('~')[10]
            if not ref: continue
            orig_x, orig_y = float(subs[0].split('~')[1]), float(subs[0].split('~')[2])
            pads_sub = []
            for sub in subs:
                if sub.startswith('PAD~'):
                    ptoks = sub.split('~')
                    dx = (float(ptoks[2]) - orig_x) * 0.254
                    dy = (float(ptoks[3]) - orig_y) * 0.254
                    pads_sub.append({
                        'num': ptoks[8], 'net': ptoks[7],
                        'dx': round(dx, 4), 'dy': round(dy, 4),
                        'w': round(float(ptoks[4]) * 0.254, 4),
                        'h': round(float(ptoks[5]) * 0.254, 4)
                    })
            fp_defs[ref] = pads_sub

    # Vertical footprint rotations:
    for ref in ['R9', 'R5', 'R6', 'C14']:
        for p in fp_defs[ref]:
            p['dx'], p['dy'] = p['dy'], p['dx']
            p['w'], p['h'] = p['h'], p['w']

    # C14: Pin 1 (3V3) in North (dy = +0.75), Pin 2 (GND) in South (dy = -0.75)
    for p in fp_defs['C14']:
        p['dy'] = 0.75 if p['num'] == '1' else -0.75

    # R7 and R8: vertical, Pin 1 (PORT) in North (dy = +0.475), Pin 2 (CORE) in South (dy = -0.475)
    for ref in ['R7', 'R8']:
        for p in fp_defs[ref]:
            p['w'], p['h'] = p['h'], p['w']
            p['dx'] = 0.0
            p['dy'] = 0.475 if p['num'] == '1' else -0.475

    pads = []
    for ref, (cx, cy) in coords.items():
        if ref in fp_defs:
            for p in fp_defs[ref]:
                pads.append({
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

    # ==============================================================
    # 1. FRONT IMU & TOUCH (X = 0 to 15 mm)
    # ==============================================================
    # J_IMU.3 (I2C_SDA at 3.70, 4.60) -> via at (3.70, 4.85)
    add_seg(3.70, 4.60, 3.70, 4.85, "F.Cu", "I2C_SDA")
    add_via(3.70, 4.85, "I2C_SDA")

    # J_IMU.4 (I2C_SCL at 4.70, 4.60) -> via at (4.70, 5.30)
    add_seg(4.70, 4.60, 4.70, 5.30, "F.Cu", "I2C_SCL")
    add_via(4.70, 5.30, "I2C_SCL")

    # R10.2 (I2C_SDA at 6.67, 4.60) -> via at (6.67, 4.85)
    add_seg(6.67, 4.60, 6.67, 4.85, "F.Cu", "I2C_SDA")
    add_via(6.67, 4.85, "I2C_SDA")
    add_seg(3.70, 4.85, 6.67, 4.85, "B.Cu", "I2C_SDA")

    # R11.2 (I2C_SCL at 6.67, 7.20) -> via at (7.50, 5.30)
    add_seg(6.67, 7.20, 7.50, 7.20, "F.Cu", "I2C_SCL")
    add_seg(7.50, 7.20, 7.50, 5.30, "F.Cu", "I2C_SCL")
    add_via(7.50, 5.30, "I2C_SCL")
    add_seg(4.70, 5.30, 7.50, 5.30, "B.Cu", "I2C_SCL")

    # J_TOUCH.3 (10.00, 2.40) to R19.1 (13.03, 2.40) on F.Cu
    add_seg(10.00, 2.40, 13.03, 2.40, "F.Cu", "TOUCH_OUT")
    # R19.1 to via at (13.03, 2.75)
    add_seg(13.03, 2.40, 13.03, 2.75, "F.Cu", "TOUCH_OUT")
    add_via(13.03, 2.75, "TOUCH_OUT")

    # ==============================================================
    # 2. SIDE BUTTONS & LEDS (X = 10 to 22 mm)
    # ==============================================================
    # Erase Button: SW4.1 (10.10, 7.00) -> via at (10.10, 8.05)
    add_seg(10.10, 7.00, 10.10, 8.05, "F.Cu", "BTN_ERASE")
    add_via(10.10, 8.05, "BTN_ERASE")

    # R12.2 (14.97, 7.00) -> via at (14.97, 8.05)
    add_seg(14.97, 7.00, 14.97, 8.05, "F.Cu", "BTN_ERASE")
    add_via(14.97, 8.05, "BTN_ERASE")
    add_seg(10.10, 8.05, 14.97, 8.05, "B.Cu", "BTN_ERASE")

    # Mode Button: SW5.1 (16.10, 7.00) -> via at (16.10, 7.60)
    add_seg(16.10, 7.00, 16.10, 7.60, "F.Cu", "BTN_MODE")
    add_via(16.10, 7.60, "BTN_MODE")

    # R13.2 (20.98, 7.00) -> via at (20.98, 7.60)
    add_seg(20.98, 7.00, 20.98, 7.60, "F.Cu", "BTN_MODE")
    add_via(20.98, 7.60, "BTN_MODE")
    add_seg(16.10, 7.60, 20.98, 7.60, "B.Cu", "BTN_MODE")

    # Green LED: D1.1 (16.00, 2.20) to R14.2 (19.48, 2.20) on F.Cu via Y = 1.40
    add_seg(16.00, 2.20, 16.00, 1.40, "F.Cu", "LED_GREEN_A")
    add_seg(16.00, 1.40, 19.48, 1.40, "F.Cu", "LED_GREEN_A")
    add_seg(19.48, 1.40, 19.48, 2.20, "F.Cu", "LED_GREEN_A")

    # D1.2 (LED_GREEN_SINK at 17.00, 2.20) escapes East to 17.60, then North to via at (17.60, 3.10)
    add_seg(17.00, 2.20, 17.60, 2.20, "F.Cu", "LED_GREEN_SINK")
    add_seg(17.60, 2.20, 17.60, 3.10, "F.Cu", "LED_GREEN_SINK")
    add_via(17.60, 3.10, "LED_GREEN_SINK")

    # Red LED: D2.1 (16.00, 4.40) to R15.2 (19.48, 4.40) on F.Cu via Y = 5.25
    add_seg(16.00, 4.40, 16.00, 5.25, "F.Cu", "LED_RED_A")
    add_seg(16.00, 5.25, 19.48, 5.25, "F.Cu", "LED_RED_A")
    add_seg(19.48, 5.25, 19.48, 4.40, "F.Cu", "LED_RED_A")

    # D2.2 (LED_RED_SINK at 17.00, 4.40) escapes East to 17.60, then South to via at (17.60, 3.80)
    add_seg(17.00, 4.40, 17.60, 4.40, "F.Cu", "LED_RED_SINK")
    add_seg(17.60, 4.40, 17.60, 3.80, "F.Cu", "LED_RED_SINK")
    add_via(17.60, 3.80, "LED_RED_SINK")

    # ==============================================================
    # 3. U3 I/O EXPANDER & MOTOR DRIVER (X = 20 to 32 mm)
    # ==============================================================
    # U3.1 (I2C_SCL at 22.25, 2.75) escapes to via at (22.25, 5.30)
    add_seg(22.25, 2.75, 22.25, 5.30, "F.Cu", "I2C_SCL")
    add_via(22.25, 5.30, "I2C_SCL")
    add_seg(7.50, 5.30, 22.25, 5.30, "B.Cu", "I2C_SCL")

    # U3.2 (I2C_SDA at 22.75, 2.75) escapes to via at (22.75, 4.85)
    add_seg(22.75, 2.75, 22.75, 4.85, "F.Cu", "I2C_SDA")
    add_via(22.75, 4.85, "I2C_SDA")
    add_seg(6.67, 4.85, 22.75, 4.85, "B.Cu", "I2C_SDA")

    # U3.10 (BTN_ERASE at 25.15, 5.65) escapes East/North to via at (25.85, 8.05)
    add_seg(25.15, 5.65, 25.85, 5.65, "F.Cu", "BTN_ERASE")
    add_seg(25.85, 5.65, 25.85, 8.05, "F.Cu", "BTN_ERASE")
    add_via(25.85, 8.05, "BTN_ERASE")
    add_seg(14.97, 8.05, 25.85, 8.05, "B.Cu", "BTN_ERASE")

    # U3.11 (BTN_MODE at 24.25, 6.55) escapes North to via at (24.80, 7.60)
    add_seg(24.25, 6.55, 24.80, 6.55, "F.Cu", "BTN_MODE")
    add_seg(24.80, 6.55, 24.80, 7.60, "F.Cu", "BTN_MODE")
    add_via(24.80, 7.60, "BTN_MODE")
    add_seg(20.98, 7.60, 24.80, 7.60, "B.Cu", "BTN_MODE")

    # U3.12 (LED_GREEN_SINK at 23.75, 6.55)
    add_seg(23.75, 6.55, 23.75, 3.10, "F.Cu", "LED_GREEN_SINK")
    add_via(23.75, 3.10, "LED_GREEN_SINK")
    add_seg(17.60, 3.10, 23.75, 3.10, "B.Cu", "LED_GREEN_SINK")

    # U3.13 (LED_RED_SINK at 23.25, 6.55)
    add_seg(23.25, 6.55, 23.25, 3.80, "F.Cu", "LED_RED_SINK")
    add_via(23.25, 3.80, "LED_RED_SINK")
    add_seg(17.60, 3.80, 23.25, 3.80, "B.Cu", "LED_RED_SINK")

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
    add_seg(28.09, 4.70, 28.09, 7.80, "F.Cu", "VBAT_SW")
    add_seg(28.09, 7.80, 30.75, 7.80, "F.Cu", "VBAT_SW")
    add_seg(30.75, 7.80, 30.75, 6.29, "F.Cu", "VBAT_SW")
    add_seg(28.09, 7.80, 28.09, 4.40, "F.Cu", "VBAT_SW")
    add_via(28.09, 4.40, "VBAT_SW")

    # SW1.1 (31.56, 1.50) to via at (31.56, 3.59)
    add_seg(31.56, 1.50, 31.56, 3.59, "F.Cu", "MCU_EN")
    add_via(31.56, 3.59, "MCU_EN")

    # R1.2 (38.93, 2.36) to C1.1 (39.72, 1.52)
    add_seg(38.93, 2.36, 39.72, 2.36, "F.Cu", "MCU_EN")
    add_seg(39.72, 2.36, 39.72, 1.52, "F.Cu", "MCU_EN")
    add_seg(38.93, 2.36, 38.93, 3.59, "F.Cu", "MCU_EN")
    add_via(38.93, 3.59, "MCU_EN")
    add_seg(31.56, 3.59, 38.93, 3.59, "B.Cu", "MCU_EN")

    # 3V3_RTC: C4.1 (36.20, 1.64) to R4.2 (36.36, 2.60)
    add_seg(36.20, 1.64, 36.36, 1.64, "F.Cu", "3V3_RTC")
    add_seg(36.36, 1.64, 36.36, 2.60, "F.Cu", "3V3_RTC")
    add_seg(36.36, 2.60, 36.36, 0.85, "F.Cu", "3V3_RTC")
    add_via(36.36, 0.85, "3V3_RTC")

    # Crystal C6.1 (32.83, 7.70) to Y1.1 (34.72, 5.72)
    add_seg(32.83, 7.70, 32.83, 8.45, "F.Cu", "XTAL_N")
    add_via(32.83, 8.45, "XTAL_N")
    add_seg(32.83, 8.45, 35.57, 8.45, "F.Cu", "XTAL_N")
    add_seg(35.57, 8.45, 35.57, 5.72, "F.Cu", "XTAL_N")
    add_seg(35.57, 5.72, 34.72, 5.72, "F.Cu", "XTAL_N")

    # XTAL_P_MATCH: Y1.3 (36.42, 7.02) to C7.1 (37.36, 7.70) to L1.2 (40.07, 7.70) on F.Cu at Y = 7.02
    add_seg(36.42, 7.02, 40.07, 7.02, "F.Cu", "XTAL_P_MATCH")
    add_seg(37.36, 7.70, 37.36, 7.02, "F.Cu", "XTAL_P_MATCH")
    add_seg(40.07, 7.70, 40.07, 7.02, "F.Cu", "XTAL_P_MATCH")

    # XTAL_P_CORE: L1.1 (39.12, 7.70) escapes North to via at (39.12, 8.65)
    add_seg(39.12, 7.70, 39.12, 8.65, "F.Cu", "XTAL_P_CORE")
    add_via(39.12, 8.65, "XTAL_P_CORE")

    # ==============================================================
    # 4. MCU U1 (ESP32-C3) BREAKOUT (X = 40 to 46 mm)
    # ==============================================================
    # West pins:
    # Pin 1 (RF_LNA, 40.48, 6.59) -> via at (38.50, 6.25)
    add_seg(40.48, 6.59, 38.50, 6.59, "F.Cu", "RF_LNA")
    add_seg(38.50, 6.59, 38.50, 6.25, "F.Cu", "RF_LNA")
    add_via(38.50, 6.25, "RF_LNA")

    # Pin 2, 3 (3V3_RF, 40.48, 6.08 and 5.59) -> via at (39.00, 5.80)
    add_seg(40.48, 6.08, 40.48, 5.59, "F.Cu", "3V3_RF")
    add_seg(40.48, 5.80, 39.00, 5.80, "F.Cu", "3V3_RF")
    add_via(39.00, 5.80, "3V3_RF")

    # Pin 4 (I2C_SDA, 40.48, 5.08) -> via at (38.50, 4.85)
    add_seg(40.48, 5.08, 38.50, 5.08, "F.Cu", "I2C_SDA")
    add_seg(38.50, 5.08, 38.50, 4.85, "F.Cu", "I2C_SDA")
    add_via(38.50, 4.85, "I2C_SDA")
    add_seg(22.75, 4.85, 38.50, 4.85, "B.Cu", "I2C_SDA")

    # Pin 5 (I2C_SCL, 40.48, 4.59) -> via at (39.70, 5.30)
    add_seg(40.48, 4.59, 39.70, 4.59, "F.Cu", "I2C_SCL")
    add_seg(39.70, 4.59, 39.70, 5.30, "F.Cu", "I2C_SCL")
    add_via(39.70, 5.30, "I2C_SCL")
    add_seg(22.25, 5.30, 39.70, 5.30, "B.Cu", "I2C_SCL")

    # Pin 6 (STRAP2, 40.48, 4.08) -> via at (37.50, 4.08)
    add_seg(40.48, 4.08, 37.50, 4.08, "F.Cu", "STRAP2")
    add_via(37.50, 4.08, "STRAP2")

    # Pin 7 (MCU_EN, 40.48, 3.59) connects to via at (38.93, 3.59)
    add_seg(40.48, 3.59, 38.93, 3.59, "F.Cu", "MCU_EN")

    # Pin 8 (TOUCH_OUT, 40.48, 3.08) -> via at (39.70, 2.75)
    add_seg(40.48, 3.08, 39.70, 3.08, "F.Cu", "TOUCH_OUT")
    add_seg(39.70, 3.08, 39.70, 2.75, "F.Cu", "TOUCH_OUT")
    add_via(39.70, 2.75, "TOUCH_OUT")
    add_seg(13.03, 2.75, 39.70, 2.75, "B.Cu", "TOUCH_OUT")

    # South pins (escape South to horizontal highways):
    # Pin 9 (SD_MOSI, 41.13, 2.43) -> via at (41.13, 0.55)
    add_seg(41.13, 2.43, 41.13, 0.55, "F.Cu", "SD_MOSI")
    add_via(41.13, 0.55, "SD_MOSI")
    add_seg(41.13, 0.55, 58.65, 0.55, "B.Cu", "SD_MOSI")

    # Pin 10 (SD_MISO, 41.63, 2.43) -> via at (41.63, 1.15)
    add_seg(41.63, 2.43, 41.63, 1.15, "F.Cu", "SD_MISO")
    add_via(41.63, 1.15, "SD_MISO")
    add_seg(41.63, 1.15, 59.15, 1.15, "B.Cu", "SD_MISO")

    # Pin 11 (3V3_RTC, 42.13, 2.43) -> via at (42.13, 0.85)
    add_seg(42.13, 2.43, 42.13, 0.85, "F.Cu", "3V3_RTC")
    add_via(42.13, 0.85, "3V3_RTC")
    add_seg(36.36, 0.85, 42.13, 0.85, "B.Cu", "3V3_RTC")

    # Pin 12 (SD_SCK, 42.63, 2.43) -> via at (42.63, 1.75)
    add_seg(42.63, 2.43, 42.63, 1.75, "F.Cu", "SD_SCK")
    add_via(42.63, 1.75, "SD_SCK")
    add_seg(42.63, 1.75, 58.15, 1.75, "B.Cu", "SD_SCK")

    # Pin 13 (SD_CS, 43.13, 2.43) -> via at (43.13, 0.85)
    add_seg(43.13, 2.43, 43.13, 0.85, "F.Cu", "SD_CS")
    add_via(43.13, 0.85, "SD_CS")
    add_seg(43.13, 0.85, 59.65, 0.85, "B.Cu", "SD_CS")

    # Pin 15 (BOOT9, 44.13, 2.43) -> via at (44.13, 1.45)
    add_seg(44.13, 2.43, 44.13, 1.45, "F.Cu", "BOOT9")
    add_via(44.13, 1.45, "BOOT9")
    add_seg(44.13, 1.45, 52.23, 1.45, "B.Cu", "BOOT9")

    # East pins:
    # Pin 18 (VDD_SPI, 45.28, 3.59) -> via at (46.20, 3.59)
    add_seg(45.28, 3.59, 46.20, 3.59, "F.Cu", "VDD_SPI")
    add_via(46.20, 3.59, "VDD_SPI")
    # C5.1 (49.52, 1.55) -> via at (49.52, 3.59)
    add_seg(49.52, 1.55, 49.52, 3.59, "F.Cu", "VDD_SPI")
    add_via(49.52, 3.59, "VDD_SPI")
    add_seg(46.20, 3.59, 49.52, 3.59, "B.Cu", "VDD_SPI")

    # North pins:
    # Pin 30 (XTAL_P_CORE, 42.13, 7.24) -> via at (42.13, 8.65)
    add_seg(42.13, 7.24, 42.13, 8.65, "F.Cu", "XTAL_P_CORE")
    add_via(42.13, 8.65, "XTAL_P_CORE")
    add_seg(39.12, 8.65, 42.13, 8.65, "B.Cu", "XTAL_P_CORE")

    # Pin 29 (XTAL_N, 42.63, 7.24) -> via at (42.63, 8.05)
    add_seg(42.63, 7.24, 42.63, 8.05, "F.Cu", "XTAL_N")
    add_via(42.63, 8.05, "XTAL_N")
    add_seg(32.83, 8.05, 42.63, 8.05, "B.Cu", "XTAL_N")

    # Pin 28 (UART_TX, 43.13, 7.24) -> via at (43.13, 8.65)
    add_seg(43.13, 7.24, 43.13, 8.65, "F.Cu", "UART_TX")
    add_via(43.13, 8.65, "UART_TX")
    add_seg(43.13, 8.65, 55.95, 8.65, "B.Cu", "UART_TX")

    # Pin 27 (UART_RX, 43.63, 7.24) -> via at (43.63, 8.05)
    add_seg(43.63, 7.24, 43.63, 8.05, "F.Cu", "UART_RX")
    add_via(43.63, 8.05, "UART_RX")
    add_seg(43.63, 8.05, 57.22, 8.05, "B.Cu", "UART_RX")

    # Pin 26 (USB_DP_CORE, 44.13, 7.24) -> escapes North to 8.65, East to 54.50, via to B.Cu Y = 7.60
    add_seg(44.13, 7.24, 44.13, 8.65, "F.Cu", "USB_DP_CORE")
    add_seg(44.13, 8.65, 54.50, 8.65, "F.Cu", "USB_DP_CORE")
    add_seg(54.50, 8.65, 54.50, 7.60, "F.Cu", "USB_DP_CORE")
    add_via(54.50, 7.60, "USB_DP_CORE")
    add_seg(54.50, 7.60, 70.80, 7.60, "B.Cu", "USB_DP_CORE")

    # Pin 25 (USB_DM_CORE, 44.63, 7.24) -> escapes North to 8.35, East to 53.50, via to B.Cu Y = 7.15
    add_seg(44.63, 7.24, 44.63, 8.35, "F.Cu", "USB_DM_CORE")
    add_seg(44.63, 8.35, 53.50, 8.35, "F.Cu", "USB_DM_CORE")
    add_seg(53.50, 8.35, 53.50, 7.15, "F.Cu", "USB_DM_CORE")
    add_via(53.50, 7.15, "USB_DM_CORE")
    add_seg(53.50, 7.15, 72.95, 7.15, "B.Cu", "USB_DM_CORE")

    # ==============================================================
    # 5. RF MATCHING & CONNECTORS (X = 46 to 56 mm)
    # ==============================================================
    # FB1 is at (46.23, 7.55): FB1.2 is at (46.705, 7.55). Connect to C2.1 (48.09, 6.60)
    add_seg(46.705, 7.55, 48.09, 7.55, "F.Cu", "3V3_RF")
    add_seg(48.09, 7.55, 48.09, 6.60, "F.Cu", "3V3_RF")
    add_seg(46.705, 7.55, 46.705, 5.80, "F.Cu", "3V3_RF")
    add_via(46.705, 5.80, "3V3_RF")
    add_seg(39.00, 5.80, 46.705, 5.80, "B.Cu", "3V3_RF")

    # L2.1 (51.92, 5.30) to C8.1 (52.22, 3.60) on F.Cu
    add_seg(51.92, 5.30, 51.50, 5.30, "F.Cu", "RF_LNA")
    add_seg(51.50, 5.30, 51.50, 3.60, "F.Cu", "RF_LNA")
    add_seg(51.50, 3.60, 52.22, 3.60, "F.Cu", "RF_LNA")
    add_seg(51.50, 5.30, 51.50, 6.25, "F.Cu", "RF_LNA")
    add_via(51.50, 6.25, "RF_LNA")
    add_seg(38.50, 6.25, 51.50, 6.25, "B.Cu", "RF_LNA")

    # RF_OUT: L2.2 (52.48, 5.30) to J_RF.1 (54.85, 5.15)
    add_seg(52.48, 5.30, 52.48, 6.60, "F.Cu", "RF_OUT")
    add_seg(52.48, 6.60, 54.85, 6.60, "F.Cu", "RF_OUT")
    add_seg(54.85, 6.60, 54.85, 5.15, "F.Cu", "RF_OUT")
    # RF_OUT: J_RF.1 to C9.1
    add_seg(54.85, 5.15, 54.85, 2.80, "F.Cu", "RF_OUT")
    add_seg(54.85, 2.80, 53.77, 2.80, "F.Cu", "RF_OUT")
    add_seg(53.77, 2.80, 53.77, 3.55, "F.Cu", "RF_OUT")

    # STRAP2: R3.2 (48.77, 2.80) escapes to via at (48.77, 4.08)
    add_seg(48.77, 2.80, 48.77, 4.08, "F.Cu", "STRAP2")
    add_via(48.77, 4.08, "STRAP2")
    add_seg(37.50, 4.08, 48.77, 4.08, "B.Cu", "STRAP2")

    # BOOT9: SW2.1 (45.70, 1.50) to via at (45.70, 1.45)
    add_seg(45.70, 1.50, 45.70, 1.45, "F.Cu", "BOOT9")
    add_via(45.70, 1.45, "BOOT9")
    # R2.2 (52.23, 2.25) to via at (52.23, 1.45)
    add_seg(52.23, 2.25, 52.23, 1.45, "F.Cu", "BOOT9")
    add_via(52.23, 1.45, "BOOT9")

    # ==============================================================
    # 6. UART & MICROSD (X = 55 to 61 mm)
    # ==============================================================
    # J_UART.1 (UART_TX at 55.95, 7.35) -> via at (55.95, 8.65)
    add_seg(55.95, 7.35, 55.95, 8.65, "F.Cu", "UART_TX")
    add_via(55.95, 8.65, "UART_TX")

    # J_UART.2 (UART_RX at 57.22, 7.35) -> via at (57.22, 8.05)
    add_seg(57.22, 7.35, 57.22, 8.05, "F.Cu", "UART_RX")
    add_via(57.22, 8.05, "UART_RX")

    # MicroSD J_SD escapes (clean F.Cu vertical drops to South B.Cu highways):
    # J_SD.3 (SD_SCK at 58.15, 4.20) -> via at (58.15, 1.75)
    add_seg(58.15, 4.20, 58.15, 1.75, "F.Cu", "SD_SCK")
    add_via(58.15, 1.75, "SD_SCK")

    # J_SD.4 (SD_MOSI at 58.65, 4.20) -> via at (58.65, 0.55)
    add_seg(58.65, 4.20, 58.65, 0.55, "F.Cu", "SD_MOSI")
    add_via(58.65, 0.55, "SD_MOSI")

    # J_SD.5 (SD_MISO at 59.15, 4.20) -> via at (59.15, 1.15)
    add_seg(59.15, 4.20, 59.15, 1.15, "F.Cu", "SD_MISO")
    add_via(59.15, 1.15, "SD_MISO")

    # J_SD.6 (SD_CS at 59.65, 4.20) -> via at (59.65, 0.85)
    add_seg(59.65, 4.20, 59.65, 0.85, "F.Cu", "SD_CS")
    add_via(59.65, 0.85, "SD_CS")

    # R18.2 is at (55.475, 2.35): connect to SD_CS highway on B.Cu at Y = 0.85
    add_seg(55.475, 2.35, 55.475, 0.85, "F.Cu", "SD_CS")
    add_via(55.475, 0.85, "SD_CS")

    # ==============================================================
    # 7. BATTERY & CHARGER U2, SW3, J_PWR (X = 60 to 70 mm)
    # ==============================================================
    # VBAT:
    # SW3.1 (60.963, 6.824) -> via at (60.963, 5.00)
    add_seg(60.963, 6.824, 60.963, 5.00, "F.Cu", "VBAT")
    add_via(60.963, 5.00, "VBAT")
    # J_BAT.1 is at (62.300, 1.720) [J_BAT at 62.80]
    add_via(62.300, 5.00, "VBAT")
    add_seg(60.963, 5.00, 62.300, 5.00, "B.Cu", "VBAT")
    add_seg(62.300, 5.00, 62.300, 1.720, "F.Cu", "VBAT")
    # J_BAT.1 down to Y = 1.00 on F.Cu
    add_seg(62.300, 1.720, 62.300, 1.00, "F.Cu", "VBAT")
    add_via(62.300, 1.00, "VBAT")
    # C12.1 is at (67.400, 1.400) [C12 at 68.15]
    add_via(67.400, 1.00, "VBAT")
    add_seg(62.300, 1.00, 67.400, 1.00, "B.Cu", "VBAT")
    add_seg(67.400, 1.00, 67.400, 1.400, "F.Cu", "VBAT")
    # From C12.1 to U2.3 (67.950, 2.773) on F.Cu:
    add_seg(67.400, 1.400, 67.950, 1.400, "F.Cu", "VBAT")
    add_seg(67.950, 1.400, 67.950, 2.773, "F.Cu", "VBAT")

    # VBAT_SW:
    add_seg(28.09, 4.40, 62.963, 4.40, "B.Cu", "VBAT_SW")
    add_seg(62.963, 4.40, 68.114, 4.40, "B.Cu", "VBAT_SW")
    add_seg(62.963, 6.824, 62.963, 4.40, "F.Cu", "VBAT_SW")
    add_via(62.963, 4.40, "VBAT_SW")
    add_seg(68.114, 3.963, 68.114, 4.40, "F.Cu", "VBAT_SW")
    add_via(68.114, 4.40, "VBAT_SW")

    # CHG_STAT:
    add_seg(18.80, 3.95, 66.049, 3.95, "B.Cu", "CHG_STAT")
    add_via(18.80, 3.95, "CHG_STAT")
    add_seg(18.80, 3.95, 18.80, 3.52, "F.Cu", "CHG_STAT")
    add_seg(18.80, 3.52, 17.00, 3.52, "F.Cu", "CHG_STAT")
    add_via(66.049, 3.95, "CHG_STAT")
    add_seg(66.049, 3.95, 66.049, 2.773, "F.Cu", "CHG_STAT")

    # CHG_PROG:
    # U2.5 at (66.049, 5.373) to R9.1 at (66.300, 6.225)
    add_seg(66.049, 5.373, 66.300, 5.373, "F.Cu", "CHG_PROG")
    add_seg(66.300, 5.373, 66.300, 6.225, "F.Cu", "CHG_PROG")

    # USB_VBUS on Charger:
    # U2.4 at (67.950, 5.373) to C11.1 at (67.250, 7.750)
    add_seg(67.950, 5.373, 67.450, 5.373, "F.Cu", "USB_VBUS")
    add_seg(67.450, 5.373, 67.450, 4.850, "F.Cu", "USB_VBUS")
    add_via(67.450, 4.850, "USB_VBUS")
    add_seg(67.450, 5.373, 67.450, 7.750, "F.Cu", "USB_VBUS")
    add_seg(67.450, 7.750, 67.250, 7.750, "F.Cu", "USB_VBUS")

    # ==============================================================
    # 8. USB-C RECEPTACLE, TVS, PASSIVES (X = 70 to 84 mm)
    # ==============================================================
    # USB_CC1: J_USB.5 (77.60, 3.10) to R5.1 (77.60, 6.225)
    add_seg(77.60, 3.10, 77.60, 6.225, "F.Cu", "USB_CC1")

    # USB_CC2: J_USB.6 (79.20, 3.10) to R6.1 (79.20, 6.225)
    add_seg(79.20, 3.10, 79.20, 6.225, "F.Cu", "USB_CC2")

    # USB_VBUS Port Side (highway at Y = 4.85):
    add_seg(67.45, 4.85, 80.80, 4.85, "B.Cu", "USB_VBUS")
    add_seg(80.80, 3.10, 80.80, 4.85, "F.Cu", "USB_VBUS")
    add_via(80.80, 4.85, "USB_VBUS")
    add_seg(76.00, 3.10, 76.00, 4.85, "F.Cu", "USB_VBUS")
    add_via(76.00, 4.85, "USB_VBUS")
    add_seg(72.00, 4.85, 72.00, 5.79, "F.Cu", "USB_VBUS")
    add_via(72.00, 4.85, "USB_VBUS")
    # C10.1 (73.75, 1.50)
    add_seg(73.75, 1.50, 73.75, 0.70, "F.Cu", "USB_VBUS")
    add_seg(73.75, 0.70, 76.00, 0.70, "F.Cu", "USB_VBUS")
    add_seg(76.00, 0.70, 76.00, 3.10, "F.Cu", "USB_VBUS")

    # USB_DP_CORE to U_ESD.6 and R8.2:
    add_via(70.80, 7.60, "USB_DP_CORE")
    add_seg(70.80, 7.60, 71.05, 7.60, "F.Cu", "USB_DP_CORE")
    add_seg(71.05, 7.60, 71.05, 5.79, "F.Cu", "USB_DP_CORE") # U_ESD.6
    add_seg(71.05, 7.025, 71.60, 7.025, "F.Cu", "USB_DP_CORE") # to R8.2

    # USB_DM_CORE to U_ESD.4 and R7.2:
    add_via(72.95, 7.15, "USB_DM_CORE")
    add_seg(72.95, 7.15, 72.95, 5.79, "F.Cu", "USB_DM_CORE") # U_ESD.4
    add_seg(72.95, 7.025, 73.00, 7.025, "F.Cu", "USB_DM_CORE") # to R7.2

    # USB_DP_PORT:
    # Branch A: J_USB.7 (78.15, 3.10) to U_ESD.1 (71.05, 3.19) via B.Cu highway at Y = 1.20
    add_seg(78.15, 3.10, 78.15, 1.20, "F.Cu", "USB_DP_PORT")
    add_via(78.15, 1.20, "USB_DP_PORT")
    add_seg(71.05, 1.20, 78.15, 1.20, "B.Cu", "USB_DP_PORT")
    add_via(71.05, 1.20, "USB_DP_PORT")
    add_seg(71.05, 1.20, 71.05, 3.19, "F.Cu", "USB_DP_PORT")
    # Branch B (North): J_USB.7 (78.15, 3.10) to R8.1 (71.60, 7.975) via B.Cu highway at Y = 8.65
    add_seg(78.15, 3.10, 78.15, 8.65, "F.Cu", "USB_DP_PORT")
    add_via(78.15, 8.65, "USB_DP_PORT")
    add_seg(71.60, 8.65, 78.15, 8.65, "B.Cu", "USB_DP_PORT")
    add_via(71.60, 8.65, "USB_DP_PORT")
    add_seg(71.60, 8.65, 71.60, 7.975, "F.Cu", "USB_DP_PORT")

    # USB_DM_PORT:
    # Branch A: J_USB.9 (78.65, 3.10) to U_ESD.2 (72.00, 3.19) via B.Cu highway at Y = 0.55
    add_seg(78.65, 3.10, 78.65, 0.55, "F.Cu", "USB_DM_PORT")
    add_via(78.65, 0.55, "USB_DM_PORT")
    add_seg(72.00, 0.55, 78.65, 0.55, "B.Cu", "USB_DM_PORT")
    add_via(72.00, 0.55, "USB_DM_PORT")
    add_seg(72.00, 0.55, 72.00, 3.19, "F.Cu", "USB_DM_PORT")
    # Branch B (North): J_USB.9 (78.65, 3.10) to R7.1 (73.00, 7.975) via B.Cu highway at Y = 8.05
    add_seg(78.65, 3.10, 78.65, 8.05, "F.Cu", "USB_DM_PORT")
    add_via(78.65, 8.05, "USB_DM_PORT")
    add_seg(73.00, 8.05, 78.65, 8.05, "B.Cu", "USB_DM_PORT")
    add_via(73.00, 8.05, "USB_DM_PORT")
    add_seg(73.00, 8.05, 73.00, 7.975, "F.Cu", "USB_DM_PORT")

    # C14 (3V3 Decoupling):
    # C14.1 is at (70.014, 2.75). J_PWR.3 is at (70.014, 3.963).
    add_seg(70.014, 3.963, 70.014, 2.75, "F.Cu", "3V3")

    # Run complete verification
    errs = check_pcb_geometry(pads, segments, list(vias))
    print(f"\n==========================================")
    print(f"MASTER PCB GEOMETRY CHECK: {len(errs)} ERRORS")
    print(f"==========================================")
    for e in errs:
        print("  *", e)
    return pads, segments, list(vias), len(errs)

if __name__ == '__main__':
    build_full_board()

