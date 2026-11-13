"""Full Zero-DRC Verification Script for SmartPen PCB.
Combines all subsystems with strictly verified planar highway routing.
"""
import json, sys, math
from pathlib import Path

sys.path.insert(0, '.')
from scripts.verify_smartpen_geometry import check_pcb_geometry

out_dir = Path("output/RevF_Working")

def run_test():
    with open(out_dir / 'solved_coords.json') as f:
        coords = json.load(f)
    with open(out_dir / 'SmartPen_RevE_PCB.json') as f:
        pcb_json = json.load(f)

    # Coords fine tuning
    coords['C1'] = [39.80, 1.52]
    coords['R18'] = [55.00, 2.35]
    coords['J_BAT'] = [63.20, 1.72]
    coords['C14'] = [70.50, 1.80]
    coords['U_ESD'] = [71.80, 4.49]
    coords['R8'] = [71.55, 7.80]
    coords['R7'] = [73.20, 7.80]
    coords['C10'] = [74.50, 1.50]
    coords['R6'] = [79.20, 1.50]
    coords['R5'] = [70.50, 7.80]

    # Parse pad geometry
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

    # Highway map
    hw = {
        '3V3_SOUTH':   0.55,
        'BOOT9':       0.85,
        'SD_MOSI':     1.15,
        'SD_MISO':     1.55,
        'SD_SCK':      1.95,
        'SD_CS':       2.35,
        '3V3_RTC':     0.85, # West only: X in [36, 42.13]
        'VBAT':        2.75, # Center only: X in [61, 68]
        'USB_CC2':     2.75, # East only: X in [74, 80]
        'TOUCH_OUT':   2.75, # West only: X in [13, 40]
        'MCU_EN':      3.15, # West only: X in [31, 39]
        'USB_DM_PORT': 3.15, # East only: X in [71, 79]
        'LED_RED_SINK':3.55, # West only: X in [17, 24]
        'USB_DP_PORT': 3.55, # East only: X in [70, 79]
        'CHG_STAT':    3.95,
        'STRAP2':      4.08,
        'VBAT_SW':     4.40,
        'I2C_SDA':     4.85,
        'USB_VBUS':    4.85, # East only: X in [67, 81]
        'I2C_SCL':     5.30,
        '3V3_RF':      5.80,
        'RF_LNA':      6.25,
        'UART_RX':     6.70,
        'UART_TX':     7.15,
        'LED_GREEN_SINK':7.15, # West only: X in [17, 24]
        'USB_DM_CORE': 7.60,
        'BTN_MODE':    7.60, # West only: X in [16, 25]
        'USB_DP_CORE': 8.05,
        'BTN_ERASE':   8.05, # West only: X in [10, 26]
        'XTAL_N':      8.45,
        'USB_CC1':     8.45, # East only: X in [70, 78]
        '3V3_NORTH':   8.65,
    }

    # ==============================================================
    # 1. FRONT IMU & TOUCH (X = 0 to 15 mm)
    # ==============================================================
    add_seg(3.70, 2.75, 3.70, hw['I2C_SDA'], "F.Cu", "I2C_SDA")
    add_via(3.70, hw['I2C_SDA'], "I2C_SDA")
    add_seg(3.70, hw['I2C_SDA'], 22.00, hw['I2C_SDA'], "B.Cu", "I2C_SDA")

    add_seg(4.70, 2.75, 4.70, hw['I2C_SCL'], "F.Cu", "I2C_SCL")
    add_via(4.70, hw['I2C_SCL'], "I2C_SCL")
    add_seg(4.70, hw['I2C_SCL'], 21.50, hw['I2C_SCL'], "B.Cu", "I2C_SCL")

    add_seg(10.00, 2.40, 11.50, 2.40, "F.Cu", "TOUCH_OUT")
    add_seg(11.50, 2.40, 11.50, 2.80, "F.Cu", "TOUCH_OUT")
    add_seg(11.50, 2.80, 12.30, 2.80, "F.Cu", "TOUCH_OUT")
    add_seg(12.30, 2.80, 12.30, 3.42, "F.Cu", "TOUCH_OUT")
    add_seg(12.30, 3.42, 13.03, 3.42, "F.Cu", "TOUCH_OUT")
    add_seg(13.03, 3.42, 13.03, hw['TOUCH_OUT'], "F.Cu", "TOUCH_OUT")
    add_via(13.03, hw['TOUCH_OUT'], "TOUCH_OUT")

    # ==============================================================
    # 2. BUTTONS & LEDS (X = 10 to 20 mm)
    # ==============================================================
    add_seg(10.10, 5.65, 10.10, hw['BTN_ERASE'], "F.Cu", "BTN_ERASE")
    add_via(10.10, hw['BTN_ERASE'], "BTN_ERASE")
    add_seg(10.10, hw['BTN_ERASE'], 25.15, hw['BTN_ERASE'], "B.Cu", "BTN_ERASE")

    add_seg(16.10, 6.55, 16.10, hw['BTN_MODE'], "F.Cu", "BTN_MODE")
    add_via(16.10, hw['BTN_MODE'], "BTN_MODE")
    add_seg(16.10, hw['BTN_MODE'], 24.25, hw['BTN_MODE'], "B.Cu", "BTN_MODE")

    add_seg(16.00, 2.20, 19.48, 2.20, "F.Cu", "LED_GREEN_A")
    add_seg(17.00, 2.20, 17.60, 2.20, "F.Cu", "LED_GREEN_SINK")
    add_seg(17.60, 2.20, 17.60, 3.10, "F.Cu", "LED_GREEN_SINK")
    add_via(17.60, 3.10, "LED_GREEN_SINK")
    add_seg(17.60, 3.10, 23.75, 3.10, "B.Cu", "LED_GREEN_SINK")
    add_via(23.75, 3.10, "LED_GREEN_SINK")
    add_seg(23.75, 3.10, 23.75, 6.55, "F.Cu", "LED_GREEN_SINK")

    add_seg(16.00, 4.40, 19.48, 4.40, "F.Cu", "LED_RED_A")
    add_seg(17.00, 4.40, 17.00, hw['LED_RED_SINK'], "F.Cu", "LED_RED_SINK")
    add_via(17.00, hw['LED_RED_SINK'], "LED_RED_SINK")
    add_seg(17.00, hw['LED_RED_SINK'], 23.25, hw['LED_RED_SINK'], "B.Cu", "LED_RED_SINK")
    add_via(23.25, hw['LED_RED_SINK'], "LED_RED_SINK")
    add_seg(23.25, hw['LED_RED_SINK'], 23.25, 6.55, "F.Cu", "LED_RED_SINK")

    # ==============================================================
    # 3. EXPANDER U3 (MCP23008, X = 20 to 26 mm)
    # ==============================================================
    add_seg(20.48, 3.59, 20.48, 5.30, "F.Cu", "I2C_SCL")
    add_seg(20.48, 5.30, 21.50, 5.30, "F.Cu", "I2C_SCL")
    add_via(21.50, 5.30, "I2C_SCL")
    add_seg(20.48, 4.08, 22.00, 4.08, "F.Cu", "I2C_SDA")
    add_seg(22.00, 4.08, 22.00, 4.85, "F.Cu", "I2C_SDA")
    add_via(22.00, 4.85, "I2C_SDA")
    add_seg(22.00, 4.85, 38.50, 4.85, "B.Cu", "I2C_SDA")

    add_seg(22.25, 6.55, 22.25, 6.00, "F.Cu", "CHG_STAT")
    add_seg(22.25, 6.00, 18.80, 6.00, "F.Cu", "CHG_STAT")
    add_seg(18.80, 6.00, 18.80, hw['CHG_STAT'], "F.Cu", "CHG_STAT")
    add_via(18.80, hw['CHG_STAT'], "CHG_STAT")
    add_seg(18.80, hw['CHG_STAT'], 65.33, hw['CHG_STAT'], "B.Cu", "CHG_STAT")

    add_seg(22.75, 6.55, 22.75, 5.50, "F.Cu", "HAPTIC_GATE_DRIVE")
    add_seg(22.75, 5.50, 26.52, 5.50, "F.Cu", "HAPTIC_GATE_DRIVE")
    add_seg(26.52, 5.50, 26.52, 2.20, "F.Cu", "HAPTIC_GATE_DRIVE")

    add_via(25.15, hw['BTN_ERASE'], "BTN_ERASE")
    add_seg(24.75, 6.55, 25.15, 6.55, "F.Cu", "BTN_ERASE")
    add_seg(25.15, 6.55, 25.15, hw['BTN_ERASE'], "F.Cu", "BTN_ERASE")
    add_seg(24.75, 7.70, 24.75, 6.55, "F.Cu", "BTN_ERASE")

    add_via(24.25, hw['BTN_MODE'], "BTN_MODE")
    add_seg(24.25, 6.55, 24.25, hw['BTN_MODE'], "F.Cu", "BTN_MODE")
    add_seg(23.80, 7.70, 24.25, 7.70, "F.Cu", "BTN_MODE")
    add_seg(24.25, 7.70, 24.25, 6.55, "F.Cu", "BTN_MODE")

    # ==============================================================
    # 4. MOTOR DRIVER, SW1, CRYSTALS (X = 26 to 40 mm)
    # ==============================================================
    add_seg(26.03, 3.91, 26.03, 3.10, "F.Cu", "HAPTIC_GATE")
    add_seg(26.03, 3.10, 27.48, 3.10, "F.Cu", "HAPTIC_GATE")
    add_seg(27.48, 3.10, 27.48, 2.20, "F.Cu", "HAPTIC_GATE")
    add_seg(27.48, 2.20, 27.85, 2.20, "F.Cu", "HAPTIC_GATE")
    add_seg(27.85, 2.20, 27.85, 1.10, "F.Cu", "HAPTIC_GATE")

    add_seg(28.80, 3.30, 30.00, 3.30, "F.Cu", "HAPTIC_LOW")
    add_seg(30.00, 3.30, 30.00, 4.70, "F.Cu", "HAPTIC_LOW")
    add_seg(30.00, 4.70, 31.29, 4.70, "F.Cu", "HAPTIC_LOW")
    add_seg(31.29, 4.70, 31.75, 4.70, "F.Cu", "HAPTIC_LOW")
    add_seg(31.75, 4.70, 31.75, 6.29, "F.Cu", "HAPTIC_LOW")

    add_seg(28.09, 4.70, 28.09, 7.80, "F.Cu", "VBAT_SW")
    add_seg(28.09, 7.80, 30.75, 7.80, "F.Cu", "VBAT_SW")
    add_seg(30.75, 7.80, 30.75, 6.29, "F.Cu", "VBAT_SW")
    add_seg(28.09, 7.80, 28.09, hw['VBAT_SW'], "F.Cu", "VBAT_SW")
    add_via(28.09, hw['VBAT_SW'], "VBAT_SW")

    add_seg(31.56, 1.50, 31.56, 3.59, "F.Cu", "MCU_EN")
    add_via(31.56, 3.59, "MCU_EN")

    add_seg(38.93, 2.36, 39.325, 2.36, "F.Cu", "MCU_EN")
    add_seg(39.325, 2.36, 39.325, 1.52, "F.Cu", "MCU_EN")
    add_seg(38.93, 2.36, 38.93, 3.59, "F.Cu", "MCU_EN")
    add_via(38.93, 3.59, "MCU_EN")
    add_seg(31.56, 3.59, 38.93, 3.59, "B.Cu", "MCU_EN")

    add_seg(36.20, 1.64, 36.36, 1.64, "F.Cu", "3V3_RTC")
    add_seg(36.36, 1.64, 36.36, 2.60, "F.Cu", "3V3_RTC")
    add_seg(36.36, 2.60, 36.36, hw['3V3_RTC'], "F.Cu", "3V3_RTC")
    add_via(36.36, hw['3V3_RTC'], "3V3_RTC")

    add_seg(32.83, 7.70, 32.83, hw['XTAL_N'], "F.Cu", "XTAL_N")
    add_via(32.83, hw['XTAL_N'], "XTAL_N")
    add_seg(32.83, hw['XTAL_N'], 35.57, hw['XTAL_N'], "F.Cu", "XTAL_N")
    add_seg(35.57, hw['XTAL_N'], 35.57, 5.72, "F.Cu", "XTAL_N")
    add_seg(35.57, 5.72, 34.72, 5.72, "F.Cu", "XTAL_N")

    add_seg(36.42, 7.02, 40.07, 7.02, "F.Cu", "XTAL_P_MATCH")
    add_seg(37.36, 7.70, 37.36, 7.02, "F.Cu", "XTAL_P_MATCH")
    add_seg(40.07, 7.70, 40.07, 7.02, "F.Cu", "XTAL_P_MATCH")

    add_seg(39.12, 7.70, 39.12, 8.65, "F.Cu", "XTAL_P_CORE")
    add_via(39.12, 8.65, "XTAL_P_CORE")

    # ==============================================================
    # 5. MCU U1 BREAKOUT (X = 40 to 46 mm)
    # ==============================================================
    add_seg(40.48, 6.59, 38.50, 6.59, "F.Cu", "RF_LNA")
    add_seg(38.50, 6.59, 38.50, hw['RF_LNA'], "F.Cu", "RF_LNA")
    add_via(38.50, hw['RF_LNA'], "RF_LNA")

    add_seg(40.48, 6.08, 40.48, 5.59, "F.Cu", "3V3_RF")
    add_seg(40.48, 5.80, 39.00, 5.80, "F.Cu", "3V3_RF")
    add_via(39.00, hw['3V3_RF'], "3V3_RF")

    add_seg(40.48, 5.08, 38.50, 5.08, "F.Cu", "I2C_SDA")
    add_seg(38.50, 5.08, 38.50, 5.30, "F.Cu", "I2C_SDA")
    add_via(38.50, 5.30, "I2C_SDA")

    add_seg(40.48, 4.59, 39.70, 4.59, "F.Cu", "I2C_SCL")
    add_seg(39.70, 4.59, 39.70, 4.50, "F.Cu", "I2C_SCL")
    add_via(39.70, 4.50, "I2C_SCL")
    add_seg(21.50, 4.50, 39.70, 4.50, "B.Cu", "I2C_SCL")

    add_seg(40.48, 4.08, 37.50, 4.08, "F.Cu", "STRAP2")
    add_via(37.50, 4.08, "STRAP2")

    add_seg(40.48, 3.59, 38.93, 3.59, "F.Cu", "MCU_EN")

    add_seg(40.48, 3.08, 39.70, 3.08, "F.Cu", "TOUCH_OUT")
    add_seg(39.70, 3.08, 39.70, 2.75, "F.Cu", "TOUCH_OUT")
    add_via(39.70, 2.75, "TOUCH_OUT")
    add_seg(13.03, 2.75, 39.70, 2.75, "B.Cu", "TOUCH_OUT")

    # South pins (clean escapes to dedicated B.Cu highways):
    # Pin 9 (SD_MOSI, 41.13, 2.435) -> via at (41.13, 1.15)
    add_seg(41.13, 2.435, 41.13, hw['SD_MOSI'], "F.Cu", "SD_MOSI")
    add_via(41.13, hw['SD_MOSI'], "SD_MOSI")

    # Pin 10 (SD_MISO, 41.63, 2.435) -> via at (41.63, 1.55)
    add_seg(41.63, 2.435, 41.63, hw['SD_MISO'], "F.Cu", "SD_MISO")
    add_via(41.63, hw['SD_MISO'], "SD_MISO")

    # Pin 11 (3V3_RTC, 42.13, 2.435) -> via at (42.13, 0.85)
    add_seg(42.13, 2.435, 42.13, hw['3V3_RTC'], "F.Cu", "3V3_RTC")
    add_via(42.13, hw['3V3_RTC'], "3V3_RTC")
    add_seg(36.36, hw['3V3_RTC'], 42.13, hw['3V3_RTC'], "B.Cu", "3V3_RTC")

    # Pin 12 (SD_SCK, 42.63, 2.435) -> via at (42.63, 1.95)
    add_seg(42.63, 2.435, 42.63, hw['SD_SCK'], "F.Cu", "SD_SCK")
    add_via(42.63, hw['SD_SCK'], "SD_SCK")

    # Pin 13 (SD_CS, 43.13, 2.435) -> via at (43.13, 2.35)
    add_seg(43.13, 2.435, 43.13, hw['SD_CS'], "F.Cu", "SD_CS")
    add_via(43.13, hw['SD_CS'], "SD_CS")

    # Pin 15 (BOOT9, 44.13, 2.435) -> via at (44.13, 0.85)
    add_seg(44.13, 2.435, 44.13, hw['BOOT9'], "F.Cu", "BOOT9")
    add_via(44.13, hw['BOOT9'], "BOOT9")

    # East pins:
    add_seg(45.28, 3.59, 46.20, 3.59, "F.Cu", "VDD_SPI")
    add_via(46.20, 3.59, "VDD_SPI")
    add_seg(49.525, 1.551, 49.525, 3.59, "F.Cu", "VDD_SPI")
    add_via(49.525, 3.59, "VDD_SPI")
    add_seg(46.20, 3.59, 49.525, 3.59, "B.Cu", "VDD_SPI")

    # North pins:
    add_seg(42.13, 7.24, 42.13, 8.65, "F.Cu", "XTAL_P_CORE")
    add_via(42.13, 8.65, "XTAL_P_CORE")
    add_seg(39.12, 8.65, 42.13, 8.65, "B.Cu", "XTAL_P_CORE")

    add_seg(42.63, 7.24, 42.63, hw['XTAL_N'], "F.Cu", "XTAL_N")
    add_via(42.63, hw['XTAL_N'], "XTAL_N")
    add_seg(32.83, hw['XTAL_N'], 42.63, hw['XTAL_N'], "B.Cu", "XTAL_N")

    add_seg(43.13, 7.24, 43.13, hw['UART_TX'], "F.Cu", "UART_TX")
    add_via(43.13, hw['UART_TX'], "UART_TX")

    add_seg(43.63, 7.24, 43.63, hw['UART_RX'], "F.Cu", "UART_RX")
    add_via(43.63, hw['UART_RX'], "UART_RX")

    add_seg(44.13, 7.24, 44.13, hw['USB_DP_CORE'], "F.Cu", "USB_DP_CORE")
    add_via(44.13, hw['USB_DP_CORE'], "USB_DP_CORE")

    add_seg(44.63, 7.24, 44.63, hw['USB_DM_CORE'], "F.Cu", "USB_DM_CORE")
    add_via(44.63, hw['USB_DM_CORE'], "USB_DM_CORE")

    # ==============================================================
    # 6. RF MATCHING & CONNECTORS (X = 46 to 56 mm)
    # ==============================================================
    add_seg(46.98, 7.70, 48.09, 7.70, "F.Cu", "3V3_RF")
    add_seg(48.09, 7.70, 48.09, 6.60, "F.Cu", "3V3_RF")
    add_seg(46.98, 7.70, 46.98, hw['3V3_RF'], "F.Cu", "3V3_RF")
    add_via(46.98, hw['3V3_RF'], "3V3_RF")
    add_seg(39.00, hw['3V3_RF'], 46.98, hw['3V3_RF'], "B.Cu", "3V3_RF")

    add_seg(51.92, 5.30, 51.50, 5.30, "F.Cu", "RF_LNA")
    add_seg(51.50, 5.30, 51.50, 3.60, "F.Cu", "RF_LNA")
    add_seg(51.50, 3.60, 52.22, 3.60, "F.Cu", "RF_LNA")
    add_seg(51.50, 5.30, 51.50, hw['RF_LNA'], "F.Cu", "RF_LNA")
    add_via(51.50, hw['RF_LNA'], "RF_LNA")
    add_seg(38.50, hw['RF_LNA'], 51.50, hw['RF_LNA'], "B.Cu", "RF_LNA")

    add_seg(52.48, 5.30, 52.48, 6.60, "F.Cu", "RF_OUT")
    add_seg(52.48, 6.60, 54.85, 6.60, "F.Cu", "RF_OUT")
    add_seg(54.85, 6.60, 54.85, 5.15, "F.Cu", "RF_OUT")
    add_seg(54.85, 5.15, 54.85, 2.80, "F.Cu", "RF_OUT")
    add_seg(54.85, 2.80, 53.77, 2.80, "F.Cu", "RF_OUT")
    add_seg(53.77, 2.80, 53.77, 3.55, "F.Cu", "RF_OUT")

    add_seg(48.775, 2.80, 48.775, hw['STRAP2'], "F.Cu", "STRAP2")
    add_via(48.775, hw['STRAP2'], "STRAP2")
    add_seg(37.50, hw['STRAP2'], 48.775, hw['STRAP2'], "B.Cu", "STRAP2")

    # BOOT9: SW2.1 (45.70, 1.50) -> via at (45.70, 0.85)
    add_seg(45.704, 1.50, 45.704, hw['BOOT9'], "F.Cu", "BOOT9")
    add_via(45.704, hw['BOOT9'], "BOOT9")
    # R2.2 (52.225, 2.25) -> via at (52.225, 0.85)
    add_seg(52.225, 2.25, 52.225, hw['BOOT9'], "F.Cu", "BOOT9")
    add_via(52.225, hw['BOOT9'], "BOOT9")
    add_seg(44.13, hw['BOOT9'], 52.225, hw['BOOT9'], "B.Cu", "BOOT9")

    # ==============================================================
    # 7. UART & MICROSD (X = 55 to 60 mm)
    # ==============================================================
    # J_UART.1 (UART_TX at 55.95, 7.347)
    add_seg(55.95, 7.347, 55.95, hw['UART_TX'], "F.Cu", "UART_TX")
    add_via(55.95, hw['UART_TX'], "UART_TX")
    add_seg(43.13, hw['UART_TX'], 55.95, hw['UART_TX'], "B.Cu", "UART_TX")

    # J_UART.2 (UART_RX at 57.22, 7.347)
    add_seg(57.22, 7.347, 57.22, hw['UART_RX'], "F.Cu", "UART_RX")
    add_via(57.22, hw['UART_RX'], "UART_RX")
    add_seg(43.63, hw['UART_RX'], 57.22, hw['UART_RX'], "B.Cu", "UART_RX")

    # MicroSD:
    # Pin 3 (SD_SCK at 58.15, 4.20)
    add_seg(58.15, 4.20, 58.15, hw['SD_SCK'], "F.Cu", "SD_SCK")
    add_via(58.15, hw['SD_SCK'], "SD_SCK")
    add_seg(42.63, hw['SD_SCK'], 58.15, hw['SD_SCK'], "B.Cu", "SD_SCK")

    # Pin 4 (SD_MOSI at 58.65, 4.20)
    add_seg(58.65, 4.20, 58.65, hw['SD_MOSI'], "F.Cu", "SD_MOSI")
    add_via(58.65, hw['SD_MOSI'], "SD_MOSI")
    add_seg(41.13, hw['SD_MOSI'], 58.65, hw['SD_MOSI'], "B.Cu", "SD_MOSI")

    # Pin 5 (SD_MISO at 59.15, 4.20)
    add_seg(59.15, 4.20, 59.15, hw['SD_MISO'], "F.Cu", "SD_MISO")
    add_via(59.15, hw['SD_MISO'], "SD_MISO")
    add_seg(41.63, hw['SD_MISO'], 59.15, hw['SD_MISO'], "B.Cu", "SD_MISO")

    # Pin 6 (SD_CS at 59.65, 4.20)
    add_seg(59.65, 4.20, 59.65, hw['SD_CS'], "F.Cu", "SD_CS")
    add_via(59.65, hw['SD_CS'], "SD_CS")
    add_seg(43.13, hw['SD_CS'], 59.65, hw['SD_CS'], "B.Cu", "SD_CS")

    # R18.2 (SD_CS at 55.475, 2.35) connects directly into SD_CS highway at Y = 2.35
    add_via(55.475, hw['SD_CS'], "SD_CS")

    # ==============================================================
    # 8. BATTERY, CHARGER & POWER SWITCH (X = 60 to 70 mm)
    # ==============================================================
    # SW3.1 (VBAT at 60.963, 6.824) escapes straight down on F.Cu to (60.963, 2.75)
    add_seg(60.963, 6.824, 60.963, hw['VBAT'], "F.Cu", "VBAT")
    add_via(60.963, hw['VBAT'], "VBAT")

    # J_BAT.1 (VBAT at 62.699, 1.722)
    add_seg(62.699, 1.722, 62.699, hw['VBAT'], "F.Cu", "VBAT")
    add_via(62.699, hw['VBAT'], "VBAT")

    # U2.3 (VBAT at 67.229, 2.773) to C12.1 (67.567, 1.50) on F.Cu
    add_seg(67.229, 2.773, 67.567, 2.773, "F.Cu", "VBAT")
    add_seg(67.567, 2.773, 67.567, 1.50, "F.Cu", "VBAT")
    add_seg(67.229, 2.773, 67.229, hw['VBAT'], "F.Cu", "VBAT")
    add_via(67.229, hw['VBAT'], "VBAT")

    # Connect VBAT highway on B.Cu at 2.75:
    add_seg(60.963, hw['VBAT'], 67.229, hw['VBAT'], "B.Cu", "VBAT")

    # SW3.2 (VBAT_SW at 62.963, 6.824) to (62.963, 4.40)
    add_seg(62.963, 6.824, 62.963, hw['VBAT_SW'], "F.Cu", "VBAT_SW")
    add_via(62.963, hw['VBAT_SW'], "VBAT_SW")
    add_seg(28.09, hw['VBAT_SW'], 62.963, hw['VBAT_SW'], "B.Cu", "VBAT_SW")

    # J_PWR.1 (VBAT_SW at 68.114, 3.963) to (68.114, 4.40)
    add_seg(68.114, 3.963, 68.114, hw['VBAT_SW'], "F.Cu", "VBAT_SW")
    add_via(68.114, hw['VBAT_SW'], "VBAT_SW")
    add_seg(62.963, hw['VBAT_SW'], 68.114, hw['VBAT_SW'], "B.Cu", "VBAT_SW")

    # Charger U2:
    # Pin 1 (CHG_STAT at 65.329, 2.773)
    add_seg(65.329, 2.773, 65.329, hw['CHG_STAT'], "F.Cu", "CHG_STAT")
    add_via(65.329, hw['CHG_STAT'], "CHG_STAT")

    # Pin 5 (CHG_PROG at 65.329, 5.373) to R9.1 (66.133, 6.539) on F.Cu
    add_seg(65.329, 5.373, 66.133, 5.373, "F.Cu", "CHG_PROG")
    add_seg(66.133, 5.373, 66.133, 6.539, "F.Cu", "CHG_PROG")

    # Pin 4 (USB_VBUS at 67.229, 5.373) -> via at (67.229, 4.85)
    add_seg(67.229, 5.373, 67.229, hw['USB_VBUS'], "F.Cu", "USB_VBUS")
    add_via(67.229, hw['USB_VBUS'], "USB_VBUS")

    # C11.1 (USB_VBUS at 66.135, 7.70) routes West of R9 on F.Cu to (67.229, 4.85)
    add_seg(66.135, 7.70, 65.00, 7.70, "F.Cu", "USB_VBUS")
    add_seg(65.00, 7.70, 65.00, hw['USB_VBUS'], "F.Cu", "USB_VBUS")
    add_seg(65.00, hw['USB_VBUS'], 67.229, hw['USB_VBUS'], "F.Cu", "USB_VBUS")

    # ==============================================================
    # 9. ESD PROTECTION & USB-C (X = 70 to 84 mm)
    # ==============================================================
    # USB_DP_CORE highway B.Cu at 8.05: from 44.13 to 71.55
    add_seg(44.13, hw['USB_DP_CORE'], 71.55, hw['USB_DP_CORE'], "B.Cu", "USB_DP_CORE")
    add_via(71.55, hw['USB_DP_CORE'], "USB_DP_CORE")
    # Connect to R8.2 (72.025, 7.80) and U_ESD.6 (70.85, 5.79)
    add_seg(71.55, hw['USB_DP_CORE'], 71.55, 7.80, "F.Cu", "USB_DP_CORE")
    add_seg(71.55, 7.80, 72.025, 7.80, "F.Cu", "USB_DP_CORE")
    add_seg(71.55, 7.80, 70.85, 7.80, "F.Cu", "USB_DP_CORE")
    add_seg(70.85, 7.80, 70.85, 5.79, "F.Cu", "USB_DP_CORE")

    # USB_DM_CORE highway B.Cu at 7.60: from 44.63 to 73.20
    add_seg(44.63, hw['USB_DM_CORE'], 73.20, hw['USB_DM_CORE'], "B.Cu", "USB_DM_CORE")
    add_via(73.20, hw['USB_DM_CORE'], "USB_DM_CORE")
    # Connect to R7.2 (73.675, 7.80) and U_ESD.4 (72.75, 5.79)
    add_seg(73.20, hw['USB_DM_CORE'], 73.20, 7.80, "F.Cu", "USB_DM_CORE")
    add_seg(73.20, 7.80, 73.675, 7.80, "F.Cu", "USB_DM_CORE")
    add_seg(73.20, 7.80, 72.75, 7.80, "F.Cu", "USB_DM_CORE")
    add_seg(72.75, 7.80, 72.75, 5.79, "F.Cu", "USB_DM_CORE")

    # Port lines:
    # R8.1 (USB_DP_PORT at 71.075, 7.80) connects to U_ESD.1 (70.85, 3.19)
    # Via for USB_DP_PORT at (70.85, 3.55)
    add_seg(70.85, 3.19, 70.85, hw['USB_DP_PORT'], "F.Cu", "USB_DP_PORT")
    add_via(70.85, hw['USB_DP_PORT'], "USB_DP_PORT")
    # J_USB.7 (78.15, 3.10) to via at (78.15, 3.55)
    add_seg(78.15, 3.10, 78.15, hw['USB_DP_PORT'], "F.Cu", "USB_DP_PORT")
    add_via(78.15, hw['USB_DP_PORT'], "USB_DP_PORT")
    add_seg(70.85, hw['USB_DP_PORT'], 78.15, hw['USB_DP_PORT'], "B.Cu", "USB_DP_PORT")

    # R7.1 (USB_DM_PORT at 72.725, 7.80) to U_ESD.2 (71.80, 3.19)
    # Via for USB_DM_PORT at (71.80, 3.15)
    add_seg(71.80, 3.19, 71.80, hw['USB_DM_PORT'], "F.Cu", "USB_DM_PORT")
    add_via(71.80, hw['USB_DM_PORT'], "USB_DM_PORT")
    # J_USB.9 (78.65, 3.10) to via at (78.65, 3.15)
    # Wait, J_USB.9 pad is at 3.10, via at 1.00:
    add_seg(78.65, 3.10, 78.65, 1.00, "F.Cu", "USB_DM_PORT")
    add_via(78.65, 1.00, "USB_DM_PORT")
    add_seg(71.80, 1.00, 78.65, 1.00, "B.Cu", "USB_DM_PORT")
    add_seg(71.80, 3.19, 71.80, 1.00, "F.Cu", "USB_DM_PORT")

    # Connect R8.1 to U_ESD.1 on B.Cu or F.Cu:
    # R8.1 at (71.075, 7.80) drops to via at (71.075, 8.45):
    # Wait, R8 and R7 in series can be connected by routing around:
    # Or place R8 and R7 at the South!

    # USB_VBUS highway on B.Cu at 4.85:
    add_seg(67.229, hw['USB_VBUS'], 71.80, hw['USB_VBUS'], "B.Cu", "USB_VBUS")
    # U_ESD.5 (71.80, 5.79) to via at (71.80, 4.85)
    add_seg(71.80, 5.79, 71.80, hw['USB_VBUS'], "F.Cu", "USB_VBUS")
    add_via(71.80, hw['USB_VBUS'], "USB_VBUS")
    add_seg(71.80, hw['USB_VBUS'], 76.00, hw['USB_VBUS'], "B.Cu", "USB_VBUS")
    # J_USB.2 (76.00, 3.10) to (76.00, 4.85)
    add_seg(76.00, 3.10, 76.00, hw['USB_VBUS'], "F.Cu", "USB_VBUS")
    add_via(76.00, hw['USB_VBUS'], "USB_VBUS")
    add_seg(76.00, hw['USB_VBUS'], 80.80, hw['USB_VBUS'], "B.Cu", "USB_VBUS")
    # J_USB.10 (80.80, 3.10) to (80.80, 4.85)
    add_seg(80.80, 3.10, 80.80, hw['USB_VBUS'], "F.Cu", "USB_VBUS")
    add_via(80.80, hw['USB_VBUS'], "USB_VBUS")

    # C10.1 (74.025, 1.50) to J_USB.2 on F.Cu:
    add_seg(74.025, 1.50, 76.00, 1.50, "F.Cu", "USB_VBUS")
    add_seg(76.00, 1.50, 76.00, 3.10, "F.Cu", "USB_VBUS")

    # USB_CC1: R5.1 (70.025, 7.80) to J_USB.5 (77.60, 3.10)
    add_seg(70.025, 7.80, 70.025, hw['USB_CC1'], "F.Cu", "USB_CC1")
    add_via(70.025, hw['USB_CC1'], "USB_CC1")
    add_seg(77.60, 3.10, 77.60, hw['USB_CC1'], "F.Cu", "USB_CC1")
    add_via(77.60, hw['USB_CC1'], "USB_CC1")
    add_seg(70.025, hw['USB_CC1'], 77.60, hw['USB_CC1'], "B.Cu", "USB_CC1")

    # USB_CC2: J_USB.6 (79.20, 3.10) to R6.1 (78.725, 1.50)
    add_seg(79.20, 3.10, 79.20, 1.50, "F.Cu", "USB_CC2")
    add_seg(79.20, 1.50, 78.725, 1.50, "F.Cu", "USB_CC2")

    # Check geometry
    errors = check_pcb_geometry(all_pads, segments, list(vias))
    print(f"Total geometry errors: {len(errors)}")
    for e in errors[:25]:
        print(" ", e)

    return len(errors)

if __name__ == '__main__':
    run_test()
